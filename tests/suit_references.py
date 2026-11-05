#!/usr/bin/env python3
"""R4: exactly eight categories, approved immutable reference IDs, truthful empty states and metadata."""
from pathlib import Path
import sys,json,subprocess,re
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from suit_references import model,categories,assignment,references
from build_collections import load
from build_public_routes import public_routes
m=model();cats=categories();pool=load()[0]
assert len(cats)==8 and len({c['id'] for c in cats})==8 and len({c['route'] for c in cats})==8
assert [c['title'] for c in cats if c['gender']=='men']==['Single-Breasted Suits','Double-Breasted Suits','Tuxedos & Formalwear','Three-Piece Suits']
assert [c['title'] for c in cats if c['gender']=='women']==['Single-Breasted Suits','Double-Breasted Suits','Skirt Suits','Three-Piece Suits']
assert len(m['references'])==6 and set(m['references']).issubset({d['id'] for d in pool})
assert all(r['publicationEvidence'] and r['classificationEvidence'] for r in m['references'].values())
assert sum(bool(c['designIds']) for c in cats)==3
for c in cats:
 rows=references(c,pool);page=(ROOT/c['route'].strip('/')/'index.html').read_text();assert c['route'] in page
 if rows:
  assert c['route'] in public_routes() and 'data-publication-hold' not in page
  assert all(d['id'] in page for d in rows)
 else:
  assert c['route'] not in public_routes() and 'data-publication-hold' in page and 'noindex, follow' in page
  assert not re.search(r'<main.*?<img',page,re.S)
for gender in ['men','women']:
 route='/mensuits/' if gender=='men' else '/womensuits/';p=(ROOT/route.strip('/')/'index.html').read_text();assert p.count('class="suit-category-card"')==4;assert 'Explore Suit Styles' in p;assert 'Special Order — Send Your Design' in p
 assert 'Men’s Collection' not in p and 'Women’s Collection' not in p
for f in ['_data/collection-designs.json','_data/collection-id-registry.json','_data/customer-projects.json','index.html','_templates/customer-site.css','_templates/homepage-sections.html','_data/customer-release.json','_data/fabric-reference-catalogue.json','_data/measurement-guide-images.json']:
 assert (ROOT/f).read_bytes()==subprocess.check_output(['git','show','fea75aa7b3329fd819ad06e6b28b99e53119d0ba:'+f],cwd=ROOT),f
print('PASS: 8 exact category routes, 6 existing authorised references, 3 populated/5 truthful noindex galleries, stable registry/media/customer policies and approved homepage.')
