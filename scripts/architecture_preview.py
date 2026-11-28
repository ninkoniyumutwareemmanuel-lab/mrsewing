#!/usr/bin/env python3
"""Export or serve a private, submission-disabled architecture review bundle.

This tool never builds the application, deploys it, starts a backend, or sends an
external request. Export uses the existing public-only production projection.
The exported copy of this file serves public/ using Python's standard library.
"""
from __future__ import annotations

import argparse
import functools
import hashlib
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import mimetypes
from pathlib import Path
import shutil
import subprocess
from urllib.parse import quote, unquote, urlsplit
import zipfile

ROOT = Path(__file__).resolve().parents[1]
DENIED_PARTS = {
    "_data", "_templates", "_media", "scripts", "tests", "docs", "functions",
    ".github", ".git", ".agents", ".codex", ".aws", "staff", "artifacts",
    "node_modules", ".wrangler", "runtime", "attachments", "private",
    "mrsewing-rebuild-records", "masters", "registers",
}
DENIED_SUFFIXES = {".py", ".pyc", ".md", ".map", ".env", ".sqlite", ".db"}
CSP = "; ".join((
    "default-src 'self'", "script-src 'self' 'unsafe-inline'",
    "style-src 'self' 'unsafe-inline'", "img-src 'self' data: blob:",
    "font-src 'self' data:", "media-src 'self' blob:", "connect-src 'self'",
    "frame-src 'self'", "frame-ancestors 'self'", "form-action 'none'",
    "object-src 'none'", "base-uri 'self'", "worker-src 'none'",
))
DISABLED = {
    "success": False, "preview": True,
    "error": "Private preview only: submissions are disabled. No request was submitted.",
}


def clean_path(raw: str) -> str:
    """Decode before checking: encoded source paths must not bypass exclusions."""
    path = urlsplit(raw).path
    for _ in range(8):
        decoded = unquote(path, errors="strict")
        if decoded == path:
            break
        path = decoded
    else:
        raise ValueError("Excessively encoded path")
    if not path.startswith("/") or "\\" in path or any(ord(c) < 32 or ord(c) == 127 for c in path):
        raise ValueError("Invalid path")
    parts = [part for part in path.split("/") if part]
    if any(part in (".", "..") or part.startswith((".", "_")) or part.lower() in DENIED_PARTS for part in parts):
        raise ValueError("Private path")
    if Path(path).suffix.lower() in DENIED_SUFFIXES:
        raise ValueError("Private file type")
    return path


class PreviewHandler(BaseHTTPRequestHandler):
    """Serve only a public projection. Every API and write request is disabled."""

    server_version = "PrivateArchitecturePreview/1"

    def __init__(self, *args, directory: Path, **kwargs):
        self.directory = Path(directory).resolve()
        super().__init__(*args, **kwargs)

    def end_headers(self):
        self.send_header("X-Robots-Tag", "noindex, nofollow, noarchive, nosnippet")
        self.send_header("Content-Security-Policy", CSP)
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Referrer-Policy", "no-referrer")
        self.send_header("Permissions-Policy", "camera=(), microphone=(), geolocation=(), payment=()")
        super().end_headers()

    def respond(self, code, body=b"", content_type="text/plain; charset=utf-8", headers=None):
        self.send_response(code)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        for key, value in (headers or {}).items():
            self.send_header(key, value)
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(body)

    def disabled(self):
        self.respond(503, json.dumps(DISABLED).encode(), "application/json; charset=utf-8")

    def read_public(self):
        try:
            path = clean_path(self.path)
        except (ValueError, UnicodeError):
            self.respond(404, b"Not found in the private public-only preview.\n")
            return
        if path.rstrip("/") == "/api" or path.startswith("/api/"):
            self.disabled()
            return
        if path == "/robots.txt":
            self.respond(200, b"User-agent: *\nDisallow: /\n")
            return
        target = (self.directory / path.lstrip("/")).resolve()
        if not target.is_relative_to(self.directory):
            self.respond(404, b"Not found.\n")
            return
        if target.is_dir():
            if not path.endswith("/"):
                query = urlsplit(self.path).query
                destination = quote(path, safe="/") + "/" + ("?" + query if query else "")
                self.respond(301, headers={"Location": destination})
                return
            target = target / "index.html"
        if not target.is_file() or target.is_symlink() or not target.resolve().is_relative_to(self.directory):
            self.respond(404, b"Not found in the private public-only preview.\n")
            return
        # Symlinked ancestors are also forbidden even when the resolved target is local.
        relative = target.relative_to(self.directory)
        check = self.directory
        for part in relative.parts:
            check = check / part
            if check.is_symlink():
                self.respond(404, b"Not found.\n")
                return
        self.respond(200, target.read_bytes(), mimetypes.guess_type(str(target))[0] or "application/octet-stream")

    do_GET = read_public
    do_HEAD = read_public
    do_POST = disabled
    do_PUT = disabled
    do_PATCH = disabled
    do_DELETE = disabled
    do_OPTIONS = disabled


def make_server(directory, host="127.0.0.1", port=3000, http_portal_configured=False):
    root = Path(directory).resolve()
    if not root.is_dir():
        raise ValueError("The public preview directory does not exist")
    if host not in ("127.0.0.1", "localhost", "0.0.0.0"):
        raise ValueError("Use loopback, or 0.0.0.0 with a configured HTTP portal")
    if host == "0.0.0.0" and not http_portal_configured:
        raise ValueError("0.0.0.0 requires --http-portal-configured after the private HTTP portal is configured")
    return ThreadingHTTPServer((host, port), functools.partial(PreviewHandler, directory=root))


