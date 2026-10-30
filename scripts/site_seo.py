"""Deterministic page metadata and staging indexing protection, shared by builders."""
import json,re
from pathlib import Path
from html import escape
ROOT=Path(__file__).resolve().parents[1]
DOMAIN='https://mrsewingfashion.com'
NOINDEX={'booking.html','booking-adjustment.html','booking-housecall.html','booking-workplace.html','measurement-submission.html','reviews.html','w-doublebreasted.html','w-modernsuits.html','shop.html','shop/collections.html','shop/ordering.html','loyalty-program.html','referral-program.html'}
STAGING='<script data-staging-indexing>if(location.hostname.endsWith(".pages.dev")){const m=document.querySelector(\'meta[name="robots"]\');if(m)m.content="noindex, nofollow";}</script>'
def route_for(path):
    rel=Path(path).relative_to(ROOT)
    aliases=json.loads((ROOT/'_data/route-aliases.json').read_text())
    key=rel.parent.name+'.html' if rel.name=='index.html' and rel.parent!=Path('.') else str(rel)
    if key in aliases:return aliases[key]
    if str(rel)=='index.html':return '/'
    return '/'+(str(rel.parent) if rel.name=='index.html' else str(rel.with_suffix(''))) .strip('/')+'/'
def finalize(source,path):
    route=route_for(path);name='index.html' if route=='/' else route.strip('/')+'.html'
    # These tags are regenerated, so repeated builds never duplicate them.
    source=re.sub(r'<script data-staging-indexing>.*?</script>','',source,flags=re.S)
    source=re.sub(r'<meta\b(?=[^>]*\bname=["\']robots["\'])[^>]*>','',source,flags=re.I)
    rel=Path(path).relative_to(ROOT);aliases=json.loads((ROOT/'_data/route-aliases.json').read_text())
    key=rel.parent.name+'.html' if rel.name=='index.html' and rel.parent!=Path('.') else str(rel)
    robots='noindex, follow' if name in NOINDEX or key in aliases else 'index, follow'
    # Ensure basic Open Graph coverage on all canonical documents without new claims.
    title=re.search(r'<title>(.*?)</title>',source,re.S)[1]
    desc=re.search(r'<meta\b[^>]*name=["\']description["\'][^>]*content=["\'](.*?)["\']\s*/?>',source,re.I)
    desc=desc[1] if desc else ''
    tags={'og:type':'website','og:title':title,'og:description':desc,'og:url':DOMAIN+route,'og:image':DOMAIN+'/assets/images/mr-logo-480.webp'}
    for key,value in tags.items():
        if not re.search(r'<meta\b[^>]*(?:name|property)=["\']'+re.escape(key)+'["\']',source):source=source.replace('</head>','<meta property="'+key+'" content="'+value+'"></head>',1)
    source=source.replace('</head>','<meta name="robots" content="'+robots+'">'+STAGING+'</head>',1)
    return '\n'.join(line.rstrip() for line in source.splitlines())+'\n'
