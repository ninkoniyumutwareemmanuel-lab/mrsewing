"""Temporary Shop release boundary; never change catalogue or intake contracts."""
from html import escape
import json
from pathlib import Path
import re
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]


def settings(root=ROOT):
    value = json.loads((Path(root) / '_data/shop-release.json').read_text())
    if type(value.get('publicNavigation')) is not bool or type(value.get('publicIndexing')) is not bool:
        raise ValueError('Explicit Shop navigation and indexing decisions are required')
    if value.get('productionAccess') not in ('temporary-holding', 'normal') or value.get('stagingDirectAccess') != 'development':
        raise ValueError('Unsupported Shop release state')
    return value


SHOP_ANCHOR = r'''<a\b(?=[^>]*\bhref=["'](?:https://mrsewingfashion\.com)?/shop(?:/[^"']*)?["'])[^>]*>.*?</a>'''


def public_navigation(markup, root=ROOT):
    """Remove actual anchors and their standalone list item, never CSS-hide them."""
    if settings(root)['publicNavigation']:
        return markup
    markup = re.sub(r'<li\b[^>]*>\s*' + SHOP_ANCHOR + r'\s*</li>', '', markup, flags=re.S | re.I)
    return re.sub(SHOP_ANCHOR, '', markup, flags=re.S | re.I)


def public_page_navigation(source, root=ROOT):
    """Keep legacy page navigation aligned; leave Shop's local controls intact."""
    def replace(match):
        if re.search(r'''<header\b[^>]*class=["'][^"']*\bshop-masthead\b''', match[0], re.I):
            return match[0]
        return public_navigation(match[0], root)
    return re.sub(r'<header\b[^>]*>.*?</header>|<footer\b[^>]*>.*?</footer>', replace, source, flags=re.S | re.I)


def public_indexing(root=ROOT):
    return settings(root)['publicIndexing']


def holding_page(route, root=ROOT):
    """Stable 200/noindex bookmark fallback, only in a prepared production export."""
    if settings(root)['productionAccess'] != 'temporary-holding':
        raise ValueError('Shop holding view is not the current release decision')
    parsed = urlsplit(route)
    if parsed.scheme or parsed.netloc or parsed.query or parsed.fragment or not route.startswith('/shop/') or '..' in route or '//' in route:
        raise ValueError('Expected an existing clean Shop route')
    url = 'https://mrsewingfashion.com' + route
    return ('<!doctype html><html lang="en"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        '<title>Online Shop | Mr Sewing Fashion</title>'
        '<meta name="description" content="Explore tailoring services and contact Mr Sewing Fashion while the online Shop is temporarily unavailable.">'
        '<meta name="robots" content="noindex, follow"><meta name="theme-color" content="#0b0b0c">'
        '<link rel="canonical" href="' + escape(url, quote=True) + '">'
        '<link rel="icon" href="/assets/images/favicon-192.png">'
        '<style>:root{color-scheme:dark}*{box-sizing:border-box}body{margin:0;background:#0b0b0c;color:#f1eee6;font:16px/1.6 Arial,Helvetica,sans-serif}'
        'main{width:min(680px,calc(100% - 40px));margin:clamp(36px,12vh,100px) auto}img{width:120px;height:auto;display:block;margin-bottom:40px}'
        'h1{font:400 clamp(30px,6vw,46px)/1.2 Georgia,serif}p{color:#c5c1b9;max-width:55ch}.actions{display:flex;gap:16px;flex-wrap:wrap;margin-top:28px}'
        'a{color:#d4af37;text-underline-offset:4px}a:focus-visible{outline:2px solid #d4af37;outline-offset:5px}.primary{background:#d4af37;color:#0b0b0c;padding:12px 18px;text-decoration:none;border-radius:3px;min-height:48px}'
        '.secondary{padding:12px 0;min-height:48px}</style></head><body><main>'
        '<a href="/" aria-label="Mr Sewing Fashion home"><img src="/assets/images/mr-logo-480.webp" width="480" height="309" alt="Mr Sewing Fashion"></a>'
        '<h1>Online Shop</h1><p>The online Shop is temporarily unavailable. Explore our tailoring services or contact us for assistance.</p>'
        '<div class="actions"><a class="primary" href="/services/custom-tailoring/">Tailoring &amp; Clothing Services</a>'
        '<a class="secondary" href="/contact/">Contact Us</a></div></main></body></html>\n')


def http_headers(root=ROOT):
    if public_indexing(root):
        return ''
    return '\n# Temporary Shop exclusion; public service pages remain unaffected.\n/shop\n  X-Robots-Tag: noindex, follow\n/shop/*\n  X-Robots-Tag: noindex, follow\n'
