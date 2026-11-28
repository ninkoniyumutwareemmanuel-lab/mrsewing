#!/usr/bin/env python3
"""Build a branch-scoped, authenticated, read-only Pages preview at the existing root.

No account configuration or bindings are changed. Advanced-mode _worker.js
supersedes the old Pages Functions in this deployment only. The live Main alias
retains its separate, unchanged deployed code. The review key never enters Git;
only a cryptographically random key's SHA256 verifier is an input here.
"""
from __future__ import annotations

import argparse
from datetime import datetime
import json
import os
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
MIME = {
    '.html': 'text/html', '.css': 'text/css', '.js': 'application/javascript',
    '.mjs': 'application/javascript', '.json': 'application/json',
    '.txt': 'text/plain', '.xml': 'application/xml',
    '.webmanifest': 'application/manifest+json', '.svg': 'image/svg+xml',
    '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.png': 'image/png',
    '.avif': 'image/avif', '.webp': 'image/webp', '.gif': 'image/gif',
    '.ico': 'image/x-icon', '.mp4': 'video/mp4', '.webm': 'video/webm',
    '.woff': 'font/woff', '.woff2': 'font/woff2', '.ttf': 'font/ttf', '.otf': 'font/otf',
}


def current_branch(root=ROOT):
    value = os.environ.get('CF_PAGES_BRANCH') or os.environ.get('GITHUB_HEAD_REF') or os.environ.get('GITHUB_REF_NAME')
    if value:
        return value
    return subprocess.check_output(['git', 'branch', '--show-current'], cwd=root, text=True).strip()


def validate(settings, branch):
    if settings.get('schemaVersion') != 1 or settings.get('enabled') is not True:
        raise ValueError('An explicitly enabled preview configuration is required')
    if settings.get('project') != 'mrsewing-staging':
        raise ValueError('Only the existing staging project is authorized')
    if branch not in settings.get('allowedBranches', []) or branch == 'main':
        raise ValueError('Rebuild preview cannot build on an unauthorized or Main branch')
    if settings.get('submissionsEnabled') is not False or settings.get('trackingEnabled') is not False:
        raise ValueError('Preview submissions and production tracking must remain disabled')
    if not re.fullmatch(r'[a-f0-9]{64}', settings.get('tokenSha256', '')):
        raise ValueError('A random private review key SHA256 verifier is required')
    expires = datetime.fromisoformat(settings['expiresAt'].replace('Z', '+00:00'))
    if expires.utcoffset() is None:
        raise ValueError('Preview expiry must have an explicit timezone')


def outputs(root=ROOT, *, branch=None, projection_fn=None):
    root = Path(root)
    path = root / '_data/rebuild-preview.json'
    if not path.is_file():
        return {}
    settings = json.loads(path.read_text())
    if settings.get('enabled') is not True:
        return {}
    validate(settings, branch or current_branch(root))
    if projection_fn is None:
        from prepare_release_candidate import projection
        projection_fn = projection
    files, _ = projection_fn(root=root, mode='production')
    assets, overrides = {}, {}
    for name, data in sorted(files.items()):
        if name.startswith('.') or name.startswith('_'):
            continue
        # Do not inherit platform-specific /etc/mime.types differences in CI.
        media_type = MIME.get(Path(name).suffix.lower(), 'application/octet-stream')
        if media_type.startswith('text/') or media_type in ('application/json', 'application/javascript', 'application/xml'):
            media_type += '; charset=utf-8'
        assets[name] = {'type': media_type}
        # Only policy/Shop holding projections differ from files already present.
        # Embed these small reviewed replacements instead of copying media again.
        original = root / name
        if not original.is_file() or original.read_bytes() != data:
            if not name.endswith(('.html', '.json', '.txt')):
                raise ValueError('Unsupported inline preview replacement: ' + name)
            overrides[name] = data.decode('utf-8')
    marker = {
        'preview': True, 'phase': '1', 'commit': os.environ.get('CF_PAGES_COMMIT_SHA'),
        'submissionsEnabled': False, 'trackingEnabled': False,
        'publication': 'authenticated-staging-review',
    }
    assets['build-info.json'] = {'type': 'application/json; charset=utf-8'}
    overrides['build-info.json'] = json.dumps(marker, separators=(',', ':')) + '\n'
    config = {
        'version': 1, 'project': settings['project'],
        'allowedHosts': ['mrsewing-staging.pages.dev'],
        'allowedSuffix': '.mrsewing-staging.pages.dev',
        'deniedHosts': ['main.mrsewing-staging.pages.dev', 'mrsewingfashion.com', 'www.mrsewingfashion.com'],
        'tokenSha256': settings['tokenSha256'], 'expiresAt': settings['expiresAt'],
        'commit': marker['commit'], 'assets': assets, 'overrides': overrides,
    }
    template = (root / '_templates/rebuild-preview-worker.js').read_text()
    hook = '/*REBUILD_PREVIEW_CONFIG*/ null'
    if template.count(hook) != 1:
        raise ValueError('Preview worker must contain exactly one configuration hook')
    encoded = json.dumps(config, ensure_ascii=False, separators=(',', ':')).replace('<', '\\u003c')
    worker = '// Generated by scripts/build_rebuild_preview.py; never place the raw review key here.\n' + template.replace(hook, encoded)
    routes = json.dumps({'version': 1, 'include': ['/*'], 'exclude': []}, indent=2) + '\n'
    return {root / '_worker.js': worker, root / '_routes.json': routes}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    generated = outputs()
    for path, value in generated.items():
        if args.check:
            if not path.is_file() or path.read_text() != value:
                raise SystemExit('Stale authenticated preview output: ' + path.name)
        else:
            path.write_text(value)
    print('PASS: authenticated preview worker and all-path routing synchronized; no provider/configuration change.' if generated else 'Preview mode is not enabled; existing deployment unchanged.')


if __name__ == '__main__':
    main()
