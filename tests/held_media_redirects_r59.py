"""R61/recovery: owner-authorized assets unblocked; genuine held fixtures stay gated."""
import sys,json,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
import build_public_routes as routes
from urllib.parse import quote
held=routes.held_r53_media_paths()
assert held==[],('R61 repository-media permission must not remain a missing-permission hold',held)
content=routes.outputs()[ROOT/'_redirects']
assert ' /404.html 302' not in content
assert '/1024X768VIDEO.mp4 /404.html' not in content and '/1024X768black.mp4 /404.html' not in content
# No approved data is mutated. Unapproved temporary records still produce a
# verified exact local path rather than a broad redirect or invented asset.
with tempfile.TemporaryDirectory() as temp:
 fixture=Path(temp);(fixture/'_data').mkdir();(fixture/'test-photo.webp').write_bytes(b'temporary fixture')
 (fixture/'_data/collection-designs.json').write_text(json.dumps({'designs':[{'published':False,'publicationBasis':'prepared_owner_catalogue_pending_usage_rights','images':[{'src':'/test-photo.webp'}]}]}))
 (fixture/'_data/media-video-records.json').write_text(json.dumps({'videos':[]}))
 oldroot=routes.ROOT
 try:
  routes.ROOT=fixture;assert routes.held_r53_media_paths()==['/test-photo.webp']
 finally:routes.ROOT=oldroot
print('PASS R61 owner-authorized media no longer falsely blocked; temporary unapproved media retains exact-path gate')
