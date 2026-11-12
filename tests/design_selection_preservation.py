"""R43 scoped selection UI: preserve SEO, approved data and unrelated page markup."""
from pathlib import Path
from html.parser import HTMLParser
import sys,subprocess,re,json
R=Path(__file__).resolve().parents[1];BASE='4c9dd3cd1fa5c8411fe3b98b16b77b9c6c28273d';sys.path.insert(0,str(R/'scripts'))
from build_collections import load,design_route
from suit_references import categories
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
 assert a.tags==b.tags and a.schemas==b.schemas,f+' SEO changed'
 assert [x for x in a.text if x[0]=='title']==[x for x in b.text if x[0]=='title'],f+' title'
 if route!='/services/custom-tailoring/selected-designs/':
  normalized=new.replace('design-selections.js?v=staging-r43','design-selections.js?v=staging-r33').replace('design-selections.css?v=staging-r43','design-selections.css')
  assert normalized==old,f+' unrelated static page changed'
 else:
  assert ('h1','Your Selected Designs') in b.text and 'content="noindex, follow"' in new
  assert 'Share Selected Designs' in new and 'Continue on Website' in new
for f in ['sitemap.xml','robots.txt','_headers','_data/collection-designs.json','_data/collection-id-registry.json','_data/suit-reference-categories.json','_data/request-reference-allowlist.json','_data/customer-faqs.json','_data/suit-package-prices.json','_data/tuxedo-package-prices.json','_data/fabric-reference-catalogue.json','_templates/customer-interactions.js','_templates/customer-site.js','functions/_lib/selected-design-handler.js','index.html']:
 assert (R/f).read_bytes()==subprocess.check_output(['git','show',BASE+':'+f],cwd=R),f+' preserved scope'
print('PASS43canonicalpages metadata/schema/canonicals preserved;reviewH1onlyexplicitchange;allotherstaticmarkup preservedapartfromsharedassetcacheversions;catalogue/SEO/noindex/prices/forms/WhatsAppTerms/provider unchanged')
