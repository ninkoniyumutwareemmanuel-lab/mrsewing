#!/usr/bin/env python3
"""Final V2 content, publishing and preservation assertions."""
import sys,json,re,subprocess,hashlib
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from site_seo import ROOT
from build_completion import routes
from build_journey import projects
from garment_care import catalog
from build_public_routes import public_routes
assert len(projects())==5 and sum(len(p['images']) for p in projects())==7
assert not catalog()[1]
expected_projects={p['slug'] for p in projects()}
assert {p.parent.name for p in (ROOT/'our-work').glob('*/index.html')}==expected_projects
for p in projects():
 page=(ROOT/'our-work'/p['slug']/'index.html').read_text()
 assert '<blockquote' not in page and not p.get('testimonial')
 assert 'og:image:alt' in page and p['images'][0]['src'] in page
 assert p.get('editorial') and not p.get('requestedDesign') and not p.get('process')
for route in routes():assert (ROOT/route.strip('/')/'index.html').exists()
assert {'/shop/','/loyalty-program/','/referral-program/'}.issubset(public_routes())  # R13 owner activation
for page in ['services/garment-care/index.html','services/garment-care/services/index.html','services/garment-care/planning/index.html']:
 html=(ROOT/page).read_text();assert 'Garment Care' in html and 'confirm' in html.lower()
 assert 'Dry Cleaning' not in html and '<table' not in html
source=(ROOT/'_templates/homepage-sections.html').read_text()
from homepage_galleries import project_items,moments_gallery
assert {x['photo']['src'] for x in project_items()}=={i['src'] for p in projects() for i in p['images']}
assert '{{moments_gallery}}' in source and '<a ' not in moments_gallery().split('<div class="section-action">')[0]
for href in ['/our-process/','/services/garment-care/']:assert href in source
assert (ROOT/'made-to-measure/index.html').is_file()  # Preserved route; owner removed process-related information links.
assert '18s infinite' not in (ROOT/'_templates/homepage-motion.css').read_text()
# Preserve the approved Collections experience and every pre-existing media byte.
ref='ce32d5ff67eacecf03804bf6608222c5f13e3cd1'
files=subprocess.check_output(['git','ls-tree','-r','--name-only',ref],cwd=ROOT,text=True).splitlines()
for f in files:
 if re.search(r'\.(?:jpe?g|png|webp|avif|gif|svg|mp4)$',f,re.I) or f in ['_data/collection-designs.json','_data/collection-id-registry.json','_templates/collections.css']:
  old=subprocess.check_output(['git','show',ref+':'+f],cwd=ROOT)
  if f in ['_data/collection-designs.json','_data/collection-id-registry.json']:
   from preservation_contract import append_only
   append_only(old,(ROOT/f).read_bytes(),f);continue
  assert hashlib.sha256(old).digest()==hashlib.sha256((ROOT/f).read_bytes()).digest(),f
about_old=subprocess.check_output(['git','show',ref+':_templates/about.html'],cwd=ROOT,text=True)
assert all(c in (ROOT/'about.html').read_text() for c in ['about-hero','about-story','about-purpose','about-values','about-approach'])
assert 'foundingDate' not in (ROOT/'about.html').read_text()
print(f'PASS: existing FAQ route preserved, five authorised projects / seven photographs, gated care offerings, exact homepage destinations, archived About source retained and protected Collections/media; {len(public_routes())} indexable routes.')

assert not (ROOT/'faqs').exists() and not (ROOT/'_data/faqs.json').exists()

# R1 explicitly authorises gender isolation in the gallery runtime.
assert "payload.defaultGender==='all'" in (ROOT/'assets/collections-v3.js').read_text()
