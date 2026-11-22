"""R60: two owner-authorised videos render with muted default controls."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from homepage_video_cards import render
html=render()
assert html.count('<figure')==2 and html.count('<video')==2
assert html.count('controls muted playsinline preload="none"')==2
assert '/1024X768VIDEO.mp4' in html and '/1024X768black.mp4' in html
assert 'poster="/r7.jpeg"' in html and 'poster="/h2.jpeg"' in html
print('PASS: two authorized videos, muted default, posters and controls')
