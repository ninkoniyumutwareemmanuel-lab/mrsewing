#!/usr/bin/env python3
"""R42 compare approved SEO and detail journeys to pre-edit staging baseline."""
from pathlib import Path
from html.parser import HTMLParser
import json,re,subprocess,sys,argparse
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_collections import load,design_route
BASE='d0885a738f0aae0c1e6324acd5efee8412dccd90'
class Parse(HTMLParser):
 def __init__(self,s):
  super().__init__(convert_charrefs=True);self.tags=[];self.heading=[];self.current=None;self.buf='';self.schemas=[];self.feed(s)
 def handle_starttag(self,t,attrs):
  a=dict(attrs);self.tags.append((t,a))
  if t in ['h1','h2','h3','h4','title'] or t=='script' and a.get('type')=='application/ld+json':self.current=t;self.buf=''
 def handle_data(self,s):
  if self.current:self.buf+=s
 def handle_endtag(self,t):
  if self.current==t:
   if t=='script':self.schemas.append(json.loads(self.buf))
   else:self.heading.append((t,self.buf.strip()))
   self.current=None
 def attrs(self,t):return [a for name,a in self.tags if name==t]
def original(f):return subprocess.check_output(['git','show',BASE+':'+f],cwd=ROOT,text=True)
def main(s):return re.search(r'<main\b.*?</main>',s,re.S)[0]
def r44_stable(s):
 # Only approved recommendation sections and breadcrumb presentation may change.
 s=re.sub(r'<section class="design-related".*?</section>','',s,flags=re.S)
 return re.sub(r'<nav class="customer-breadcrumb".*?</nav>','<!-- breadcrumb contract covered by design_detail_preservation.py -->',s,flags=re.S)
def schema_preserved(before,after):
 old=[n for s in before for n in s.get('@graph',[s])];new=[n for s in after for n in s.get('@graph',[s])]
 assert all(n in new for n in old),'existing schema removed or changed'
 assert all(n in old or n.get('@type')=='BreadcrumbList'for n in new),'unapproved schema addition'

def snapshot(s):
 p=Parse(s);return {'headings':p.heading,'meta':p.attrs('meta'),'canonical':[a for a in p.attrs('link') if a.get('rel')=='canonical'],'images':p.attrs('img'),'links':p.attrs('a'),'schemas':p.schemas}
model=json.loads((ROOT/'_data/suit-reference-categories.json').read_text());galleries={c['route']:c for c in model['categories']};detail_routes=[design_route(d) for d in load()[0]];routes=['/services/custom-tailoring/','/mensuits/','/womensuits/',*galleries,*detail_routes]
parser=argparse.ArgumentParser();parser.add_argument('--capture-baseline',action='store_true');parser.add_argument('--report',default='/workspace/review/suit-gallery-refinement-2026-11-12/seo-preservation.json');args=parser.parse_args()
report={'baseline':BASE,'scope':len(routes),'routes':{},'preserved':['canonical URLs','existing titles and H1s','all non-recommendation image src/srcset/alt/dimensions','all non-recommendation anchor destinations','JSON-LD structure and verified business data','sitemap/robots/staging-noindex','published detail primary content and quotation context; R44 recommendation/breadcrumb regions audited separately'],'intentionalChanges':['category gallery introductions and H2 instructions','gallery card names omit visible internal IDs','shared OFFER insertion','R44 category-aware recommendation sections and breadcrumb presentation/BreadcrumbList; exact contracts in design_detail_preservation.py'],'limitations':['Local source comparison; rendered/live status and Google indexing are not established by this test.']}
for route in routes:
 f=route.strip('/')+'/index.html';old=original(f);before=Parse(old);new=(ROOT/f).read_text();after=Parse(new)
 report['routes'][route]={'before':snapshot(old),'after':snapshot(new)}
 if args.capture_baseline:continue
 assert [(h,v) for h,v in before.heading if h in ['title','h1']]==[(h,v) for h,v in after.heading if h in ['title','h1']],f+' title/H1'
 assert [a for a in before.attrs('link') if a.get('rel')=='canonical']==[a for a in after.attrs('link') if a.get('rel')=='canonical'],f+' canonical'
 stable_before=Parse(r44_stable(old)) if route in detail_routes else before
 stable_after=Parse(r44_stable(new)) if route in detail_routes else after
 assert stable_before.attrs('img')==stable_after.attrs('img'),f+' non-recommendation image/alt preservation'
 assert stable_before.attrs('a')==stable_after.attrs('a'),f+' non-recommendation link preservation'
 assert before.attrs('meta')==after.attrs('meta'),f+' metadata/indexing preservation'
 if route in detail_routes:schema_preserved(before.schemas,after.schemas)
 else:assert before.schemas==after.schemas,f+' schema preservation'
 for pattern,kind in [(r'<header\b[^>]*class="homepage-header"[^>]*>.*?</header>','brand header'),(r'<footer\b.*?</footer>','footer')]:
  assert re.search(pattern,old,re.S).group()==re.search(pattern,new,re.S).group(),f+' '+kind
 if route not in galleries:
  assert main(r44_stable(old)if route in detail_routes else old)==main(r44_stable(new)if route in detail_routes else new),f+' non-recommendation main content changed'
  assert before.attrs('meta')==after.attrs('meta'),f+' existing detail/landing metadata changed'
for f in ['sitemap.xml','robots.txt','_headers','_data/collection-designs.json','_data/collection-id-registry.json','_data/request-reference-allowlist.json','_data/suit-package-prices.json','_data/tuxedo-package-prices.json','_data/fabric-reference-catalogue.json','_data/customer-faqs.json','index.html']:
 if not args.capture_baseline:assert (ROOT/f).read_text()==original(f),f+' out of scope change'
if not args.capture_baseline:
 original_images={image['originalPath'] for design in json.loads((ROOT/'_data/collection-designs.json').read_text())['designs'] if design['id'] in {d['id'] for d in load()[0]} for image in design['images']}
 for image in original_images:
  assert (ROOT/image).read_bytes()==subprocess.check_output(['git','show',BASE+':'+image],cwd=ROOT),'Original image changed: '+image
 report['originalImageBytesPreserved']=len(original_images)
Path(args.report).parent.mkdir(parents=True,exist_ok=True);Path(args.report).write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(('CAPTURED' if args.capture_baseline else 'PASS')+f' {len(routes)} page SEO baselines; canonical/title/H1/alt/links/schema preservation and details/landing main-content contract')
