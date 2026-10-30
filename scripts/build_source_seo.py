#!/usr/bin/env python3
"""Synchronize original page metadata and indexability before rendering consumers."""
import argparse,json,re
from pathlib import Path
from sync_page_seo import apply
from site_seo import ROOT,finalize
p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');a=p.parse_args()
for name,data in json.loads((ROOT/'_data/page-seo.json').read_text()).items():
    if name in json.loads((ROOT/'_data/route-aliases.json').read_text()):continue
    path=ROOT/('_templates/homepage.html' if name=='index.html' else name)
    old=path.read_text();new=apply(old,data)
    def structured(match):
        graph=json.loads(match[2])
        if isinstance(graph,dict) and '@graph' in graph:
            cleaned=[n for n in graph['@graph'] if n.get('@type') not in ['Product','AggregateOffer','Review','AggregateRating']]
            if cleaned!=graph['@graph']:graph['@graph']=cleaned;return match[1]+json.dumps(graph,ensure_ascii=False)+match[3]
        return match[0]
    new=re.sub(r'(<script[^>]*type="application/ld\+json"[^>]*>)(.*?)(</script>)',structured,new,flags=re.S)
    # Templates acquire final tags when rendered; legacy source pages need them now.
    if name!='index.html':new=finalize(new,ROOT/name)
    if a.check and old!=new:raise SystemExit('Stale source SEO: '+name)
    if not a.check and old!=new:path.write_text(new)
print('PASS: source metadata and indexability synchronized.')
