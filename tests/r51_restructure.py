#!/usr/bin/env python3
"""R51 staged architecture checks; immutable Git baseline, no live/inbox claims.

Use --capture-baseline before implementation to save review evidence. Approved
service prices remain internal data; only their public presentation is removed.
"""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import unquote,urlsplit
import argparse,copy,hashlib,json,re,subprocess,sys
ROOT=Path(__file__).resolve().parents[1]
BASE='b2b8946882929da4ce7e0e01de4ba1511eed818a'
OUT=Path('/workspace/review/r51-restructure-2026-11-19')
PROTECTED={
 '_data/suit-package-prices.json','_data/tuxedo-package-prices.json',
 '_data/customer-policy-facts.json','_data/shop-products.json',
 '_data/shop-public-enquiries.json','_data/customer-request-backend.json',
 '_data/public-api.json','functions/_lib/public-api-config.js',
 'functions/_lib/public-api-cors.js','CNAME','robots.txt','_headers',
 '_data/collection-designs.json','_data/customer-projects.json',
 '_data/suit-reference-categories.json','_data/collection-id-registry.json',
 '_data/collection-image-inventory.json',
}
def git(*args):return subprocess.check_output(['git',*args],cwd=ROOT)
def old(path):return git('show',BASE+':'+path)
def digest(data):return hashlib.sha256(data).hexdigest()
class Page(HTMLParser):
 def __init__(self,source):
  super().__init__(convert_charrefs=True);self.tags=[];self.schemas=[];self.blocks=[];self.active=[];self.headings=[];self.feed(source)
 def handle_starttag(self,tag,attrs):
  attrs=dict(attrs);self.tags.append((tag,attrs))
  if tag in ['title','h1','h2'] or tag=='script' and attrs.get('type')=='application/ld+json':self.active.append([tag,attrs,[]])
 def handle_data(self,value):
  for row in self.active:row[2].append(value)
 def handle_endtag(self,tag):
  for row in self.active[::-1]:
   if row[0]==tag:
    self.active.remove(row);text=''.join(row[2]);self.blocks.append((tag,row[1],text))
    if tag=='script':
     try:self.schemas.append(json.loads(text))
     except json.JSONDecodeError:self.schemas.append({'template':text})
    if tag in ['h1','h2']:self.headings.append((tag,text))
    break
 def metadata(self):
  return {'title':[x[2] for x in self.blocks if x[0]=='title'],
   'description':[a.get('content','') for t,a in self.tags if t=='meta' and a.get('name')=='description'],
   'canonical':[a.get('href','') for t,a in self.tags if t=='link' and a.get('rel')=='canonical'],
   'robots':[a.get('content','') for t,a in self.tags if t=='meta' and a.get('name')=='robots'],
   'h1':[x[1] for x in self.headings if x[0]=='h1']}
def capture():
 # NUL delimiters preserve filenames with Unicode, quotes and whitespace; Git's
 # default quotePath formatting would silently omit seven approved WebP names.
 files=[name.decode() for name in git('ls-tree','-r','--name-only','-z',BASE).split(b'\0') if name];media={};html={};forms={}
 for name in files:
  if re.search(r'\.(?:jpe?g|png|webp|avif|svg|gif|mp4|webm)$',name,re.I):media[name]=digest(old(name))
  if name.endswith('.html'):
   page=Page(old(name).decode());html[name]=page.metadata()
   names=[a.get('name') for t,a in page.tags if t in ['input','select','textarea'] and a.get('name')]
   if names:forms[name]={'names':names,'actions':[a.get('action','') for t,a in page.tags if t=='form']}
 result={'baseline':BASE,'media':media,'html':html,'forms':forms,'protected':{name:digest(old(name)) for name in PROTECTED}}
 OUT.mkdir(parents=True,exist_ok=True);(OUT/'immutable-baseline.json').write_text(json.dumps(result,indent=2)+'\n')
 print('PASS baseline captured:',len(html),'HTML,',len(media),'media,',len(forms),'form pages')
 return result

