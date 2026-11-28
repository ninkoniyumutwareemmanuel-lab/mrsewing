#!/usr/bin/env python3
"""Private fixture tests; the 10% example is never an approved public offer."""
from copy import deepcopy
from datetime import datetime
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from content_offers import eligible, preview_card, render, select_offer, validate

BENEFITS = {'fixture-only-10-percent': {'approved': True, 'type': 'percentage', 'value': 10}}


def fixture():
    return {'id': 'fixture-only', 'revision': 'fixture-1', 'title': 'Private test offer',
            'description': 'Synthetic test only', 'terms': 'Subject to fixture eligibility.',
            'termsUrl': '/terms-and-conditions/', 'benefitRef': 'fixture-only-10-percent',
            'status': 'scheduled', 'publicationStatus': 'approved',
            'startsAt': '2026-12-01T09:00:00+02:00', 'endsAt': '2026-12-02T17:00:00+02:00',
            'scope': {'serviceIds': ['custom-tailoring'], 'categoryIds': ['suits']},
            'placements': ['H01', 'S01']}


def context(stamp='2026-12-01T09:00:00+02:00', **kwargs):
    return {'now': datetime.fromisoformat(stamp), 'placement': 'H01',
            'service_id': 'custom-tailoring', 'category_id': 'suits',
            'resolve_benefit': BENEFITS.get, **kwargs}


class ContentOfferTests(unittest.TestCase):
    def test_default_registry_is_empty_and_cannot_be_flag_activated(self):
        self.assertEqual(render(), '')
        self.assertEqual(render(registry={'schemaVersion': 1, 'publishingEnabled': False, 'offers': [fixture()]}), '')
        with self.assertRaises(ValueError):
            render(registry={'schemaVersion': 1, 'publishingEnabled': True, 'offers': [fixture()]})

    def test_kigali_boundaries_inclusive_start_exclusive_end(self):
        item = fixture()
        for stamp, expected in [('2026-12-01T08:59:59+02:00', False),
                                ('2026-12-01T09:00:00+02:00', True),
                                ('2026-12-02T16:59:59+02:00', True),
                                ('2026-12-02T17:00:00+02:00', False),
                                ('2026-12-02T17:00:01+02:00', False),
                                ('2026-12-01T07:00:00+00:00', True)]:
            with self.subTest(stamp=stamp):
                self.assertEqual(eligible(item, **context(stamp)), expected)
        with self.assertRaises(ValueError):
            eligible(item, **context(now=datetime(2026, 12, 1, 9)))

    def test_scope_does_not_expand_from_display_placement(self):
        item = fixture()
        self.assertFalse(eligible(item, **context(service_id='alterations')))
        self.assertFalse(eligible(item, **context(category_id='shirts')))
        self.assertFalse(eligible(item, **context(placement='I01')))
        self.assertTrue(eligible(item, **context(placement='S01')))

    def test_pause_unapproved_expired_and_overlap_fail_closed(self):
        item = fixture()
        for status in ['draft', 'paused', 'expired', 'archived']:
            item['status'] = status
            self.assertFalse(eligible(item, **context()))
        item['status'] = 'active'
        item['publicationStatus'] = 'draft'
        self.assertFalse(eligible(item, **context()))
        item['publicationStatus'] = 'approved'
        self.assertTrue(eligible(item, **context()))
        other = deepcopy(item)
        other['id'] = 'second'
        self.assertIsNone(select_offer([item, other], **context()))
        self.assertEqual(select_offer([item], **context()), item)

    def test_invalid_values_dates_terms_and_duplicate_rate_rejected(self):
        item = fixture()
        for key, value in [('startsAt', '2026-12-01T09:00:00'), ('endsAt', item['startsAt']),
                           ('scope', {}), ('termsUrl', '//external.invalid/'),
                           ('termsUrl', '/\\external.invalid/'), ('value', 10)]:
            bad = {**item, key: value}
            self.assertFalse(eligible(bad, **context()))
        for benefit in [{'approved': True, 'type': 'percentage', 'value': 0},
                        {'approved': True, 'type': 'percentage', 'value': 101},
                        {'approved': True, 'type': 'fixed-rwf', 'value': 10.5, 'currency': 'RWF'},
                        {'approved': False, 'type': 'percentage', 'value': 10}]:
            self.assertFalse(eligible(item, **context(resolve_benefit=lambda _: benefit)))
        self.assertEqual(validate(item, BENEFITS.get)[2]['value'], 10)
        self.assertNotIn('value', item)

    def test_card_escaped_has_conditions_and_never_renders_ineligible(self):
        item = fixture()
        item['title'] = '<script>test</script>'
        html = preview_card(item, **context())
        self.assertIn('&lt;script&gt;', html)
        self.assertNotIn('<script>', html)
        self.assertIn('Offer conditions', html)
        self.assertIn(item['terms'], html)
        self.assertNotIn('fixture-only-10-percent', html)
        self.assertEqual(preview_card(item, **context(service_id='alterations')), '')


if __name__ == '__main__':
    unittest.main()
