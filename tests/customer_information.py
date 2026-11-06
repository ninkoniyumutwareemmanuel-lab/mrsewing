#!/usr/bin/env python3
"""Regression for the confirmed customer facts, policy drafts and publication boundaries."""
from pathlib import Path
from html.parser import HTMLParser
import sys,re,json,subprocess,hashlib
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from build_customer_information import outputs,plain
from customer_information import information,expand
from build_public_routes import public_routes
info=information();assert info['advancePercent']==70
assert info['cotton']==[] and info['priceScheduleStatus'].startswith('UNVERIFIED')
from faq_help import catalogue, routes as faq_routes
for path,output in outputs().items():
 assert path.read_text()==output,path.name
 if path.suffix=='.html':
  assert output.count('<header ')==1
  assert "fetch('header.html')" not in output and "file: 'header.html'" not in output
hub_schema=json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>',(ROOT/'faq.html').read_text(),re.S)[1])
assert hub_schema['@type']=='CollectionPage'
data,topics,questions,_=catalogue()
for topic in topics:
 html=(ROOT/'faq'/topic['slug']/'index.html').read_text()
 schema=json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>',html,re.S)[1])
 assert [(q['name'],q['acceptedAnswer']['text']) for q in schema['mainEntity']]==[(questions[id]['question'],plain(expand(questions[id]['answer']))) for id in topic['questions']]
# Inspect metadata/JSON-LD as well as visible HTML in affected public output.
paths=[ROOT/n for n in ['index.html','faq.html','terms-and-conditions.html','refund-policy.html','privacy-policy.html','measurement-submission.html','booking.html','booking-adjustment.html','booking-housecall.html','booking-workplace.html','why-choose.html']]+list((ROOT/'services').rglob('index.html'))
for p in paths:
 text=p.read_text()
 for stale in ['75%','10% of','day 12','1 to 2 weeks','1 to 3 days','within 24 hours','at least 70%','5% off','10% off','ownership rights and deposits paid are forfeited','we do not offer cancellations, returns or refunds','250,000</td><td>350,000','complimentary garment cleaning and special gifts','approved for publication','not listed until their availability']:
  assert stale not in text,(p,stale)
 assert not re.search(r'\b(?:supplier costs|maker fees|owner pay|profit margin)\b',text,re.I)
for file in ['booking.html','booking-housecall.html','booking-workplace.html','booking-adjustment.html','measurement-submission.html']:
 text=(ROOT/file).read_text();old=subprocess.check_output(['git','show','ac639f1:'+file],cwd=ROOT,text=True)
 assert 'action="https://api.web3forms.com/submit"' in text
 # No fields, endpoints or access-key/integration values are changed.
 attrs=lambda s: re.findall(r'<(?:input|select|textarea)\b[^>]*\bname="([^"]+)"',s)
 if file=='booking.html':
  assert 'data-kind="consultation"' in text and 'Preferred Consultation Date' in text and 'Preferred Consultation Time' in text and text.count('<option value=')>=5
  continue
 assert attrs(text)==attrs(old)
 assert re.search(r'<p class="form-note">[^<]*Web3Forms.*?<a href="/privacy-policy/">',text)
 assert 'not a confirmed appointment or accepted production order' in text
source=(ROOT/'_templates/homepage-sections.html').read_text();hero=source.split('</section>',1)[0]
assert 'hero-lcp' in hero and 'hero-highlights' in hero and 'data-hero-step' not in hero
assert 'fetchpriority="high"' in hero and 'hero-image-note' not in hero
assert 'Pause slideshow' not in hero and '>01<' not in hero and '>02<' not in hero
assert 'id="programs"' in source and source.count('class="program-status">Coming Soon')==1
assert 'const interval=10000' in (ROOT/'_templates/hero-slideshow.js').read_text()
assert len(list((ROOT/'collections/designs').glob('*/index.html')))==119
# This phase must not rewrite the approved gallery, projects, original assets or submissions.
ref='ac639f145fc976ecefe02e2b8ff5b82f1aae184b'
files=subprocess.check_output(['git','ls-tree','-r','--name-only',ref],cwd=ROOT,text=True).splitlines()
protected=['assets/forms.js','_data/collection-designs.json','_data/collection-id-registry.json','_data/customer-projects.json','_templates/collections.css']
for file in files:
 if file in protected or re.search(r'\.(?:jpe?g|png|webp|avif|svg|mp4)$',file,re.I):
  if file in ['_data/collection-designs.json','_data/collection-id-registry.json']:
   from preservation_contract import append_only
   append_only(subprocess.check_output(['git','show',ref+':'+file],cwd=ROOT),(ROOT/file).read_bytes(),file);continue
  assert hashlib.sha256((ROOT/file).read_bytes()).digest()==hashlib.sha256(subprocess.check_output(['git','show',ref+':'+file],cwd=ROOT)).digest(),file
assert len(public_routes())==17+len(__import__('shop_catalog').load())+len(__import__('shop_catalog').categories())+len(__import__('project_catalog').projects())  # R13 adds programme pages and Shop
assert '60%' in (ROOT/'customer-information/index.html').read_text()
assert '72 hours' in (ROOT/'refund-policy.html').read_text()
assert '<table' not in (ROOT/'terms-and-conditions.html').read_text()
print('PASS: policy/FAQ output and schema parity, quote-only unverified prices and supported payment phases, stale-claim boundaries, Coming Soon previews and protected forms/gallery/projects/media.')

# R1 explicitly authorises gender isolation in the gallery runtime.
assert "payload.defaultGender==='all'" in (ROOT/'assets/collections-v3.js').read_text()
