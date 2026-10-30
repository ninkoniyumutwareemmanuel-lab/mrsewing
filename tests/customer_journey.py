#!/usr/bin/env python3
"""Public route/SEO validation and negative tests for customer-project publication."""
import sys,json,re,subprocess,hashlib
from pathlib import Path
from unittest.mock import patch
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import build_journey as journey
from build_public_routes import public_routes,ROOT,DOMAIN,outputs
from site_seo import finalize
routes=public_routes();assert len(routes)==len(set(routes))
class Tags(HTMLParser):
 def __init__(self):super().__init__();self.tags=[]
 def handle_starttag(self,t,a):self.tags.append((t,dict(a)))
for route in routes:
 path=ROOT/'index.html' if route=='/' else ROOT/route.strip('/')/'index.html';source=path.read_text();tags=Tags();tags.feed(source)
 assert finalize(source,path)==source,('SEO not idempotent',route)
 for key in ['og:title','og:description','og:url','og:image']:
  assert len([a for t,a in tags.tags if t=='meta' and a.get('property')==key])==1,(route,key)
 for t,a in tags.tags:
  if t=='img' and a.get('src'):assert a.get('alt') and int(a.get('width','0'))>0 and int(a.get('height','0'))>0,(route,a)
  if t=='a' and a.get('href','').startswith('/'):
   url=urlsplit(a['href']);target=ROOT/unquote(url.path.lstrip('/'))
   assert target.exists(),(route,a['href'])
 assert DOMAIN in source and 'data-staging-indexing' in source
assert '/our-work/' in routes and len(journey.services())==7
assert len(journey.projects())==5
assert len(list((ROOT/'our-work').glob('*/index.html')))==5
# Existing photo use is not publication permission; reject progressively incomplete evidence.
read=Path.read_text
base={'slug':'test-project','published':True,'title':'Test only','context':'Test only','images':[{'src':'/h2.jpeg','alt':'Test only','width':750,'height':938}]}
def reject(record):
 def replacement(path,*a,**k):
  return json.dumps({'projects':[record]}) if path==ROOT/'_data/customer-projects.json' else read(path,*a,**k)
 with patch.object(Path,'read_text',replacement):
  try:journey.projects()
  except (AssertionError,KeyError):return
 raise AssertionError('Unverified project accepted')
reject(base)
base.update(completedWorkEvidence='test evidence');reject(base)
base.update(publicationPermission={'approved':False,'evidenceRef':'test'});reject(base)
base['publicationPermission']['approved']=True;reject(base)
base['images'][0].update(permissionEvidenceRef='test permission',projectAssociationEvidenceRef='test association');base.update(testimonial={'text':'Test only'});reject(base)
# Never change registry, excluded photos or any original/optimized image bytes.
ref='08191fde2c1e984206ca40d53fbe99f69ce218da'
files=subprocess.check_output(['git','ls-tree','-r','--name-only',ref],cwd=ROOT,text=True).splitlines()
for file in files:
 if re.search(r'\.(?:jpe?g|png|webp|avif|gif|svg|mp4)$',file,re.I) or file in ['_data/collection-designs.json','_data/collection-id-registry.json','_templates/collections.css']:
  original=subprocess.check_output(['git','show',ref+':'+file],cwd=ROOT)
  assert hashlib.sha256(original).digest()==hashlib.sha256((ROOT/file).read_bytes()).digest(),file
assert '/views.html /our-work/ 301' in outputs()[ROOT/'_redirects']
headers=outputs()[ROOT/'_headers'];assert 'https://mrsewingfashion.com' not in headers
assert '/reviews/' not in routes and not any('?' in r or '.html' in r for r in routes)
print(f'PASS: {len(routes)} canonical pages with unique metadata, internal links/alt text, idempotent SEO, project consent/completion/testimonial gates, unchanged photos/registry/V3 gallery CSS and staging-only noindex rules.')

original_inventory=json.loads(subprocess.check_output(['git','show','08191fde2c1e984206ca40d53fbe99f69ce218da:_data/collection-image-inventory.json'],cwd=ROOT,text=True))
current_inventory=json.loads((ROOT/'_data/collection-image-inventory.json').read_text())
assert current_inventory['images'][:len(original_inventory['images'])]==original_inventory['images']
