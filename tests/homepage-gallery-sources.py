#!/usr/bin/env python3
"""Verify projection parity and actual authoritative-source mutations, restoring every file."""
from pathlib import Path
import sys,json,re
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from homepage_galleries import collection_items,project_items,suit_section,moments_gallery
from build_collections import load
from suit_references import categories,references
from build_journey import projects
from build_homepage import render
for gender in ['men','women']:
 expected={i['src'] for c in categories() if c['gender']==gender for d in references(c,load()[0]) for i in d['images']}
 assert {x['photo']['src'] for x in collection_items(gender)}==expected
assert [x['photo']['src'] for x in project_items()]==[i['src'] for p in projects() for i in p['images']]
p=ROOT/'_data/suit-reference-categories.json';original=p.read_bytes()
try:
 d=json.loads(original);category=next(c for c in d['categories'] if c['gender']=='men' and len(c['designIds'])>1);ident=category['designIds'].pop();p.write_text(json.dumps(d));assert not any(x['id']==ident for x in collection_items('men'));assert 'data-reference="'+ident+'"' not in suit_section();assert 'data-reference="'+ident+'"' not in render()
finally:p.write_bytes(original)
assert any(x['id']==ident for x in collection_items('men'))
p=ROOT/'_data/customer-projects.json';original=p.read_bytes()
try:
 d=json.loads(original);project=next(x for x in d['projects'] if x['published'] and len(x['images'])>1);removed=project['images'].pop();p.write_text(json.dumps(d));assert removed['src'] not in [x['photo']['src'] for x in project_items()];assert 'data-photo-source="'+removed['src']+'"' not in moments_gallery()
 d=json.loads(original);project=next(x for x in d['projects'] if x['published']);project['images'][0]['alt']='Source synchronisation audit marker';p.write_text(json.dumps(d));assert 'Source synchronisation audit marker' in render()
finally:p.write_bytes(original)
assert 'Source synchronisation audit marker' not in render()
print('PASS shared collection/project loader parity; remove/restore category design and project photo; authoritative alt update reaches full rendered homepage; files restored')
