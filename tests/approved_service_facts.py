#!/usr/bin/env python3
"""Verify the 30 October handoff and 31 October staging-only approval boundaries."""
from pathlib import Path
import sys,json,re,subprocess
from html.parser import HTMLParser
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from customer_information import information,expand
from faq_help import catalogue,search_data
D=information();BASE='ff43efe85a9ba098ef1d9231bf1639cba710ac6f'
def old(p):return subprocess.check_output(['git','show',BASE+':'+p],cwd=ROOT,text=True)
expected=[[200000,250000,150000,200000],[270000,320000,220000,270000],[400000,450000,350000,400000],[600000,650000,500000,550000]]
assert [r['pricesRwf'] for r in D['collections']]==expected
assert [r['startingPriceRwf'] for r in D['alterations']]==[25000,25000,35000,45000,35000]
for p in [150000,200000,600000]:assert p*135//100 in [202500,270000,810000]
for r in D['paidSuitCleaning']:assert r['expressPriceRwf']==r['standardPriceRwf']*135//100
assert 200000+200000*35//100+200000*50//100+20000==390000
assert 'once per order' in D['mobilePricing'] and 'agreed for that order' in D['mobilePricing']
assert 'unlimited' in D['mobilePricing'] and 'before payment' in D['mobileScope']
assert '7–10 working days' in D['timing'] and '3–4 working days' in D['timing']
assert '4–5 working days' in D['careTiming'] and 'two working days' in D['careExpress']
assert D['advancePercent']==70 and D['suitPayment']==json.loads(old('_data/customer-information.json'))['suitPayment']
assert D['standalonePayment']==json.loads(old('_data/customer-information.json'))['standalonePayment']
assert '30,000' in D['accessoryTerms'] and '45,000' in D['accessoryTerms'] and '20,000' in D['packagingTerms']
for method in ['bank transfer','MTN Mobile Money','Airtel Money','cash','cryptocurrency']:assert method in D['paymentMethods']
assert 'PayPal' in D['paymentComingSoon'] and 'Visa' in D['paymentComingSoon'] and 'Coming Soon' in D['paymentComingSoon']
class Form(HTMLParser):
 def __init__(self,text):super().__init__();self.fields=[];self.action=None;self.feed(text)
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag=='form':self.action=a.get('action')
  if tag in ['input','select','textarea']:self.fields.append((tag,sorted(attrs)))
for name in ['booking.html','booking-housecall.html','booking-workplace.html','booking-adjustment.html','measurement-submission.html']:
 current=(ROOT/name).read_text();before=old(name);a=Form(current);b=Form(before)
 assert a.fields==b.fields and a.action==b.action=='https://api.web3forms.com/submit',name
 assert 'privacy-policy' in current and 'terms-and-conditions' in current
 assert re.findall(r'<script(?:\s[^>]*)?>(.*?)</script>',current,re.S)==re.findall(r'<script(?:\s[^>]*)?>(.*?)</script>',before,re.S),name
 assert 'Prices, packages and payment stages' in current
booking=(ROOT/'booking.html').read_text();assert not re.search(r'<(?:header|footer)\b|id="site-header"',booking)
assert '← Back to website' in booking
# Unapproved legal sections are retained exactly except approved identity/service facts.
previous=json.loads(old('_data/policy-pages.json'));now=json.loads((ROOT/'_data/policy-pages.json').read_text())
for page in ['refund-policy','privacy-policy']:
 assert now[page]==json.loads(json.dumps(previous[page]).replace('Mr Sewing Fashion Designer','Mr Sewing'))
for ident in ['design','responsibilities','returns','photos','delivery']:
 find=lambda obj:next(s for s in obj['terms-and-conditions']['sections'] if s['id']==ident)
 assert find(now)==find(previous),ident
# Defined program publication is now approved; untested forms/automation remain absent.
for route in ['loyalty-program','referral-program']:
 text=(ROOT/route/'index.html').read_text()
 assert '<meta name="robots" content="index, follow">' in text
 assert not re.search(r'<form\b',text)
assert not json.loads((ROOT/'_data/garment-care.json').read_text())['businessConfirmation']
assert all(not s['published'] for s in json.loads((ROOT/'_data/garment-care.json').read_text())['services'])
# Preserve all working media, registry, site routing, Maps/business data and integrations.
for p in ['_data/business.json','_data/contact-v2.json','_data/page-seo.json','_data/collection-designs.json','_data/customer-projects.json','_data/collection-id-registry.json','_headers','_redirects','robots.txt','assets/forms.js','assets/homepage.js','_templates/hero-slideshow.js','_templates/shared/header.html','_templates/shared/footer.html']:
 assert (ROOT/p).read_text()==old(p),p
for name in ['_data/customer-information.json','_data/customer-faqs.json','_data/policy-pages.json','_data/care-information.json']:
 text=(ROOT/name).read_text()
 assert not re.search(r'supplier costs|maker fees|profit margin|owner pay|sales targets|financial.manager costs|internal budgets',text,re.I),name
 assert not re.search(r'Mr Sewing Fashion Designer|12–15|2–4 days|one maker day',text),name
_,topics,questions,owners=catalogue();assert len(topics)==16 and len(owners)==101
assert len(search_data()['entries'])==101
for route in ['services/custom-tailoring','services/express-tailoring','services/mobile-fitting','services/alterations','services/garment-care','services/garment-care/services','services/garment-care/planning','faq/prices-packages-payments']:
 text=(ROOT/route/'index.html').read_text();assert '{{' not in text
assert 'Paid suit cleaning — RWF' in (ROOT/'services/garment-care/index.html').read_text()
print('PASS: 16 suit prices, approved surcharge arithmetic, cleaning/alteration rates and timing, exact form integrations, booking layout, held legal rules and defined program publication, confidentiality, preserved SEO/media and 101 FAQ answers.')
