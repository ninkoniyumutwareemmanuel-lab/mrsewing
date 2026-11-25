"""Approved text-first catalogue, shared by browsing and request validation.

Collection names describe reference groups, not confirmed fibre composition,
stock or selling prices. Legacy audience/tier references remain supported by
their separate historical request format; no new tier is inferred here.
"""
import json,re
from html import escape
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def catalogue():
    data=json.loads((ROOT/'_data/fabric-collections.json').read_text())
    assert data['schemaVersion']==1
    ids=set()
    for collection in data['collections']:
        assert collection['group'] in ['premium','standard']
        assert re.fullmatch(r'[a-z0-9-]+',collection['id'])
        assert collection['styles']
        for style in collection['styles']:
            assert style['id'] not in ids and re.fullmatch(r'[a-z0-9-]+',style['id'])
            ids.add(style['id']);assert style['name']
    assert len(data['patterns'])==len({p['id'] for p in data['patterns']})
    return data

def fabrics():
    return {style['id']:{'id':style['id'],'name':style['name'],
            'collectionId':collection['id'],'collection':collection['name'],
            'collectionGroup':collection['group'],'category':'all'}
            for collection in catalogue()['collections'] for style in collection['styles']}

def patterns():
    return {p['id']:{'name':p['name'],'description':p['description']}
            for p in catalogue()['patterns']}

def detail_template(slug):
    """Retain approved editorial descriptions; validate controls against source.

    Templates own rich general characteristics, while selectable names/IDs and
    pattern choices have one canonical record. Fail instead of silently drifting.
    """
    collection=next(c for c in catalogue()['collections'] if c['id']==slug)
    source=(ROOT/('_templates/fabric-showroom-'+slug+'.html')).read_text()
    match=re.search(r'<script id="fg-data" type="application/json">(.*?)</script>',source)
    original=json.loads(match[1])
    assert original['types']==[s['name'] for s in collection['styles']]
    assert [(p[0],p[1]) for p in original['patterns']]==[(p['id'],p['name']) for p in catalogue()['patterns']]
    colours=json.loads((ROOT/'_data/fabric-colours.json').read_text())['colours']
    assert [(c['id'],c['name']) for c in original['colors']]==[(c['id'],c['name']) for c in colours]
    payload={**original,'collectionId':slug,'styles':collection['styles']}
    source=source[:match.start(1)]+json.dumps(payload,ensure_ascii=False).replace('<','\\u003c')+source[match.end(1):]
    source=source.replace('</dl>','<dt>Care considerations</dt><dd>'+escape(catalogue()['careNotice'])+'</dd></dl>')
    return source.replace('/assets/fabric-showroom.js','/assets/fabric-showroom.js?v=recovery-20261125')
