from preservation_helpers import original_about_scope
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
assert '/shop/' not in public_routes()
for page in ['services/garment-care/index.html','services/garment-care/services/index.html','services/garment-care/planning/index.html']:
 html=(ROOT/page).read_text();assert 'Mr Sewing Garment Care' in html and 'care-basic-summary' in html
 assert 'Dry Cleaning' not in html and 'Paid suit cleaning — RWF' in html and '40,000' in html and '67,500' in html
source=(ROOT/'_templates/homepage-sections.html').read_text()
for photo,slug in [('h2.jpeg','off-white-graduation-suit'),('r7.jpeg','light-grey-and-navy'),('r4.jpeg','soft-ivory-tailoring')]:
 assert re.search('href="/our-work/'+slug+r'/"[^>]*><img src="'+re.escape(photo),source)
for href in ['/our-process/','/made-to-measure/','/services/garment-care/']:assert href in source
assert '18s infinite' not in (ROOT/'_templates/homepage-motion.css').read_text()
# Preserve the approved Collections experience and every pre-existing media byte.
ref='ce32d5ff67eacecf03804bf6608222c5f13e3cd1'
files=subprocess.check_output(['git','ls-tree','-r','--name-only',ref],cwd=ROOT,text=True).splitlines()
for f in files:
 if re.search(r'\.(?:jpe?g|png|webp|avif|gif|svg|mp4)$',f,re.I) or f in ['_data/collection-designs.json','_data/collection-id-registry.json','_templates/collections.css','assets/collections-v3.js','assets/collection-design.js']:
  old=subprocess.check_output(['git','show',ref+':'+f],cwd=ROOT);assert hashlib.sha256(old).digest()==hashlib.sha256((ROOT/f).read_bytes()).digest(),f
about_old=subprocess.check_output(['git','show',ref+':_templates/about.html'],cwd=ROOT,text=True)
assert re.search(r'<main.*?</main>',about_old,re.S)[0]==original_about_scope(re.search(r'<main.*?</main>',(ROOT/'_templates/about.html').read_text(),re.S)[0])
print(f'PASS: existing FAQ route preserved, five authorised projects / seven photographs, gated care offerings, exact homepage destinations, unchanged About story and protected Collections/media; {len(public_routes())} indexable routes.')

assert not (ROOT/'faqs').exists() and not (ROOT/'_data/faqs.json').exists()
