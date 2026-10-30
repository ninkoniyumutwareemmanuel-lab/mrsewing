#!/usr/bin/env python3
"""Central registry, inventory and invalid-data guard tests (no file mutations)."""
from copy import deepcopy
import json
from pathlib import Path
import sys
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import build_collections as build
public,inventory=build.load()
assert len({d['id'] for d in public})==len(public)
assert all(d['provenance']=='unverified' for d in public)
assert not inventory['missingLegacyReferences']
read=Path.read_text
source=json.loads(read(build.ROOT/'_data/collection-designs.json'))
def rejected(change):
    data=deepcopy(source);change(data)
    def override(path,*a,**kw):
        return json.dumps(data) if path==build.ROOT/'_data/collection-designs.json' else read(path,*a,**kw)
    with patch.object(Path,'read_text',override):
        try:build.load()
        except (AssertionError,KeyError):return
    raise AssertionError('Invalid design data was accepted')
rejected(lambda d:d['designs'].append(deepcopy(d['designs'][0])))
rejected(lambda d:d['designs'][0].update(id='MS-NEW'))
rejected(lambda d:d['designs'][0]['images'][0].update(src='/missing-collection-photo.jpg'))
rejected(lambda d:d['designs'][0].update(provenance='made_by_mr_sewing',provenanceEvidence=None))
rejected(lambda d:d['designs'][0].update(rightsStatus='restricted',published=True))
rejected(lambda d:d['designs'][0].update(publicationBasis='new_unreviewed_photo',published=True))
rejected(lambda d:d['designs'][0]['images'].append(deepcopy(d['designs'][0]['images'][0])))
rejected(lambda d:d['retiredIds'].append(d['designs'][0]['id']))
print(f'PASS: {len(public)} existing-public records, {len(inventory["images"])} inventoried assets; stable IDs, source ownership-review gates, missing assets, invalid provenance and retirement guards.')
