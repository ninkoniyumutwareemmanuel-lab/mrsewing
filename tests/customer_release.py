#!/usr/bin/env python3
"""5 November owner release: scope, provenance gates, publication and homepage protection."""
from pathlib import Path
import json,hashlib,re,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from build_public_routes import public_routes
from build_collections import load
names=['Custom Tailoring & Suits','Clothing Alterations & Repairs','Garment Care & Cleaning','Mobile Tailoring, Styling & Event Assistance']
release=json.loads((ROOT/'_data/customer-release.json').read_text());assert [s['title'] for s in release['services']]==names
registry=json.loads((ROOT/'_data/journey-services.json').read_text());assert [s['title'] for s in registry if s['primary']]==names
assert '5 November 2026' in release['source']
for f,h in json.loads((ROOT/'docs/homepage-approved-baseline.json').read_text())['files'].items():assert hashlib.sha256((ROOT/f).read_bytes()).hexdigest()==h,f
facts=json.loads((ROOT/'_data/customer-information.json').read_text());assert not facts['cotton'];assert facts['priceScheduleStatus'].startswith('UNVERIFIED')
assert all(p['source'].startswith('S-OWNER-2026-11-05') for p in release['pages'].values())
for route in ['/customer-information/','/guides/fabrics/','/delivery-and-collection/','/benefits/','/customer-support/']:assert route in public_routes()
for route in ['/request/','/services/custom-tailoring/design-choice/','/services/custom-tailoring/standard-order/','/services/custom-tailoring/special-order/']:assert route not in public_routes()
for route in ['/suits/','/m-classicsuits/','/m-doublebreasted/','/w-classicsuits/']:assert route not in public_routes()
for text in ['35%','25%','60%','24 support working hours','22:00']:
 assert text in (ROOT/'customer-information/index.html').read_text(),text
assert '72 hours' in (ROOT/'refund-policy.html').read_text()
assert '6,000 RWF' in (ROOT/'benefits/index.html').read_text()
assert 'Privacy Policy — Staging Draft' in (ROOT/'privacy-policy.html').read_text()
assert len(load()[0])==7
for s in release['services']:
 html=(ROOT/s['route'].strip('/')/'index.html').read_text();assert 'Choose Standard Service' in html and 'Choose VIP Service' in html
 assert 'name="subscription"' not in html and 'checkout.stripe' not in html
for filename in ['CUSTOMER_FACING_SOURCE_REGISTER.md','POLICY_RECONCILIATION_REPORT.md','UNRESOLVED_DECISIONS.md']:
 assert not (ROOT/filename).exists(),'Internal review must remain outside deployment root'
print('PASS: four primary categories, owner-source references, quote-only unknown prices, gated references/workflows, source-supported rates and protected homepage.')
