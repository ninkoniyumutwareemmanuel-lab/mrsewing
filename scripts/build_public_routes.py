#!/usr/bin/env python3
"""Generate canonical production sitemap, exact redirects and staging HTTP noindex rules."""
import argparse,json,re
from html.parser import HTMLParser
from html import unescape
from pathlib import Path
from site_seo import ROOT,DOMAIN,NOINDEX
from build_journey import services,projects
from garment_care import catalog as care_catalog
from build_completion import routes as completion_routes
from build_collections import load,design_route
from faq_help import routes as faq_routes

def candidates():
    aliases=json.loads((ROOT/'_data/route-aliases.json').read_text())
    original=[aliases.get(n,'/' if n=='index.html' else '/'+n[:-5]+'/') for n in json.loads((ROOT/'_data/page-seo.json').read_text())]
    return list(dict.fromkeys(original+['/our-work/']+[s['route'] for s in services()]+[design_route(d) for d in load()[0]]+['/our-work/'+p['slug']+'/' for p in projects()]+['/services/garment-care/'+c['slug']+'/' for c in care_catalog()[1]]+completion_routes()+faq_routes()))

def public_routes():
    routes=[];titles=set();descs=set()
    for route in candidates():
        path=ROOT/'index.html' if route=='/' else ROOT/route.strip('/')/'index.html';assert path.is_file(),route
        source=path.read_text();canonical=re.findall(r'<link\b[^>]*rel="canonical"[^>]*href="([^"]+)"',source)
        assert canonical==[DOMAIN+route],(route,canonical)
        if re.search(r'<meta\b[^>]*name="robots"[^>]*content="[^"]*noindex',source):continue
        title=unescape(re.search(r'<title>(.*?)</title>',source,re.S)[1]);desc=unescape(re.search(r'<meta\b[^>]*name="description"[^>]*content="([^"]+)"',source)[1])
        assert title and title not in titles,('duplicate title',route,title);titles.add(title)
        assert desc and desc not in descs,('duplicate description',route);descs.add(desc)
        assert len(re.findall(r'<h1\b',source))==1,route
        routes.append(route)
    return routes

def outputs():
    routes=public_routes();sitemap='<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join('  <url><loc>'+DOMAIN+r+'</loc></url>\n' for r in routes)+'</urlset>\n'
    aliases=json.loads((ROOT/'_data/route-aliases.json').read_text())
    redirects='# Generated exact aliases. Cloudflare Pages preserves query strings.\n'+'\n'.join('/'+name+' '+aliases.get(name,'/' if name=='index.html' else '/'+name[:-5]+'/')+' 301' for name in json.loads((ROOT/'_data/page-seo.json').read_text()))+'\n/views.html /our-work/ 301\n/views/ /our-work/ 301\n/views /our-work/ 301\n/our-work.html /our-work/ 301\n'
    redirects+=''.join('/'+name[:-5]+'/ '+target+' 301\n/'+name[:-5]+' '+target+' 301\n' for name,target in aliases.items())
    redirects+='/happy-customers.html /our-work/ 301\n/happy-customers /our-work/ 301\n'
    headers='# Staging only: never apply these noindex rules to the production hostname.\nhttps://mrsewing-staging.pages.dev/*\n  X-Robots-Tag: noindex, nofollow, noarchive\nhttps://:preview.mrsewing-staging.pages.dev/*\n  X-Robots-Tag: noindex, nofollow, noarchive\n'
    alias='<head><meta charset="utf-8"><meta name="robots" content="noindex, follow"><link rel="canonical" href="'+DOMAIN+'/our-work/"><meta http-equiv="refresh" content="0;url=/our-work/"><title>Our Work | Mr Sewing Fashion</title><script>location.replace("/our-work/"+location.search+location.hash)</script></head><body><a href="/our-work/">Continue to Our Work</a></body>\n'
    return {ROOT/'sitemap.xml':sitemap,ROOT/'_redirects':redirects,ROOT/'_headers':headers,ROOT/'views.html':alias,ROOT/'views/index.html':alias,ROOT/'robots.txt':'User-agent: *\nAllow: /\n\nSitemap: '+DOMAIN+'/sitemap.xml\n'}

def main():
    p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');a=p.parse_args()
    for path,value in outputs().items():
        if a.check:
            if not path.exists() or path.read_text()!=value:raise SystemExit('Stale public routes output: '+str(path.relative_to(ROOT)))
        else:path.parent.mkdir(parents=True,exist_ok=True);path.write_text(value)
    print(f'PASS: {len(public_routes())} canonical indexable routes, exact legacy redirects and staging noindex rules '+('synchronized.' if a.check else 'generated.'))
if __name__=='__main__':main()
