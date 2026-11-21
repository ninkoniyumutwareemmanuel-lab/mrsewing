#!/usr/bin/env python3
"""R57: retain original homepage sections and functionality; enhance only the approved areas."""
import json
import re
import sys
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from homepage_galleries import collection_items, suit_section, project_items, moments_gallery
from homepage_r57_additions import portrait_showcase, featured_photo
from homepage_redesign import source_families
from build_collections import load

class R57PreservingHomepageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html=(ROOT/'index.html').read_text()
        cls.source=(ROOT/'_templates/homepage-sections.html').read_text()
        cls.template=(ROOT/'_templates/homepage.html').read_text()
        cls.builder=(ROOT/'scripts/build_homepage.py').read_text()

    def test_original_homepage_sections_are_present_and_ordered(self):
        html=self.html
        expected=['id="hero-section"','id="services-section"','id="information-section"',
                  'id="process-section"','id="suit-collections"','id="benefits-section"',
                  'id="options-section"','id="customers-section"','id="programs-section"',
                  'id="final-section"','id="contact-section"','id="site-footer"']
        positions=[html.find(x) for x in expected]
        self.assertTrue(all(p>=0 for p in positions),list(zip(expected,positions)))
        self.assertEqual(positions,sorted(positions),'original homepage section ordering must remain intact')
        for section in ['customer-support','loyalty-program','referral-program',
                        'photoshoot-preview','payment-methods','order-options',
                        'customer-information','process-title']:
            self.assertIn(section,html)
        self.assertIn('AI-generated tailoring illustration',html,'original hero image retained')
        self.assertIn('id="supportForm"',html)
        self.assertIn('Request a Quote',html)
        self.assertIn('Our Work',html)
        self.assertIn('Shop Suit Styles',html)
        self.assertIn('Payment Methods',html)
        self.assertIn('Clothing Alterations &amp; Repairs',html)
        self.assertIn('Garment Care &amp; Cleaning',html)
        self.assertIn('Mobile Tailoring, Styling &amp; Event Assistance',html)

    def test_requested_additions_only(self):
        html=self.html
        self.assertEqual(len(re.findall(r'<h1\b',html)),1)
        self.assertIn('Professional <em>Tailor</em> in Kigali, Rwanda',html)
        self.assertIn('Custom suits and clothing, made to suit your design, style and measurements.',html)
        for label in ['Send Your Design on WhatsApp','Explore Clothing Designs','Tailoring &amp; Clothing Services']:
            self.assertIn(label,html)
        self.assertIn('data-whatsapp-modal',html)
        self.assertIn('class="service-card service-card-primary"',html)
        self.assertIn('class="service-card service-card-vip"',html)
        self.assertIn('href="/services/vip/"',html)
        self.assertEqual(html.count('class="r56-showcase-card"'),2)
        self.assertIn('home-r57-feature-layout',html)
        self.assertNotIn('1024X768black.mp4',html)
        self.assertNotIn('1024X768VIDEO.mp4',html)
        self.assertNotIn('<video',html)
        self.assertIn('/terms-and-conditions/current/',html)
        self.assertIn('staging noindex', (ROOT/'docs/R57_PRESERVE_ORIGINAL_HOMEPAGE_2026-11-21.md').read_text().lower())
        self.assertIn('noindex',html.lower())

    def test_authorized_newer_photos_but_no_new_shop_products(self):
        families=source_families()
        self.assertEqual(len(families),17)
        self.assertEqual(sum(len(group['photos']) for group in families),25)
        mens=collection_items('men')
        womens=collection_items('women')
        for collection in (mens,womens):
            self.assertGreater(len(collection),4)
            self.assertTrue(collection[0]['id'].startswith('MS-1'))
        newer=[item for item in mens+womens if int(item['id'].split('-')[1])>=152]
        self.assertEqual(len(newer),25,'all 25 owner-approved uploads appear in two suit galleries')
        self.assertEqual(len(load()[0]),28,'old Showroom publication gate must remain unchanged')
        registry=json.loads((ROOT/'_data/collection-designs.json').read_text())['designs']
        newly=[x for x in registry if (x.get('homepagePublication') or {}).get('approved')]
        self.assertEqual(len(newly),22)
        self.assertTrue(all(x['published'] is False for x in newly))
        self.assertTrue(all((x['homepagePublication'] or {})['independentThirdPartyLicenseInspected'] is False for x in newly))
        self.assertEqual(len(project_items())>0,True,'original Our Work gallery retained')

    def test_existing_men_women_galleries_move_opposite_and_pause(self):
        markup=suit_section()
        self.assertIn('data-gallery-direction="left"',markup)
        self.assertIn('data-gallery-direction="right"',markup)
        self.assertEqual(markup.count('data-gallery-toggle'),2)
        self.assertIn('View All Men',markup)
        self.assertIn('View All Women',markup)
        self.assertIn('Completed Mr Sewing tailoring projects',moments_gallery())
        css=(ROOT/'_templates/homepage-galleries.css').read_text()
        js=(ROOT/'_templates/homepage-galleries.js').read_text()
        self.assertIn('gallery-drift-right',css)
        self.assertIn('prefers-reduced-motion:reduce',css)
        self.assertIn('data-galleries-paused',js)
        self.assertIn('Pause photos',js)
        self.assertIn('Resume photos',js)

    def test_existing_terms_and_seo_are_unchanged(self):
        html=self.html
        self.assertIn('rel="canonical" href="https://mrsewingfashion.com/"',html)
        self.assertIn('assets/homepage.js',html)
        self.assertIn('MR LOGO.jpeg',html)
        self.assertIn('id="site-header"',html)
        self.assertIn('id="site-footer"',html)
        self.assertTrue((ROOT/'terms-and-conditions/current/index.html').is_file())
        self.assertTrue((ROOT/'assets/policy-documents/terms-and-conditions/1.0.pdf').is_file())

if __name__=='__main__':
    unittest.main()
