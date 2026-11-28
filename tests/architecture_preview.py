#!/usr/bin/env python3
"""Isolated preview security and export tests; no external services or app build."""
import importlib.util
import json
from pathlib import Path
import tempfile
import threading
import unittest
from urllib.error import HTTPError
from urllib.request import Request, urlopen
import zipfile

spec = importlib.util.spec_from_file_location("architecture_preview_tool", Path(__file__).resolve().parents[1] / "scripts/architecture_preview.py")
tool = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tool)


class PreviewTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.public = self.root / "public"
        self.public.mkdir()
        (self.public / "index.html").write_text("<h1>Private review</h1>")
        (self.public / "images").mkdir()
        (self.public / "images/suit.svg").write_text("<svg/>")
        (self.public / "request").mkdir()
        (self.public / "request/index.html").write_text("<form>Review only</form>")
        self.server = tool.make_server(self.public, port=0)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.origin = "http://127.0.0.1:" + str(self.server.server_address[1])

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join()
        self.temp.cleanup()

    def request(self, path, method="GET", data=None):
        try:
            return urlopen(Request(self.origin + path, data=data, method=method), timeout=2)
        except HTTPError as error:
            return error

    def test_visual_files_and_guard_headers(self):
        with self.request("/") as response:
            self.assertEqual(response.status, 200)
            self.assertIn(b"Private review", response.read())
            self.assertIn("noindex", response.headers["X-Robots-Tag"])
            self.assertEqual(response.headers["Cache-Control"], "no-store")
            csp = response.headers["Content-Security-Policy"]
            for directive in ("connect-src 'self'", "form-action 'none'", "script-src 'self' 'unsafe-inline'", "frame-src 'self'", "object-src 'none'"):
                self.assertIn(directive, csp)
            self.assertNotIn("https:", csp)
        with self.request("/images/suit.svg") as response:
            self.assertEqual(response.status, 200)
        with self.request("/request") as response:
            self.assertEqual(response.status, 200)  # urllib follows safe local slash redirect
            self.assertTrue(response.url.endswith("/request/"))

    def test_all_api_methods_and_post_fail_honestly(self):
        for method in ("GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"):
            with self.subTest(method=method), self.request("/api/selected-design-request", method, b'{}' if method == "POST" else None) as response:
                self.assertEqual(response.status, 503)
                result = json.loads(response.read())
                self.assertFalse(result["success"])
                self.assertTrue(result["preview"])
                self.assertIn("No request was submitted", result["error"])
                self.assertIn("noindex", response.headers["X-Robots-Tag"])
        for path in ("/request/", "/anything", "/"):
            with self.request(path, "POST", b'{"name":"synthetic"}') as response:
                self.assertEqual(response.status, 503)
                self.assertFalse(json.loads(response.read())["success"])
        for path in ("/api", "/%61pi/selected-design-request", "/%2561pi%252fshop-request"):
            with self.request(path) as response:
                self.assertEqual(response.status, 503)

    def test_private_encoded_paths_and_directory_listings_denied(self):
        for path in ("/docs/test.md", "/%64ocs/test.html", "/%2564ocs/test.html", "/staff/", "/_data/test.json", "/%2e%2e/docs/", "/%252e%252e%252fdocs/", "/.git/config", "/runtime/functions/test.js", "/images/", "/script.py", "/x.map", "/%00", "/..%5csecret"):
            with self.subTest(path=path), self.request(path) as response:
                self.assertEqual(response.status, 404)
                self.assertIn("noindex", response.headers["X-Robots-Tag"])

    def test_symlink_escape_denied(self):
        secret = self.root / "secret.html"
        secret.write_text("never serve")
        (self.public / "outside.html").symlink_to(secret)
        with self.request("/outside.html") as response:
            self.assertEqual(response.status, 404)
            self.assertNotIn(b"never serve", response.read())

    def test_head_and_robots(self):
        with self.request("/", "HEAD") as response:
            self.assertEqual(response.status, 200)
            self.assertEqual(response.read(), b"")
        with self.request("/robots.txt") as response:
            self.assertIn(b"Disallow: /", response.read())
        with self.request("/api/shop-request", "HEAD") as response:
            self.assertEqual(response.status, 503)
            self.assertEqual(response.read(), b"")

    def test_non_loopback_requires_explicit_portal(self):
        with self.assertRaises(ValueError):
            tool.make_server(self.public, host="0.0.0.0", port=0)
        with self.assertRaises(ValueError):
            tool.make_server(self.public, host="192.0.2.1", port=0, http_portal_configured=True)

    def test_offline_bundle_uses_production_projection_and_no_runtime(self):
        source = self.root / "checkout"
        source.mkdir()
        output = self.root / "bundle"
        archive = self.root / "review.zip"
        calls = []
        def fake_projection(**kwargs):
            calls.append(kwargs)
            return {"index.html": b"safe", "assets/photo.svg": b"<svg/>", ".nojekyll": b"",
                    "_headers": b"Hosting-only headers", "_redirects": b"/legacy / 301"}, ["assets/policy-documents/review.pdf"]
        result = tool.export_bundle(output, archive, root=source, projection_fn=fake_projection)
        self.assertEqual(calls, [{"root": source.resolve(), "mode": "production"}])
        self.assertFalse(result["deployed"])
        self.assertFalse(result["submissionsEnabled"])
        self.assertFalse((output / "runtime").exists())
        self.assertEqual(result["omittedHostingFiles"], ["_headers", "_redirects"])
        self.assertFalse((output / "public/_headers").exists())
        self.assertFalse((output / "public/_redirects").exists())
        self.assertTrue((output / "public/index.html").is_file())
        self.assertTrue((output / "server.py").is_file())
        self.assertIn("current effective HTML", (output / "README.md").read_text())
        with zipfile.ZipFile(archive) as bundle:
            self.assertIn("public/index.html", bundle.namelist())
            self.assertIn("server.py", bundle.namelist())
            self.assertNotIn("public/_headers", bundle.namelist())
            self.assertNotIn("public/_redirects", bundle.namelist())
            self.assertFalse(any(name.startswith(("runtime/", "docs/", "masters/", "registers/")) for name in bundle.namelist()))
        with self.assertRaises(ValueError):
            tool.export_bundle(output, root=source, projection_fn=fake_projection)

    def test_exports_preserve_checkout_and_reject_private_projection(self):
        source = self.root / "checkout"
        source.mkdir()
        with self.assertRaises(ValueError):
            tool.export_bundle(source / "bad", root=source, projection_fn=lambda **_: ({}, []))
        for name in ("docs/a.html", "../secret.html", "_data/config.json", "staff/index.html"):
            with self.subTest(name=name), self.assertRaises(ValueError):
                tool.export_bundle(self.root / "bad-export", root=source, projection_fn=lambda **_: ({name: b"x"}, []))
        self.assertFalse((self.root / "bad-export").exists())


if __name__ == "__main__":
    unittest.main()
