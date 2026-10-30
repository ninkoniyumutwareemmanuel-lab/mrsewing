#!/usr/bin/env python3
"""FAQ publication/parity, scope preservation and restored-preview boundaries."""
import json,re,sys,subprocess,hashlib
from pathlib import Path
from html import escape
from html.parser import HTMLParser
import xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from faq_help import catalogue,outputs,search_data,routes,plain
from customer_information import expand
from build_homepage import Section,render
from build_public_routes import public_routes
baseline='40c18afc0e4094fd9e1616ad6fe48db1fd4df757'
def old(file,raw=False):
 b=subprocess.check_output(['git','show',baseline+':'+file],cwd=ROOT);return b if raw else b.decode()
data,topics,questions,owners=catalogue();assert len(topics)==14
entries=search_data()['entries'];assert len(entries)==len(owners) and len({e['url'] for e in entries})==len(entries)
assert {t['destination'] for t in topics if t['destination'].startswith('/services/')}=={s['route'] for s in json.loads((ROOT/'_data/journey-services.json').read_text())}
for path,output in outputs().items():assert path.read_text()==output,path
for t in topics:
 path='/faq/'+t['slug']+'/';html=(ROOT/path.strip('/')/'index.html').read_text();schema=json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>',html,re.S)[1])
 assert schema['@type']=='FAQPage' and schema['url']=='https://mrsewingfashion.com'+path
 assert len(schema['mainEntity'])==len(t['questions'])==html.count('class="faq-question"')
 for id,item in zip(t['questions'],schema['mainEntity']):
  q=questions[id];assert item['name']==q['question'] and item['acceptedAnswer']['text']==plain(expand(q['answer']))
  assert 'id="'+id+'"' in html and expand(q['answer']) in html
 assert 'All FAQ topics' in html and t['destination'] in html
 for stale in ['35%','75%','72 hours','day 12','at least 70%','1 to 2 weeks','1 to 3 days','5% off','10% off','special gifts','supplier costs','maker fees','loyalty program','referral program','free photoshoot']:
  assert stale not in html,(t['slug'],stale)
hub=(ROOT/'faq.html').read_text();assert 'class="faq-question"' not in hub and '"@type": "FAQPage"' not in hub
assert hub.count('class="faq-card"')==len(topics)
assert json.loads((ROOT/'_data/page-seo.json').read_text())['faq.html']==json.loads(old('_data/page-seo.json'))['faq.html']
class Metadata(HTMLParser):
 def __init__(self,text):super().__init__();self.meta={};self.feed(text)
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag=='meta' and ('name' in a or 'property' in a):self.meta[a.get('name',a.get('property'))]=a.get('content')
before_meta=Metadata(old('faq.html')).meta;after_meta=Metadata(hub).meta
for key,value in before_meta.items():assert after_meta.get(key)==value,(key,value,after_meta.get(key))

# Preserve all unrelated site assets/configuration and the existing policy wording/output.
protected=['_data/customer-information.json','_data/policy-pages.json','_data/business.json','_data/contact-v2.json','_data/page-seo.json','assets/homepage.js','_templates/hero-slideshow.js','_templates/homepage-motion.css','_headers','_redirects','robots.txt','header.html','footer.html']
files=subprocess.check_output(['git','ls-tree','-r','--name-only',baseline],cwd=ROOT,text=True).splitlines()
for f in files:
 if f in protected or f.startswith(('_templates/shared/','collections/','our-work/')) or re.search(r'\.(?:jpe?g|png|avif|webp|svg|mp4)$',f,re.I) or any(f.startswith(x) for x in ['terms-and-conditions','refund-policy','privacy-policy']) or f in ['_templates/terms-and-conditions.html','_templates/refund-policy.html','_templates/privacy-policy.html']:
  assert hashlib.sha256((ROOT/f).read_bytes()).digest()==hashlib.sha256(old(f,True)).digest(),f
# Homepage outside the restored block must be literally unchanged.
new=(ROOT/'index.html').read_text();parser=Section(new,'div',('id','programs-section'));parser.feed(new);assert parser.markup
assert new.replace('    '+parser.markup+'\n','',1)==old('index.html')
p=Section(new,'div',('id','programs'));p.feed(new);block=p.markup
assert block.count('Coming Soon')==3 and not re.search(r'<(?:a|button|input|form)\b',block)
assert all(name in block for name in ['Loyalty Program','Referral Program','Complimentary Photoshoot'])
assert not re.search(r'%|\bRWF\b|\b(?:discount|commission|gift|cleaning|enrol|redeem|guaranteed)\b',block,re.I)
assert new.index('id="services-section"')<new.index('id="programs-section"')<new.index('id="final-section"')
ns={'s':'http://www.sitemaps.org/schemas/sitemap/0.9'}
oldurls={e.text for e in ET.fromstring(old('sitemap.xml')).findall('s:url/s:loc',ns)};newurls={e.text for e in ET.parse(ROOT/'sitemap.xml').findall('s:url/s:loc',ns)}
assert newurls==oldurls|{'https://mrsewingfashion.com'+r for r in routes()}
assert len(public_routes())==len(oldurls)+len(topics)
print(f'PASS: {len(topics)} topics/{len(owners)} unique published answers, source/schema/search parity, exact homepage/policy/hero/shared/asset/config preservation, safe Coming Soon previews and FAQ-only sitemap additions.')
