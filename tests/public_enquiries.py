"""Public visual approval never grants stock/price/purchase approval."""
import sys,json,tempfile,copy
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import public_enquiries as pe
from shop_catalog import load
ROOT=pe.ROOT;raw=json.loads((ROOT/'_data/shop-products.json').read_text());policy=json.loads((ROOT/'_data/shop-public-enquiries.json').read_text())
assert len(pe.approved())==21 and not load()
with tempfile.TemporaryDirectory() as d:
 tmp=Path(d);(tmp/'_data').mkdir()
 for p in raw['products']:
  for image in p['images']:
   target=tmp/image['src'].lstrip('/');target.parent.mkdir(parents=True,exist_ok=True)
   if not target.exists():target.symlink_to(ROOT/image['src'].lstrip('/'))
 (tmp/'_data/shop-public-enquiries.json').write_text(json.dumps(policy))
 future=copy.deepcopy(raw['products'][0]);future.update(id='FUTURE_UNAPPROVED_QA',slug='future-unapproved-qa')
 source=copy.deepcopy(raw);source['products'].append(future);(tmp/'_data/shop-products.json').write_text(json.dumps(source));old=pe.ROOT;pe.ROOT=tmp
 try:
  assert len(pe.approved())==21 and all(p['id']!='FUTURE_UNAPPROVED_QA' for p in pe.approved())
  source['products'][0]['name']='Unreviewed change';(tmp/'_data/shop-products.json').write_text(json.dumps(source))
  try:pe.approved();raise RuntimeError('Unapproved display edit escaped fingerprint')
  except AssertionError:pass
 finally:pe.ROOT=old
print('PASS21explicit public enquiry approvals;future draft excluded;changed content rejected;raw drafts/commerce publication gate preserved')
