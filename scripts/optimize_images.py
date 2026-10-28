#!/usr/bin/env python3
"""Generate local WebP derivatives; retain every source and its full resolution.
Authoring dependency: Pillow. No dependency is shipped to visitors.
"""
import json
from pathlib import Path
from PIL import Image, ImageOps
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets/images'
OUT.mkdir(exist_ok=True)
manifest = {}
for source in sorted(ROOT.glob('*.jpeg')):
    with Image.open(source) as original:
        image = ImageOps.exif_transpose(original)
        variants = []
        for width in sorted(set([min(480, image.width), min(960, image.width), image.width])):
            resized = image if width == image.width else image.resize((width, round(image.height * width / image.width)), Image.Resampling.LANCZOS)
            name = source.stem.strip().replace(' ', '-').lower() + f'-{width}.webp'
            target = OUT / name
            # Logos retain every RGBA pixel, including transparency.
            resized.save(target, 'WEBP', lossless=source.name.startswith('MR LOGO'), quality=90, method=6)
            if target.stat().st_size < source.stat().st_size * .95:
                variants.append({'src':target.relative_to(ROOT).as_posix(), 'width':width, 'bytes':target.stat().st_size})
            else:
                target.unlink()
        manifest[source.name] = {'width':image.width,'height':image.height,'originalBytes':source.stat().st_size,'variants':variants}
logo = Image.open(ROOT / 'MR LOGO.jpeg')
logo.thumbnail((192, 192), Image.Resampling.LANCZOS)
logo.save(OUT / 'logo-icon.png', optimize=True)
(ROOT / '_data/image-delivery.json').write_text(json.dumps(manifest, indent=2)+'\n')
print('Generated derivatives for', len(manifest), 'original images; originals untouched.')
