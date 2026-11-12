"""R43 scoped selection UI: preserve SEO, approved data and unrelated page markup."""
from pathlib import Path
from html.parser import HTMLParser
import sys,subprocess,re,json
R=Path(__file__).resolve().parents[1];BASE='4c9dd3cd1fa5c8411fe3b98b16b77b9c6c28273d';sys.path.insert(0,str(R/'scripts'))
from build_collections import load,design_route
from suit_references import categories
def schema_preserved(before,after):
 old=[n for s in before for n in s.get('@graph',[s])];new=[n for s in after for n in s.get('@graph',[s])]
 assert all(n in new for n in old) and all(n in old or n.get('@type')=='BreadcrumbList'for n in new),'existing schema changed or unapproved addition'
class SEO(HTMLParser):
 def __init__(self,s):super().__init__(convert_charrefs=True);self.tags=[];self.schemas=[];self.kind=None;self.buf='';self.text=[];self.feed(s)
 def handle_starttag(self,t,a):
  a=dict(a)
  if t in ['meta'] or t=='link' and a.get('rel')=='canonical':self.tags.append((t,a))
  if t in ['title','h1'] or t=='script' and a.get('type')=='application/ld+json':self.kind=t;self.buf=''
 def handle_data(self,s):
  if self.kind:self.buf+=s
 def handle_endtag(self,t):
  if self.kind==t:
   if t=='script':self.schemas.append(json.loads(self.buf))
   else:self.text.append((t,self.buf))
   self.kind=None
routes=['/services/custom-tailoring/','/mensuits/','/womensuits/',*[c['route'] for c in categories()],*[design_route(d) for d in load()[0]],'/services/custom-tailoring/selected-designs/','/services/custom-tailoring/fabric/','/request/']
for route in routes:
 f=route.strip('/')+'/index.html';old=subprocess.check_output(['git','show',BASE+':'+f],cwd=R,text=True);new=(R/f).read_text();a,b=SEO(old),SEO(new)
 assert a.tags==b.tags,f+' metadata/canonicals changed'
 if route.startswith('/collections/designs/'):schema_preserved(a.schemas,b.schemas)
 else:assert a.schemas==b.schemas,f+' schema changed'
 assert [x for x in a.text if x[0]=='title']==[x for x in b.text if x[0]=='title'],f+' title'
 if route.startswith('/collections/designs/'):
  # R44 permits only the recommendation/breadcrumb/style changes audited in the dedicated test.
  assert re.search(r'<article class="design-layout">.*?</article>',old,re.S)[0]==re.search(r'<article class="design-layout">.*?</article>',new,re.S)[0],f+' primary photo/copy/selection journey changed'
 elif route!='/services/custom-tailoring/selected-designs/':
  normalized=lambda text:re.sub(r'((?:src|href)="/assets/[^"?]+\.(?:js|css))\?v=[^"]+',r'\1',text)
  assert normalized(new)==normalized(old),f+' unrelated static page changed'
 else:
  assert ('h1','Your Selected Designs') in b.text and 'content="noindex, follow"' in new
  assert 'Send Selected Designs to Mr Sewing on WhatsApp' in new and 'Continue on Website' in new
# R45 selected-only shared JS/intake changes are audited in selected_suit_preservation.py and selected-suit-refinement tests.
for f in ['sitemap.xml','robots.txt','_headers','_data/collection-designs.json','_data/collection-id-registry.json','_data/suit-reference-categories.json','_data/request-reference-allowlist.json','_data/customer-faqs.json','_data/suit-package-prices.json','_data/tuxedo-package-prices.json','_data/fabric-reference-catalogue.json','_templates/customer-interactions.js','index.html']:
 assert (R/f).read_bytes()==subprocess.check_output(['git','show',BASE+':'+f],cwd=R),f+' preserved scope'
print('PASS43canonicalpages metadata/schema/canonicals preserved;reviewH1onlyexplicitchange;allotherstaticmarkup preservedapartfromsharedassetcacheversions;R44 detailrec/breadcrumb scope audited separately;catalogue/SEO/noindex/prices/forms/WhatsAppTerms/provider unchanged')
