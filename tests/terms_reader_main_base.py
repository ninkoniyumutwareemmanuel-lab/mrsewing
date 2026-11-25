#!/usr/bin/env python3
"""Real PDF images, full-screen reader and protected unactivated Terms consent."""
import hashlib
import json
import re
import sys
from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from terms_reader import received_version,render,CURRENT_PATH,page_url,page_manifest

class TermsReaderTests(unittest.TestCase):
    def test_approved_pdf_unactivated(self):
        entry=received_version()
        registry=json.loads((ROOT/'_data/policy-documents.json').read_text())['documents']['terms-and-conditions']
        self.assertIsNone(registry['currentVersion'])
        self.assertIsNone(entry['effectiveDate'])
        self.assertEqual(registry['mainBaselineReview']['status'],'pending-fresh-technical-comparison')
        self.assertEqual(hashlib.sha256((ROOT/entry['originalUploadPath']).read_bytes()).hexdigest(),entry['sha256'])
        self.assertEqual((ROOT/entry['sourcePath']).read_bytes(),(ROOT/entry['publishedPath'].lstrip('/')).read_bytes())
        self.assertEqual(entry['version'],'1.2')
        self.assertEqual(entry['approvalStatus'],'approved-for-staging-review')
        self.assertEqual(entry['technicalInspection']['numberedSections'],20)
        old=registry['receivedVersions'][0]
        self.assertEqual(old['version'],'1.0')
        self.assertEqual(old['sha256'],'9b35d9384cf4d06dec88e92cfcde4c30d687ea1b126b6e0a8164784f5ee057c0')
        for field in ('originalUploadPath','sourcePath','publishedPath'):
            self.assertEqual(hashlib.sha256((ROOT/old[field].lstrip('/')).read_bytes()).hexdigest(),old['sha256'])

    def test_fullscreen_dialog_not_native_pdf_object(self):
        html=render()
        self.assertIn('<dialog id="termsPdfDialog"',html)
        self.assertIn('aria-label="Close PDF reader"',html)
        self.assertIn('data-terms-scroll',html)
        self.assertIn('data-terms-zoom-in',html)
        self.assertIn('data-terms-zoom-out',html)
        self.assertIn('download=',html)
        self.assertIn('Open the staging-review PDF in a new tab',html)
        self.assertIn('Version 1.2',html)
        self.assertIn('v1.2_Staging_Review.pdf',html)
        self.assertNotIn('v1.1_Approved.pdf',html)
        self.assertEqual(html.count('class="terms-popup-page"'),received_version()['technicalInspection']['pages'])
        self.assertNotIn('<object',html)
        self.assertNotIn('This browser cannot display',html)
        self.assertNotIn('Read the current online Terms',html)
        self.assertNotIn('release-section',html)
        for index in range(1,received_version()['technicalInspection']['pages']+1):
            self.assertIn(page_url(received_version(),index),html)
        for path in ('terms-and-conditions.html','terms-and-conditions/index.html'):
            document=(ROOT/path).read_text()
            self.assertIn('<dialog id="termsPdfDialog"',document)
            self.assertIn('class="terms-popup-page"',document)
            self.assertNotIn('This browser cannot display',document)
            self.assertNotIn('class="release-section" id="1"',document)

    def test_pdf_image_manifest_and_png_integrity(self):
        entry=received_version()
        path=ROOT/'assets/policy-documents/terms-and-conditions/pages/manifest.json'
        manifest=json.loads(path.read_text())
        self.assertEqual(manifest,page_manifest(entry))
        self.assertEqual(manifest['sourcePdfSha256'],entry['sha256'])
        self.assertEqual(manifest['effectiveDate'],None)
        self.assertEqual(manifest['publicationStatus'],'staging-review')
        self.assertEqual(len(manifest['pages']),entry['technicalInspection']['pages'])
        for index,item in enumerate(manifest['pages'],1):
            self.assertEqual(item['page'],index)
            self.assertEqual(item['path'],page_url(entry,index))
            raw=(ROOT/item['path'].lstrip('/')).read_bytes()
            self.assertTrue(raw.startswith(b'\x89PNG\r\n\x1a\n'))
            self.assertEqual(hashlib.sha256(raw).hexdigest(),item['sha256'])
            self.assertEqual(item['width'],1360)
            self.assertTrue(1000<=item['height']<=2400)
            if entry['version']=='1.0':self.assertEqual(item['height'],1760)
        old_manifest=json.loads(path.with_name('manifest-1.0.json').read_text())
        self.assertEqual(old_manifest['version'],'1.0')
        self.assertEqual(len(old_manifest['pages']),5)
        for item in old_manifest['pages']:
            self.assertEqual(hashlib.sha256((ROOT/item['path'].lstrip('/')).read_bytes()).hexdigest(),item['sha256'])
        self.assertEqual(path.with_name('manifest-1.2.json').read_bytes(),path.read_bytes())

    def test_mobile_scroll_and_close_js(self):
        css=(ROOT/'_templates/terms-reader.css').read_text()
        js=(ROOT/'_templates/terms-reader.js').read_text()
        self.assertIn('height:100dvh',css)
        self.assertIn('overflow:auto',css)
        self.assertIn('touch-action:pan-x pan-y',css)
        self.assertIn('dialog.showModal()',js)
        self.assertIn("closeButton.addEventListener('click'",js)
        self.assertIn('history.back()',js)
        self.assertIn('requestPageIndicator',js)
        self.assertIn('deepLink()',js)

    def test_effective_html_terms_consent_preserved(self):
        old=(ROOT/'terms-and-conditions/current/index.html').read_text()
        self.assertIn('noindex',old)
        self.assertIn('Identity and scope',old)
        self.assertIn('id="1"',old)
        source=(ROOT/'scripts/customer_site.py').read_text()
        self.assertIn("link('/terms-and-conditions/current/','Terms & Conditions','')",source)
        self.assertIn("if route!='/terms-and-conditions/'",source)

if __name__=='__main__':
    unittest.main()
