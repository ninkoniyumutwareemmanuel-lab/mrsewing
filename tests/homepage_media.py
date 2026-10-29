#!/usr/bin/env python3
"""Verify the homepage candidate inventory and visibly lossless logos."""
import hashlib,json
from pathlib import Path
from PIL import Image,ImageChops
ROOT=Path(__file__).resolve().parents[1]
data=json.loads((ROOT/'_data/homepage-media.json').read_text());count=0
for name,entry in data.items():
    source=Image.open(ROOT/name).convert('RGBA')
    assert source.size==(entry['width'],entry['height'])
    for v in entry['variants']:
        path=ROOT/v['src'];assert path.stat().st_size==v['bytes'];assert hashlib.sha256(path.read_bytes()).hexdigest()[:10] in path.name
        image=Image.open(path).convert('RGBA');assert image.width==v['width'];assert image.height==round(source.height*image.width/source.width)
        if name=='MR LOGO.jpeg':
            expected=source.resize(image.size,Image.Resampling.LANCZOS)
            assert ImageChops.difference(expected.getchannel('A'),image.getchannel('A')).getbbox() is None
            for color in ['black','white']:
                base=Image.new('RGBA',image.size,color)
                assert ImageChops.difference(Image.alpha_composite(base,expected).convert('RGB'),Image.alpha_composite(base,image).convert('RGB')).getbbox() is None
        else:assert v['psnr']>=35,(name,v['width'],v['psnr'])
        count+=1
print(f'PASS: {count} hashed homepage candidates exist, have correct dimensions/aspect ratios, retain visible logo pixels/alpha, and meet the recorded photo-quality threshold.')
