"""R59 synthetic publication-gate and Backorder label tests; no draft merchandise published."""
import sys,copy
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from shop_catalog import load,STATUSES
from build_commerce import outputs
assert STATUSES==('Available in Stock','Available on Backorder','Out of Stock')
assert load()==[], 'No unverified Shop products may become sale-published'
p={'id':'QA_R59','slug':'qa-r59','name':'QA Example','category':'QA','description':'Nonpublic synthetic example','publicationStatus':'published','approval':{'publicDisplay':True,'source':'test-only','date':'2026-11-22'},'images':[{'src':'/hero-custom-tailoring.webp','alt':'Test asset only','width':1024,'height':1024,'rightsApproved':True,'approvalSource':'test-only'}],'availability':'Available in Stock','priceRwf':12000,'priceApproved':True,'stockQuantity':1,'variations':[{'id':'qa-var','size':'Test','colour':'Test','stockQuantity':1}],'specifications':{'Scope':'test only'},'careInstructions':'test only','orderingNotes':'test only','seoTitle':'Test product','seoDescription':'Test only','socialImage':'/hero-custom-tailoring.webp'}
assert len(load({'schemaVersion':1,'products':[p]}))==1
for status in ('Available on Backorder','Out of Stock'):
 q=copy.deepcopy(p);q['availability']=status;q['priceRwf']=None;q['stockQuantity']=0;q['variations'][0]['stockQuantity']=0
 assert len(load({'schemaVersion':1,'products':[q]}))==1
q=copy.deepcopy(p);q['availability']='Available on Orders'
try:load({'schemaVersion':1,'products':[q]});raise RuntimeError('Legacy label still accepted')
except AssertionError:pass
q=copy.deepcopy(p);q['publicationStatus']='draft';q['availability']=None
assert load({'schemaVersion':1,'products':[q]})==[]
html=outputs()[ROOT/'shop/index.html']
assert 'Explore Made-to-Order Clothing Designs' in html and 'href="/collections/"' in html
assert 'Reference designs are not Shop stock' in html
runtime=(ROOT/'functions/_lib/shop-handler.js').read_text()
assert 'Available on Backorder' in runtime and 'Available on Orders' not in runtime
assert 'Available on Backorder' in (ROOT/'assets/commerce.js').read_text()
print('PASS: three availability labels, honest Shop inspiration, sale publication/stock and quote gate')
