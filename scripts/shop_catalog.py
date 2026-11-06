"""Single Git-maintained merchandise catalogue. Suit reference designs are not stock."""
from pathlib import Path
import json,re
ROOT=Path(__file__).resolve().parents[1]
STATUSES=('Available in Stock','Available on Orders','Out of Stock')
def load(source=None):
 data=source if source is not None else json.loads((ROOT/'_data/shop-products.json').read_text())
 assert data.get('schemaVersion')==1 and isinstance(data.get('products'),list),'Unsupported catalogue'
 ids=set();slugs=set();out=[]
 for p in data['products']:
  assert p.get('publicationStatus') in ['draft','published','archived'],'Invalid publication status'
  if p['publicationStatus']!='published':continue
  for k in ['id','name','slug','category','description','seoTitle','seoDescription','orderingNotes','careInstructions']:
   assert isinstance(p.get(k),str) and p[k].strip() and len(p[k])<=4000,('Missing product field',k)
  assert re.fullmatch(r'[A-Za-z0-9_-]{1,64}',p['id']) and p['id'] not in ids,'Duplicate/unsafe ID';ids.add(p['id'])
  assert re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*',p['slug']) and p['slug'] not in slugs and p['slug'] not in ['cart','checkout'],'Duplicate/reserved slug';slugs.add(p['slug'])
  assert p.get('approval',{}).get('publicDisplay') is True and p['approval'].get('source') and p['approval'].get('date'),'Publication evidence required'
  assert p.get('availability') in STATUSES,'Invalid availability'
  assert isinstance(p.get('specifications'),dict),'Specifications required'
  assert isinstance(p.get('images'),list) and p['images'],'Approved product photographs required'
  for i in p['images']:
   assert i.get('src','').startswith('/') and not i['src'].startswith('//') and '..' not in i['src'] and (ROOT/i['src'].lstrip('/')).is_file(),'Missing local image'
   assert i.get('alt') and i.get('rightsApproved') is True and i.get('approvalSource'),'Image permission required'
   assert all(type(i.get(n)) is int and i[n]>0 for n in ['width','height']),'Image dimensions required'
   for variant in i.get('responsiveSources',[]):
    assert variant.get('src','').startswith('/') and not variant['src'].startswith('//') and '..' not in variant['src'] and (ROOT/variant['src'].lstrip('/')).is_file(),'Missing responsive source'
    assert type(variant.get('width')) is int and variant['width']>0,'Responsive width required'
  assert p.get('socialImage') in [i['src'] for i in p['images']],'Social image must be approved product image'
  price=p.get('priceRwf')
  assert price is None or type(price) is int and 0<price<=100000000,'Invalid approved price'
  assert price is None or p.get('priceApproved') is True,'Price approval required'
  assert p['availability']!='Available on Orders' or price is None,'On-order products have no fixed price'
  assert p['availability']!='Available in Stock' or price is not None,'Stock price required'
  assert type(p.get('stockQuantity')) is int and p['stockQuantity']>=0,'Stock quantity required'
  assert isinstance(p.get('variations'),list) and p['variations'],'Explicit variations required (use Not applicable if genuinely unsized)'
  vids=set()
  for v in p['variations']:
   assert re.fullmatch(r'[A-Za-z0-9_-]{1,64}',v.get('id','')) and v['id'] not in vids,'Invalid/duplicate variation';vids.add(v['id'])
   assert all(isinstance(v.get(n),str) and v[n].strip() for n in ['size','colour']),'Size/colour required'
   assert type(v.get('stockQuantity')) is int and v['stockQuantity']>=0,'Variation stock required'
  assert sum(v['stockQuantity'] for v in p['variations'])==p['stockQuantity'],'Stock totals inconsistent'
  assert p['availability']=='Available in Stock' and p['stockQuantity']>0 or p['availability']!='Available in Stock' and p['stockQuantity']==0,'Stock/status conflict'
  out.append(p)
 return out

def route(p):return '/shop/'+p['slug']+'/'
