#!/usr/bin/env python3
"""R44 source audit: category-aware recommendations, breadcrumbs and preserved detail journey."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,urljoin
import argparse,json,re,subprocess,sys
ROOT=Path(__file__).resolve().parents[1];BASE='778555792a24f87c97ab3e7e47c5d3f3b8219936';DOMAIN='https://mrsewingfashion.com'
sys.path.insert(0,str(ROOT/'scripts'))
from build_collections import load,design_route,recommendations
from suit_references import assignment,categories
class Parse(HTMLParser):
 def __init__(self,s):
  super().__init__(convert_charrefs=True);self.tags=[];self.headings=[];self.schemas=[];self.current=None;self.buf='';self.feed(s)
 def handle_starttag(self,t,attrs):
  a=dict(attrs);self.tags.append((t,a))
  if t in ['title','h1','h2','h3','h4'] or t=='script' and a.get('type')=='application/ld+json':self.current=t;self.buf=''
 def handle_data(self,s):
  if self.current:self.buf+=s
 def handle_endtag(self,t):
  if self.current==t:
   if t=='script':self.schemas.append(json.loads(self.buf))
   else:self.headings.append((t,self.buf.strip()))
   self.current=None
 def attrs(self,t):return [a for n,a in self.tags if n==t]
def original(f):return subprocess.check_output(['git','show',BASE+':'+f],cwd=ROOT,text=True)
def semantic_nodes(schemas):
 return [n for s in schemas for n in (s['@graph'] if '@graph' in s else [s])]
def primary(s):return re.search(r'<article class="design-layout">.*?</article>',s,re.S).group()
def section(s,ident):return re.search(r'<div class="show-grid" id="'+ident+r'">(.*?)</section>',s,re.S).group(1)
def records(s,ident):
 area=section(s,ident);ids=re.findall(r'<article\b[^>]*data-id="([^"]+)"',area);a=Parse(area);return ids,a
parser=argparse.ArgumentParser();parser.add_argument('--capture-baseline',action='store_true');parser.add_argument('--report',default='/workspace/review/design-detail-refinement-2026-11-12/preservation.json');args=parser.parse_args()
pool=load()[0];by_id={d['id']:d for d in pool};catalog=categories();out={'baseline':BASE,'scope':len(pool),'details':{},'limitations':['Static source audit; real device, live rendering, rich-result eligibility and Google indexing not established.']}
for d in pool:
 route=design_route(d);f=route.strip('/')+'/index.html';old=original(f);new=(ROOT/f).read_text();a,b=Parse(old),Parse(new);c=assignment(d['id'])
 out['details'][route]={'id':d['id'],'category':c['id'] if c else None,'before':{'metadata':a.attrs('meta'),'headings':a.headings,'schemas':a.schemas,'canonical':[x for x in a.attrs('link') if x.get('rel')=='canonical']},'after':{'metadata':b.attrs('meta'),'headings':b.headings,'schemas':b.schemas,'canonical':[x for x in b.attrs('link') if x.get('rel')=='canonical']}}
 if args.capture_baseline:continue
 assert a.attrs('meta')==b.attrs('meta'),f+' metadata/indexing changed'
 assert re.findall(r'<script data-staging-indexing>.*?</script>',old,re.S)==re.findall(r'<script data-staging-indexing>.*?</script>',new,re.S),f+' staging noindex script'
 assert [(t,v)for t,v in a.headings if t in ['title','h1']]==[(t,v)for t,v in b.headings if t in ['title','h1']],f+' title/H1'
 assert [x for x in a.attrs('link') if x.get('rel')=='canonical']==[x for x in b.attrs('link') if x.get('rel')=='canonical'],f+' canonical'
 assert primary(old)==primary(new),f+' primary photograph/copy/selection/fabric journey changed'
 for pattern,kind in [(r'<header\b[^>]*class="homepage-header"[^>]*>.*?</header>','brand header'),(r'<footer\b.*?</footer>','footer'),(r'<aside class="announcement-bar".*?</aside>','OFFER markup')]:
  assert re.search(pattern,old,re.S).group()==re.search(pattern,new,re.S).group(),f+' '+kind
 old_nodes=semantic_nodes(a.schemas);new_nodes=semantic_nodes(b.schemas)
 for node in old_nodes:
  matches=[x for x in new_nodes if x.get('@type')==node.get('@type') and x.get('url')==node.get('url')]
  assert len(matches)==1,f+' existing schema removed/duplicated'
  assert all(matches[0].get(k)==v for k,v in node.items() if k!='@context'),f+' existing schema information changed'
 assert all(n.get('@type') in {x.get('@type')for x in old_nodes}|{'BreadcrumbList'}for n in new_nodes),f+' unrelated structured data'
 old_crumb=re.search(r'<nav class="customer-breadcrumb".*?</nav>',old,re.S);new_crumb=re.search(r'<nav class="customer-breadcrumb".*?</nav>',new,re.S)
 if c:
  assert old_crumb and new_crumb,f+' breadcrumb missing'
  before=Parse(old_crumb.group());after=Parse(new_crumb.group());assert [(x.get('href'),x.get('aria-current'))for x in before.attrs('a')]==[(x.get('href'),x.get('aria-current'))for x in after.attrs('a')],f+' breadcrumb destinations changed'
  expected=[('Custom Tailoring & Suits','/services/custom-tailoring/'),("Men's Suits"if c['gender']=='men'else"Women's Suits",'/mensuits/'if c['gender']=='men'else'/womensuits/'),(c['title'],c['route']),(dict(Parse(old).headings).get('h1'),route)]
  crumbs=[x for x in new_nodes if x.get('@type')=='BreadcrumbList'];assert len(crumbs)==1,f+' exactly one BreadcrumbList required'
  items=crumbs[0]['itemListElement'];assert len(items)==4,f+' schema breadcrumb length'
  for pos,((name,dest),item) in enumerate(zip(expected,items),1):
   assert item['position']==pos and item['name']==name and item['item']==DOMAIN+dest,f+' BreadcrumbList mismatch'
 else:
  assert not new_crumb,f+' must not fabricate category for unassigned record'
 used={d['id']};photos={d['images'][0]['src']};groups=[]
 for which in ['similar-designs','more-designs']:
  ids,parsed=records(new,which);groups.append(ids)
  assert len(ids)==len(set(ids)),f+' duplicate recommended design'
  assert len(ids)<=4,f+' excessive recommendations'
  for ident in ids:
   assert ident in by_id and ident not in used,f+' current/unapproved/duplicate recommendation'
   other=by_id[ident];assigned=assignment(ident)
   assert c and assigned and assigned['gender']==c['gender'],f+' cross-gender/unassigned recommendation'
   assert (assigned['id']==c['id'])==(which=='similar-designs'),f+' wrong recommendation category'
   photo=other['images'][0]['src'];assert photo not in photos,f+' duplicate recommended photograph'
   photos.add(photo);used.add(ident)
  expected_links=[design_route(by_id[ident])for ident in ids]
  assert [x['href']for x in parsed.attrs('a')]==expected_links,f+' recommended link mismatch'
  assert [x['src']for x in parsed.attrs('img')]==[by_id[ident]['images'][0]['thumb']for ident in ids],f+' recommended photo mismatch'
 more_categories=[assignment(i)['id']for i in groups[1]];assert len(more_categories)==len(set(more_categories)),f+' cross-category diversity'
 if not c:assert groups==[[],[]],f+' unassigned detail must not infer category/gender'
 first=recommendations(d,pool);second=recommendations(d,pool);assert [[x['id']for x in g]for g in first]==[[x['id']for x in g]for g in second],f+' unstable recommendations'
 assert groups==[[x['id']for x in g]for g in first],f+' generated recommendation list stale'
 out['details'][route]['recommendations']={'similar':groups[0],'more':groups[1]}
if not args.capture_baseline:
 for f in ['sitemap.xml','robots.txt','_headers','_data/collection-designs.json','_data/collection-id-registry.json','_data/suit-reference-categories.json','_data/request-reference-allowlist.json','_data/suit-package-prices.json','_data/tuxedo-package-prices.json','_data/customer-faqs.json','_data/fabric-reference-catalogue.json','_templates/design-selection-sharing.js','_templates/customer-interactions.js','_templates/customer-site.js','functions/_lib/selected-design-handler.js','index.html']:
  assert (ROOT/f).read_bytes()==subprocess.check_output(['git','show',BASE+':'+f],cwd=ROOT),f+' out-of-scope change'
 images={i['originalPath'] for d in json.loads((ROOT/'_data/collection-designs.json').read_text())['designs'] if d['id'] in {x['id'] for x in pool} for i in d['images']}
 for image in images:assert (ROOT/image).read_bytes()==subprocess.check_output(['git','show',BASE+':'+image],cwd=ROOT),image+' original changed'
 out['originalImagesPreserved']=len(images)
Path(args.report).parent.mkdir(parents=True,exist_ok=True);Path(args.report).write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(('CAPTURED'if args.capture_baseline else'PASS')+'28published detail SEO/primary journey/header/footer/OFFER/photo preservation;27category recommendation boundaries/diversity/stability/BreadcrumbList;MS007unassigned guard')
