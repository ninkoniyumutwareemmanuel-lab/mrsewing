#!/usr/bin/env python3
"""Prepare technical favicon formats from the approved logo; no artwork changes.

Run manually when the approved source changes. Pillow is needed for preparation,
not for the ordinary deployment build, which validates committed artifacts.
"""
from pathlib import Path
from io import BytesIO
import hashlib
import json
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'assets/images/logo-icon.png'
SIZES = [16, 32, 48, 64, 96, 128, 144, 192]
logo = Image.open(SOURCE).convert('RGBA')
side = max(logo.size)
assert side == 192, 'Review a changed source dimension before preparing favicons'
canvas = Image.new('RGBA', (side, side), (0, 0, 0, 0))
canvas.alpha_composite(logo, ((side - logo.width) // 2, (side - logo.height) // 2))
outputs = {}
for name, kind, options in [
    ('assets/images/favicon-192.png', 'PNG', {'optimize': True}),
    ('favicon.ico', 'ICO', {'sizes': [(n, n) for n in SIZES]}),
]:
    data = BytesIO()
    canvas.save(data, format=kind, **options)
    path = ROOT / name
    path.write_bytes(data.getvalue())
    outputs[name] = hashlib.sha256(path.read_bytes()).hexdigest()
manifest = {
    'approval': 'Owner technical SEO repair instruction, 13 November 2026',
    'source': 'assets/images/logo-icon.png',
    'sourceSha256': hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
    'sourceDimensions': list(logo.size),
    'treatment': 'Unchanged artwork, centered on transparent square padding; aspect ratio preserved',
    'squareDimensions': [side, side],
    'icoSizes': SIZES,
    'outputs': outputs,
}
(ROOT / '_data/favicon-assets.json').write_text(json.dumps(manifest, indent=2) + '\n')
print('Prepared approved-logo square PNG and multi-size root ICO; original source unchanged')
