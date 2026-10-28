#!/usr/bin/env python3
"""Check responsive file dimensions, byte benefits and lossless logo appearance."""
import json
from pathlib import Path
from PIL import Image, ImageChops
ROOT=Path(__file__).resolve().parents[1]
manifest=json.loads((ROOT/'_data/image-delivery.json').read_text())
count=0
for name,entry in manifest.items():
    with Image.open(ROOT/name) as source:
        assert source.size==(entry['width'],entry['height']),name
        for variant in entry['variants']:
            path=ROOT/variant['src']
            assert path.stat().st_size==variant['bytes']<entry['originalBytes']*.95
            with Image.open(path) as image:
                assert image.width==variant['width']
                assert image.height==round(source.height*image.width/source.width)
                if name.startswith('MR LOGO'):
                    expected=source.resize(image.size,Image.Resampling.LANCZOS).convert('RGBA')
                    actual=image.convert('RGBA')
                    assert ImageChops.difference(expected.getchannel('A'),actual.getchannel('A')).getbbox() is None
                    # WebP may normalize invisible RGB under zero alpha. Composite
                    # over both black and white to compare all visible logo pixels.
                    for color in ['black','white']:
                        base=Image.new('RGBA',image.size,color)
                        assert ImageChops.difference(Image.alpha_composite(base,expected).convert('RGB'),Image.alpha_composite(base,actual).convert('RGB')).getbbox() is None
            count+=1
print(f'PASS: {count} responsive derivatives exist, are smaller, preserve aspect ratios, and retain exact visible logo pixels and transparency.')
