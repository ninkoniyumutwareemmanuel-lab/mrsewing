"""Explicit build-time staging display gate; never a merchandise publication gate."""
import json,os
from urllib.parse import urlparse
from shop_catalog import ROOT
BRANCH='phase1/customer-journey-repairs'
def enabled(env=None):
 env=os.environ if env is None else env
 host=urlparse(env.get('CF_PAGES_URL','')).hostname or ''
 return urlparse(env.get('CF_PAGES_URL','')).scheme=='https' and env.get('CF_PAGES')=='1' and env.get('CF_PAGES_BRANCH')==BRANCH and (host=='mrsewing-staging.pages.dev' or host.endswith('.mrsewing-staging.pages.dev'))
def candidates():
 out=[]
 for p in json.loads((ROOT/'_data/shop-products.json').read_text())['products']:
  if p['publicationStatus']!='draft':continue
  # Validate identity via the ordinary loader; check original assets without granting rights.
  from shop_catalog import load
  load({'schemaVersion':1,'products':[p]})
  assert p.get('name') and p.get('category') and p.get('images')
  for image in p['images']:
   src=image['src'];assert src.startswith('/') and not src.startswith('//') and '..' not in src and (ROOT/src.lstrip('/')).is_file()
  # Deliberately omit commercial fields and internal evidence from the display model.
  out.append({k:p[k] for k in ['id','slug','name','category','description','images']})
 return out
