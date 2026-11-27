#!/usr/bin/env python3
"""Read-only local HTTP/canonical audit from the complete public route inventory.

The preview simulates redirects/headers. Local results never establish live
production responses or Google indexing. Evidence must stay outside the site.
"""
from __future__ import annotations
import argparse
from concurrent.futures import ThreadPoolExecutor
import json
from pathlib import Path
import sys
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin, urlsplit
from urllib.request import Request, build_opener, HTTPRedirectHandler

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from audit_customer_experience import Document

class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self,*args,**kwargs):return None

def fetch(base,path,host=None):
    opener=build_opener(NoRedirect());current=urljoin(base,path);chain=[]
    for _ in range(9):
        if urlsplit(current).netloc!=urlsplit(base).netloc:
            return {'status':'BLOCKED','chain':chain,'externalDestination':current,'scope':'External redirect target not requested'}
        try:
            request=Request(current,headers={'User-Agent':'MrSewingLocalReleaseAudit/1.0',**({'Host':host}if host else{})})
            with opener.open(request,timeout=15)as response:status=response.status;headers=dict(response.headers);body=response.read()
        except HTTPError as error:status=error.code;headers=dict(error.headers);body=error.read()
        except (URLError,TimeoutError)as error:return {'status':'FAIL','chain':chain,'error':str(error)}
        chain.append({'url':current,'status':status,'location':headers.get('Location'),'xRobotsTag':headers.get('X-Robots-Tag')})
        if status in [301,302,303,307,308]and headers.get('Location'):
            current=urljoin(current,headers['Location'])
            if any(row['url']==current for row in chain):return {'status':'FAIL','chain':chain,'error':'Redirect loop'}
            continue
        return {'status':'PASS'if status==200 else 'FAIL','httpStatus':status,'finalURL':current,'chain':chain,'headers':headers,'body':body.decode(errors='replace')}
    return {'status':'FAIL','chain':chain,'error':'More than eight redirects'}

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--inventory',required=True);parser.add_argument('--output',required=True);parser.add_argument('--base',default='http://127.0.0.1:3087');args=parser.parse_args()
    out=Path(args.output).resolve()
    if out.is_relative_to(ROOT):raise SystemExit('Keep audit evidence outside the deployable repository')
    out.mkdir(parents=True,exist_ok=True);inventory=json.loads(Path(args.inventory).read_text())
    def inspect(page):
        response=fetch(args.base,page['url'],'mrsewing-staging.pages.dev');body=response.pop('body','');doc=Document(body)
        canonical=[a.get('href')for tag,a in doc.tags if tag=='link'and'canonical'in a.get('rel','').split()]
        canonicalChecks=[]
        for target in canonical:
            u=urlsplit(target);local=fetch(args.base,u.path+('?' +u.query if u.query else''))if u.netloc=='mrsewingfashion.com'else{}
            canonicalChecks.append({'url':target,'absolute':u.scheme=='https'and bool(u.netloc),'productionDomain':u.netloc=='mrsewingfashion.com','localTargetHTTP':local.get('httpStatus'),'localRedirects':len(local.get('chain',[]))-1,'productionTargetHTTP':'BLOCKED: external origin not verified'})
        return {'route':page['url'],'purpose':page['purpose'],'http':response,'canonical':canonical,'canonicalChecks':canonicalChecks,'title':doc.texts['title'],'h1':doc.texts['h1'],'description':[a.get('content')for t,a in doc.tags if t=='meta'and a.get('name')=='description'],'robots':[a.get('content')for t,a in doc.tags if t=='meta'and a.get('name')=='robots'],'sitemapIncluded':page['sitemapIncluded'],'initialSourceFindings':page['knownProblems'],'actualGoogleIndexing':'BLOCKED: Search Console access unavailable','googleSelectedCanonical':'BLOCKED: Search Console access unavailable'}
    rows=list(ThreadPoolExecutor(max_workers=4).map(inspect,inventory['pages']))
    data={'layer':'Actual local preview HTTP and initial response HTML; redirects/headers simulated, not live Cloudflare/production','base':args.base,'pages':rows,'summary':{'routes':len(rows),'successfulHTTP':sum(r['http'].get('httpStatus')==200 for r in rows),'unexpectedHTTP':sum(r['http']['status']=='FAIL'for r in rows),'redirectLoops':sum('loop'in r['http'].get('error','').lower()for r in rows),'canonicalCount':sum(len(r['canonical'])for r in rows)}}
    (out/'http-canonical.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
    lines=['# Complete HTTP/canonical audit','',data['layer'],'','| Route | Initial/final HTTP | Canonical | Target local HTTP | Robots / sitemap | Findings |','| --- | --- | --- | --- | --- | --- |']
    for row in rows:
        chain=row['http'].get('chain',[]);status=' → '.join(str(x['status'])for x in chain);checks=row['canonicalChecks'];findings=[]
        if row['http']['status']!='PASS':findings.append(row['http'].get('error',row['http']['status']))
        if not row['canonical']:findings.append('No canonical; inspect legacy/error/fragment scope')
        for c in checks:
            if not c['absolute']or not c['productionDomain']:findings.append('Invalid canonical domain/format')
            if c['localTargetHTTP']!=200:findings.append('Canonical local target not200')
        values=[row['route'],status,', '.join(row['canonical']),', '.join(str(x['localTargetHTTP'])for x in checks),', '.join(row['robots'])+('; sitemap'if row['sitemapIncluded']else'; excluded'),'; '.join(findings)or'Local HTTP/canonical PASS; production/Google verification BLOCKED']
        lines.append('| '+' | '.join(v.replace('|','/')for v in values)+' |')
    (out/'canonical-audit.md').write_text('\n'.join(lines)+'\n');print(json.dumps(data['summary']))

if __name__=='__main__':main()
