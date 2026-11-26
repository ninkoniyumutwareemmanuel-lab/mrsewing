#!/usr/bin/env python3
"""Temporary Shop navigation/indexing hold with intact development contracts."""
from pathlib import Path
import json
import re
import subprocess
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from shop_release_hold import settings, public_navigation, public_page_navigation, holding_page, http_headers
from custom_tailoring import component
from prepare_release_candidate import projection


class ShopReleasePreparationTests(unittest.TestCase):
    def test_actual_navigation_is_removed_and_hero_is_preserved(self):
        self.assertFalse(settings()['publicNavigation'])
        for source in [component('header'), component('footer'),
                       (ROOT / 'header.html').read_text(), (ROOT / 'footer.html').read_text()]:
            self.assertNotRegex(source, r'''<a\b[^>]*href=["']/shop(?:/|["'])''')
        probe = '<header><ul><li><a href="/shop/">Shop <span>More</span></a></li><li><a href="/contact/">Contact Us</a></li></ul></header>'
        self.assertEqual(public_page_navigation(probe), '<header><ul><li><a href="/contact/">Contact Us</a></li></ul></header>')
        self.assertNotIn('/shop/', public_navigation('<a class="button" href="https://mrsewingfashion.com/shop/">Shop</a>'))
        masthead = '<header class="shop-masthead"><a href="/shop/">Home</a></header>'
        self.assertEqual(public_page_navigation(masthead), masthead)
        hero = '_templates/homepage-tailoring.html'
        self.assertEqual((ROOT / hero).read_bytes(), subprocess.check_output(['git', 'show', '7808a5a1:' + hero], cwd=ROOT))

    def test_sitemap_and_all_direct_staging_pages_are_excluded(self):
        urls = [node.text for node in ET.parse(ROOT / 'sitemap.xml').findall('.//{*}loc')]
        self.assertFalse(any('/shop/' in url for url in urls))
        intents = json.loads((ROOT / '_data/seo-search-intent.json').read_text())
        held = intents['temporarilyExcludedPages']['pages']
        self.assertEqual(len(held), 7)
        self.assertTrue(all(row['route'].startswith('/shop/') for row in held))
        self.assertFalse(any(row['route'].startswith('/shop/') for row in intents['pages']))
        pages = list((ROOT / 'shop').rglob('index.html'))
        self.assertGreater(len(pages), 20)
        for path in pages:
            html = path.read_text()
            self.assertRegex(html, r'<meta name="robots" content="noindex[, ]')
        self.assertIn('/shop/*\n  X-Robots-Tag: noindex, follow', (ROOT / '_headers').read_text())
        self.assertNotIn('Disallow: /shop', (ROOT / 'robots.txt').read_text())
        self.assertIn('/shop/*', http_headers())
        excluded = {'_templates', '_data', '_media', 'scripts', 'tests', 'docs', 'functions', 'artifacts', 'node_modules'}
        for path in ROOT.rglob('*.html'):
            relative = path.relative_to(ROOT)
            if any(part.startswith('.') or part in excluded for part in relative.parts):
                continue
            source = path.read_text()
            self.assertEqual(public_page_navigation(source), source, 'Prominent Shop navigation remains: ' + str(relative))

    def test_production_uses_only_holding_views_at_existing_urls(self):
        files, _ = projection()
        existing = {str(path.relative_to(ROOT)) for path in (ROOT / 'shop').rglob('index.html')}
        self.assertTrue(existing.issubset(files))
        for name in existing:
            source = files[name].decode()
            self.assertIn('The online Shop is temporarily unavailable.', source)
            self.assertIn('name="robots" content="noindex, follow"', source)
            self.assertIn('href="https://mrsewingfashion.com/' + name.removesuffix('index.html') + '"', source)
            self.assertNotIn('<form', source)
            self.assertNotIn('data-shop-whatsapp', source)
            self.assertNotIn('data-commerce-form', source)
            self.assertNotIn('"@type":"Product"', source)
            self.assertIn('href="/services/custom-tailoring/"', source)
            self.assertIn('href="/contact/"', source)
        staged, _ = projection(mode='staging')
        self.assertIn('data-shop-whatsapp-form', staged['shop/sky-blue-elegance-suit/index.html'].decode())

    def test_existing_shop_data_and_receiving_functions_remain(self):
        for name in ['_data/shop-products.json', '_data/shop-public-enquiries.json', 'functions/api/shop-request.js',
                     'functions/_lib/shop-handler.js', 'functions/_lib/shop-runtime.js', 'functions/shop/[[path]].js']:
            self.assertEqual((ROOT / name).read_bytes(), subprocess.check_output(['git', 'show', '7808a5a1:' + name], cwd=ROOT), name)
        terms = 'terms-and-conditions/current/index.html'
        legal_body = lambda source: re.search(r'<main\b[^>]*>(.*?)</main>', source, re.S)[1]
        self.assertEqual(legal_body((ROOT / terms).read_text()), legal_body(subprocess.check_output(['git', 'show', '7808a5a1:' + terms], cwd=ROOT, text=True)))
        for route in ['https://example.invalid/shop/', '/shop/../contact/', '/shop/?a=b', '//shop/']:
            with self.assertRaises(ValueError):
                holding_page(route)
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / '_data').mkdir()
            (root / '_data/shop-release.json').write_text(json.dumps({'publicNavigation': 'false'}))
            with self.assertRaises(ValueError):
                settings(root)


if __name__ == '__main__':
    unittest.main()
