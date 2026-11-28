#!/usr/bin/env python3
"""Shared shell contract tests using temporary sources, without approved-data edits."""
from html import unescape
from html.parser import HTMLParser
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from urllib.parse import parse_qs, urlsplit

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import site_shell as shell
from custom_tailoring import component
import shared_components


class Navigation(HTMLParser):
    def __init__(self, markup):
        super().__init__()
        self.links = []
        self.feed(markup)

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            self.links.append(dict(attrs))


class SiteShellTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.fixture = Path(self.temp.name)
        (self.fixture / '_data').mkdir()
        (self.fixture / '_templates').mkdir()
        for name in ('business.json', 'contact-v2.json', 'business-hours.json',
                     'customer-information.json', 'customer-interface-labels.json',
                     'homepage-guides.json', 'service-contact-actions.json', 'site-shell.json'):
            shutil.copyfile(ROOT / '_data' / name, self.fixture / '_data' / name)
        for name in ('homepage-header.html', 'homepage-footer.html'):
            shutil.copyfile(ROOT / '_templates' / name, self.fixture / '_templates' / name)

    def tearDown(self):
        self.temp.cleanup()

    def edit(self, filename, change):
        path = self.fixture / '_data' / filename
        data = json.loads(path.read_text())
        change(data)
        path.write_text(json.dumps(data))

    def render(self, name, current='/'):
        return shell.render(name, current, root=self.fixture)

    def test_navigation_contract_and_existing_controller_selectors(self):
        header = self.render('header')
        config = shell.configuration(self.fixture)
        self.assertEqual(config['primaryNavigation'], ['home', 'services', 'suits', 'showroom', 'our-work', 'about', 'contact'])
        self.assertEqual(config['serviceNavigation'], ['custom-tailoring', 'alterations', 'garment-care', 'combined'])
        self.assertIn('id="home-navigation"', header)
        self.assertIn('class="home-menu-toggle"', header)
        self.assertIn('aria-expanded="false" aria-controls="home-navigation"', header)
        self.assertIn('class="services-dropdown"><details><summary>Services', header)
        self.assertNotIn('/shop/', header)
        self.assertNotIn('/services/vip/', header)
        self.assertNotIn('/services/mobile-fitting/', header)
        current = [a for a in Navigation(header).links if a.get('aria-current') == 'page']
        self.assertEqual([a['href'] for a in current], ['/'])
        current = [a for a in Navigation(self.render('header', '/services/alterations/')).links if a.get('aria-current') == 'page']
        self.assertEqual([a['href'] for a in current], ['/services/alterations/'])

    def test_one_contact_edit_updates_shell_and_combined_action(self):
        self.edit('business.json', lambda d: d.update(telephone='+250 700 000 123', email='synthetic@example.invalid'))
        footer = self.render('footer')
        self.assertIn('href="tel:+250 700 000 123"', footer)
        self.assertIn('href="mailto:synthetic@example.invalid"', footer)
        for name in ('header', 'footer'):
            self.assertIn('https://wa.me/250700000123?text=', self.render(name))
            self.assertNotIn('https://wa.me/250787411501', self.render(name))
        combined = shell.destination('combined', self.fixture)
        self.assertEqual(parse_qs(urlsplit(combined['href']).query)['text'], [shell.read('service-contact-actions.json', self.fixture)['messages']['combined']])

    def test_single_hours_address_social_edit_is_escaped_and_propagates(self):
        self.edit('business-hours.json', lambda d: d.update(regularOpen='10:15', regularClose='16:45', umugandaOpen='13:15'))
        self.edit('contact-v2.json', lambda d: (d['mainWorkshop'].update(streetAddress='Test Street <script>'), d['social'].update(youtube='https://youtube.com/@synthetic-fixture')))
        header = self.render('header')
        self.assertIn('Mon–Sat 10:15–16:45', header)
        self.assertIn('Umuganda: 13:15–17:00 by advance appointment', header)
        self.assertIn('Test Street &lt;script&gt;', header)
        self.assertNotIn('Test Street <script>', header)
        footer = self.render('footer')
        self.assertIn('https://youtube.com/@synthetic-fixture', footer)
        self.assertNotIn('@mr.sewingfashion', footer)

    def test_navigation_label_update_propagates_without_changing_api_service(self):
        original = shell.read('customer-interface-labels.json', self.fixture)['services']['custom-tailoring']
        self.edit('site-shell.json', lambda d: d['destinations']['custom-tailoring'].update(navLabel='Fixture Tailoring'))
        self.assertIn('>Fixture Tailoring</a>', self.render('header'))
        self.assertIn('>Fixture Tailoring</a>', self.render('footer'))
        self.assertEqual(shell.destination('custom-tailoring', self.fixture)['label'], 'Fixture Tailoring')
        self.assertEqual(shell.read('customer-interface-labels.json', self.fixture)['services']['custom-tailoring'], original)
        self.edit('customer-interface-labels.json', lambda d: d['actions'].update(contact='Fixture Contact'))
        for name in ('header', 'footer'):
            self.assertIn('>Fixture Contact</a>', self.render(name))

    def test_legacy_destinations_and_interim_routes_are_genuine(self):
        config = shell.configuration()
        self.assertEqual(shell.destination('suits')['href'], '/services/custom-tailoring/#tailoring-hub-categories')
        self.assertIn('id="tailoring-hub-categories"', (ROOT / 'services/custom-tailoring/index.html').read_text())
        self.assertTrue(shell.destination('combined')['href'].startswith('https://wa.me/'))
        for key, entry in config['destinations'].items():
            href = shell.destination(key)['href']
            if href.startswith('/'):
                path = ROOT / urlsplit(href).path.lstrip('/')
                self.assertTrue((path / 'index.html').is_file() if path.is_dir() else path.is_file(), key)
        footer = self.render('footer')
        for route in ('/services/vip/', '/services/mobile-fitting/', '/measurements/', '/guides/fabrics/', '/faq/', '/terms-and-conditions/', '/privacy-policy/', '/refund-policy/', '/loyalty-program/', '/referral-program/'):
            self.assertIn('href="' + route + '"', footer)

    def test_same_shell_adapter_and_preserved_five_service_about_picker(self):
        self.assertEqual(shared_components.header('/'), component('header', '/'))
        self.assertEqual(shared_components.footer(), component('footer') + '<script src="/assets/request-context.js" defer></script>')
        picker = shared_components.services_picker()
        self.assertEqual(len(Navigation(picker).links), 5)
        self.assertIn('/services/vip/', picker)
        self.assertIn('/services/mobile-fitting/', picker)
        for name in ('header', 'footer'):
            self.assertNotIn('{{', component(name))

    def test_no_business_numbers_or_social_urls_in_editable_shell_templates(self):
        source = '\n'.join((ROOT / '_templates' / f'homepage-{name}.html').read_text() for name in ('header', 'footer'))
        for text in ('787411501', '09:00', '17:00', 'youtube.com', 'instagram.com', 'gmail.com', 'NINKONIYUMUTWARE NEXUS LTD'):
            self.assertNotIn(text, source)

    def test_invalid_external_page_or_social_destination_fails_validation(self):
        self.edit('site-shell.json', lambda d: d['destinations']['home'].update(href='javascript:alert(1)'))
        with self.assertRaises(ValueError):
            self.render('header')
        self.edit('site-shell.json', lambda d: d['destinations']['home'].update(href='/'))
        self.edit('contact-v2.json', lambda d: d['social'].update(youtube='javascript:alert(1)'))
        with self.assertRaises(ValueError):
            self.render('footer')


if __name__ == '__main__':
    unittest.main()
