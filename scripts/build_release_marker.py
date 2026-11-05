"""Non-sensitive deployment fingerprint. Cloudflare CI supplies the served commit."""
from pathlib import Path
import os,json,argparse
ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');a=p.parse_args()
base={'release':'complete-repair-2026-11-05-r7','branch':'phase1/customer-journey-repairs','commit':None,'note':'When built in Cloudflare CI, commit is populated from CF_PAGES_COMMIT_SHA.'}
if os.environ.get('CF_PAGES_COMMIT_SHA'):
 base.update(commit=os.environ['CF_PAGES_COMMIT_SHA'],branch=os.environ.get('CF_PAGES_BRANCH','unknown'))
path=ROOT/'build-info.json';text=json.dumps(base,indent=2)+'\n'
if a.check:
 current=json.loads(path.read_text());assert current['release']==base['release']
else:path.write_text(text)
print('PASS: public release marker prepared; no credentials or customer data.')
