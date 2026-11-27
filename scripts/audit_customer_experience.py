#!/usr/bin/env python3
"""Read-only customer-experience inventory. Evidence stays outside the website output.

Use --revision to capture immutable initial HTML while implementation is underway.
No credential values, form hidden-field values or private record contents are collected.
"""
from __future__ import annotations
import argparse, collections, hashlib, json, re, subprocess
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit
import xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1]
VOID={'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}
SKIP={'_templates','docs','tests','artifacts','node_modules','.git','.wrangler','.github'}
DOMAIN='https://mrsewingfashion.com'
def norm(s):return ' '.join(s.split())
class Document(HTMLParser):
 def __init__(self,source):
  super().__init__(convert_charrefs=True);self.stack=[];self.tags=[];self.texts=collections.defaultdict(list);self.links=[];self.images=[];self.actions=[];self.forms=[];self.ld=[];self.visible=[];self.feed(source)
 def handle_starttag(self,tag,attrs):
  a=dict(attrs);self.tags.append((tag,a));hidden=any(f['hidden'] for f in self.stack) or tag in {'script','style'} or 'hidden' in a or a.get('aria-hidden')=='true'
  f={'tag':tag,'a':a,'text':[],'hidden':hidden}
  if tag=='img':self.images.append({k:a.get(k) for k in ['src','alt','width','height','loading','srcset']})
  if tag=='form':self.forms.append({'id':a.get('id'),'method':a.get('method'),'action':a.get('action'),'fields':[]})
  if tag in {'input','select','textarea'} and self.forms:self.forms[-1]['fields'].append({k:a.get(k) for k in ['name','id','type']}|{'required':'required' in a})
  if tag not in VOID:self.stack.append(f)
 def handle_startendtag(self,tag,attrs):self.handle_starttag(tag,attrs);self.handle_endtag(tag)
 def handle_data(self,data):
  for f in self.stack:f['text'].append(data)
  if not any(f['hidden'] for f in self.stack):self.visible.append(data)
 def handle_endtag(self,tag):
  index=next((i for i in range(len(self.stack)-1,-1,-1) if self.stack[i]['tag']==tag),None)
  if index is None:return
  f=self.stack[index];del self.stack[index:];a=f['a'];text=norm(''.join(f['text']))
  if tag in {'title','h1','h2','h3'}:self.texts[tag].append(text)
  if tag=='a' and a.get('href'):
   row={'label':text or a.get('aria-label',''),'href':a['href']};self.links.append(row)
   if not f['hidden']:self.actions.append(row|{'kind':'link'})
  if tag=='button' and not f['hidden']:self.actions.append({'label':text or a.get('aria-label',''),'kind':'button','type':a.get('type','submit')})
  if tag=='script' and a.get('type')=='application/ld+json':self.ld.append(''.join(f['text']))
def purpose(route):
 if route=='/':return 'Brand introduction and service/design discovery'
 pairs=[('/staff/','Restricted staff request application; not a public marketing destination'),('/request/','Service quotation/request and review'),('/booking','Consultation/appointment enquiry'),('/shop','Product browsing or product-specific enquiry'),('/collections/designs/','Direct garment-reference detail and selection'),('/collections/','Universal clothing Showroom'),('/mensuits/','Men’s suit collection/category browsing'),('/womensuits/','Women’s suit collection/category browsing'),('/guides/fabrics/','Text-first fabric information and context-aware selection'),('/services/custom-tailoring/selected-designs/','Selected-design review and sharing'),('/services/custom-tailoring/fabric/','Shared fabric preference'),('/services/custom-tailoring/special-order/','Special Tailoring enquiry'),('/services/custom-tailoring/','Tailoring & Clothing Services hub'),('/services/','Service information or service-specific guidance'),('/our-work/','Verified project/workmanship evidence'),('/faq/','Searchable customer questions'),('/terms-and-conditions/','Terms document review/current contractual fallback'),('/privacy','Privacy information'),('/refund','Cancellation/refund information and review'),('/about','Brand story and verified company identity'),('/contact','Verified contacts/location/hours'),('/measurements','Measurement guidance'),('/delivery','Delivery/collection policy'),('/benefits','Approved benefits/eligibility')]
 return next((p for prefix,p in pairs if route.startswith(prefix)),'Customer guidance, legacy alias or supporting route; inspect route details')
def script_types(value):
 if isinstance(value,dict):return ([value['@type']] if isinstance(value.get('@type'),str) else value.get('@type',[]))+sum((script_types(v) for v in value.values() if isinstance(v,(dict,list))),[])
 if isinstance(value,list):return sum((script_types(v) for v in value),[])
 return []
def main():
 p=argparse.ArgumentParser();p.add_argument('--revision',help='Immutable Git revision; omit for current generated tree');p.add_argument('--output',required=True);p.add_argument('--baseline',help='Prior route-inventory.json for per-route change comparison');a=p.parse_args()
 out=Path(a.output).resolve()
 if out.is_relative_to(ROOT):raise SystemExit('Evidence must be written outside the deployable repository root')
 out.mkdir(parents=True,exist_ok=True)
 def git(*args):return subprocess.check_output(['git',*args],cwd=ROOT)
 rev=git('rev-parse',a.revision or 'HEAD').decode().strip()
 names=git('ls-tree','-r','--name-only','-z',a.revision).decode().split('\0')[:-1] if a.revision else [str(x.relative_to(ROOT)) for x in ROOT.rglob('*') if x.is_file() and not any(part in SKIP for part in x.relative_to(ROOT).parts)]
 def read(name):return git('show',a.revision+':'+name).decode() if a.revision else (ROOT/name).read_text()
 def exists(name):return name in name_set
 name_set=set(names);sitemap=read('sitemap.xml');urls=[x.text for x in ET.fromstring(sitemap).findall('.//{*}loc')];sm=set(urlsplit(x).path for x in urls)
 intents={x['route']:x for x in json.loads(read('_data/seo-search-intent.json'))['pages']}
 pages=[];all_broken=[]
 for name in sorted(names):
  if not name.endswith('.html') or any(part in SKIP for part in Path(name).parts):continue
  source=read(name);doc=Document(source);route='/'+name;route=route[:-10] if route.endswith('index.html') else route
  meta=lambda key:[a.get('content','') for t,a in doc.tags if t=='meta' and a.get('name',a.get('property','')).lower()==key]
  canonical=[x.get('href') for t,x in doc.tags if t=='link' and 'canonical' in x.get('rel','').split()]
  visible=norm(' '.join(doc.visible));aliases=bool(re.search(r'<meta[^>]+http-equiv=["\']refresh',source,re.I))
  schema=[];invalid=0
  for text in doc.ld:
   try:schema+=script_types(json.loads(text))
   except (ValueError,TypeError):invalid+=1
  broken=[]
  for item in doc.links:
   u=urlsplit(urljoin(DOMAIN+route,item['href']))
   if u.netloc!='mrsewingfashion.com':continue
   dest=unquote(u.path).lstrip('/');dest='index.html' if not dest else dest+'index.html' if dest.endswith('/') else dest
   if not exists(dest) and not exists(dest+'/index.html') and not u.path.startswith('/api/'):
    broken.append(item['href']);all_broken.append({'route':route,'href':item['href']})
  problems=[]
  if len(doc.texts['h1'])!=1 and not aliases:problems.append('H1 count is '+str(len(doc.texts['h1']))+'; review intended legacy/error-page scope')
  if not doc.texts['title']:problems.append('Missing title')
  if not meta('description'):problems.append('Missing description; review alias/private-page scope')
  if not canonical:problems.append('Missing canonical; review alias/private-page scope')
  if invalid:problems.append('Invalid JSON-LD syntax')
  if any(x['alt'] is None for x in doc.images):problems.append('Image missing alt attribute')
  refs=sorted(set(re.findall(r'\b(?:Reference\s+)?MS-\d{3}\b',visible,re.I)))
  if refs:problems.append('Visible technical design identifier(s): '+str(len(refs)))
  if broken:problems.append('Unresolved static local targets; may include intentional dynamic/redirect destinations')
  if 'VIP Subscription' in visible:problems.append('Unfinished VIP subscription presentation requires review')
  pages.append({'file':name,'url':route,'purpose':purpose(route),'initialTitle':doc.texts['title'],'h1':doc.texts['h1'],'h2':doc.texts['h2'],'description':meta('description'),'canonical':canonical,'robots':meta('robots'),'stagingRuntimeNoindexPresent':'data-staging-indexing' in source,'sitemapIncluded':route in sm,'primaryKeyword':intents.get(route,{}).get('primaryTopic'),'supportingKeywords':intents.get(route,{}).get('secondaryTopics',[]),'actions':doc.actions,'importantContentExcerpt':visible[:900],'internalLinks':[x for x in doc.links if not urlsplit(x['href']).netloc or urlsplit(x['href']).netloc=='mrsewingfashion.com'],'externalLinks':[x for x in doc.links if urlsplit(x['href']).netloc and urlsplit(x['href']).netloc!='mrsewingfashion.com'],'openGraph':{k:meta(k) for k in ['og:title','og:description','og:image','og:url','og:type','twitter:card']},'structuredDataTypes':sorted(set(schema)),'invalidStructuredDataBlocks':invalid,'images':doc.images,'forms':doc.forms,'visibleTechnicalDesignReferenceCount':len(refs),'aliasOrRefresh':aliases,'htmlBytes':len(source.encode()),'visibleWordCount':len(visible.split()),'knownProblems':problems,'proposedCorrections':['Review actual customer purpose, preserve existing routes/backend and apply approved scoped changes'] if problems else [],'mobileUsability':'NOT TESTED in static inventory; see browser evidence','actualGoogleIndexing':'BLOCKED: no Search Console access','initialHttpStatus':'NOT TESTED: static source is not HTTP verification'})
 report={'date':'2026-11-26','baselineCommit':rev,'mode':'immutable Git source' if a.revision else 'current generated working tree','pageCount':len(pages),'sitemapRouteCount':len(sm),'importantLimit':'Source inventory does not establish deployed HTTP status, browser usability, actual indexing, remote analytics delivery or legal compliance. Aliases are intentionally inventoried separately.','sourceBoundary':'Internal audit evidence is outside the deployment root; scripts/docs paths denied on staging by Pages middleware.','pages':pages,'staticUnresolvedLinks':all_broken,'robotsTxt':read('robots.txt'),'headers':read('_headers')}
 (out/'route-inventory.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
 lines=['# Customer-experience route inventory — 26 November 2026','',f'Commit `{rev}`. {len(pages)} generated HTML routes (aliases included), {len(sm)} sitemap canonical routes.','', 'Static source only. Browser and deployed-origin verification are separate; Google indexing is unverified.','', '| Route | Purpose | Title / H1 | Canonical | Robots / sitemap | Initial findings |','| --- | --- | --- | --- | --- | --- |']
 esc=lambda s:str(s).replace('|',' / ').replace('\n',' ')
 for row in pages:lines.append('| '+' | '.join(esc(x) for x in [row['url'],row['purpose'],' / '.join(row['initialTitle']+row['h1']),' / '.join(row['canonical']),' / '.join(row['robots'])+('; sitemap' if row['sitemapIncluded'] else '; excluded'),'; '.join(row['knownProblems']) or 'No automated source issue; interaction review still required'])+' |')
 (out/'route-inventory.md').write_text('\n'.join(lines)+'\n')
 seo=[{'url':x['url'],'primaryKeyword':x['primaryKeyword'],'supportingKeywords':x['supportingKeywords'],'title':x['initialTitle'],'description':x['description'],'h1':x['h1'],'canonical':x['canonical'],'robots':x['robots'],'sitemapIncluded':x['sitemapIncluded'],'structuredDataTypes':x['structuredDataTypes'],'imageCount':len(x['images']),'missingAltCount':sum(y['alt'] is None for y in x['images']),'internalLinks':x['internalLinks'],'actualGoogleIndexing':x['actualGoogleIndexing']} for x in pages if x['sitemapIncluded'] or x['url'] in ['/collections/','/guides/fabrics/','/our-work/'] or x['url'].startswith('/guides/fabrics/')]
 (out/'seo-page-map.json').write_text(json.dumps(seo,ensure_ascii=False,indent=2)+'\n')
 (out/'three-tailoring-pages.json').write_text(json.dumps([x for x in seo if x['url'] in ['/services/custom-tailoring/','/mensuits/','/womensuits/']],ensure_ascii=False,indent=2)+'\n')
 if a.baseline:
  old=json.loads(Path(a.baseline).read_text());prior={x['url']:x for x in old['pages']};changes=[]
  for row in pages:
   before=prior.pop(row['url'],None)
   fields=['initialTitle','h1','h2','description','canonical','robots','sitemapIncluded','actions','images','forms','structuredDataTypes','visibleTechnicalDesignReferenceCount','htmlBytes']
   changed=[k for k in fields if before is None or before.get(k)!=row.get(k)]
   changes.append({'url':row['url'],'purpose':row['purpose'],'initialProblems':before.get('knownProblems',[]) if before else ['New route'],'changedFields':changed,'finalSourceProblems':row['knownProblems'],'sourceStatus':'PASS' if not row['knownProblems'] else 'NOT TESTED','browserStatus':'NOT TESTED here; use final browser evidence','note':'Static source validation is not functionality, deployed-origin or Google-indexing verification.'})
  for route,before in prior.items():changes.append({'url':route,'purpose':before['purpose'],'initialProblems':before['knownProblems'],'changedFields':['route removed or no longer represented in generated HTML'],'sourceStatus':'NOT TESTED','browserStatus':'NOT TESTED'})
  (out/'route-changes.json').write_text(json.dumps({'baselineCommit':old['baselineCommit'],'finalRecordedCommit':rev,'changes':changes},ensure_ascii=False,indent=2)+'\n')
  table=['# Per-route change reconciliation','', '| Route | Initial findings | Changed fields | Final static findings / status |','| --- | --- | --- | --- |']
  for x in changes:table.append('| '+' | '.join(esc(y) for y in [x['url'],'; '.join(x['initialProblems']) or 'No automated source issue','; '.join(x['changedFields']) or 'Preserved','; '.join(x.get('finalSourceProblems',[])) or x['sourceStatus']])+' |')
  (out/'route-changes.md').write_text('\n'.join(table)+'\n')
 summary={'pages':len(pages),'sitemapPages':len(sm),'visibleReferencePages':sum(x['visibleTechnicalDesignReferenceCount']>0 for x in pages),'sourceIssues':sum(bool(x['knownProblems']) for x in pages),'staticUnresolvedLinks':len(all_broken),'schemaSyntaxFailures':sum(x['invalidStructuredDataBlocks'] for x in pages),'output':str(out)}
 print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
