"""Owner-approved public enquiry displays, independent of sale/stock publication."""
import json,hashlib
from shop_catalog import ROOT,load
KEYS=['id','slug','name','category','description','images']
def display_model(p):return {k:p[k] for k in KEYS}
def fingerprint(p):
 model=display_model(p);assets=[]
 for i in model['images']:
  src=i['src'];assert src.startswith('/') and not src.startswith('//') and '..' not in src
  path=ROOT/src.lstrip('/');assert path.is_file()
  assets.append(hashlib.sha256(path.read_bytes()).hexdigest())
 return hashlib.sha256(json.dumps({'display':model,'assets':assets},sort_keys=True,ensure_ascii=False).encode()).hexdigest()
def approved():
 data=json.loads((ROOT/'_data/shop-products.json').read_text());load(data)
 policy=json.loads((ROOT/'_data/shop-public-enquiries.json').read_text());assert policy['scope']=='public-enquiry-display-only' and policy.get('ownerApproval') and policy.get('date')
 entries=policy['products'];assert len({e['id'] for e in entries})==len(entries)
 by_id={p['id']:p for p in data['products']};out=[]
 for e in entries:
  assert e['id'] in by_id,'Remove obsolete enquiry approval before withdrawing a record'
  p=by_id[e['id']]
  if p['publicationStatus'] in ['published','archived']:continue
  assert p['publicationStatus']=='draft' and fingerprint(p)==e['displayFingerprint'],'Unreviewed display change requires owner approval'
  out.append(display_model(p))
 return out
