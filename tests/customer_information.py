#!/usr/bin/env python3
"""Regression for the confirmed customer facts, policy drafts and publication boundaries."""
from pathlib import Path
from html.parser import HTMLParser
import sys,re,json,subprocess,hashlib
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from preservation_helpers import without_shared_shell
from build_customer_information import outputs,plain
from customer_information import information,expand
from build_public_routes import public_routes
info=information();assert info['advancePercent']==70
assert [(x['garment'],x['priceRwf']) for x in info['cotton']]==[('Men two-piece',200000),('Men three-piece',250000),('Women two-piece',150000),('Women three-piece',200000)]
from faq_help import catalogue, routes as faq_routes, route as faq_route
for path,output in outputs().items():
 assert path.read_text()==output,path.name
 if path.suffix=='.html':
  assert output.count('<header ')==1
  assert "fetch('header.html')" not in output and "file: 'header.html'" not in output
hub_schema=json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>',(ROOT/'faq.html').read_text(),re.S)[1])
assert hub_schema['@type']=='CollectionPage'
data,topics,questions,_=catalogue()
for topic in topics:
 html=(ROOT/faq_route(topic).strip('/')/'index.html').read_text()
 schema=json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>',html,re.S)[1])
 assert [(q['name'],q['acceptedAnswer']['text']) for q in schema['mainEntity']]==[(questions[id]['question'],plain(expand(questions[id]['answer']))) for id in topic['questions']]
# Inspect metadata/JSON-LD as well as visible HTML in affected public output.
paths=[ROOT/n for n in ['index.html','faq.html','terms-and-conditions.html','refund-policy.html','privacy-policy.html','measurement-submission.html','booking.html','booking-adjustment.html','booking-housecall.html','booking-workplace.html','why-choose.html']]+list((ROOT/'services').rglob('index.html'))
for p in paths:
 text=p.read_text()
 for stale in ['75%','72 hours','10% of','day 12','1 to 2 weeks','1 to 3 days','within 24 hours','at least 70%','5% off','10% off','ownership rights and deposits paid are forfeited','we do not offer cancellations, returns or refunds','250,000</td><td>350,000','complimentary garment cleaning and special gifts','approved for publication','not listed until their availability']:
  assert stale not in text,(p,stale)
 assert not re.search(r'\b(?:supplier costs|maker fees|owner pay|profit margin)\b',text,re.I)
for file in ['booking.html','booking-housecall.html','booking-workplace.html','booking-adjustment.html','measurement-submission.html']:
 text=(ROOT/file).read_text();old=subprocess.check_output(['git','show','ac639f1:'+file],cwd=ROOT,text=True)
 assert 'action="https://api.web3forms.com/submit"' in text
 # No fields, endpoints or access-key/integration values are changed.
 attrs=lambda s: re.findall(r'<(?:input|select|textarea)\b[^>]*\bname="([^"]+)"',s)
 assert attrs(text)==attrs(old)
 assert re.search(r'<p class="form-note">[^<]*Web3Forms.*?<a href="/privacy-policy/">',text)
 assert 'not a confirmed appointment or accepted production order' in text
source=(ROOT/'_templates/homepage-sections.html').read_text();hero=source.split('</section>',1)[0]
assert 'data-hero-step' in hero and 'data-hero-select' not in hero
assert 'Pause slideshow' not in hero and '>01<' not in hero and '>02<' not in hero
assert 'id="programs"' in source and source.count('class="program-status">Coming Soon')==1
assert 'const interval=10000' in (ROOT/'_templates/hero-slideshow.js').read_text()
assert len(list((ROOT/'collections/designs').glob('*/index.html')))==111
# This phase must not rewrite the approved gallery, projects, original assets or submissions.
ref='ac639f145fc976ecefe02e2b8ff5b82f1aae184b'
files=subprocess.check_output(['git','ls-tree','-r','--name-only',ref],cwd=ROOT,text=True).splitlines()
protected=['assets/forms.js','assets/collections-v3.js','assets/collection-design.js','_data/collection-designs.json','_data/collection-id-registry.json','_data/customer-projects.json','_templates/collections.css']
for file in files:
 if file in protected or file.startswith('collections/') or file.startswith('our-work/') or re.search(r'\.(?:jpe?g|png|webp|avif|svg|mp4)$',file,re.I):
  current=(ROOT/file).read_bytes();previous=subprocess.check_output(['git','show',ref+':'+file],cwd=ROOT)
  if file.endswith('.html') and file.startswith(('collections/','our-work/')):
   assert without_shared_shell(current.decode())==without_shared_shell(previous.decode()),file
  else:assert current==previous,file
assert len(public_routes())==146+len(faq_routes())
print('PASS: policy/FAQ output and schema parity, Cotton prices/payment phases, stale-claim boundaries, Coming Soon previews and protected forms/gallery/projects/media.')