def export_bundle(output, archive=None, root=ROOT, projection_fn=None):
    root, output = Path(root).resolve(), Path(output).resolve()
    if output.is_relative_to(root):
        raise ValueError("Keep the private preview bundle outside the website checkout")
    if output.exists() and (not output.is_dir() or any(output.iterdir())):
        raise ValueError("Preserve existing bundles; choose a new empty output directory")
    archive = Path(archive).resolve() if archive else None
    if archive and (archive.is_relative_to(root) or archive.is_relative_to(output) or archive.exists()):
        raise ValueError("Use a new archive path outside the checkout and bundle directory")
    if projection_fn is None:
        from prepare_release_candidate import projection
        projection_fn = projection
    files, excluded = projection_fn(root=root, mode="production")
    # These files configure a hosting platform, not the loopback review server.
    # Keep its explicit security/noindex policy authoritative and avoid copying
    # deployment routing/configuration into a visual-only local review bundle.
    omitted_hosting = sorted(set(files) & {"_headers", "_redirects"})
    files = {name: data for name, data in files.items() if name not in omitted_hosting}
    # Validate everything before writing. Never add runtime, masters or registers.
    for name in files:
        if name == ".nojekyll":
            continue
        clean_path("/" + name)
    public = output / "public"
    public.mkdir(parents=True, exist_ok=True)
    for name, data in files.items():
        target = public / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
    shutil.copyfile(Path(__file__), output / "server.py")
    readme = """# Mr Sewing Fashion — private offline architecture preview

This is a visual review bundle, not a deployable release or a submission system.
It uses the existing public-only PRODUCTION projection: current effective HTML
Terms and temporary Shop holding pages. Review PDFs and private runtime/source,
management references and reconciliation registers are not included. It may show
new homepage architecture work, but it does not publish that work anywhere.

1. Extract the complete ZIP into a new folder on your own computer.
2. Install Python 3.10 or later if needed. No packages or account are required.
3. Open Terminal/Command Prompt in the extracted folder.
4. Run: `python server.py --serve public` (or `python3` on macOS/Linux).
5. Open http://127.0.0.1:3000/ in your browser. Keep the terminal running.
6. Press Ctrl+C in the terminal to stop. Nothing is uploaded or deployed.

The server binds to your computer only. Do not upload the bundle to a public
host, expose a router port or share a public tunnel. In a managed environment,
0.0.0.0 is allowed ONLY after its private HTTP portal is configured, using the
explicit --http-portal-configured flag. The tool never invents a hosted URL.

Every response is noindex/noarchive. External scripts, fonts, media, frames,
fetches and form actions are blocked by Content Security Policy. Same-origin
frames are allowed so the existing guided tailoring dialog remains reviewable.
ALL API routes and POST/write requests return503 with success:false and an
explicit preview-only message. No email provider, private database, payment
system or advertising vendor is connected. A failed preview submission is
expected and is not evidence that the production provider failed. Do not enter
real personal information. Use synthetic visual test data only.

Local navigation, images, selection, fabric preferences and dialog presentation
can be reviewed. External maps/fonts/videos/widgets may be absent by design.
Contact links remain real links: opening an external telephone/WhatsApp/email
application is under your control; the preview never sends a message. Cloudflare
routing, binding behavior, provider inbox receipt and advertising event receipt
are not verified by this bundle. Do not use file:// directly; use the server.

This server serves only public/. It does not serve this README, the manifest or
server source. Private source paths, encoded traversal, hidden paths and directory
listings are rejected. Browser storage still belongs to this local origin; clear
site data after review if desired. This preview must never replace the live site.
Hosting-only _headers/_redirects are omitted; this local server supplies its own
security and noindex headers. Cloudflare redirect behavior is not simulated.
"""
    (output / "README.md").write_text(readme)
    try:
        commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root, text=True, stderr=subprocess.DEVNULL).strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        commit = None
    manifest = {
        "purpose": "private-offline-visual-review", "sourceCommit": commit,
        "projection": "production", "deployed": False, "submissionsEnabled": False,
        "trackingEnabled": False, "runtimeIncluded": False,
        "terms": "current effective HTML", "shop": "existing production holding projection",
        "excludedUnactivatedDocuments": excluded,
        "omittedHostingFiles": omitted_hosting,
        "files": {name: {"bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()} for name, data in sorted(files.items())},
    }
    (output / "preview-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    if archive:
        archive.parent.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(archive, "x", compression=zipfile.ZIP_DEFLATED) as bundle:
            for path in sorted(output.rglob("*")):
                if path.is_file():
                    bundle.write(path, path.relative_to(output))
    return manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--bundle", help="New private output folder outside the checkout")
    action.add_argument("--serve", help="Existing public/ directory to serve privately")
    parser.add_argument("--archive", help="Optional new ZIP path outside checkout and bundle")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=3000)
    parser.add_argument("--http-portal-configured", action="store_true", help="Explicit confirmation of a configured PRIVATE HTTP portal before binding 0.0.0.0")
    args = parser.parse_args()
    try:
        if args.bundle:
            manifest = export_bundle(args.bundle, args.archive)
            print(json.dumps({"bundle": str(Path(args.bundle).resolve()), "archive": str(Path(args.archive).resolve()) if args.archive else None, "files": len(manifest["files"]), "deployed": False}))
        else:
            if args.archive:
                parser.error("--archive is available only with --bundle")
            with make_server(args.serve, args.host, args.port, args.http_portal_configured) as server:
                print(f"Private visual preview: http://{args.host}:{server.server_address[1]}/ (no submission backend)", flush=True)
                try:
                    server.serve_forever()
                except KeyboardInterrupt:
                    pass
    except ValueError as error:
        parser.error(str(error))


if __name__ == "__main__":
    main()
