"""Real repository image candidates remain drafts; no inferred commercial facts."""
from pathlib import Path
import json,sys,copy,subprocess,hashlib
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from shop_catalog import load,category_route,categories
from inventory_shop_images import inventory
rows=inventory();candidates=[r for r in rows if r['role']=='candidate'];raw=json.loads((ROOT/'_data/shop-products.json').read_text())['products']
assert len(rows)==165 and all(r['decoded'] for r in rows)
assert len(candidates)==len(raw)==21 and not load()
assert len({p['id'] for p in raw})==21 and len({p['slug'] for p in raw})==21
assert len({p['images'][0]['src'] for p in raw})==21 and len({p['candidateEvidence']['imageSha256'] for p in raw})==21
assert sum(bool(p['candidateEvidence']['existingSuitReferenceIds']) for p in raw)==8
for p in raw:
 assert p['publicationStatus']=='draft' and p['approval']['publicDisplay'] is False and p['availability'] is None and p['stockQuantity'] is None and p['priceRwf'] is None
 assert p['priceApproved'] is False and p['variations']==[] and p['specifications']=={} and p['careInstructions'] is None and p['orderingNotes'] is None
 assert p['images'][0]['rightsApproved'] is False and p['missingInformation']
 q=copy.deepcopy(p);q['publicationStatus']='published'
 try:load({'schemaVersion':1,'products':[q]});raise RuntimeError('Unapproved product escaped gate')
 except AssertionError:pass
 q['approval']={'publicDisplay':True,'source':'Test only','date':'2026-11-06'}
 try:load({'schemaVersion':1,'products':[q]});raise RuntimeError('Null availability escaped gate')
 except AssertionError:pass
 for f in ['shop/index.html','shop/cart/index.html','functions/_lib/shop-runtime.js','sitemap.xml']:
  assert p['id'] not in (ROOT/f).read_text(),(p['id'],f)
 assert not (ROOT/'shop'/p['slug']/'index.html').exists()
try:load({'schemaVersion':1,'products':[raw[0],raw[0]]});raise RuntimeError('Duplicate drafts accepted')
except AssertionError:pass
assert not categories() and category_route("Men's Suits")=='/shop/category/mens-suits/'
# Preserve all existing original images and all unrelated generated pages byte-for-byte.
for path in subprocess.check_output(['git','ls-tree','-r','--name-only','626ccd8'],cwd=ROOT,text=True).splitlines():
 if path.lower().endswith(('.jpeg','.jpg','.png','.webp','.avif','.gif','.svg')) or path in ['index.html','assets/homepage.js','booking/index.html','assets/consultation.js','loyalty-program/index.html','referral-program/index.html','_data/collection-designs.json','_data/customer-projects.json']:
  assert (ROOT/path).read_bytes()==subprocess.check_output(['git','show','626ccd8:'+path],cwd=ROOT),path
print('PASS165 real WebP decode;21 unique drafts/8 suit-reference matches; all commercial unknowns null; publication/duplicate gates; no draft pages/schema/server catalogue; originals/home/booking/programmes preserved')
