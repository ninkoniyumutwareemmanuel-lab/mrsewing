"""R5 append-only design registry contract. Existing records remain byte-equivalent JSON values."""
import json
from pathlib import Path
def append_only(original,current,file):
 old=json.loads(original);now=json.loads(current)
 if file.endswith('collection-id-registry.json'):
  assert all(now.get(k)==v for k,v in old.items());assert len(now)==len(old)+13
 else:
  assert now['designs'][:len(old['designs'])]==old['designs'];assert now['retiredIds']==old['retiredIds'];assert now['nextId']==old['nextId']+13
  new=now['designs'][len(old['designs']):];assert len(new)==13
  assert all(d['rightsStatus']=='approved' and d['published'] and d['provenance']=='design_inspiration' and d['provenanceEvidence'] for d in new)
