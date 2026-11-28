#!/usr/bin/env python3
"""One-source hours projection fixtures; no approved business records are edited."""
from copy import deepcopy
from datetime import date, timedelta
import hashlib
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from sync_business_hours import derive_business, derived_outputs
from sync_business_schema import synchronize
from homepage_metadata import render_head
from site_shell import hours_summary


class BusinessSettingsSyncTests(unittest.TestCase):
    def setUp(self):
        self.hours = json.loads((ROOT / '_data/business-hours.json').read_text())
        self.business = json.loads((ROOT / '_data/business.json').read_text())

    def test_current_projection_retains_exact_approved_information(self):
        projected = derive_business(self.hours, self.business, year=2026)
        self.assertEqual(projected, self.business)

    def test_single_hours_edit_reaches_visible_summary_metadata_and_calendar(self):
        hours = dict(self.hours, regularOpen='10:15', regularClose='16:45', umugandaOpen='13:15', umugandaClose='16:30')
        original = deepcopy(self.business)
        business = derive_business(hours, self.business, year=2030)
        self.assertEqual(self.business, original)
        self.assertIn('10:15–16:45', business['disambiguatingDescription'])
        self.assertIn('13:15–16:30', business['disambiguatingDescription'])
        self.assertNotIn('09:00', business['disambiguatingDescription'])
        self.assertEqual(business['openingHoursSpecification'][0]['opens'], '10:15')
        self.assertEqual(len(business['specialOpeningHoursSpecification']), 24)
        for exception in business['specialOpeningHoursSpecification']:
            stamp = date.fromisoformat(exception['validFrom'])
            self.assertIn(stamp.year, (2030, 2031))
            self.assertEqual(stamp.weekday(), 5)
            self.assertNotEqual((stamp + timedelta(days=7)).month, stamp.month)
            self.assertEqual((exception['opens'], exception['closes']), ('13:15', '16:30'))
        with tempfile.TemporaryDirectory() as temporary:
            fixture = Path(temporary)
            for folder in ('_data', '_templates', 'assets'):
                (fixture / folder).mkdir()
            (fixture / '_data/business-hours.json').write_text(json.dumps(hours))
            (fixture / '_data/business.json').write_text(json.dumps(business))
            shutil.copyfile(ROOT / '_data/contact-v2.json', fixture / '_data/contact-v2.json')
            shutil.copyfile(ROOT / '_templates/business-hours.js', fixture / '_templates/business-hours.js')
            (fixture / 'assets/forms.js').write_text('// Synthetic controller fixture')
            (fixture / 'booking.html').write_text('<script src="assets/business-hours.js?v=old"></script><script src="assets/forms.js"></script>')
            generated = derived_outputs(fixture, year=2030)
            calendar = generated[fixture / 'assets/business-hours.js']
            self.assertIn('"regularOpen":"10:15"', calendar)
            digest = hashlib.sha256(calendar.encode()).hexdigest()[:10]
            self.assertIn('business-hours.js?v=' + digest, generated[fixture / 'booking.html'])
            self.assertIn('10:15–16:45', hours_summary(fixture))
            seo = {'title': 'Fixture', 'description': 'Fixture metadata'}
            head = render_head(seo=seo, business=business, media={})
            self.assertIn('10:15–16:45', head)
            legacy_schema = '<script type="application/ld+json">' + json.dumps(original) + '</script>'
            updated_schema = synchronize(legacy_schema, business)
            self.assertIn('10:15–16:45', updated_schema)
            self.assertNotIn('09:00', updated_schema)

    def test_invalid_time_values_fail_before_publication(self):
        for field, value in [('regularOpen', '25:00'), ('umugandaClose', 'not-a-time'), ('regularClose', '08:00'), ('sundayByAppointment', 'true')]:
            with self.subTest(field=field), self.assertRaises(ValueError):
                derive_business(dict(self.hours, **{field: value}), self.business, year=2026)

    def test_social_authority_reaches_business_schema_projection(self):
        with tempfile.TemporaryDirectory() as temporary:
            fixture = Path(temporary)
            for folder in ('_data', '_templates', 'assets'):
                (fixture / folder).mkdir()
            for name in ('business.json', 'business-hours.json', 'contact-v2.json'):
                shutil.copyfile(ROOT / '_data' / name, fixture / '_data' / name)
            shutil.copyfile(ROOT / '_templates/business-hours.js', fixture / '_templates/business-hours.js')
            (fixture / 'assets/forms.js').write_text('// Fixture')
            path = fixture / '_data/contact-v2.json'
            data = json.loads(path.read_text())
            data['social']['youtube'] = 'https://example.invalid/fixture-channel'
            path.write_text(json.dumps(data))
            generated = derived_outputs(fixture, year=2026)
            business = json.loads(generated[fixture / '_data/business.json'])
            self.assertIn(data['social']['youtube'], business['sameAs'])
            self.assertNotIn('https://youtube.com/@mr.sewingfashion', business['sameAs'])
            self.assertIn('https://example.invalid/fixture-channel', render_head(seo={'title':'Fixture','description':'Fixture'}, business=business, media={}))

    def test_build_orders_shared_sync_before_page_generators(self):
        source = (ROOT / 'scripts/build_site.py').read_text()
        self.assertLess(source.index("'sync_business_hours.py'"), source.index("'sync_business_schema.py'"))
        self.assertLess(source.index("'sync_business_schema.py'"), source.index("'build_homepage.py'"))


if __name__ == '__main__':
    unittest.main()