def shop_price_fixture():
 sys.path.insert(0,str(ROOT/'scripts'))
 from shop_catalog import load
 from build_commerce import card,product_page
 p=copy.deepcopy(json.loads(old('_data/shop-products.json'))['products'][0])
 p.update(id='R51_SYNTHETIC',slug='r51-synthetic-stock',name='Fictional R51 stock garment',category='Synthetic QA garments',description='Temporary test fixture; never published.',seoTitle='Fictional R51 stock garment | QA',seoDescription='Temporary synthetic approved-product fixture.',orderingNotes='Fictional order notes',careInstructions='Fictional care instructions',specifications={},publicationStatus='published',availability='Available in Stock',priceRwf=173000,priceApproved=True,stockQuantity=3,variations=[{'id':'R51_SIZE','size':'M','colour':'Navy','stockQuantity':3}],missingInformation=[],approval={'publicDisplay':True,'source':'Synthetic fixture, not real approval','date':'2026-11-19'})
 for image in p['images']:image.update(rightsApproved=True,approvalSource='Synthetic test only; no new publication')
 p['socialImage']=p['images'][0]['src']
 assert load({'schemaVersion':1,'products':[p]})==[p]
 assert 'RWF 173,000' in card(p)
 page=Page(product_page(p,[p]));products=[d for d in page.schemas if isinstance(d,dict) and d.get('@type')=='Product'];assert len(products)==1 and products[0]['offers']['price']==173000
 assert 'RWF 173,000' in product_page(p,[p])
 assert not load(),'Real Shop catalogue must remain publication-gated and empty until approved stock exists'


def faq_consistency():
 sys.path.insert(0,str(ROOT/'scripts'))
 from faq_help import catalogue,search_data,plain
 from customer_information import expand
 data,topics,questions,owners=catalogue();search=search_data();entries={row['id']:row for row in search['entries']}
 for topic in topics:
  path=ROOT/'faq'/topic['slug']/'index.html';page=Page(path.read_text());schemas=[d for d in page.schemas if isinstance(d,dict) and d.get('@type')=='FAQPage'];assert len(schemas)==1,topic['slug']
  expected=[(questions[i]['question'],plain(expand(questions[i]['answer']))) for i in topic['questions']]
  actual=[(q['name'],q['acceptedAnswer']['text']) for q in schemas[0]['mainEntity']];assert actual==expected,('FAQvisible/schema',topic['slug'])
  for ident in topic['questions']:
   assert entries[ident]['answer']==plain(expand(questions[ident]['answer']))
   assert 'id="'+ident+'"' in path.read_text()
 for row in search['entries']:
  u=urlsplit(row['source']);assert u.netloc=='mrsewingfashion.com',row
  target=ROOT/'index.html' if u.path=='/' else ROOT/u.path.strip('/')/'index.html';assert target.is_file(),row
  if u.fragment:assert 'id="'+unquote(u.fragment)+'"' in target.read_text(),row
 return len(topics),sum(len(t['questions']) for t in topics)


def shared_controller_contract():
 # Every canonical page must remain unchanged by another finalization pass.
 # In particular, cache versions must not prevent consent-controller cleanup.
 sys.path.insert(0,str(ROOT/'scripts'))
 from site_seo import INDEXABLE_ROUTES,finalize
 routes=set(INDEXABLE_ROUTES)|{'/terms-and-conditions/','/request/','/whatsapp/'}
 for route in sorted(routes):
  path=ROOT/'index.html' if route=='/' else ROOT/route.strip('/')/'index.html'
  source=path.read_text();assert finalize(source,path)==source,('non-idempotent finalizer',route)
  scripts=[urlsplit(a.get('src','')).path for tag,a in Page(source).tags if tag=='script' and a.get('src')]
  for asset in ['/assets/whatsapp-consent.js','/assets/customer-interactions.js']:
   assert scripts.count(asset)==1,('duplicate/missing shared consent controller',route,asset,scripts.count(asset))

