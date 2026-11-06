#!/usr/bin/env python3
"""Build new approved customer guidance and request assets before existing consumers."""
import argparse
from customer_site import outputs
from site_seo import finalize,ROOT
p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');args=p.parse_args()
for path,value in outputs().items():
 if path.suffix=='.html':value=finalize(value,path)
 if args.check:
  if not path.exists() or path.read_text()!=value:raise SystemExit('Stale customer release: '+str(path.relative_to(ROOT)))
 else:path.parent.mkdir(parents=True,exist_ok=True);path.write_text(value)
print('PASS: customer guidance and review-before-submit assets '+('synchronized.' if args.check else 'generated.'))
