"""Single permission/completion-gated portfolio source, without page-builder dependencies."""
from pathlib import Path
import json,re
ROOT=Path(__file__).resolve().parents[1]
def projects():
    records=json.loads((ROOT/'_data/customer-projects.json').read_text())['projects'];published=[]
    for p in records:
        assert re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*',p['slug'])
        if not p.get('published'):continue
        assert p.get('completedWorkEvidence') and p.get('publicationPermission',{}).get('approved') is True and p['publicationPermission'].get('evidenceRef'),'Completion and publication permission required'
        assert p.get('title') and p.get('context') and p.get('images')
        for image in p['images']:
            assert image.get('permissionEvidenceRef') and image.get('projectAssociationEvidenceRef')
            path=(ROOT/image['src'].lstrip('/')).resolve()
            assert image['src'].startswith('/') and path.is_relative_to(ROOT) and path.is_file() and path.suffix.lower() in ['.jpg','.jpeg','.png','.webp','.avif']
            assert image.get('alt') and image.get('width') and image.get('height')
        if p.get('testimonial'):assert p['testimonial'].get('approvalEvidenceRef') and p['testimonial'].get('text')
        published.append(p)
    assert len({p['slug'] for p in records})==len(records)
    return published

