#!/usr/bin/env python3
"""R54 PDF-only Terms reader regression tests."""
import hashlib
import json
import sys
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from terms_reader import received_version, render, CURRENT_PATH

class TermsReaderTests(unittest.TestCase):
    def test_approved_pdf_is_still_pending_activation(self):
        item=received_version()
        registry=json.loads((ROOT/'_data/policy-documents.json').read_text())['documents']['terms-and-conditions']
        self.assertIsNone(registry['currentVersion'])
        self.assertIsNone(item['effectiveDate'])
        self.assertEqual(registry['mainBaselineReview']['status'],'pending-fresh-technical-comparison')
        self.assertEqual(hashlib.sha256((ROOT/item['originalUploadPath']).read_bytes()).hexdigest(),item['sha256'])
        self.assertEqual((ROOT/item['sourcePath']).read_bytes(),(ROOT/item['publishedPath'].lstrip('/')).read_bytes())

    def test_minimal_document_reader(self):
        viewer=render()
        self.assertIn('type="application/pdf"',viewer)
        self.assertIn('Open PDF',viewer)
        self.assertIn('Download PDF',viewer)
        self.assertIn(CURRENT_PATH,viewer)
        self.assertNotIn('release-section',viewer)
        for path in ('terms-and-conditions.html','terms-and-conditions/index.html'):
            html=(ROOT/path).read_text()
            self.assertIn('terms-document-viewport',html)
            self.assertIn('terms-and-conditions/current/',html)
            self.assertNotIn('class="release-section" id="1"',html)

    def test_current_html_terms_still_accessible(self):
        html=(ROOT/'terms-and-conditions/current/index.html').read_text()
        self.assertIn('noindex',html)
        self.assertIn('Identity and scope',html)
        self.assertIn('id="1"',html)
        site=(ROOT/'scripts/customer_site.py').read_text()
        self.assertIn("link('/terms-and-conditions/current/','Terms & Conditions','')",site)
        self.assertIn("if route!='/terms-and-conditions/'",site)
        self.assertIn("location.hash",(ROOT/'_templates/terms-reader.js').read_text())

if __name__=='__main__':
    unittest.main()
