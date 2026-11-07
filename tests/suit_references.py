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
assert len(m['references'])==19 and set(m['references']).issubset({d['id'] for d in pool})
assert all(r['publicationEvidence'] and r['classificationEvidence'] for r in m['references'].values())
assert sum(bool(c['designIds']) for c in cats)==8
for c in cats:
 rows=references(c,pool);page=(ROOT/c['route'].strip('/')/'index.html').read_text();assert c['route'] in page
 if rows:
  assert c['route'] not in public_routes() and 'content="noindex, follow"' in page and 'data-publication-hold' not in page
  assert all(d['id'] in page for d in rows)
 else:
  assert c['route'] not in public_routes() and 'data-publication-hold' in page and 'noindex, follow' in page
  assert not re.search(r'<main.*?<img',page,re.S)
for gender in ['men','women']:
 route='/mensuits/' if gender=='men' else '/womensuits/';p=(ROOT/route.strip('/')/'index.html').read_text();assert p.count('class="suit-category-card"')==4;assert 'Explore Suit Styles' in p;assert 'Special Order — Send Your Own Design' in p
 assert 'Men’s Collection' not in p and 'Women’s Collection' not in p
# R5 permits append-only references, clean guide descriptions, breadcrumbs and consent routing.
from preservation_contract import append_only
for file in ['_data/collection-designs.json','_data/collection-id-registry.json']:
 append_only(subprocess.check_output(['git','show','70dfdd7:'+file],cwd=ROOT),(ROOT/file).read_bytes(),file)
for file in ['_data/customer-projects.json']:
 assert (ROOT/file).read_bytes()==subprocess.check_output(['git','show','70dfdd7:'+file],cwd=ROOT),file
print('PASS: 8 populated categories/19 assigned references, append-only IDs and protected homepage/media.')

from build_homepage import Section,SECTIONS
for name,(file,tag,identifier) in SECTIONS.items():
 if name in ['hero','customers','contact','final']:continue
 before=subprocess.check_output(['git','show','e2139dec2d96c1ec0d4083e860d9ab6445c145a7:'+file],cwd=ROOT,text=True)
 a=Section(before,tag,identifier);a.feed(before);b=Section((ROOT/file).read_text(),tag,identifier);b.feed((ROOT/file).read_text());current=b.markup.replace('aria-label="Online Shop"','aria-label="Shop — Coming Soon" title="Shop — Coming Soon; online purchasing is not available yet"');current=re.sub(r'<a href="/(?:loyalty|referral)-program/">([^<]+)</a>',r'\1',current);assert a.markup==current,name
old=json.loads(subprocess.check_output(['git','show','433107e:_data/measurement-guide-images.json'],cwd=ROOT,text=True));now=json.loads((ROOT/'_data/measurement-guide-images.json').read_text())
assert {m['id']:m for m in old['measurements']}=={m['id']:m for m in now['measurements']}
assert now['measurements'][0]['id']=='neck' and now['measurements'][-1]['id']=='trouser-length'
