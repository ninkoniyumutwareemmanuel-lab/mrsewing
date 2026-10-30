#!/usr/bin/env python3
"""Re-encode the preserved AI still life into responsive WebP; never alter source media."""
import argparse,io,json
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');a=p.parse_args()
folder=ROOT/'assets/journey'
with Image.open(folder/'garment-care-illustration.png') as im:
 for width in [480,960]:
  out=io.BytesIO();im.resize((width,round(im.height*width/im.width)),Image.Resampling.LANCZOS).save(out,'WEBP',quality=84,method=6)
  path=folder/f'garment-care-{width}.webp'
  if a.check:assert path.read_bytes()==out.getvalue(),'Stale care illustration derivative'
  else:path.write_bytes(out.getvalue())
print('PASS: responsive care illustration derivatives preserve the original aspect ratio and reproduce exactly.')
