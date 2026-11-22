"""R59 held-video HTML never embeds unapproved video URLs or posters."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from homepage_video_cards import render
html=render()
assert html.count('<figure>')==2 and html.count('<img ')==2
assert '<video' not in html and '1024X768VIDEO.mp4' not in html and '1024X768black.mp4' not in html
assert 'r7.jpeg' in html and 'h2.jpeg' in html
print('PASS: two non-activated video cards use approved photo fallbacks')
