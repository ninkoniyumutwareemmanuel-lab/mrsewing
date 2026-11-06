"""Build-time preview isolation; this is not merchandise approval."""
import sys,os,json
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from shop_preview import enabled,candidates,BRANCH
from shop_catalog import ROOT,load
from build_commerce import outputs
base={'CF_PAGES':'1','CF_PAGES_BRANCH':BRANCH,'CF_PAGES_URL':'https://abc.mrsewing-staging.pages.dev'}
assert enabled(base)
for edits in [{'CF_PAGES_BRANCH':'main'},{'CF_PAGES_URL':'https://mrsewingfashion.com'},{'CF_PAGES_URL':'https://evil-mrsewing-staging.pages.dev'},{'CF_PAGES':'0'},{'CF_PAGES_BRANCH':'other'},{'CF_PAGES_URL':'http://abc.mrsewing-staging.pages.dev'}]:assert not enabled(base|edits)
assert not enabled({})
ps=candidates();assert len(ps)==21 and len({p['id'] for p in ps})==21
assert sorted(__import__('collections').Counter(p['category'] for p in ps).values())==[2,2,2,4,4,7]
assert not load()
prod=outputs();assert 'Draft — Awaiting Approval' not in prod[ROOT/'shop/index.html']
os.environ.update(base);preview=outputs()
assert preview[ROOT/'shop/index.html'].count('class="product-card draft-card"')==21
assert '<meta name="robots" content="noindex, nofollow"' in preview[ROOT/'shop/index.html']
assert preview[ROOT/'functions/_lib/shop-runtime.js']==prod[ROOT/'functions/_lib/shop-runtime.js']
for p in ps:
 html=preview[ROOT/'shop'/p['slug']/'index.html']
 assert 'Draft — Awaiting Approval' in html and 'productSelection' not in html and 'data-commerce-form' not in html
 assert '"@type": "Product"' not in html and '"@type": "Offer"' not in html
 assert 'noindex, nofollow' in html
 assert ROOT/'shop'/p['slug']/'index.html' not in prod
print('PASS 21 drafts;6categories;8gate scenarios;production exclusion;no actions/offers/schema;unchanged API catalogue')
