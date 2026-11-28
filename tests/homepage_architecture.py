#!/usr/bin/env python3
"""H01 single-source propagation and protected journey contracts, no writes."""
from copy import deepcopy
from html import unescape
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import subprocess
import sys
import unittest
from unittest.mock import patch
from urllib.parse import parse_qs, urlsplit

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import homepage_content
from build_homepage import render, Section
from homepage_resources import hero_preloads
from site_seo import finalize

BASELINE = '824ae5f1ca341440489876c7e3ce9239fc9bf2af'


def old(name):
    return subprocess.check_output(['git', 'show', BASELINE + ':' + name], cwd=ROOT, text=True)


class Elements(HTMLParser):
    def __init__(self, markup):
        super().__init__()
        self.elements = []
        self.feed(markup)

    def handle_starttag(self, tag, attrs):
        self.elements.append((tag, dict(attrs)))


class HomepageArchitectureTests(unittest.TestCase):
    def test_effective_copy_update_changes_homepage_without_template_edit(self):
        data = deepcopy(homepage_content.content())
        data['information']['cards'][0]['description'] = 'Fixture copy <safe> & escaped.'
        with patch.object(homepage_content, 'content', return_value=data):
            output = render()
        self.assertIn('Fixture copy &lt;safe&gt; &amp; escaped.', output)
        self.assertNotIn('Fixture copy', render())
        self.assertNotIn(data['information']['cards'][0]['description'], (ROOT / '_templates/homepage-tailoring.html').read_text())

    def test_four_primary_cards_and_safe_interim_suits(self):
        sections = homepage_content.render_sections()
        doc = Elements(sections['services'])
        cards = [a for t, a in doc.elements if t == 'a' and 'tailoring-primary-card' in a.get('class', '').split()]
        self.assertEqual(len(cards), 4)
        self.assertEqual([a['href'] for a in cards[:3]], ['/services/custom-tailoring/', '/services/alterations/', '/services/garment-care/'])
        wa = urlsplit(cards[3]['href'])
        self.assertEqual(wa.netloc, 'wa.me')
        business = json.loads((ROOT / '_data/business.json').read_text())
        self.assertEqual(wa.path, '/' + re.sub(r'\D', '', business['telephone']))
        self.assertEqual(parse_qs(wa.query)['text'], [json.loads((ROOT / '_data/service-contact-actions.json').read_text())['messages']['combined']])
        self.assertIn('/services/custom-tailoring/#tailoring-hub-categories', sections['services'])
        self.assertNotIn('href="/suits/"', sections['services'])
        self.assertNotIn('href="/shop/', render())

    def test_feature_resolves_only_eligible_library_records_and_existing_image(self):
        current = json.loads((ROOT / '_data/media-library-settings.json').read_text())
        self.assertIn('r4-480.webp', homepage_content.feature(current))
        held = deepcopy(current)
        held['homepage']['featuredDesign']['designId'] = 'UNPUBLISHED-FIXTURE'
        self.assertEqual(homepage_content.feature(held), '')
        held = deepcopy(current)
        held['homepage']['featuredDesign']['imageSrc'] = '/unapproved-photo.jpeg'
        self.assertEqual(homepage_content.feature(held), '')
        self.assertNotIn('UNPUBLISHED-FIXTURE', render())

    def test_business_edit_propagates_home_contact_footer_and_schema(self):
        original = Path.read_text
        def fixture(path, *args, **kwargs):
            source = original(path, *args, **kwargs)
            if path == ROOT / '_data/business.json':
                data = json.loads(source)
                data.update(name='Fixture Brand', telephone='+250700000000', email='fixture@example.invalid')
                return json.dumps(data)
            return source
        with patch.object(Path, 'read_text', fixture):
            output = render()
        for value in ('FIXTURE BRAND', 'tel:+250700000000', '+250 700 000 000', 'mailto:fixture@example.invalid', 'wa.me/250700000000'):
            self.assertIn(value, output)
        self.assertNotIn('tel:+250787411501', output)
        self.assertNotIn('mailto:mrsewingfashiondesigner@gmail.com', output)

    def test_hero_image_preload_matches_current_hero_not_legacy_document(self):
        hero = homepage_content.render_sections()['hero']
        image = next(attrs for tag, attrs in Elements(hero).elements if tag == 'img')
        preload = next(attrs for tag, attrs in Elements(hero_preloads(hero)).elements if tag == 'link')
        self.assertEqual(preload['imagesrcset'], image['srcset'])
        self.assertEqual(preload['imagesizes'], image['sizes'])
        self.assertIn('tailoring-hero', preload['imagesrcset'])

    def test_support_form_and_current_customer_scripts_preserved(self):
        output = finalize(render(), ROOT / 'index.html')
        form = lambda s: re.search(r'<form\b[^>]*id="supportForm".*?</form>', s, re.S).group()
        self.assertEqual(form(output), form(old('index.html')))
        for filename in ('_templates/homepage-corrective.js', '_templates/customer-tracking.js', '_templates/enquiry-measurement.js', '_templates/whatsapp-consent.js', '_templates/design-selections.js', '_data/customer-policy-facts.json', '_data/advertising-measurement.json', '_data/selected-design-request-config.json'):
            path = ROOT / filename
            if path.is_file():
                self.assertEqual(path.read_text(), old(filename), filename)
        for name in ('Standard Order', 'Express Order', 'VIP Order', 'Loyalty Programme', 'Referral Programme', 'Payment Methods', 'Customer <em>Support</em>'):
            self.assertIn(name, output)

    def test_homepage_route_metadata_and_no_active_offer(self):
        output = finalize(render(), ROOT / 'index.html')
        self.assertIn('href="https://mrsewingfashion.com/"', output)
        self.assertEqual(len(re.findall(r'<h1\b', output)), 1)
        self.assertNotIn('name="keywords"', output)
        self.assertNotIn('{{', output)
        self.assertNotIn('content-offer', output)
        self.assertIn('https://youtube.com/@mr.sewingfashion', output)
        self.assertNotIn('https://youtube.com/@mr.sewingfashiondesigner', output)


if __name__ == '__main__':
    unittest.main()
