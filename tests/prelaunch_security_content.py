#!/usr/bin/env python3
"""Unactivated production Terms export preserves the actual effective document."""
from pathlib import Path
import json
import re
import shutil
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from terms_reader import production_terms_html, received_version, render


def main_body(source):
    match = re.search(r'<main\b[^>]*>(.*?)</main>', source, re.S)
    if not match:
        raise ValueError('Main document body missing')
    return match[1]


class ProductionTermsTests(unittest.TestCase):
    def test_production_uses_current_terms_not_review_document(self):
        current = (ROOT / 'terms-and-conditions/current/index.html').read_text()
        production = production_terms_html()
        self.assertEqual(main_body(production), main_body(current))
        self.assertIn('href="https://mrsewingfashion.com/terms-and-conditions/"', production)
        self.assertIn('content="https://mrsewingfashion.com/terms-and-conditions/"', production)
        self.assertNotIn('termsPdfDialog', production)
        self.assertNotIn('/terms-and-conditions/1.2.pdf', production)
        self.assertNotIn('data-terms-pages', production)
        self.assertIn('<meta name="robots" content="noindex, follow">', production)
        for identifier in re.findall(r'\bid="([^"]+)"', current):
            self.assertIn('id="' + identifier + '"', production)
        for raw in re.findall(r'<script type="application/ld\+json">(.*?)</script>', production, re.S):
            json.loads(raw)

    def test_staging_reader_stays_real_version_1_2(self):
        self.assertEqual(received_version()['version'], '1.2')
        self.assertIn('termsPdfDialog', render())
        self.assertIn('authorized for staging review', render())
        self.assertIsNone(json.loads((ROOT / '_data/policy-documents.json').read_text())['documents']['terms-and-conditions']['currentVersion'])

    def test_activated_or_invalid_source_fails_closed(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / '_data').mkdir()
            (root / 'terms-and-conditions/current').mkdir(parents=True)
            registry = {'documents': {'terms-and-conditions': {'currentVersion': 'future'}}}
            (root / '_data/policy-documents.json').write_text(json.dumps(registry))
            shutil.copyfile(ROOT / 'terms-and-conditions/current/index.html', root / 'terms-and-conditions/current/index.html')
            with self.assertRaisesRegex(ValueError, 'Activated Terms'):
                production_terms_html(root=root)
            registry['documents']['terms-and-conditions']['currentVersion'] = None
            (root / '_data/policy-documents.json').write_text(json.dumps(registry))
            source = root / 'terms-and-conditions/current/index.html'
            source.write_text(source.read_text().replace('Identity and scope', 'Unverified replacement'))
            with self.assertRaisesRegex(ValueError, 'could not be verified'):
                production_terms_html(root=root)
        with self.assertRaisesRegex(ValueError, 'Unsupported'):
            production_terms_html(route='https://unrelated.example/terms/')


if __name__ == '__main__':
    unittest.main()
