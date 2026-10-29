#!/usr/bin/env python3
"""Validate generated route/schema/sitemap consistency without network requests."""
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import subprocess
from urllib.parse import urlparse,unquote
import xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1]
DOMAIN='https://mrsewingfashion.com'
pages=json.loads((ROOT/'_data/page-seo.json').read_text())
routes={name:'/' if name=='index.html' else '/'+name.removesuffix('.html')+'/' for name in pages}
class Tags(HTMLParser):
    def __init__(self):super().__init__();self.tags=[]
    def handle_starttag(self,t,a):self.tags.append((t,dict(a)))
for name,route in routes.items():
    path=ROOT/'index.html' if route=='/' else ROOT/route.strip('/')/'index.html'
    source=path.read_text();parser=Tags();parser.feed(source)
    assert [a['href'] for t,a in parser.tags if t=='link' and a.get('rel')=='canonical']==[DOMAIN+route],name
    for t,a in parser.tags:
        if t=='a' and a.get('href','').startswith('/'):
            href=a['href'];pathname=urlparse(href).path
            assert not pathname.endswith('.html'),(name,href)
            target=ROOT/unquote(pathname.lstrip('/'))
            assert target.exists(),(name,href)
        if t=='meta' and a.get('property')=='og:url':assert a['content']==DOMAIN+route
    for block in re.findall(r'<script[^>]*type="application/ld\+json"[^>]*>(.*?)</script>',source,re.S):
        data=json.loads(block)
        def walk(value):
            if isinstance(value,str):
                assert not re.search(re.escape(DOMAIN)+r'/[^"\s]*\.html(?:[#?]|$)',value),(name,value)
            elif isinstance(value,list):
                for child in value:walk(child)
            elif isinstance(value,dict):
                for child in value.values():walk(child)
        walk(data)
    assert 'Saturday and Sunday are closed' not in source
    assert 'Saturday &amp; Sunday: Closed' not in source
urls=[e.text for e in ET.parse(ROOT/'sitemap.xml').findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc')]
assert len(urls)==len(set(urls))==27
assert DOMAIN+'/' in urls
assert all(u in {DOMAIN+r for r in routes.values()} for u in urls)
assert all('.html' not in u for u in urls)
for name in ['booking.html','booking-adjustment.html','booking-housecall.html','booking-workplace.html','measurement-submission.html']:
    assert DOMAIN+routes[name] not in urls
business=json.loads((ROOT/'_data/business.json').read_text())
assert len(business['openingHoursSpecification'])==1
assert business['openingHoursSpecification'][0]['opens']=='09:00'
assert business['openingHoursSpecification'][0]['closes']=='17:00'
assert 'Ordinary Saturday visits do not require an appointment' in business['disambiguatingDescription']
assert 'advance appointment' in business['disambiguatingDescription']
assert 'On Umuganda (the last Saturday)' in (ROOT/'index.html').read_text()
subprocess.run(['python3','scripts/build_clean_urls.py','--check'],cwd=ROOT,check=True)
print('PASS: 32 clean canonical pages, 27 unique indexable sitemap routes, clean JSON-LD references and weekday/weekend appointment representation.')
