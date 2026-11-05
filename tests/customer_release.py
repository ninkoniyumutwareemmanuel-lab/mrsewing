#!/usr/bin/env python3
"""5 November owner release: scope, provenance gates, publication and homepage protection."""
from pathlib import Path
import json,hashlib,re,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from build_public_routes import public_routes
from build_collections import load
names=['Custom Tailoring & Suits','Clothing Alterations & Repairs','Garment Care & Cleaning','Mobile Tailoring, Styling & Event Assistance']
release=json.loads((ROOT/'_data/customer-release.json').read_text());assert [s['title'] for s in release['services']]==names+['VIP Services']
registry=json.loads((ROOT/'_data/journey-services.json').read_text());assert [s['title'] for s in registry if s['primary']]==names
assert '5 November 2026' in release['source']
allowed={'index.html','_templates/homepage-sections.html','_templates/homepage-header.html','_templates/homepage-footer.html','_templates/homepage-phase1.css','_data/homepage-guides.json','_data/page-seo.json'}
for f,h in json.loads((ROOT/'docs/homepage-approved-baseline.json').read_text())['files'].items():
 if f not in allowed:assert hashlib.sha256((ROOT/f).read_bytes()).hexdigest()==h,f
import subprocess
from build_homepage import Section,SECTIONS
for name,(file,tag,identifier) in SECTIONS.items():
 if name in ['header','footer','services']:continue
 old=subprocess.check_output(['git','show','0e6100183aa03c6929ebb5eca572f215eee40250:'+file],text=True,cwd=ROOT)
 a=Section(old,tag,identifier);a.feed(old);b=Section((ROOT/file).read_text(),tag,identifier);b.feed((ROOT/file).read_text());current=re.sub(r'<a class="hero-highlight hero-highlight-vip".*?</a>','',b.markup,flags=re.S) if name=='hero' else b.markup;assert a.markup==current,name
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
 html=(ROOT/s['route'].strip('/')/'index.html').read_text();assert 'Choose Standard Service' not in html and 'Choose VIP Service' not in html
 assert ('Explore Men’s Suits' in html and 'Explore Women’s Suits' in html) if s['id']=='custom-tailoring' else 'id="customerRequestForm"' in html
 assert 'name="subscription"' not in html and 'checkout.stripe' not in html
for filename in ['CUSTOMER_FACING_SOURCE_REGISTER.md','POLICY_RECONCILIATION_REPORT.md','UNRESOLVED_DECISIONS.md']:
 assert not (ROOT/filename).exists(),'Internal review must remain outside deployment root'
print('PASS: four ordinary categories plus VIP entry, revised direct journeys and protected unrelated homepage sections;, owner-source references, quote-only unknown prices, gated references/workflows, source-supported rates and protected homepage.')

# R3 appends only targeted ticket layout rules; existing approved stylesheet stays intact.
assert (ROOT/'_templates/homepage-phase1.css').read_text().startswith(subprocess.check_output(['git','show','0e6100183aa03c6929ebb5eca572f215eee40250:_templates/homepage-phase1.css'],text=True,cwd=ROOT))

assert next(g for g in json.loads((ROOT/'_data/homepage-guides.json').read_text()) if g['label']=='Fabric Guide')['href']=='/guides/fabrics/'

# R4 changes only gender landing metadata; all other approved SEO remains intact.
oldseo=json.loads(subprocess.check_output(['git','show','fea75aa7b3329fd819ad06e6b28b99e53119d0ba:_data/page-seo.json'],text=True,cwd=ROOT));newseo=json.loads((ROOT/'_data/page-seo.json').read_text())
for key in ['mensuits.html','womensuits.html']:
 assert 'Suits' in newseo[key]['title'] and 'Collection' not in newseo[key]['title'];newseo.pop(key);oldseo.pop(key)
assert oldseo==newseo
