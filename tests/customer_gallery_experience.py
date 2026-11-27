#!/usr/bin/env python3
"""26Nov customer gallery contracts; presentation may change, identity/rights may not."""
import json,re,sys,tempfile
from pathlib import Path
from html.parser import HTMLParser
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import build_collections as gallery
from suit_references import categories,references
from media_sorting import newest_first
from project_catalog import projects

class Visible(HTMLParser):
    def __init__(self,html):
        super().__init__();self.hidden=0;self.text=[];self.titles=[];self.feed(html)
    def handle_starttag(self,tag,attrs):
        if tag in ('script','style'):self.hidden+=1
    def handle_endtag(self,tag):
        if tag in ('script','style'):self.hidden-=1
    def handle_data(self,value):
        if not self.hidden:self.text.append(value)

designs,_=gallery.load()
raw=json.loads((ROOT/'_data/collection-designs.json').read_text())['designs']
by_id={d['id']:d for d in designs}
assert len(designs)==28,'No new image publication authorized by this visual task'
titles=[]
for design in designs:
    name=gallery.design_name(design)
    assert name and name not in ('Tailoring Design','Tailored Suit','Women’s Suit')
    assert not re.search(r'MS-\d+',name)
    html=gallery.render_design(design,designs)
    visible=' '.join(Visible(html).text)
    assert not re.search(r'\bMS-\d+',visible),'Public reference leaked: '+design['id']
    assert 'Reference '+design['id'] not in html
    assert 'design reference '+design['id'] not in html
    assert 'name="description"' in html and 'rel="canonical"' in html
    assert 'data-select-design' not in html or design['id'] in html
    assert '/services/custom-tailoring/fabric/?' in html
    assert design['images'][0]['src'] in html
    titles.append(re.search(r'<title>(.*?)</title>',html).group(1))
    label=gallery.workmanship_label(design)
    assert label in ('Made by Mr Sewing','Design Inspiration')
    if design['id'] in {f'MS-{n:03}'for n in range(29,37)}:assert label=='Design Inspiration'
assert len(titles)==len(set(titles)),'Detail titles must distinguish legitimate different views'
assert gallery.workmanship_label({'provenance':'made_by_mr_sewing','images':[{'src':'/unverified.jpeg'}]})=='Design Inspiration'
assert gallery.workmanship_label({'provenance':'unverified','images':[{'src':'/h1.jpeg'}]})=='Design Inspiration'
html=gallery.render('collections.html','all','Showroom',designs)
assert '<h1 id="show-title">Showroom</h1>' in html
assert '<details class="show-filter-panel">' in html
assert all(x in html for x in ('id="design-search"','id="style-filter"','id="occasion-filter"','id="load-more"'))
assert html.count('<article class="show-card"')==12
assert len({d['id'] for d in designs})==28
assert gallery.public_data(by_id['MS-142'])['name']=='Royal Ivory Tuxedo'
assert gallery.public_data(by_id['MS-142'])['workmanship']=='Design Inspiration'
assert gallery.workmanship_label(by_id['MS-005'])=='Made by Mr Sewing'
# Old undated records keep their existing stable order; unknown/unproven dates
# cannot masquerade as a fresh publication. Whole and category galleries share it.
sample=[{'id':'old'},{'id':'unknown'},{'id':'new'},{'id':'tie'},{'id':'fake'}]
evidence={'old':{'mediaDateAdded':'2026-01-01','mediaDateEvidence':'verified fixture','mediaDateBasis':'verified-publication'},'new':{'mediaDateAdded':'2026-11-26','mediaDateEvidence':'verified fixture','mediaDateBasis':'verified-added'},'tie':{'mediaDateAdded':'2026-11-26','mediaDateEvidence':'verified fixture','mediaDateBasis':'verified-upload'},'fake':{'mediaDateAdded':'2026-12-01'}}
assert [d['id'] for d in newest_first(sample,evidence)]==['new','tie','old','unknown','fake']
assert [d['id'] for d in newest_first(sample)]==[d['id']for d in sample]
with tempfile.TemporaryDirectory() as directory:
    base=Path(directory);(base/'_data').mkdir()
    (base/'_data/collection-designs.json').write_text(json.dumps({'designs':[{'id':ident,**value}for ident,value in evidence.items()]}))
    with patch.object(gallery,'ROOT',base):
        assert [d['id']for d in gallery.ordered_designs(sample)]==['new','tie','old','unknown','fake']
        category={'designIds':['old','unknown','new','tie','fake']}
        assert [d['id']for d in references(category,sample)]==['new','tie','old','unknown','fake']
for category in categories():
    assert {d['id'] for d in references(category,designs)}==set(category['designIds'])
assert len(projects())==5
print('PASS:28 published identities/photos,unique meaningful names,hidden references,verified workmanship,compact filters,dated/unknown/tie/category ordering and5permission-gated projects')
