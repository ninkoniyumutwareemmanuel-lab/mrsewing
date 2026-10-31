#!/usr/bin/env python3
"""Preserve guide evidence, shared navigation boundaries and unfinished-page indexing gates."""
from pathlib import Path
from html import escape,unescape
from html.parser import HTMLParser
import sys,json,re,subprocess
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from build_measurements import outputs
from build_clean_urls import clean_document
from preparation_pages import routes
BASE='171ba92c9c872382010ceee9cb514473d7e69acf'
def old(path):return subprocess.check_output(['git','show',BASE+':'+path],cwd=ROOT,text=True)
class Metadata(HTMLParser):
 def __init__(self,text):super().__init__();self.items=[];self.feed(text)
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag=='meta' or tag=='link' and a.get('rel')=='canonical':self.items.append((tag,sorted(attrs)))
oldguide=old('measurements.html');guide=(ROOT/'measurements.html').read_text();data=json.loads((ROOT/'_data/measurements.json').read_text())
assert Metadata(guide).items==Metadata(oldguide).items
for path,content in outputs().items():assert path.read_text()==content,path
assert (ROOT/'measurements/index.html').read_text()==clean_document('measurements.html')
assert len(data['measurements'])==guide.count('class="measurement-card"')==12
for m in data['measurements']:
 assert m['image'].lstrip('/') in oldguide and m['description'] in unescape(oldguide)
 assert escape(m['description']) in guide and 'href="'+m['image']+'"' in guide
for q in data['questions']:
 assert q['question'] in unescape(oldguide) and q['answer'] in unescape(oldguide)
 assert escape(q['answer']) in guide
assert re.findall(r'<script type="application/ld\+json">(.*?)</script>',guide,re.S)==re.findall(r'<script type="application/ld\+json">(.*?)</script>',oldguide,re.S)
# Only the new guide link is added to each shared component. Keep map/business details exact.
addition='<li><a href="/measurements/">Measurements Guide</a></li>'
for name in ['header.html','footer.html']:
 source=(ROOT/'_templates/shared'/name).read_text()
 assert source.count(addition)==1
 assert source.replace(addition,'')==old('_templates/shared/'+name)
css=(ROOT/'_templates/shared/site.css').read_text();assert css.startswith(old('_templates/shared/site.css'))
for name in ['navigation.js','motion.js']:
 path=ROOT/'_templates/shared'/name
 if path.exists():assert path.read_text()==old('_templates/shared/'+name)
for route in [r for r in routes() if r.startswith('/shop/')]:
 html=(ROOT/route.strip('/')/'index.html').read_text()
 assert '<meta name="robots" content="noindex, follow">' in html,route
 assert 'https://mrsewingfashion.com'+route not in (ROOT/'sitemap.xml').read_text(),route
 assert html.count('<h1>')==1 and 'Coming Soon' in html
 assert not re.search(r'<(?:form|input|select|textarea)\b',html)
 assert not re.search(r'\b(?:RWF|discount|commission|enrol|redeem)\b',html,re.I)
 assert 'href="/measurements/"' in html
import xml.etree.ElementTree as ET
ns={'s':'http://www.sitemaps.org/schemas/sitemap/0.9'}
urls=lambda text:{e.text for e in ET.fromstring(text).findall('s:url/s:loc',ns)}
assert urls((ROOT/'sitemap.xml').read_text())==urls(old('sitemap.xml'))|{'https://mrsewingfashion.com/loyalty-program/','https://mrsewingfashion.com/referral-program/'}
for file in ['_headers','_redirects','robots.txt','_data/page-seo.json','assets/forms.js','assets/homepage.js','_templates/hero-slideshow.js']:
 assert (ROOT/file).read_text()==old(file),file
care=(ROOT/'services/garment-care/index.html').read_text()
for route in ['/services/garment-care/services/','/services/garment-care/planning/']:
 assert 'href="'+route+'"' in care
print('PASS: original 12 guide instructions/images, 4 answers, metadata/schema, shared guide-only links, two Shop drafts and two approved program routes, protected hero/forms and connected existing care pages.')
