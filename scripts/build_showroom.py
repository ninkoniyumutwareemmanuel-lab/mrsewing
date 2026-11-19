#!/usr/bin/env python3
"""Generate the central approved-media Showroom and recoverable inventory."""
import argparse
from showroom import outputs
from site_seo import finalize,ROOT
p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');a=p.parse_args()
for path,value in outputs().items():
 if path.suffix=='.html':value=finalize(value,path)
 payload=value if isinstance(value,bytes) else value.encode()
 if a.check:
  if not path.exists() or path.read_bytes()!=payload:raise SystemExit('Stale Showroom output: '+str(path.relative_to(ROOT)))
 else:path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(payload)
print('PASS approved-media Showroom and inventory '+('synchronized' if a.check else 'generated'))
