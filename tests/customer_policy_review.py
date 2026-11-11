"""Approved owner facts and clean, source-linked FAQ/policy draft; no real submission."""
from pathlib import Path
from urllib.parse import urlsplit,unquote
from decimal import Decimal
import json,sys,re
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'scripts'))
from customer_policies import facts
from faq_help import catalogue,search_data
f=facts();assert f['charges']['expressPercent']+f['charges']['afterHoursPercent']==f['charges']['combinedPercent']==60
base=Decimal('100000');assert base*(1+Decimal(f['charges']['combinedPercent'])/100)==160000
assert base*(1+Decimal(f['charges']['expressPercent'])/100)==135000
assert base*(1+Decimal(f['charges']['afterHoursPercent'])/100)==125000
assert f['payments']['domesticCustomAdvancePercent']+f['payments']['domesticCustomBalancePercent']==100
assert f['payments']['internationalCustomAdvancePercent']==100 and f['payments']['standaloneAdvancePercent'] is None
assert f['mobile']=={'confirmedOrderMeasurementVisitRwf':10000,'consultationAndFittingRwf':25000,'independentAssistanceRwf':50000,'maximumPeople':5,'maximumHours':3}
assert f['transport']['eligibleKigaliRoundTripRwf']==10000 and f['transport']['combinedOrderChargedOnce']
for id,phrase in [('custom-tailoring','1–3 weeks'),('alterations','12–15 working hours'),('garment-care','approximately 3 days')]:
 s=(R/'services'/id/'index.html').read_text();assert phrase.lower() in s.lower();assert '35%' in s and '60%' in s
terms=(R/'terms-and-conditions/index.html').read_text();assert all(x in terms for x in ['1–3 weeks','2–3 days','12–15 working hours','2–12 working hours','25,000 RWF','50,000 RWF','10,000 RWF','100%'])
for id,phrase in [('mobile-fitting','five people'),('vip','family')]:assert phrase in (R/'services'/id/'index.html').read_text()
pricepage=(R/'services/custom-tailoring/index.html').read_text()
for price in json.loads((R/'_data/suit-package-prices.json').read_text())['prices'].values():
 if price.get('publicationApproved'):
  assert format(price['twoPieceRwf'],',')+' RWF' in pricepage and format(price['threePieceRwf'],',')+' RWF' in pricepage
for price in json.loads((R/'_data/tuxedo-package-prices.json').read_text())['tiers']:
 assert format(price['twoPieceRwf'],',')+' RWF' in pricepage and format(price['threePieceRwf'],',')+' RWF' in pricepage
assert '30 minutes' in (R/'privacy-policy/index.html').read_text()
assert 'MrFaqActions.make' not in (R/'assets/faq-help.js').read_text();assert 'Copy Answer' not in (R/'assets/faq-help.js').read_text()
search=search_data();assert len(search['entries'])>=140
for e in search['entries']:
 u=urlsplit(e['source']);assert u.scheme=='https' and u.netloc=='mrsewingfashion.com'
 p=R/'index.html' if u.path=='/' else R/u.path.strip('/')/'index.html';assert p.is_file(),e
 if u.fragment:assert 'id="'+unquote(u.fragment)+'"' in p.read_text(),e
assert {'Terms & Conditions','Refund & Cancellation Policy','Privacy Policy','Online Shop'}.issubset({e['topic'] for e in search['entries']})
assert not json.loads((R/'_data/customer-request-backend.json').read_text())['enabled']
print('PASS approved times/35+25additive/70+30/100international/3mobilefees/roundtrip/sharedserviceTerms/validatedsource-linkedsearchrows/privacydrafttruth/private-disabled')
