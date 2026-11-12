#!/usr/bin/env python3
"""R39: approved categories, current indexing and exact two-page preservation contract."""
from pathlib import Path
import sys,json,subprocess,re
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from suit_references import model,categories,references
from build_collections import load
from build_public_routes import public_routes
BASE='2c8b2fa062adc4a97d1dd095ea37e994b18f18c8'
m=model();cats=categories();pool=load()[0]
assert len(cats)==8 and len({c['id'] for c in cats})==8 and len({c['route'] for c in cats})==8
assert [c['title'] for c in cats if c['gender']=='men']==['Single-Breasted Suits','Double-Breasted Suits','Tuxedos & Formalwear','Three-Piece Suits']
assert [c['title'] for c in cats if c['gender']=='women']==['Single-Breasted Suits','Double-Breasted Suits','Skirt Suits','Three-Piece Suits']
assert len(m['references'])==19 and set(m['references']).issubset({d['id'] for d in pool})
assert all(r['publicationEvidence'] and r['classificationEvidence'] for r in m['references'].values())
for c in cats:
 rows=references(c,pool);file=c['route'].strip('/')+'/index.html';page=(ROOT/file).read_text();assert rows
 # R29 explicitly made populated, approved browsing categories indexable.
 assert c['route'] in public_routes() and 'content="index, follow"' in page and 'data-publication-hold' not in page
 assert all(d['id'] in page for d in rows)
 assert (ROOT/file).read_bytes()==subprocess.check_output(['git','show',BASE+':'+file],cwd=ROOT),file
for gender in ['men','women']:
 file=('mensuits' if gender=='men' else 'womensuits')+'/index.html';p=(ROOT/file).read_text();old=subprocess.check_output(['git','show',BASE+':'+file],cwd=ROOT,text=True)
 assert p.count('class="suit-category-card"')==4 and 'Explore Suit Styles' in p
 assert 'Special Order — Send Your Own Design' not in p and 'class="home-button home-button-gold suit-special"' not in p
 assert old.split('<div class="suit-category-grid">',1)[1].split('</section>',1)[0]==p.split('<div class="suit-category-grid">',1)[1].split('</section>',1)[0]
 for pattern in [r'<header\b.*?</header>',r'<footer\b.*?</footer>',r'<title>.*?</title>',r'<script type="application/ld\+json">.*?</script>']:
  assert re.search(pattern,p,re.S).group()==re.search(pattern,old,re.S).group(),file
 assert re.findall(r'<meta\b[^>]*>',p)==re.findall(r'<meta\b[^>]*>',old)
for file in ['_data/collection-designs.json','_data/collection-id-registry.json','_data/suit-reference-categories.json','_data/customer-projects.json','_data/measurement-guide-images.json','_data/suit-package-prices.json','_data/tuxedo-package-prices.json','assets/suit-references.css','assets/customer-site.js','services/custom-tailoring/index.html','services/custom-tailoring/special-order/index.html','index.html']:
 assert (ROOT/file).read_bytes()==subprocess.check_output(['git','show',BASE+':'+file],cwd=ROOT),file
print('PASS8approved/indexable categories19references/cardmarkup/header/footer/meta/galleryfiles/data/styles/CustomTailoringSpecial/form/home preserved;landingSpecialOrderremoved')
