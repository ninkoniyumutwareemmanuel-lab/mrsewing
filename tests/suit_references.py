#!/usr/bin/env python3
"""R40 publication scope; R42 authorises compact cards and shared OFFER wrappers."""
from pathlib import Path
import sys,json,subprocess,re,hashlib
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from suit_references import model,categories,references
from build_collections import load
from build_public_routes import public_routes
BASE='33d23e3472691e566efac65743a03eab993c9713'
def old(f):return subprocess.check_output(['git','show',BASE+':'+f],cwd=ROOT,text=True)
def visible(s):return re.sub(r'<script id="(?:designSelectionData|requestDesignMedia|requestSuitCategories|requestDesigns)".*?</script>','',s,flags=re.S)
m=model();cats=categories();pool=load()[0];ids=[f'MS-{n:03}' for n in range(29,37)]
assert len(cats)==9 and len(m['references'])==27
assert [c['title'] for c in cats if c['gender']=='men']==['Single-Breasted Suits','Double-Breasted Suits','Tuxedos & Formalwear','Three-Piece Suits','Kaunda Suits']
before=json.loads(old('_data/suit-reference-categories.json'))
assert [c for c in cats if c['id']!='men-kaunda']==before['categories']
assert {k:v for k,v in m['references'].items() if k not in ids}==before['references']
assert cats[4]['designIds']==ids
for c in cats:
 rows=references(c,pool);f=c['route'].strip('/')+'/index.html';page=(ROOT/f).read_text();assert rows and c['route'] in public_routes()
 assert 'content="index, follow"' in page and all(d['id'] in page for d in rows)
 assert 'Tap a suit photograph to view its details.' in page and 'Choose a Reference' not in page
 assert 'data-select-design=' not in page and 'View Design <span' not in page
 for ident in c['designIds']:assert 'data-design-id="'+ident+'"' in page
for f in ['womensuits/index.html','womensuits.html','services/custom-tailoring/index.html','services/custom-tailoring/special-order/index.html','index.html']:
 assert re.search(r'<main\b.*?</main>',visible((ROOT/f).read_text()),re.S)[0]==re.search(r'<main\b.*?</main>',visible(old(f)),re.S)[0],f
for f in ['_data/collection-id-registry.json','_data/customer-projects.json','_data/measurement-guide-images.json','_data/suit-package-prices.json','_data/tuxedo-package-prices.json']:
 assert (ROOT/f).read_text()==old(f),f
now=json.loads((ROOT/'_data/collection-designs.json').read_text())['designs'];prior=json.loads(old('_data/collection-designs.json'))['designs']
assert [x for x,y in zip(now,prior) if x!=y]==[x for x in now if x['id'] in ids]
for a in json.loads((ROOT/'.github/customer-content-reference/KAUNDA_PUBLICATION_APPROVAL_2026-11-12.json').read_text())['images']:
 x=next(x for x in now if x['id']==a['designId']);assert x['rightsStatus']=='approved' and x['provenance']=='unverified'
 assert hashlib.sha256((ROOT/a['originalImagePath']).read_bytes()).hexdigest()==a['sha256']
allowed=json.loads((ROOT/'_data/request-reference-allowlist.json').read_text());assert all(i in allowed for i in ids)
assert all(f'MS-{n}' not in allowed for n in range(120,125))
print('PASS9categories27references;exact8approvals/originalbytes;R42simplegallerycards;women/home/CustomSpecialmain/prices/data unchanged;unapproveds1–5 excluded')
