"""Publication gates, source-driven generation and withdrawal contracts. No live merchandise."""
import sys,json,copy,tempfile,subprocess
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from shop_catalog import load,ROOT
from build_commerce import outputs
p={'id':'QA_ONLY','slug':'qa-only-product','name':'Synthetic QA fixture — not merchandise','category':'QA only','description':'Unpublished test fixture.','publicationStatus':'published','approval':{'publicDisplay':True,'source':'Automated test fixture only','date':'2026-11-06'},'images':[{'src':'/hero-custom-tailoring.webp','alt':'Synthetic test asset reuse, not merchandise','width':1024,'height':1024,'rightsApproved':True,'approvalSource':'Test fixture only'}],'availability':'Available in Stock','priceRwf':12345,'priceApproved':True,'stockQuantity':3,'variations':[{'id':'qa-a','size':'QA M','colour':'QA blue','stockQuantity':2},{'id':'qa-b','size':'QA L','colour':'QA blue','stockQuantity':1}],'specifications':{'Material':'QA only'},'careInstructions':'QA only','orderingNotes':'Not merchandise','seoTitle':'Synthetic QA product','seoDescription':'Automated fixture; never published.','socialImage':'/hero-custom-tailoring.webp'}
def valid(x):return load({'schemaVersion':1,'products':x})
assert load()==[], 'Live merchandise must not be fabricated for this task'
assert valid([p])==[p]
for change in [{'availability':'Made to Order'},{'priceApproved':False},{'priceRwf':None},{'stockQuantity':4},{'slug':'cart'},{'approval':{}},{'images':[]},{'availability':'Available on Orders'}]:
 q=copy.deepcopy(p);q.update(change)
 try:valid([q]);raise RuntimeError('Invalid record accepted '+repr(change))
 except AssertionError:pass
q=copy.deepcopy(p);q['publicationStatus']='draft';assert valid([q])==[]
for status in ['Available on Orders','Out of Stock']:
 q=copy.deepcopy(p);q['availability']=status;q['stockQuantity']=0;q['priceRwf']=None
 for v in q['variations']:v['stockQuantity']=0
 assert valid([q])==[q]
assert ROOT/'shop/qa-only-product/index.html' in outputs([p])
source=outputs([p])[ROOT/'shop/qa-only-product/index.html'];assert p['name'] in source and '"@type": "Product"' in source and 'https://mrsewingfashion.com/shop/qa-only-product/' in source
import re
schemas=[json.loads(x) for x in re.findall(r'<script type="application/ld\+json">(.*?)</script>',source,re.S)]
product_schema=next(x for x in schemas if x.get('@type')=='Product')
assert product_schema['offers']['priceCurrency']=='RWF' and product_schema['offers']['price']==12345
assert product_schema['offers']['availability']=='https://schema.org/InStock'
assert '<meta property="og:type" content="product">' in source
assert '<meta property="og:image" content="https://mrsewingfashion.com/hero-custom-tailoring.webp">' in source
assert '<meta name="twitter:image" content="https://mrsewingfashion.com/hero-custom-tailoring.webp">' in source
assert '<meta name="robots" content="noindex, follow">' in (ROOT/'shop/cart/index.html').read_text()
assert 'shop/qa-only-product/index.html' not in json.loads((ROOT/'_data/shop-generated-pages.json').read_text())
assert (ROOT/'booking/index.html').read_text().replace('aria-label="Online Shop"','aria-label="Shop — Coming Soon" title="Shop — Coming Soon; online purchasing is not available yet"')==subprocess.check_output(['git','show','09be5c7:booking/index.html'],cwd=ROOT,text=True)
# Only exact authorised homepage navigation edits are permitted.
current=(ROOT/'index.html').read_text().replace('aria-label="Online Shop"','aria-label="Shop — Coming Soon" title="Shop — Coming Soon; online purchasing is not available yet"')
import re
current=current.replace('from{transform:translateX(0)}to{transform:translateX(-50%)}','from{transform:translateX(-50%)}to{transform:translateX(0)}').replace('data-whatsapp-modal href="/whatsapp/"','href="/whatsapp/"')
current=re.sub(r'<a href="/(?:loyalty|referral)-program/">([^<]+)</a>',r'\1',current)
assert current==subprocess.check_output(['git','show','09be5c7:index.html'],cwd=ROOT,text=True)
assert (ROOT/'assets/homepage.js').read_bytes()==subprocess.check_output(['git','show','09be5c7:assets/homepage.js'],cwd=ROOT)
for path in ['_templates/consultation.js','scripts/consultation_form.py','_templates/homepage-quotation.html','_data/public-page-seo.json','_data/business.json','_data/collection-designs.json','_data/customer-projects.json']:
 assert (ROOT/path).read_bytes()==subprocess.check_output(['git','show','09be5c7:'+path],cwd=ROOT),path
# Prove a single catalogue edit updates listing/detail/server records, then withdrawal removes them.
import shop_catalog
with tempfile.TemporaryDirectory() as tmp:
 temp=Path(tmp);(temp/'_data').mkdir();(temp/'hero-custom-tailoring.webp').symlink_to(ROOT/'hero-custom-tailoring.webp')
 oldroot=shop_catalog.ROOT
 try:
  shop_catalog.ROOT=temp
  source=temp/'_data/shop-products.json';source.write_text(json.dumps({'schemaVersion':1,'products':[p]}))
  rendered=outputs();assert p['name'] in rendered[ROOT/'shop/index.html'] and ROOT/'shop/qa-only-product/index.html' in rendered
  changed=copy.deepcopy(p);changed['name']='Changed synthetic QA name';source.write_text(json.dumps({'schemaVersion':1,'products':[changed]}))
  rendered=outputs();assert changed['name'] in rendered[ROOT/'shop/index.html'] and changed['name'] in rendered[ROOT/'shop/qa-only-product/index.html'] and changed['name'] in rendered[ROOT/'functions/_lib/shop-runtime.js']
  source.write_text(json.dumps({'schemaVersion':1,'products':[]}));rendered=outputs();assert ROOT/'shop/qa-only-product/index.html' not in rendered and changed['name'] not in rendered[ROOT/'shop/index.html']
 finally:shop_catalog.ROOT=oldroot

# Fixture products are rendered outside deployment root for browser interception only.
ps=[]
for n,status in enumerate(['Available in Stock','Available on Orders','Out of Stock']):
 q=copy.deepcopy(p);q.update(id='QA_'+str(n),slug='qa-only-'+str(n),name='Synthetic QA '+str(n),availability=status,category=["Men's Suits",'Clothes Hangers','Garment Covers'][n])
 if n:
  q['stockQuantity']=0;q['priceRwf']=None
  for v in q['variations']:v['stockQuantity']=0
 ps.append(q)
valid(ps)
review=Path('/workspace/review/commerce');review.mkdir(parents=True,exist_ok=True)
(review/'fixtures.json').write_text(json.dumps(ps))
fixture_pages={str(k.relative_to(ROOT)):v for k,v in outputs(ps).items() if k.suffix=='.html'}
(review/'fixture-pages.json').write_text(json.dumps(fixture_pages))
print('PASS catalogue publication/stock/price/rights validation, source-driven product HTML/schema, empty live catalogue and unchanged booking body; test fixtures outside site root')