def main():
 p=argparse.ArgumentParser();p.add_argument('--capture-baseline',action='store_true');args=p.parse_args()
 if args.capture_baseline:capture();return
 baseline=json.loads((OUT/'immutable-baseline.json').read_text()) if (OUT/'immutable-baseline.json').exists() else capture()
 for path,sha in baseline['protected'].items():assert digest((ROOT/path).read_bytes())==sha,('protected source changed',path)
 for path,sha in baseline['media'].items():assert (ROOT/path).is_file() and digest((ROOT/path).read_bytes())==sha,('original media changed/lost',path)
 # R51 changes content/nav/pricing; it does not authorize unrelated SEO rewrites.
 exceptions={'terms-and-conditions.html','terms-and-conditions/index.html'}
 for path,meta in baseline['html'].items():
  current=ROOT/path;assert current.is_file(),('old public/source HTML removed',path)
  page=Page(current.read_text())
  for key,values in meta.items():
   if path in exceptions and key=='h1':continue
   if path=='faq/collections-designs/index.html' and key=='description':
    topic=next(t for t in json.loads((ROOT/'_data/customer-faqs.json').read_text())['topics'] if t['slug']=='collections-designs')
    assert page.metadata()[key]==[topic['description']+' Find practical answers from Mr Sewing and the next step for your enquiry.'],('FAQShowroommetadata',key);continue
   if path=='faq/prices-packages-payments/index.html' and key in ['title','description','h1']:
    topic=next(t for t in json.loads((ROOT/'_data/customer-faqs.json').read_text())['topics'] if t['slug']=='prices-packages-payments');expected={'title':[topic['title']+' FAQs | Mr Sewing Fashion, Kigali'],'description':[topic['description']+' Find practical answers from Mr Sewing and the next step for your enquiry.'],'h1':[topic['title']+' FAQs']}
    assert page.metadata()[key]==expected[key],('FAQquotationmetadata',key);continue
   assert page.metadata()[key]==values,('unapproved existing metadata change',path,key,values,page.metadata()[key])
 for path,form in baseline['forms'].items():
  if path.startswith('_templates/'):continue
  page=Page((ROOT/path).read_text());names=[a.get('name') for t,a in page.tags if t in ['input','select','textarea'] and a.get('name')];actions=[a.get('action','') for t,a in page.tags if t=='form'];assert names==form['names'] and actions==form['actions'],('existing form fields/provider changed',path)
 assert not json.loads((ROOT/'_data/customer-request-backend.json').read_text())['enabled']
 prices=json.loads((ROOT/'_data/suit-package-prices.json').read_text())['prices'];assert prices['men-tier-3']['twoPieceRwf']==300000 and prices['men-tier-3']['threePieceRwf']==400000
 assert (ROOT/'showroom/index.html').is_file(),'Showroom not built'
 showroom=Page((ROOT/'showroom/index.html').read_text());assert showroom.metadata()['canonical']==['https://mrsewingfashion.com/showroom/']
 # Check no visible numeric service prices; Shop and commission benefits are distinct.
 visible_prices=[]
 for path in ROOT.rglob('*.html'):
  relative=path.relative_to(ROOT).as_posix()
  if relative.startswith(('.git/','.wrangler/','.github/','_templates/','shop/','docs/')) or relative in {'header.html','footer.html'}:continue
  raw=path.read_text();visible=re.sub(r'<(?:script|style)\b.*?</(?:script|style)>',' ',raw,flags=re.S|re.I);visible=re.sub('<[^>]*>',' ',visible);visible=re.sub(r'\s+',' ',visible)
  for match in re.finditer(r'(?<![\d,])(?:\d{1,3}(?:,\d{3})+|\d{4,})\s*(?:RWF|FRW)\b',visible,re.I):
   if match[0].startswith('6,000') and re.search(r'referr|commission',visible[max(0,match.start()-250):match.end()+250],re.I):continue
   visible_prices.append((relative,match[0]))
 assert not visible_prices,('public fixed service-price displays',visible_prices)
 # Existing stable URLs/canons remain; the new canonical Showroom is included once.
 sitemap=(ROOT/'sitemap.xml').read_text();assert sitemap.count('<loc>https://mrsewingfashion.com/showroom/</loc>')==1
 assert 'pages.dev' not in sitemap and 'X-Robots-Tag: noindex' in (ROOT/'_headers').read_text()
 assert (ROOT/'docs/WEBSITE_SOURCE_MAP.md').is_file()
 shop_price_fixture()
 faq_consistency()
 shared_controller_contract()
 print('PASS R51 protectedfacts/media/metadata/routes/privategate/internalprices/publicpriceabsence/Showroom/sitemap/source-map; actual deployed verification separate')
if __name__=='__main__':main()
