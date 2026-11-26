#!/usr/bin/env python3
"""Prepare a public-only release artifact outside the checkout; never deploy it.

Existing Git-connected staging builds remain unchanged. The public directory is
safe for a static host; runtime/functions is a separate private build input for
the authorized Pages API deployment. It must never be uploaded as static assets.
"""
from __future__ import annotations
import argparse
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import subprocess
from urllib.parse import unquote, urlsplit, urljoin

ROOT=Path(__file__).resolve().parents[1]
INTERNAL={'_data','_templates','_media','scripts','tests','docs','functions','.github','.git','.agents','.codex','.aws','staff','artifacts','node_modules','.wrangler'}
FRAGMENTS={'header.html','footer.html','hero.html','why-mtm.html'}
DOMAIN='mrsewingfashion.com'

def path_for(raw, relative, root):
    raw=raw.strip()
    if not raw or raw.startswith(('#','data:','blob:','javascript:','tel:','mailto:')):return None
    u=urlsplit(raw)
    if u.netloc and u.netloc!=DOMAIN:return None
    if u.scheme and u.scheme not in ('http','https'):return None
    value=unquote(u.path)
    if not value:return None
    path=(root/value.lstrip('/')) if value.startswith('/') else (root/relative).parent/value
    path=path.resolve()
    if not path.is_relative_to(root.resolve()):raise ValueError('Asset escapes website root')
    rel=path.relative_to(root.resolve())
    if any(part.startswith('.') or part in INTERNAL for part in rel.parts):return None
    if path.is_dir():return None
    return rel

class References(HTMLParser):
    def __init__(self):super().__init__(convert_charrefs=True);self.paths=[];self.base=None
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        if tag=='base'and a.get('href'):self.base=a['href']
        for key in ('src','href','poster'):
            if a.get(key):self.paths.append(a[key])
        if a.get('srcset'):
            self.paths.extend(item.strip().split()[0] for item in a['srcset'].split(',') if item.strip())
    handle_startendtag=handle_starttag

def projection(root=ROOT, mode='production'):
    root=Path(root).resolve();out={};excluded=[]
    for p in root.rglob('*.html'):
        rel=p.relative_to(root)
        if any(part in INTERNAL or part.startswith('.') for part in rel.parts)or str(rel)in FRAGMENTS:continue
        out[str(rel)]=p.read_bytes()
    if mode=='production':
        from terms_reader import production_terms_html
        for name in ('terms-and-conditions/index.html','terms-and-conditions.html'):
            if name in out:out[name]=production_terms_html(root=root).encode()
        from shop_release_hold import holding_page, settings as shop_release_settings
        if shop_release_settings(root)['productionAccess']=='temporary-holding':
            for name in list(out):
                if name.startswith('shop/')and name.endswith('/index.html'):
                    out[name]=holding_page('/'+name.removesuffix('index.html'),root=root).encode()
    elif mode!='staging':raise ValueError('Unsupported candidate mode')
    for name in ('robots.txt','sitemap.xml','favicon.ico','favicon-16x16.png','favicon-32x32.png','apple-touch-icon.png','site.webmanifest','build-info.json','_headers','_redirects'):
        p=root/name
        if p.is_file():out[name]=p.read_bytes()
    if mode=='production'and'_redirects'in out:
        # Held, unpublished media has no equivalent public replacement. Retain
        # genuine page aliases, but let omitted media return404 rather than302to200.
        text=out['_redirects'].decode().split('# Staging-only R59 held')[0]
        out['_redirects']=text.encode()
    out['.nojekyll']=b''
    queued=list(out);visited=set();missing=[]
    while queued:
        name=queued.pop()
        if name in visited:continue
        visited.add(name)
        if Path(name).suffix.lower()not in ('.html','.css','.js','.mjs','.json','.webmanifest'):continue
        text=out[name].decode(errors='replace');strong=[]
        if name.endswith('.html'):
            doc=References();doc.feed(text)
            base=urljoin('https://'+DOMAIN+'/'+name,doc.base or '')
            strong=[urljoin(base,raw)for raw in doc.paths]
            css=re.sub(r'<script\b.*?</script>','',text,flags=re.S|re.I)
            strong.extend(urljoin(base,raw)for raw in re.findall(r'url\(\s*[\"\']?([^\)\"\']+)',css,re.I))
            strong.extend(urljoin(base,raw)for raw in re.findall(r'''\bfetch\(\s*["']([^"']+)["']''',text))
        elif name.endswith('.css'):
            strong.extend(re.findall(r'url\(\s*[\"\']?([^\)\"\']+)',text,re.I))
        # Embedded catalogue JSON and script-loaded assets must retain exact
        # original photographs. Missing constructed/prefix strings aren't files.
        literals=re.findall(r'''["']((?:https://mrsewingfashion\.com)?/[^"'<>\s]+\.(?:avif|webp|jpe?g|png|gif|svg|ico|mp4|webm|woff2?|ttf|css|js|json|pdf)(?:\?[^"'<>]*)?)["']''',text,re.I)
        for raw,required in [(x,True)for x in strong]+[(x,False)for x in literals]:
            rel=path_for(raw,name,root)
            if rel is None:continue
            target=root/rel;key=str(rel)
            if target.suffix.lower()=='.html'and key not in FRAGMENTS:continue  # Public pages were seeded; fragments can be required runtime assets.
            if mode=='production'and(key.startswith('assets/policy-documents/')or key.lower().endswith('.pdf')):
                if required:raise ValueError('Unactivated document referenced by production candidate: '+key)
                excluded.append(key);continue
            if not target.is_file():
                if required and not key.startswith('api/'):missing.append({'from':name,'path':key})
                continue
            if key not in out:out[key]=target.read_bytes();queued.append(key)
    if missing:raise ValueError('Missing public asset references: '+json.dumps(missing[:20]))
    for name in out:
        if name!='.nojekyll'and any(part in INTERNAL or part.startswith('.')for part in Path(name).parts):raise ValueError('Internal source reached public artifact: '+name)
    return out,sorted(set(excluded))

