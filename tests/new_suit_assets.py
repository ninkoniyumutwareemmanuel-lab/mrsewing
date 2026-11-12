"""Owner7November2026 release: explicit photo approvals, no commercial activation."""
import json,subprocess,sys
from pathlib import Path
from PIL import Image
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'scripts'))
from public_enquiries import approved
from shop_catalog import load
old=json.loads(subprocess.check_output(['git','show','7daf846:_data/shop-products.json'],cwd=R));now=json.loads((R/'_data/shop-products.json').read_text());assert now['products'][:21]==old['products'];assert len(now['products'])==26 and len(approved())==26 and load()==[]
for p in now['products'][21:]:
 assert p['publicationStatus']=='draft' and p['availability'] is None and p['priceRwf'] is None and p['stockQuantity'] is None and not p['variations']
 for image in p['images']:
  original=R/image['src'].lstrip('/');assert original.read_bytes()==subprocess.check_output(['git','show','7daf846:'+str(original.relative_to(R))],cwd=R)
  im=Image.open(original);assert im.size==(image['width'],image['height'])
  for v in image['responsiveSources']:
   variant=R/v['src'].lstrip('/');small=Image.open(variant);assert small.width==v['width'];assert abs(small.width/small.height-im.width/im.height)<.003;assert variant.stat().st_size<original.stat().st_size
for f in ['_data/customer-projects.json','_data/customer-request-backend.json']:
 assert (R/f).read_bytes()==subprocess.check_output(['git','show','7daf846:'+f],cwd=R),f
before=json.loads(subprocess.check_output(['git','show','7daf846:_data/fabric-reference-catalogue.json'],cwd=R))['fabrics'];current=json.loads((R/'_data/fabric-reference-catalogue.json').read_text())['fabrics'];assert [{k:f[k] for k in ['id','category','tier','image']} for f in current]==[{k:f[k] for k in ['id','category','tier','image']} for f in before]
print('PASS5unchangedapprovedoriginals/9smallerproportionalvariants/21originalShoprecordsunchanged/26enquiryonly/zero saleproducts/protected Moments,fabric,privateflag; current approved price/policy facts tested separately')
