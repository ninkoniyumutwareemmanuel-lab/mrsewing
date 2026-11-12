from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote,urljoin
from collections import defaultdict
import json,xml.etree.ElementTree as E
R=Path(__file__).resolve().parents[1]
class Page(HTMLParser):
 def __init__(self,s):
  super().__init__(convert_charrefs=True);self.tags=[];self.texts=defaultdict(list);self.stack=[];self.current=None;self.buf='';self.ld=[];self.feed(s)
 def handle_starttag(self,t,a):
  a=dict(a);self.tags.append((t,a))
  if t in ['title','h1','h2','h3','h4'] or t=='script' and a.get('type')=='application/ld+json':self.current=t;self.buf=''
 def handle_data(self,s):
  if self.current:self.buf+=s
 def handle_endtag(self,t):
  if self.current==t:
   if t=='script':self.ld.append(self.buf)
   else:self.texts[t].append(self.buf.strip())
   self.current=None
urls=[x.text for x in E.parse(R/'sitemap.xml').findall('.//{*}loc')];results=[];issues=[];titles=defaultdict(list);canon=defaultdict(list);cache={}
def path(route):
 p=R/unquote(route).lstrip('/');return p/'index.html' if p.is_dir() or route.endswith('/') else p
for url in urls:
 route=urlsplit(url).path;p=path(route);s=p.read_text();doc=Page(s);cache[p]=doc
 title=doc.texts['title'];descs=[a.get('content','') for t,a in doc.tags if t=='meta' and a.get('name')=='description'];cs=[a.get('href') for t,a in doc.tags if t=='link' and a.get('rel')=='canonical'];robots=[a.get('content','') for t,a in doc.tags if t=='meta' and a.get('name')=='robots']
 for field,ok in [('title',len(title)==1 and bool(title[0])),('description',len(descs)==1 and bool(descs[0])),('H1',len(doc.texts['h1'])==1 and bool(doc.texts['h1'][0])),('canonical',cs==[url]),('robots',robots==['index, follow'])]:
  if not ok:issues.append({'route':route,'type':field})
 titles[title[0] if title else ''].append(route)
 for c in cs:canon[c].append(route)
 for text in doc.ld:
  try:json.loads(text)
  except Exception:issues.append({'route':route,'type':'invalid JSON-LD'})
 for t,a in doc.tags:
  if t=='img' and 'alt' not in a:issues.append({'route':route,'type':'missing alt','src':a.get('src')})
  if t=='a' and a.get('href'):
   target=urlsplit(urljoin(url,a['href']))
   if target.netloc!='mrsewingfashion.com':continue
   dest=path(target.path)
   if not dest.exists():issues.append({'route':route,'type':'missing internal target','target':a['href']})
 results.append({'route':route,'title':title,'description':descs,'h1':doc.texts['h1'],'canonical':cs,'robots':robots,'jsonLdBlocks':len(doc.ld)})
for typ,groups in [('duplicate title',titles),('duplicate canonical',canon)]:
 for key,rs in groups.items():
  if len(rs)>1:issues.append({'type':typ,'value':key,'routes':rs})
headers=(R/'_headers').read_text();assert 'X-Robots-Tag: noindex, nofollow, noarchive' in headers
out={'scope':'64 sitemap-listed canonical pages, local generated staging source; excludes held/legacy/request pages from duplicate comparisons','pages':results,'issues':issues,'stagingHeaderPreserved':True,'limitations':['JSON-LD syntax checked; Google rich-result eligibility not independently verified.','Live rendering and Search Console indexing not checked; environment previously blocked pages.dev and production domains.','Internal link target files checked; server redirects, external links and remote responses not checked.']}

import argparse
parser=argparse.ArgumentParser();parser.add_argument('--report');args=parser.parse_args()
intents=json.loads((R/'_data/seo-search-intent.json').read_text())['pages']
assert {x['route'] for x in intents}=={urlsplit(u).path for u in urls},'Search-intent map must cover indexable routes exactly'
assert len({x['primaryTopic'].casefold() for x in intents})==len(intents),'Primary topics must be distinct'
if args.report:Path(args.report).write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
if issues:print(json.dumps(issues,indent=2));raise SystemExit(1)
print(f'PASS {len(results)} canonical pages: unique titles/canonicals, descriptions/H1/alt attributes, JSON-LD syntax, local internal-link targets, distinct primary topics; staging noindex header preserved. Live responses/Google indexing not verified.')
