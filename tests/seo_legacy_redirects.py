"""R66 staging regression: legacy URL fallback signals and canonical pages stay distinct."""
from html import unescape
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
DOMAIN = "https://mrsewingfashion.com"
aliases = json.loads((ROOT / "_data/route-aliases.json").read_text())
pages = json.loads((ROOT / "_data/page-seo.json").read_text())
assert "index.html" in pages
assert 'data-legacy-canonical-redirect' not in (ROOT / "index.html").read_text()

tested = 0
for name in pages:
    if name == "index.html":
        continue  # The root index file is also served at /; never redirect it.
    target = aliases.get(name, "/" + name.removesuffix(".html") + "/")
    legacy = (ROOT / name).read_text()
    clean = (ROOT / name.removesuffix(".html") / "index.html").read_text()
    tags = re.findall(r'<meta\s+data-legacy-canonical-redirect\b[^>]*>', legacy, flags=re.I)
    assert len(tags) == 1, (name, "missing/duplicate legacy redirect")
    match = re.search(r'http-equiv="refresh"\s+content="0;url=([^"]+)"', tags[0], re.I)
    assert match and unescape(match[1]) == target, (name, "wrong redirect", tags[0], target)
    assert 'data-legacy-canonical-redirect' not in clean, (name, "canonical redirects to itself")
    canonical = '<link rel="canonical" href="' + DOMAIN + target + '"'
    assert canonical in legacy, (name, "legacy canonical mismatch")
    assert canonical in clean, (name, "clean canonical mismatch")
    tested += 1

headers = (ROOT / "_headers").read_text()
assert "https://mrsewing-staging.pages.dev/*" in headers
assert "X-Robots-Tag: noindex, nofollow, noarchive" in headers
print("PASS:", tested, "legacy .html redirects; canonical copies safe; staging noindex config retained.")
