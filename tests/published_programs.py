#!/usr/bin/env python3
"""31 October program publication and homepage approval: facts, math and boundaries."""
from pathlib import Path
import json,re,subprocess,sys
from urllib.parse import urlparse,parse_qs
from html import unescape
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from customer_information import information,expand
from faq_help import catalogue,route,search_data
from build_homepage import Section
from build_public_routes import public_routes
BASE='1113e0a1e237ee3072c0eecd594d6cd3a1e06f73'
def old(p):return subprocess.check_output(['git','show',BASE+':'+p],cwd=ROOT,text=True)
d=information();assert (d['loyaltyDiscountPercent'],d['referralDiscountPercent'],d['referralCommissionRwf'])==(3,2,6000)
assert d['giftSchedule']==[
 {'collection':'Cotton / Polyester','men':'No included gift','women':'No included gift'},
 {'collection':'Wool / Star','men':'One necktie OR bow tie','women':'One inner top worn under the suit jacket'},
 {'collection':'Super / Americano','men':'One shirt AND necktie','women':'One inner top worn under the suit jacket'}]
for row in d['collections']:
 for price in row['pricesRwf']:
  for discount in [2,3]:
   total=price-price*discount//100+price*35//100+price*50//100+20000
   assert total==price*(185-discount)//100+20000
assert 200000-6000+70000+100000+20000==384000
for phrase in ['original standard suit price','two discounts do not combine','not discounted']:assert phrase in d['discountRules']
for phrase in ['third separate qualifying purchase','one purchase','suits only']:assert phrase in d['loyaltySummary']
for phrase in ['second separate qualifying suit purchase','one gift package','do not repeat']:assert phrase in d['giftTerms'].lower()
for phrase in ['three shared standard cleaning occasions in total','two follow-up','initial handover','same counter']:assert phrase in d['cleaningBenefit'].lower()
for phrase in ['only the jacket','only the trousers','only the covered accompanying shirt','one whole occasion','do not keep separate credits']:assert phrase in d['cleaningCounter']
for phrase in ['never purchased','before the advance payment','existing-customer','standalone','alterations','garment care']:assert phrase in d['referralBuyer']
for phrase in ['6,000 RWF per qualifying suit','12,000','one unique code','own purchase']:assert phrase in d['referralCommission']
for phrase in ['full customer payment','completed garment handover','Cancelled or refunded']:assert phrase in d['referralEligibility']
for phrase in ['14-day payment window','Unfinished orders carry forward','within 14 days','another sale is not required']:assert phrase in d['referralWindows']
_,topics,questions,owners=catalogue();assert len(topics)==16 and len(owners)==101 and len(search_data()['entries'])==101
for topic in [t for t in topics if t.get('externalPage')]:
 path=route(topic);html=(ROOT/path.strip('/')/'index.html').read_text();schema=json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>',html,re.S)[1])
 assert schema['@type']=='FAQPage' and schema['url']=='https://mrsewingfashion.com'+path
 assert len(schema['mainEntity'])==len(topic['questions'])
 assert '<meta name="robots" content="index, follow">' in html and 'data-staging-indexing' in html
 assert not re.search(r'<(?:form|input|select)\b',html)
 assert path in public_routes() and 'https://mrsewingfashion.com'+path in (ROOT/'sitemap.xml').read_text()
 for ident in topic['questions']:assert expand(questions[ident]['answer']) in html and 'id="'+ident+'"' in html
assert len(public_routes())==162
home=(ROOT/'index.html').read_text();source=(ROOT/'_templates/homepage-sections.html').read_text()
assert 'Custom suits for men and women, alterations and garment care in Kigali.' in home
assert 'Perfect Fit' not in source
cta=re.search(r'<a[^>]*href="([^"]+)"[^>]*>Ask for a quotation on WhatsApp',source)[1]
u=urlparse(unescape(cta));assert u.scheme=='https' and u.netloc=='wa.me' and u.path=='/250787411501'
assert parse_qs(u.query)['text']==['Hello Mr Sewing, I would like a quotation. May I share my requirements?']
for text in ['written quotation','70% advance','remaining balance before final cleaning','MIC Building, Downtown','Consultations by appointment','Norvège, KN 441 St']:assert text in home
section=lambda text,id_:Section(text,'section',('id',id_))
a=section(source,'photoshoot-preview');a.feed(source);b=section(old('_templates/homepage-sections.html'),'photoshoot-preview');b.feed(old('_templates/homepage-sections.html'));assert a.markup==b.markup
# Preserve the images, headlines and controls; only the approved hero description/CTA changes.
hero=lambda s:s.split('</section>',1)[0]
for pattern in [r'<img\b[^>]*>',r'<h1\b.*?</h1>',r'<div class="hero-controls".*?</div>']:
 assert re.findall(pattern,hero(source),re.S)==re.findall(pattern,hero(old('_templates/homepage-sections.html')),re.S)
for p in ['booking.html','booking/index.html','_data/business.json','_data/contact-v2.json','_data/page-seo.json','_data/collection-designs.json','_data/customer-projects.json','assets/forms.js','assets/homepage.js','_templates/hero-slideshow.js','_templates/shared/header.html','_templates/shared/footer.html','_templates/shared/site.css','_headers','_redirects','robots.txt']:
 assert (ROOT/p).read_text()==old(p),p
assert (ROOT/'_templates/homepage-motion.css').read_text().startswith(old('_templates/homepage-motion.css'))
policies=json.loads((ROOT/'_data/policy-pages.json').read_text());before=json.loads(old('_data/policy-pages.json'))
for p in ['refund-policy','privacy-policy']:assert policies[p]==before[p]
for ident in ['design','responsibilities','returns','photos','delivery']:
 find=lambda obj:next(s for s in obj['terms-and-conditions']['sections'] if s['id']==ident)
 assert find(policies)==find(before),ident
for p in ['shop/index.html','shop/collections/index.html','shop/ordering/index.html']:assert (ROOT/p).read_text()==old(p),p
assert 'Coming Soon' in d['paymentComingSoon']
assert not re.search(r'fetch|localStorage|sessionStorage', (ROOT/'assets/customer-programs.js').read_text())
for name in ['_data/customer-information.json','_data/customer-faqs.json','_data/policy-pages.json']:
 assert not re.search(r'owner pay|supplier costs|maker fees|profit margin|sales targets|internal budgets',(ROOT/name).read_text(),re.I)
print('PASS: approved program/gift/shared-counter rules, original-price discount arithmetic, 101 answer/schema/search parity, homepage CTA, two added sitemap routes, exact booking/Shop/media/Maps preservation and no enrollment/payout automation.')
