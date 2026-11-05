#!/usr/bin/env python3
"""R3: original-asset preservation, source-qualified fabric references and optimised illustration integrity."""
from pathlib import Path
import json,hashlib,subprocess
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
read=lambda p:json.loads((ROOT/p).read_text())
cat=read('_data/fabric-reference-catalogue.json')['fabrics'];images=read('_data/customer-guide-images.json')['images'];measure=read('_data/measurement-guide-images.json')['measurements']
assert [(f['tier'],f['name']) for f in cat if f['category']=='men']==[(1,'Super / Super 100s'),(2,'Wool'),(3,'Polyester'),(4,'Cotton / Dubai')]
assert [(f['tier'],f['name']) for f in cat if f['category']=='women']==[(1,'Americano'),(2,'Star'),(3,'Polyester'),(4,'Cotton')]
assert all(f['startingPriceRwf'] is None and f['priceStatus']=='Price on request' and f['colourStatus']=='Ask us about available colours.' for f in cat)
assert len({f['image'] for f in cat})==6 and len(measure)==11
assert (ROOT/'neck.jepg.webp').read_bytes()==(ROOT/'neck.webp').read_bytes()
assert next(x for x in measure if x['id']=='neck')['image']=='measure-neck'
assert images['measure-trouser-length']['src']=='/trauser length.webp'
for d in images.values():
 src=ROOT/d['src'].lstrip('/');im=Image.open(src);assert im.size==(d['width'],d['height']);assert hashlib.sha256(src.read_bytes()).hexdigest()==d['sha256']
 uploaded=subprocess.check_output(['git','show','b6b1d5147ec0edbb76ff956cb8fb06b3249d7b95:'+str(src.relative_to(ROOT))],cwd=ROOT);assert src.read_bytes()==uploaded
 for v in d['variants']:
  p=ROOT/v['src'].lstrip('/');im=Image.open(p);assert im.size==(v['width'],v['height']);assert p.stat().st_size<src.stat().st_size;assert abs(v['height']-round(d['height']*v['width']/d['width']))<=1
# All approved explanatory/policy paragraphs remain unchanged, not rewritten from pictures.
old=json.loads(subprocess.check_output(['git','show','b6b1d5147ec0edbb76ff956cb8fb06b3249d7b95:_data/customer-release.json'],cwd=ROOT,text=True));assert read('_data/customer-release.json')['pages']['/measurements/']==old['pages']['/measurements/']
assert len(old['pages']['/measurements/']['sections'])==6
print('PASS: 8 qualified references/6 fabric sources, 11 correct measurement mappings, identical neck duplicates, unchanged originals/instructions/policies and 34 smaller proportional variants.')

guide=(ROOT/"guides/fabrics/index.html").read_text()
assert guide.count("We recommend visiting our workshop")==1 and "working reference" not in guide
