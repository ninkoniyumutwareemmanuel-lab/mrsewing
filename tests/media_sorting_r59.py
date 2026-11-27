"""R59 source-backed newest-first and grouping tests; no invented upload dates."""
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from media_sorting import newest_first,verified_day
def row(ident,date=None,evidence=None,basis='verified-upload',views=1,gender='men'):
    return {'id':ident,'mediaDateAdded':date,'mediaDateEvidence':evidence,'mediaDateBasis':basis,
            'images':[{'src':f'/{ident}-{i}.webp'} for i in range(views)],'gender':gender}
older=row('older','2026-11-18','commit-1')
newer=row('newer','2026-11-21','commit-2',views=3)
tie=row('tie','2026-11-21','commit-3')
undated=row('unknown')
no_proof=row('unproven','2026-11-22')
nondate=row('invalid','2026-11-31','commit-4')
items=[undated,older,tie,no_proof,newer,nondate]
ordered=newest_first(items)
assert [d['id'] for d in ordered]==['tie','newer','older','unknown','unproven','invalid']
assert ordered[1]['images']==newer['images'] and len(ordered[1]['images'])==3
assert verified_day(no_proof) is None and verified_day(nondate) is None
assert verified_day(row('future','2026-11-22','reference',basis='guess')) is None
assert [d['id'] for d in newest_first([undated,no_proof,nondate])]==['unknown','unproven','invalid']
assert [d['id'] for d in newest_first([x for x in items if x['gender']=='men'])]==[x['id'] for x in ordered]
assert [d['id'] for d in newest_first([{'id':'newer'},{'id':'older'}],evidence={x['id']:x for x in items})]==['newer','older']
from build_collections import load
published,_=load()
assert len(published)>0 and all(d.get('id') not in {f'MS-{i}' for i in range(152,174)} for d in published)
assert [x['id'] for x in newest_first(published)]==[x['id'] for x in published] # No verified public dates yet
print('PASS: verified dates, unknowns, ties, filters, grouped views and held-media exclusion')
