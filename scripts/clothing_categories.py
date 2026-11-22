"""Staging R59: one reviewed category registry for the main service hub and Universal Showroom."""
from pathlib import Path
from html import escape
import json
from urllib.parse import urlencode
ROOT=Path(__file__).resolve().parents[1]

def active(designs):
    from suit_references import assignment
    config=json.loads((ROOT/'_data/clothing-category-config.json').read_text())
    assert config['schemaVersion']==1
    out=[]
    for row in config['categories']:
        assert row['filterField'] in ('gender','garment'),'Unreviewed category field'
        assert row['filterValue'] and row['name'] and row['coverDesignId']
        def matches(design):
            a=assignment(design['id'])
            if row['filterField']=='gender':
                return (a or {}).get('gender',design['gender'])==row['filterValue']
            return design.get('garmentType','').casefold()==row['filterValue'].casefold()
        eligible=[d for d in designs if matches(d)]
        if not eligible:continue
        cover=next((d for d in eligible if d['id']==row['coverDesignId']), eligible[0])
        out.append(dict(row,cover=cover,url='/collections/?'+urlencode({row['filterField']:row['filterValue']})))
    return out

def nav(designs, selected='all'):
    entries=active(designs)
    return '<a href="/collections/"'+(' aria-current="page"' if selected=='all' else '')+'>All Designs</a>'+''.join('<a href="'+escape(row['url'],quote=True)+'">'+escape(row['name'])+'</a>' for row in entries)
