"""Rendered internal fragments and all FAQ source anchors must resolve locally."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urljoin,urlsplit,unquote
import json
ROOT=Path(__file__).resolve().parents[1]
class Page(HTMLParser):
 def __init__(self,text):super().__init__();self.ids=set();self.links=[];self.feed(text)
 def handle_starttag(self,tag,attrs):
  attrs=dict(attrs)
  if attrs.get('id'):self.ids.add(attrs['id'])
  if tag=='a' and attrs.get('href'):self.links.append(attrs['href'])
cache={}
for file in ROOT.rglob('*.html'):
 if any(part in {'.git','_templates','node_modules','.wrangler','artifacts'} for part in file.relative_to(ROOT).parts):continue
 cache[file]=Page(file.read_text())
errors=[];checked=0

def check(source,base,href):
 global checked
 url=urlsplit(urljoin('https://mrsewingfashion.com'+base,href))
 if url.hostname!='mrsewingfashion.com' or not url.fragment or url.fragment.startswith(':~:'):return
 target=ROOT/unquote(url.path).lstrip('/')
 if target.is_dir():target=target/'index.html'
 checked+=1
 if target not in cache or unquote(url.fragment) not in cache[target].ids:errors.append((source,href))
for file,page in cache.items():
 route='/'+file.relative_to(ROOT).as_posix();route=route[:-10] if route.endswith('index.html') else route
 for href in page.links:check(str(file.relative_to(ROOT)),route,href)
faqs=json.loads((ROOT/'_data/customer-faqs.json').read_text())['questions']
for ident,q in faqs.items():check('FAQ '+ident,'/faq/',q.get('source',''))
assert not errors,errors
print(f'PASS {len(cache)} generated HTML documents and {len(faqs)} FAQ source mappings; {checked} internal fragment targets resolve; no stale modal/payment/fabric/benefit source anchors')
