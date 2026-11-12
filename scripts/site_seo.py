"""Deterministic page metadata and staging indexing protection, shared by builders."""
import json,re
from pathlib import Path
from html import escape
from project_catalog import projects as approved_projects
from shop_catalog import load as shop_products, route as shop_product_route, categories as shop_categories, category_route
ROOT=Path(__file__).resolve().parents[1]
DOMAIN='https://mrsewingfashion.com'
NOINDEX={'collections.html','whatsapp.html','services/custom-tailoring/fabric.html','services/vip/subscription.html','request.html','services/custom-tailoring/design-choice.html','services/custom-tailoring/standard-order.html','services/custom-tailoring/special-order.html','booking.html','booking-adjustment.html','booking-housecall.html','booking-workplace.html','measurement-submission.html','reviews.html','w-doublebreasted.html','w-modernsuits.html','shop.html'}
# Public browsing destinations explicitly requested for sitemap discovery,7Nov2026.
# Use shared approved reference/category records; never include request or draft-product routes.
_reference_model=json.loads((ROOT/'_data/suit-reference-categories.json').read_text())
_reference_ids={ident for c in _reference_model['categories'] for ident in c['designIds']}
_design_records=json.loads((ROOT/'_data/collection-designs.json').read_text())['designs']
_public_reference_routes={ '/collections/designs/'+d['slug']+'/' for d in _design_records if d['published'] and d['id'] in _reference_ids }
from public_enquiries import approved as _approved_enquiries
_public_shop_categories={category_route(c) for c in sorted({p['category'] for p in _approved_enquiries()})}
INDEXABLE_ROUTES = {
    *_public_reference_routes,
    *[c['route'] for c in _reference_model['categories'] if c['designIds']],
    *_public_shop_categories,
    '/',
    '/services/custom-tailoring/',
    '/services/alterations/',
    '/services/garment-care/',
    '/services/mobile-fitting/',
    '/services/vip/',
    '/our-work/',
    *['/our-work/'+p['slug']+'/' for p in approved_projects()],
    '/about/',
    '/contact/',
    '/faq/',
    '/guides/fabrics/',
    '/mensuits/',
    '/womensuits/',
    '/measurements/',
    '/loyalty-program/', '/referral-program/', '/shop/',
    *[shop_product_route(p) for p in shop_products()],
    *[category_route(c) for c in shop_categories()],
}
STAGING='<script data-staging-indexing>if(location.hostname.endsWith(".pages.dev")){const m=document.querySelector(\'meta[name="robots"]\');if(m)m.content="noindex, nofollow";}</script>'
def route_for(path):
    rel=Path(path).relative_to(ROOT)
    aliases=json.loads((ROOT/'_data/route-aliases.json').read_text())
    key=rel.parent.name+'.html' if rel.name=='index.html' and rel.parent!=Path('.') else str(rel)
    if key in aliases:return aliases[key]
    if str(rel)=='index.html':return '/'
    return '/'+(str(rel.parent) if rel.name=='index.html' else str(rel.with_suffix(''))) .strip('/')+'/'
def finalize(source,path):
    route=route_for(path)
    override=json.loads((ROOT/'_data/public-page-seo.json').read_text()).get(route)
    if override:
        from sync_page_seo import apply
        source=apply(source,override)
    name='index.html' if route=='/' else route.strip('/')+'.html'
    # These tags are regenerated, so repeated builds never duplicate them.
    source=re.sub(r'<script src="/assets/public-api[.]js[^"]*" defer></script>','',source)
    if 'customerRequestForm' in source or 'data-commerce-form' in source or 'shopData' in source:source=source.replace('</head>','<script src="/assets/public-api.js?v=staging-r32" defer></script></head>',1)
    source=source.replace('src="/assets/faq-help.js"','src="/assets/faq-help.js?v=staging-r32"').replace('src="/assets/faq-actions.js"','src="/assets/faq-actions.js?v=staging-r32"').replace('src="/assets/request-context.js"','src="/assets/request-context.js?v=staging-r32"').replace('src="/assets/customer-site.js"','src="/assets/customer-site.js?v=staging-r32"').replace('src="/assets/commerce.js"','src="/assets/commerce.js?v=staging-r32"').replace('src="/assets/homepage.js"','src="/assets/homepage.js?v=mobile-motion-r24"')
    source=re.sub(r'<script id="designSelectionData".*?</script>|<script src="/assets/design-selections.js[^"]*" defer></script>|<link rel="stylesheet" href="/assets/design-selections.css[^\"]*">','',source,flags=re.S)
    if route.startswith(('/mensuits/','/womensuits/','/collections/designs/','/services/custom-tailoring/','/request/','/our-work/','/guides/fabrics/')):
        refs=json.loads((ROOT/'_data/request-reference-allowlist.json').read_text());slugs={d['id']:d['slug'] for d in json.loads((ROOT/'_data/collection-designs.json').read_text())['designs']}
        for id,d in refs.items():d['id']=id;d['route']='/collections/designs/'+slugs[id]+'/'
        from customer_policies import facts as _facts
        fabrics={f['id']:f for f in json.loads((ROOT/'_data/fabric-reference-catalogue.json').read_text())['fabrics']}
        selection_data={'designs':refs,'projects':json.loads((ROOT/'_data/portfolio-request-allowlist.json').read_text()),'fabrics':fabrics}
        source=source.replace('</head>','<script id="designSelectionData" type="application/json">'+json.dumps(selection_data,ensure_ascii=False).replace('<','\\u003c')+'</script><script src="/assets/design-selections.js?v=staging-r43" defer></script><link rel="stylesheet" href="/assets/design-selections.css?v=staging-r43"></head>',1)
    source=re.sub(r'<script data-staging-indexing>.*?</script>','',source,flags=re.S)
    source=re.sub(r'<meta\b(?=[^>]*\bname=["\']robots["\'])[^>]*>','',source,flags=re.I)
    rel=Path(path).relative_to(ROOT);aliases=json.loads((ROOT/'_data/route-aliases.json').read_text())
    key=rel.parent.name+'.html' if rel.name=='index.html' and rel.parent!=Path('.') else str(rel)
    robots='index, follow' if route in INDEXABLE_ROUTES and key not in aliases and 'data-publication-hold' not in source else 'noindex, follow'
    # Ensure basic Open Graph coverage on all canonical documents without new claims.
    title=re.search(r'<title>(.*?)</title>',source,re.S)[1]
    desc=re.search(r'<meta\b[^>]*name=["\']description["\'][^>]*content=["\'](.*?)["\']\s*/?>',source,re.I)
    desc=desc[1] if desc else ''
    tags={'og:type':'website','og:title':title,'og:description':desc,'og:url':DOMAIN+route,'og:image':DOMAIN+'/assets/images/mr-logo-480.webp'}
    for key,value in tags.items():
        if not re.search(r'<meta\b[^>]*(?:name|property)=["\']'+re.escape(key)+'["\']',source):source=source.replace('</head>','<meta property="'+key+'" content="'+value+'"></head>',1)
    source=source.replace('</head>','<meta name="robots" content="'+robots+'">'+STAGING+'</head>',1)
    from whatsapp_consent import protect
    source=protect(source)
    source=re.sub(r'<script src="/assets/customer-interactions.js" defer></script>|<link rel="stylesheet" href="/assets/customer-interactions.css">','',source)
    source=source.replace('</head>','<link rel="stylesheet" href="/assets/customer-interactions.css"><script src="/assets/customer-interactions.js" defer></script></head>',1)
    return '\n'.join(line.rstrip() for line in source.splitlines())+'\n'
