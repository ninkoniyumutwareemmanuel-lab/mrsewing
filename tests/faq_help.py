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
entries=search_data()['entries'];assert len(entries)>len(owners) and set(owners).issubset({e['id'] for e in entries}) and len({e['url'] for e in entries})==len(entries)
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
 for stale in ['75%','day 12','at least 70%','1 to 2 weeks','1 to 3 days','5% off','10% off','special gifts','supplier costs','maker fees','loyalty program','referral program','free photoshoot']:
  assert stale not in html,(t['slug'],stale)
hub=(ROOT/'faq.html').read_text();assert 'class="faq-question"' not in hub and '"@type": "FAQPage"' not in hub
assert hub.count('class="faq-card"')==len(topics)
assert 'Cotton suit base prices' not in json.loads((ROOT/'_data/page-seo.json').read_text())['faq.html']['description']
class Metadata(HTMLParser):
 def __init__(self,text):super().__init__();self.meta={};self.feed(text)
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag=='meta' and ('name' in a or 'property' in a):self.meta[a.get('name',a.get('property'))]=a.get('content')
before_meta=Metadata(old('faq.html')).meta;after_meta=Metadata(hub).meta
for key,value in before_meta.items():
 if key in ['description','og:description','twitter:description']:assert after_meta.get(key)==json.loads((ROOT/'_data/page-seo.json').read_text())['faq.html']['description']
 else:assert after_meta.get(key)==value,(key,value,after_meta.get(key))

# Preserve all unrelated site assets/configuration and the existing policy wording/output.
protected=['_data/policy-pages.json','_data/business.json','_data/contact-v2.json','_templates/hero-slideshow.js','_templates/homepage-motion.css','_headers','_redirects','robots.txt','header.html','footer.html']
files=subprocess.check_output(['git','ls-tree','-r','--name-only',baseline],cwd=ROOT,text=True).splitlines()
for f in files:
 if f in protected or re.search(r'\.(?:jpe?g|png|avif|webp|svg|mp4)$',f,re.I) or f in ['_templates/terms-and-conditions.html','_templates/refund-policy.html','_templates/privacy-policy.html']:
  assert hashlib.sha256((ROOT/f).read_bytes()).digest()==hashlib.sha256(old(f,True)).digest(),f
# Phase 1 may rebuild the homepage and its metadata; all other page SEO stays frozen.
current_seo=json.loads((ROOT/'_data/page-seo.json').read_text());previous_seo=json.loads(old('_data/page-seo.json'))

for key in ['index.html','mensuits.html','womensuits.html','about.html','faq.html']:
 current_seo.pop(key);previous_seo.pop(key)
assert current_seo==previous_seo
# Keep the restored previews and their publication gates through homepage redesigns.
new=(ROOT/'index.html').read_text();parser=Section(new,'div',('id','programs-section'));parser.feed(new);assert parser.markup
from site_seo import finalize
assert new==finalize(render(),ROOT/'index.html')
from shared_components import menu_script
from build_homepage import HOMEPAGE_VISUAL_REVIEW
expected_js=menu_script()+(ROOT/'_templates/homepage-preview.js').read_text() if HOMEPAGE_VISUAL_REVIEW else menu_script()+(ROOT/'_templates/homepage-corrective.js').read_text()+(ROOT/'_templates/order-carousel.js').read_text()+(ROOT/'_templates/homepage-galleries.js').read_text()
assert (ROOT/'assets/homepage.js').read_text()==expected_js
p=Section(new,'div',('id','programs'));p.feed(new);block=p.markup
block=re.sub(r'<a href="/(?:loyalty|referral)-program/">([^<]+)</a>',r'\1',block)  # R13 only authorises these two programme links
assert block.count('Coming Soon')==1 and not re.search(r'<(?:a|button|input|form)\b',block)
assert all(name in block for name in ['Loyalty Program','Referral Program','Complimentary Photoshoot'])
assert not re.search(r'%|\bRWF\b|\b(?:discount|commission|gift|cleaning|enrol|redeem|guaranteed)\b',block,re.I)
assert new.index('id="services-section"')<new.index('id="programs-section"')<new.index('id="final-section"')
# Section J: retain every approved program word and keep both final sections adjacent.
reference=subprocess.check_output(['git','show','ba27bab0425a9df1948fe8f45dd3b941cb322f4c:index.html'],cwd=ROOT,text=True)
original=Section(reference,'div',('id','programs'));original.feed(reference)
expected=original.markup.replace('<p class="home-eyebrow">Looking ahead</p>','<p class="home-eyebrow">Customer programme</p>',2).replace('<span class="program-status">Coming Soon</span>','',2).replace('We’re developing a loyalty program for Mr Sewing customers. Details and conditions will be announced when it is ready.','Explore our Loyalty &amp; Referral Programme for Mr Sewing Fashion customers. Contact us for current programme information.').replace('We’re developing a referral program for people who introduce others to Mr Sewing. Details and conditions will be announced when it is ready.','Share Mr Sewing Fashion with others through our referral programme. Ask us about participation and current conditions.')
assert block==expected
assert re.search(r'</div>\s*<div id="final-section"',new[new.index('id="programs-section"'):])
final=Section(new,'section',('class','home-final home-section'));final.feed(new)
assert 'Let’s make it personal' in final.markup and 'Your Next Special<br>Outfit Starts Here.' in final.markup
for href in re.findall(r'href="([^"]+)"',reference[reference.index('id="final-section"'):reference.index('</main>')]):
 if href=='/contact/':
  assert 'href="/contact/"' in (ROOT/'_templates/homepage-header.html').read_text()
  continue
 if href.startswith('https://wa.me/'):
  assert 'href="/whatsapp/?text=' in final.markup;continue
 assert 'href="'+href+'"' in ((ROOT/'_templates/homepage-sections.html').read_text() if HOMEPAGE_VISUAL_REVIEW else final.markup),href

ns={'s':'http://www.sitemaps.org/schemas/sitemap/0.9'}
oldurls={e.text for e in ET.fromstring(old('sitemap.xml')).findall('s:url/s:loc',ns)};newurls={e.text for e in ET.parse(ROOT/'sitemap.xml').findall('s:url/s:loc',ns)}
assert newurls=={'https://mrsewingfashion.com'+r for r in public_routes()}
withdrawn=oldurls-newurls
assert all(u.removeprefix('https://mrsewingfashion.com') not in __import__('site_seo').INDEXABLE_ROUTES for u in withdrawn)  # Current approved public eligibility governs withdrawals
assert len(public_routes())==55  # Owner-approved R29 public browsing discovery; private/draft product details excluded
assert all('/faq/'+t['slug']+'/' not in public_routes() for t in topics)
print(f'PASS: {len(topics)} topics/{len(owners)} unique published answers, source/schema/search parity, generated homepage consistency and policy/hero/shared/asset/config preservation, safe Coming Soon previews and publication-aware canonical sitemap.')

assert all("Link to this answer" not in p.read_text() for p in (ROOT/"faq").glob("*/index.html"))