def prepare(output,mode='production',root=ROOT,check=False):
    root=Path(root).resolve();output=Path(output).resolve()
    if output.is_relative_to(root):raise ValueError('Candidate must be outside the deployed checkout')
    files,excluded=projection(root,mode);public=output/'public'
    runtime_files={str(p.relative_to(root)):p.read_bytes()for directory in ('functions','scripts/edge')for p in (root/directory).rglob('*')if p.is_file()and p.suffix in ('.js','.mjs','.json')}
    if check:
        actual={str(p.relative_to(public)):p.read_bytes()for p in public.rglob('*')if p.is_file()}
        if actual!=files:raise ValueError('Candidate differs from current approved projection')
        actual_runtime={str(p.relative_to(output/'runtime')):p.read_bytes()for p in (output/'runtime').rglob('*')if p.is_file()}
        if actual_runtime!=runtime_files:raise ValueError('Runtime compiler inputs differ from the reviewed source')
        return json.loads((output/'manifest.json').read_text())
    if output.exists()and any(output.iterdir()):raise ValueError('Preserve existing candidates; choose a fresh output directory')
    public.mkdir(parents=True,exist_ok=True)
    for name,value in files.items():
        target=public/name;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(value)
    runtime=[]
    for rel,value in sorted(runtime_files.items()):
        target=output/'runtime'/rel;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(value);runtime.append(rel)
    try:commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True,stderr=subprocess.DEVNULL).strip();dirty=bool(subprocess.check_output(['git','status','--porcelain'],cwd=root,text=True).strip())
    except subprocess.CalledProcessError:commit=None;dirty=None
    manifest={'mode':mode,'sourceCommit':commit,'sourceWorkingTreeDirty':dirty,'deploymentPerformed':False,'publicFiles':{name:{'bytes':len(value),'sha256':hashlib.sha256(value).hexdigest()}for name,value in sorted(files.items())},'runtimeBuildInputs':runtime,'runtimeWarning':'runtime/ is private compiler input, never upload it as public static files. Compatible Pages API and binding verification is a separate release gate.','excludedUnactivatedDocuments':excluded,'termsStatus':'Preserved current effective HTML; no review PDF activation'if mode=='production'else'Existing staging review reader retained','headersStatus':'Host-specific staging noindex preserved; no production-wide noindex added'}
    (output/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n');return manifest

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',required=True);p.add_argument('--mode',choices=['production','staging'],default='production');p.add_argument('--check',action='store_true');a=p.parse_args()
    result=prepare(a.output,a.mode,check=a.check);print(json.dumps({'mode':result['mode'],'publicFiles':len(result['publicFiles']),'runtimeBuildInputs':len(result['runtimeBuildInputs']),'deploymentPerformed':False,'sourceCommit':result['sourceCommit']}))

if __name__=='__main__':main()
