#!/usr/bin/env python3
"""R45 scoped selected-suit quote UI; protect SEO, fabric page and other forms."""
from pathlib import Path
from html.parser import HTMLParser
import argparse,json,re,subprocess,sys
ROOT=Path(__file__).resolve().parents[1]
BASE='3fd899e8ebee8ea90963b08e87205651e08d27d2'
sys.path.insert(0,str(ROOT/'scripts'))
from build_collections import load,design_route
from suit_references import categories
class Parse(HTMLParser):
 def __init__(self,s):
  super().__init__(convert_charrefs=True);self.tags=[];self.text=[];self.schemas=[];self.kind=None;self.buf='';self.feed(s)
 def handle_starttag(self,t,attrs):
  a=dict(attrs);self.tags.append((t,a))
  if t in ['title','h1'] or t=='script' and a.get('type')=='application/ld+json':self.kind=t;self.buf=''
 def handle_data(self,s):
  if self.kind:self.buf+=s
 def handle_endtag(self,t):
  if self.kind==t:
   if t=='script':self.schemas.append(json.loads(self.buf))
   else:self.text.append((t,self.buf.strip()))
   self.kind=None
 def attrs(self,t):return [a for tag,a in self.tags if tag==t]
def old(f):return subprocess.check_output(['git','show',BASE+':'+f],cwd=ROOT,text=True)
def cache_normalized(s):
 # Only generated version-query changes are allowed on otherwise protected pages.
 return re.sub(r'((?:src|href)="/assets/[^"?]+\.(?:js|css))\?v=[^"]+',r'\1',s)
def snapshot(s):
 p=Parse(s)
 return {'titleH1':p.text,'meta':p.attrs('meta'),'canonical':[a for a in p.attrs('link') if a.get('rel')=='canonical'],'schema':p.schemas}
parser=argparse.ArgumentParser();parser.add_argument('--capture-baseline',action='store_true');parser.add_argument('--report',default='/workspace/review/selected-suit-refinement-2026-11-12/preservation.json');args=parser.parse_args()
review='/services/custom-tailoring/selected-designs/'
selected=['/request/','/request/custom-tailoring/']
unrelated=['/services/custom-tailoring/special-order/','/request/alterations/','/request/garment-care/','/request/mobile-fitting/','/request/vip/','/request/vip-subscription/','/booking/']
browsing=['/services/custom-tailoring/','/mensuits/','/womensuits/',*[c['route']for c in categories()],*[design_route(d)for d in load()[0]]]
routes=[*browsing,review,'/services/custom-tailoring/fabric/',*selected,*unrelated]
report={'baseline':BASE,'scope':len(routes),'routes':{},'preserved':['all existing titles/descriptions/H1/canonical/JSON-LD/indexing','header/footer/OFFER markup','existing fabric-page markup and per-design selection implementation','all unrelated service-form markup and field attributes','approved catalogue/photos/prices/policies/FAQ','existing WhatsApp Terms controller and selected-submission provider endpoint'],'limitations':['Static audit does not establish device support, live responses, real inbox delivery or Google indexing.','Selected-suit runtime and provider payload behavior are covered by separate browser/server mocked tests.']}
for route in routes:
 f=route.strip('/')+'/index.html';before=old(f);after=(ROOT/f).read_text();a,b=Parse(before),Parse(after)
 report['routes'][route]={'before':snapshot(before),'after':snapshot(after)}
 if args.capture_baseline:continue
 assert snapshot(before)==snapshot(after),f+' SEO metadata/H1/schema/indexing changed'
 for pattern,label in [(r'<header\b[^>]*class="homepage-header"[^>]*>.*?</header>','header'),(r'<footer\b.*?</footer>','footer'),(r'<aside class="announcement-bar".*?</aside>','OFFER')]:
  aa,bb=re.search(pattern,before,re.S),re.search(pattern,after,re.S)
  assert (aa.group()if aa else None)==(bb.group()if bb else None),f+' '+label+' changed'
 assert re.findall(r'<script data-staging-indexing>.*?</script>',before,re.S)==re.findall(r'<script data-staging-indexing>.*?</script>',after,re.S),f+' browser staging-noindex changed'
 if route!=review and route not in selected:
  assert cache_normalized(before)==cache_normalized(after),f+' unrelated page/fabric/gallery/detail markup changed'
 if route in unrelated:
  for tag in ['form','input','select','textarea']:
   assert a.attrs(tag)==b.attrs(tag),f+' unrelated '+tag+' field changed'
 if route==review:
  assert 'content="noindex, follow"' in after,f+' review indexing changed'
if not args.capture_baseline:
 for f in ['sitemap.xml','robots.txt','_headers','_data/collection-designs.json','_data/collection-id-registry.json','_data/suit-reference-categories.json','_data/request-reference-allowlist.json','_data/suit-package-prices.json','_data/tuxedo-package-prices.json','_data/customer-faqs.json','_data/fabric-reference-catalogue.json','_templates/customer-interactions.js','_templates/whatsapp-consent.js','functions/api/selected-design-request.js','index.html']:
  assert (ROOT/f).read_bytes()==subprocess.check_output(['git','show',BASE+':'+f],cwd=ROOT),f+' protected scope changed'
 # The owner explicitly reserved the fabric page for separate review.
 before=old('_templates/design-selections.js');after=(ROOT/'_templates/design-selections.js').read_text()
 start="const fabricForm=document.getElementById('fabricChoiceForm');"
 end="for(const a of document.querySelectorAll('[data-edit-designs]'))"
 assert before.split(start,1)[1].split(end,1)[0]==after.split(start,1)[1].split(end,1)[0],'Existing per-design fabric-choice/browse/continue implementation changed'
 approved_ids={x['id']for x in load()[0]}
 for d in json.loads((ROOT/'_data/collection-designs.json').read_text())['designs']:
  if d['id'] not in approved_ids:continue
  for image in d['images']:
   f=image['originalPath'];assert (ROOT/f).read_bytes()==subprocess.check_output(['git','show',BASE+':'+f],cwd=ROOT),f+' approved photo changed'
 handler=(ROOT/'functions/_lib/selected-design-handler.js').read_text()
 assert "https://api.web3forms.com/submit" in handler,'Existing provider endpoint changed'
Path(args.report).parent.mkdir(parents=True,exist_ok=True);Path(args.report).write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(('CAPTURED'if args.capture_baseline else'PASS')+f' {len(routes)} pages SEO/header/footer/OFFER; unrelated forms, fabric implementation, approved photos/data/prices/policies/noindex/provider preserved')
