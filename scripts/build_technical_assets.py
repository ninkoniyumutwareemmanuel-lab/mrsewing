#!/usr/bin/env python3
"""Validate prepared favicons and synchronize the static-host 404 boundary.

Uses only the Python standard library in the normal deployment build.
"""
import argparse
import hashlib
import json
import struct
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--check', action='store_true')
args = parser.parse_args()
manifest = json.loads((ROOT / '_data/favicon-assets.json').read_text())
assert hashlib.sha256((ROOT / manifest['source']).read_bytes()).hexdigest() == manifest['sourceSha256'], 'Approved favicon source changed; review and prepare derivatives'
for name, digest in manifest['outputs'].items():
    assert hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == digest, 'Stale favicon artifact: ' + name
png = (ROOT / 'assets/images/favicon-192.png').read_bytes()
assert png[:8] == b'\x89PNG\r\n\x1a\n' and struct.unpack('>II', png[16:24]) == (192, 192)
ico = (ROOT / 'favicon.ico').read_bytes()
reserved, kind, count = struct.unpack('<HHH', ico[:6])
assert (reserved, kind, count) == (0, 1, len(manifest['icoSizes']))
assert sorted(ico[6 + i * 16] or 256 for i in range(count)) == manifest['icoSizes']
source = (ROOT / '_templates/not-found.html').read_text()
path = ROOT / '404.html'
if args.check:
    assert path.is_file() and path.read_text() == source, 'Stale root404 boundary'
else:
    path.write_text(source)
print('PASS: approved-logo favicons and explicit noindex404 boundary synchronized')
