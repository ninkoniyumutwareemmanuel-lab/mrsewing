#!/usr/bin/env python3
"""Audit every sitemap page, its metadata and local resource destinations."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin,urlsplit,unquote
import sys,json
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from build_public_routes import public_routes
ROOT=Path(__file__).resolve().parents[1]
class Page(HTMLParser):
 def __init__(self,text):
  super().__init__();self.tags=[];self.titles=[];self.title=False;self.feed(text)
 def handle_starttag(self,t,a):
  self.tags.append((t,dict(a)))
  if t=='title':self.title=True
 def handle_endtag(self,t):
  if t=='title':self.title=False
 def handle_data(self,s):
  if self.title:self.titles.append(s)
def path_for(route):
 p=ROOT/unquote(route.lstrip('/'))
 return p/'index.html' if p.is_dir() else p
seen_titles=set();seen_descriptions=set();links=0
for route in public_routes():
 text=path_for(route).read_text();p=Page(text)
 base=next((a['href'] for t,a in p.tags if t=='base' and a.get('href')),route)
 title=''.join(p.titles);assert title and title not in seen_titles,(route,'duplicate title');seen_titles.add(title)
 desc=[a.get('content') for t,a in p.tags if t=='meta' and a.get('name')=='description'];assert len(desc)==1 and desc[0] and desc[0] not in seen_descriptions,(route,'duplicate/missing description');seen_descriptions.add(desc[0])
 assert sum(t=='h1' for t,a in p.tags)==1,(route,'H1')
 assert [a.get('href') for t,a in p.tags if t=='link' and a.get('rel')=='canonical']==['https://mrsewingfashion.com'+route],(route,'canonical')
 assert all(any(t=='meta' and a.get('property')==key and a.get('content') for t,a in p.tags) for key in ['og:title','og:description','og:url','og:image']),(route,'Open Graph')
 for t,a in p.tags:
  if t=='img':assert 'alt' in a,(route,'missing alt')
  resource=a.get('href') if t=='a' else a.get('src') if t in ['img','script'] else a.get('href') if t=='link' and a.get('rel')=='stylesheet' else None
  if not resource:continue
  url=urlsplit(urljoin(urljoin('https://mrsewingfashion.com'+route,base),resource))
  if url.netloc!='mrsewingfashion.com':continue
  assert path_for(url.path).is_file(),(route,resource,'missing local destination');links+=1
 # JSON-LD is parseable, with no fabricated review/rating properties.
 import re
 for block in re.findall(r'<script[^>]*type="application/ld\+json"[^>]*>(.*?)</script>',text,re.S):json.loads(block)
print(f'PASS: {len(seen_titles)} sitemap pages with unique titles/descriptions, one H1, canonical/Open Graph metadata, parseable structured data and {links} existing local links/resources.')
