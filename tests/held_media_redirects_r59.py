"""R60: published video originals are unblocked; held photos remain redirected."""
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from build_public_routes import held_r53_media_paths,outputs
from urllib.parse import quote
held=held_r53_media_paths()
assert len(held)==25,(len(held),held)
assert '/1024X768VIDEO.mp4' not in held and '/1024X768black.mp4' not in held
content=outputs()[ROOT/'_redirects']
assert sum(' /404.html 302' in row for row in content.splitlines())==len(held)
for path in held:assert quote(path,safe='/-._~')+' /404.html 302' in content
assert '/1024X768VIDEO.mp4 /404.html' not in content and '/1024X768black.mp4 /404.html' not in content
print('PASS: two videos unblocked; 25 held photographs still restricted')
