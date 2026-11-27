"""R66 staging: prevent accidental deindexing or orphaning of approved core services."""
from pathlib import Path
import re
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
DOMAIN = "https://mrsewingfashion.com"
CORE = [
    "/services/custom-tailoring/",
    "/services/alterations/",
    "/services/garment-care/",
    "/mensuits/",
    "/womensuits/",
    "/services/mobile-fitting/",
    "/services/vip/",
]
sitemap = {x.text for x in ET.parse(ROOT / "sitemap.xml").findall(".//{*}loc")}
home = (ROOT / "index.html").read_text()
hub = (ROOT / "services/custom-tailoring/index.html").read_text()

for route in CORE:
    page = (ROOT / route.strip("/") / "index.html").read_text()
    absolute = DOMAIN + route
    assert absolute in sitemap, ("missing sitemap entry", route)
    assert re.search(r'<link\s+rel="canonical"\s+href="' + re.escape(absolute) + r'"', page), ("canonical", route)
    assert re.search(r'<meta\s+name="robots"\s+content="index, follow"', page), ("noindex", route)
    assert len(re.findall(r"<title>", page)) == 1, ("title", route)
    assert len(re.findall(r'<meta\s+name="description"', page)) == 1, ("description", route)
    assert len(re.findall(r"<h1\b", page)) == 1, ("H1", route)

# Crawlers must discover core service pages through normal text links,
# not only JavaScript actions or a sitemap.
for route in CORE[:3]:
    assert 'href="' + route + '"' in home, ("homepage link", route)
for route in ("/mensuits/", "/womensuits/"):
    assert 'href="' + route + '"' in hub, ("tailoring hub category link", route)

headers = (ROOT / "_headers").read_text()
assert "https://mrsewing-staging.pages.dev/*" in headers
assert "X-Robots-Tag: noindex, nofollow, noarchive" in headers
print("PASS: 7 core service routes have sitemap, canonical, indexable production metadata, H1, and crawlable links; staging still noindex.")
