"""R59 staging-only direct held-media URL suppression, from the central media registry."""
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_public_routes import held_r53_media_paths,outputs
from urllib.parse import quote
held=held_r53_media_paths()
assert len(held)==27,(len(held),held) # 25 source images and two raw held videos
assert '/1024X768VIDEO.mp4' in held and '/1024X768black.mp4' in held
content=outputs()[ROOT/'_redirects']
assert sum(' /404.html 302' in row for row in content.splitlines())==len(held)
for path in held:assert quote(path,safe='/-._~')+' /404.html 302' in content
assert '/assets/policy-documents/terms-and-conditions/pages/1.0-01.png' not in held
assert '/r7.jpeg' not in held and '/h2.jpeg' not in held
print('PASS: 25 held photographs + two held videos denied by staging-only redirect rules; published assets unaffected')
