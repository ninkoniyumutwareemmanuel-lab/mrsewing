"""S01 source ownership, safe projection, route/quotation and policy boundaries."""
import copy
from html import unescape
import json
from pathlib import Path
import re
import subprocess
import sys
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import custom_tailoring_landing as landing
from customer_site import hero, service_map, service_page
from customer_policies import facts


class CustomTailoringTests(unittest.TestCase):
    def test_distinct_page_purpose_and_direct_existing_enquiry(self):
        markup = service_page('custom-tailoring')
        self.assertIn('<h1>Custom Tailoring &amp; Clothing Services</h1>', markup)
        self.assertIn('cut, make and trim (CMT)', markup)
        self.assertIn('href="/services/custom-tailoring/special-order/"', markup)
        self.assertIn('Request a Quote', markup)
        self.assertNotIn('id="customerRequestForm"', markup)
        self.assertNotIn('How Else Can We Help?', markup)
        self.assertNotIn('official activation is being reconciled', markup)
        self.assertNotIn('Request a flexible advance payment', markup)
        self.assertIn('Existing Standard-order advance exception', markup)

    def test_editorial_copy_is_projected_and_escaped(self):
        data = copy.deepcopy(landing.content_data())
        data['scope']['title'] = 'Fixture <script> is text'
        with patch.object(landing, 'content_data', return_value=data):
            markup = landing.render(service_map()['custom-tailoring'], hero)
        self.assertIn('Fixture &lt;script&gt; is text', markup)
        self.assertNotIn('Fixture <script>', markup)
        with self.assertRaises(ValueError):
            landing.text('')

    def test_shared_policy_keys_are_used_without_another_rule_copy(self):
        policy = facts()
        for key in ['policyOwnFabric', 'policyTailoringTime', 'policyProductionStart', 'policyDomesticPayment', 'policyCharges', 'policyExpressAdvance', 'policyInternationalPayment', 'policyFlexibleAdvance', 'policyOverdueAdvance', 'policyCustomDelivery']:
            with self.subTest(key=key):
                fixture = copy.deepcopy(policy)
                fixture['texts'][key] = 'Authoritative fixture ' + key
                with patch('customer_policies.facts', return_value=fixture):
                    rendered = landing.render(service_map()['custom-tailoring'], hero)
                self.assertIn('Authoritative fixture ' + key, rendered)
        fixture = copy.deepcopy(policy)
        fixture['services']['custom-tailoring']['standardTurnaround'] = 'Fixture estimate'
        fixture['payments']['domesticCustomAdvancePercent'] = 71
        with patch('customer_policies.facts', return_value=fixture):
            rendered = landing.render(service_map()['custom-tailoring'], hero)
        self.assertIn('Fixture estimate', rendered)
        self.assertIn('<strong>71%</strong>', rendered)

    def test_categories_come_from_existing_gated_catalogue(self):
        from build_collections import load
        from clothing_categories import active
        rows = active(load()[0])
        self.assertEqual([r['landingRoute'] for r in rows], ['/mensuits/', '/womensuits/'])
        with patch('clothing_categories.active', return_value=[]):
            markup = landing.render(service_map()['custom-tailoring'], hero)
        self.assertNotIn('class="tailoring-hub-category"', markup)
        fixture = copy.deepcopy(rows[0])
        fixture.update(id='future', name='Future approved category', url='/collections/?garment=future')
        fixture.pop('landingRoute')
        with patch('clothing_categories.active', return_value=[fixture]):
            markup = landing.render(service_map()['custom-tailoring'], hero)
        self.assertIn('href="/collections/?garment=future"', markup)
        self.assertIn('Future approved category', markup)

    def test_editorial_destinations_reject_external_or_script_urls(self):
        for target in ['javascript:alert(1)', 'https://foreign.invalid/', '//foreign.invalid/', '/\\foreign', '/bad\npath']:
            with self.subTest(target=target), self.assertRaises(ValueError):
                landing.page_link(target, 'Fixture')

    def test_generated_page_keeps_canonical_media_and_keyword_ownership(self):
        markup = (ROOT / 'services/custom-tailoring/index.html').read_text()
        self.assertIn('href="https://mrsewingfashion.com/services/custom-tailoring/"', markup)
        seo = json.loads((ROOT / '_data/public-page-seo.json').read_text())['/services/custom-tailoring/']
        self.assertIn('<title>' + seo['title'].replace('&', '&amp;') + '</title>', markup)
        self.assertIn('Custom Tailoring & Clothing Services', unescape(markup))
        self.assertIn('id="tailoring-hub-categories"', markup)
        for old in ['tailoring-hub-fabric-title', 'tailoring-hub-essentials-title', 'tailoring-hub-final-title']:
            self.assertIn('id="' + old + '"', markup)
        self.assertNotIn('href="/suits/"', markup)
        image = json.loads((ROOT / '_data/service-hero-images.json').read_text())['images']['custom-tailoring']
        self.assertIn('src="' + image['src'] + '"', markup)
        self.assertNotRegex(markup, r'\b\d[\d,]*\s+RWF\b')
        self.assertNotIn('name="keywords"', markup)
        sitemap = (ROOT / 'sitemap.xml').read_text()
        self.assertIn('<loc>https://mrsewingfashion.com/services/custom-tailoring/</loc>', sitemap)
        graph = [json.loads(raw) for raw in re.findall(r'<script[^>]+type="application/ld\+json"[^>]*>(.*?)</script>', markup, re.S)]
        self.assertTrue(any(n.get('@type') == 'Service' and n.get('name') == 'Custom Tailoring' for g in graph for n in g.get('@graph', [g])))

    def test_no_protected_business_or_form_contract_changed(self):
        paths = ['index.html', '_data/homepage-content.json', '_data/customer-policy-facts.json', '_data/suit-package-prices.json', '_data/tuxedo-package-prices.json', '_data/customer-request-backend.json', '_data/policy-documents.json', '_data/advertising-measurement.json', '_data/meta-pixel.json', '_templates/design-selections.js', '_templates/request-draft.js', 'functions/_lib/selected-design-handler.js']
        # These immutable baseline bytes protect the explicitly approved Phase1
        # Home and contracts; fixtures above exercise changed presentation.
        for path in paths:
            with self.subTest(path=path):
                before = subprocess.check_output(['git', 'show', '9b8f4439ebae4310badc74a9a8a28094e4e651e6:' + path], cwd=ROOT)
                self.assertEqual((ROOT / path).read_bytes(), before)


if __name__ == '__main__':
    unittest.main()
