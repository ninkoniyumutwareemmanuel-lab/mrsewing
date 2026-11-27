#!/usr/bin/env python3
"""Exact owner conversion mapping and GTM draft privacy/activation contracts."""
import copy
import json
import re
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from build_tracking_workspace import workspace, validate, outputs

EXPECTED = {
    'whatsapp_contact_click': ('Whatsap Contact', 'zHM6CL_CjsAdEILqsZ9F'),
    'website_call_click': ('Click to call', 'tT1uCMLCjsAdEILqsZ9F'),
    'appointment_confirmed': ('Book appointment', '_QXPCMXCjsAdEILqsZ9F'),
    'directions_click': ('Get directions', '55vTCMjCjsAdEILqsZ9F'),
    'quote_request_success': ('Request quote', 'ZHLFCMvCjsAdEILqsZ9F'),
    'lead_form_success': ('Submit lead form', 'p9FJCM7CjsAdEILqsZ9F'),
}


def fixture():
    return {'googleAds': {'conversionId': '18587874562', 'tagId': 'AW-18587874562'},
            'gtm': {'containerId': 'GTM-WHR49M4D'},
            'conversions': [{'event': event, 'name': pair[0], 'label': pair[1],
                             'enabled': event != 'appointment_confirmed'} for event, pair in EXPECTED.items()]}


def params(tag):
    return {p['key']: p['value'] for p in tag['parameter']}


class TrackingWorkspaceTests(unittest.TestCase):
    def test_exact_six_labels_one_native_destination(self):
        source = fixture()
        result = workspace(source)
        self.assertEqual(source, fixture(), 'Generator must not mutate authoritative config')
        version = result['containerVersion']
        self.assertEqual(version['container']['publicId'], 'GTM-WHR49M4D')
        self.assertNotIn('accountId', version)
        self.assertNotIn('containerId', version['container'])
        self.assertEqual(len(version['tag']), 8)
        conversions = [tag for tag in version['tag'] if tag['type'] == 'awct']
        self.assertEqual(len(conversions), 6)
        for tag, (event, (name, label)) in zip(conversions, EXPECTED.items()):
            p = params(tag)
            self.assertEqual(tag['name'], 'MR Sewing — ' + name)
            self.assertEqual(p['conversionId'], '18587874562')
            self.assertEqual(p['conversionLabel'], label)
            self.assertEqual(p['transactionId'], '{{MR Sewing — event_id}}')
            self.assertEqual(p['enableEnhancedConversion'], 'false')
            self.assertEqual(p['enableProductReporting'], 'false')
            self.assertNotIn('conversionValue', p)
            self.assertNotIn('currencyCode', p)
            if event == 'appointment_confirmed':
                self.assertTrue(tag['paused'])
                self.assertEqual(tag['firingTriggerId'], [])
            else:
                self.assertFalse(tag['paused'])
                self.assertEqual(len(tag['firingTriggerId']), 1)

    def test_every_trigger_guards_consent_and_official_host(self):
        version = workspace(fixture())['containerVersion']
        self.assertEqual(len(version['trigger']), 6, 'Ready plus five active actions')
        for trigger in version['trigger']:
            filters = json.dumps(trigger['filter'], ensure_ascii=False)
            self.assertIn('MR Sewing — measurement allowed', filters)
            self.assertIn('MR Sewing — Google measurement consent', filters)
            self.assertIn('Page Hostname', filters)
            self.assertIn('mrsewingfashion', filters)
            self.assertEqual(trigger['type'], 'CUSTOM_EVENT')
            self.assertNotIn('appointment_confirmed', json.dumps(trigger))
            host = next(rule for rule in trigger['filter'] if rule['type'] == 'MATCH_REGEX')
            pattern = params(host)['arg1']
            for value in ['mrsewingfashion.com', 'www.mrsewingfashion.com']:
                self.assertIsNotNone(re.fullmatch(pattern, value))
            for value in ['mrsewing-staging.pages.dev', 'test.mrsewing-staging.pages.dev', 'mrsewingfashion.com.evil.test', 'mrsewingfashionXcom']:
                self.assertIsNone(re.fullmatch(pattern, value))
        for tag in version['tag']:
            self.assertEqual(tag['consentSettings']['consentStatus'], 'NEEDED')
            self.assertEqual(tag['consentSettings']['consentType']['type'], 'LIST')
            types = {p['value'] for p in tag['consentSettings']['consentType']['list']}
            self.assertEqual(types, {'ad_storage', 'ad_user_data'})
            self.assertNotIn('ad_personalization', types)
        ready = next(t for t in version['trigger'] if t['triggerId'] == '900100')
        self.assertIn('mr_measurement_ready', json.dumps(ready))
        self.assertTrue(all(t['firingTriggerId'] == ['900100'] for t in version['tag'] if t['type'] in ('googtag', 'gclidw')))

    def test_invalid_destination_duplicate_mapping_and_appointment_fail_closed(self):
        for change in ['container', 'conversion', 'label', 'duplicate', 'appointment']:
            source = fixture()
            if change == 'container': source['gtm']['containerId'] = 'GTM-UNRELATED'
            elif change == 'conversion': source['googleAds']['conversionId'] = '999'
            elif change == 'label': source['conversions'][0]['label'] = '<untrusted>'
            elif change == 'duplicate': source['conversions'][1]['label'] = source['conversions'][0]['label']
            else: source['conversions'][2]['enabled'] = True
            with self.subTest(change=change), self.assertRaises(ValueError): workspace(source)
        broken = workspace(fixture())
        broken['containerVersion']['tag'][0]['firingTriggerId'] = ['missing']
        with self.assertRaises(ValueError): validate(broken)

    def test_live_registry_and_committed_draft_match_exact_owner_labels(self):
        config = json.loads((ROOT / '_data/advertising-measurement.json').read_text())
        self.assertEqual({r['event']: (r['name'], r['label']) for r in config['conversions']}, EXPECTED)
        for row in config['conversions']:
            self.assertEqual(row['sendTo'], 'AW-18587874562/' + row['label'])
        for target, content in outputs().items():
            self.assertTrue(target.is_file())
            self.assertEqual(target.read_text(), content)
        text = next(iter(outputs().values())).lower()
        for bad in ['email_address', 'phone_number', 'enhanced_conversions', 'purchase', 'g-fake', 'gtm-unrelated']:
            self.assertFalse(bad in text, 'Unexpected private/unsupported field: ' + bad)
        # ad_user_data is a required consent-purpose name, not an uploaded
        # user_data conversion parameter. Do not conflate those two things.
        for tag in workspace(config)['containerVersion']['tag']:
            self.assertNotIn('user_data', params(tag))
            self.assertNotIn('userData', params(tag))


if __name__ == '__main__':
    unittest.main()
