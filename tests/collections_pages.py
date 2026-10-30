#!/usr/bin/env python3
"""Static publication boundaries, evidence-based names, recommendations and links."""
import json,re,sys,hashlib,subprocess
import xml.etree.ElementTree as ET
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import build_collections as build
public,_=build.load()
records=json.loads((build.ROOT/'_data/collection-designs.json').read_text())['designs']
expected={build.ROOT/build.design_route(d).strip('/')/'index.html' for d in public}
actual=set((build.ROOT/'collections/designs').glob('*/index.html'))
assert expected==actual,(len(expected),len(actual))
urls=[el.text for el in ET.parse(build.ROOT/'collections/designs/sitemap.xml').findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc')]
assert len(urls)==len(public)==len(set(urls))
assert set(urls)=={'https://mrsewingfashion.com'+build.design_route(d) for d in public}
for d in public:
    route=build.design_route(d);page=(build.ROOT/route.strip('/')/'index.html').read_text()
    assert f'href="https://mrsewingfashion.com{route}"' in page
    assert d['id'] not in re.search(r'<h1>(.*?)</h1>',page,re.S)[1]
    assert not any(re.search(r'MS-\d+',alt) for alt in re.findall(r' alt="([^"]*)"',page))
    assert not re.search(r'data-save|shortlist|Favourites|"@type":\s*"Product"',page)
    similar,more=build.recommendations(d,public)
    all_ids=[other['id'] for other in similar+more]
    assert d['id'] not in all_ids and len(all_ids)==len(set(all_ids))
    assert len(similar)<=4 and len(more)<=4
    for other in similar:
        assert (set(d['styles'])&set(other['styles']) or set(d['occasions'])&set(other['occasions']) or d['gender']!='unclassified' and d['gender']==other['gender'])
for d in records:
    if not d['published']:assert not (build.ROOT/build.design_route(d).strip('/')).exists()
# Confirm the approved pages, shared chrome, original assets and registry stay byte-identical.
baseline='08191fde2c1e984206ca40d53fbe99f69ce218da'
protected=['_data/collection-designs.json','_data/collection-id-registry.json','_templates/collections.css','_templates/about.html','_templates/about.css','_templates/contact.html','_templates/contact.css','_data/contact-v2.json']
required=set(protected)
protected += subprocess.check_output(['git','ls-tree','-r','--name-only',baseline],cwd=build.ROOT,text=True).splitlines()
protected={p for p in protected if p in required or re.search(r'\.(?:jpe?g|png|webp|avif|gif|svg|mp4)$',p,re.I)}
for file in protected:
    original=subprocess.check_output(['git','show',baseline+':'+file],cwd=build.ROOT)
    assert hashlib.sha256(original).digest()==hashlib.sha256((build.ROOT/file).read_bytes()).digest(),file
print(f'PASS: {len(public)} eligible static garment pages; {len(records)-len(public)} excluded records stay excluded; stable links, metadata-backed distinct recommendations and protected original media, V3 gallery styling, About/Contact templates and registry unchanged.')

original_inventory=json.loads(subprocess.check_output(['git','show','08191fde2c1e984206ca40d53fbe99f69ce218da:_data/collection-image-inventory.json'],cwd=build.ROOT,text=True))
current_inventory=json.loads((build.ROOT/'_data/collection-image-inventory.json').read_text())
assert current_inventory['images'][:len(original_inventory['images'])]==original_inventory['images']
