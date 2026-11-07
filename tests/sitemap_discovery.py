"""Owner-approved public discovery; never index private/request/draft merchandise pages."""
import sys,xml.etree.ElementTree as E
from pathlib import Path
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'scripts'))
from site_seo import DOMAIN,INDEXABLE_ROUTES
from build_public_routes import public_routes,candidates
urls=[x.text for x in E.parse(R/'sitemap.xml').findall('.//{*}loc')]
assert len(urls)==len(set(urls))==55
assert set(urls)=={DOMAIN+r for r in public_routes()}
assert INDEXABLE_ROUTES.issubset(set(candidates()))
assert 'Sitemap: '+DOMAIN+'/sitemap.xml' in (R/'robots.txt').read_text()
for u in urls:
 assert u.startswith(DOMAIN+'/') and '.pages.dev' not in u
 route=u.removeprefix(DOMAIN);p=R/'index.html' if route=='/' else R/route.strip('/')/'index.html';s=p.read_text()
 assert '<link rel="canonical" href="'+u+'"' in s and 'name="robots" content="index, follow"' in s
 assert not any(x in route for x in ['/request/','/staff/','/cart/','/booking/','/special-order/'])
for p in ['request/index.html','staff/customer-requests/index.html','shop/sky-blue-elegance-suit/index.html']:
 assert 'name="robots" content="noindex' in (R/p).read_text()
assert 'X-Robots-Tag: noindex, nofollow, noarchive' in (R/'_headers').read_text()
print('PASS55uniqueXML/canonical/indexableURLs;allapprovedroutesdiscovered;productionrobots;private/request/draftproducts excluded;stagingnoindex')
