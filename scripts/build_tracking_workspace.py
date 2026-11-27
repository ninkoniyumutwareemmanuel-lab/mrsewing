#!/usr/bin/env python3
"""Prepare an importable draft for the owner's EXISTING GTM web container.

This writes internal repository configuration only. It cannot authenticate,
import, publish, modify campaigns or establish receipt in Google Ads.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / '.github/tracking/gtm-workspace.json'
EVENTS = (
    'whatsapp_contact_click', 'website_call_click', 'appointment_confirmed',
    'directions_click', 'quote_request_success', 'lead_form_success',
)
PREFIX = 'MR Sewing — '


def parameter(key, value, kind='TEMPLATE'):
    return {'type': kind, 'key': key, 'value': str(value).lower() if isinstance(value, bool) else str(value)}


def equals(variable, value):
    return {'type': 'EQUALS', 'parameter': [parameter('arg0', '{{' + variable + '}}'), parameter('arg1', value)]}


def extra_consent():
    # Personalization and analytics remain denied; measurement does not silently
    # authorize either purpose or enhanced/customer-data conversions.
    return {'consentStatus': 'NEEDED', 'consentType': {'type': 'LIST', 'list': [
        {'type': 'TEMPLATE', 'value': 'ad_storage'},
        {'type': 'TEMPLATE', 'value': 'ad_user_data'},
    ]}}


def workspace(config):
    """Build deterministic GTM export-format configuration from one registry."""
    container = config.get('gtm', {}).get('containerId')
    conversion_id = str(config.get('googleAds', {}).get('conversionId', ''))
    tag_id = config.get('googleAds', {}).get('tagId')
    rows = config.get('conversions')
    if container != 'GTM-WHR49M4D' or conversion_id != '18587874562' or tag_id != 'AW-' + conversion_id:
        raise ValueError('Use the exact existing owner-supplied container and Google Ads identity')
    if not isinstance(rows, list) or len(rows) != len(EVENTS) or {r.get('event') for r in rows} != set(EVENTS):
        raise ValueError('Exactly six distinct approved conversion actions are required')
    actions = {r['event']: r for r in rows}
    for event in EVENTS:
        row = actions[event]
        if not isinstance(row.get('name'), str) or not row['name'].strip():
            raise ValueError('Conversion display name is required')
        if not re.fullmatch(r'[A-Za-z0-9_-]{1,100}', row.get('label', '')):
            raise ValueError('Preserve the exact approved conversion label')
        if type(row.get('enabled')) is not bool:
            raise ValueError('Conversion enabled state must be explicit')
        if 'sendTo' in row and row['sendTo'] != tag_id + '/' + row['label']:
            raise ValueError('Conversion send_to must exactly match its approved ID and label')
    if actions['appointment_confirmed']['enabled']:
        raise ValueError('Appointment conversion remains inactive without genuine confirmation infrastructure')
    if len({r['label'] for r in rows}) != len(rows):
        raise ValueError('Conversion labels must be distinct')

    variable_names = {
        'event_id': PREFIX + 'event_id',
        'mr_measurement_allowed': PREFIX + 'measurement allowed',
        'mr_consent_google': PREFIX + 'Google measurement consent',
    }
    variables = [
        {'variableId': str(900001 + i), 'name': name, 'type': 'v', 'parameter': [
            parameter('name', key), parameter('dataLayerVersion', 2, 'INTEGER'),
            parameter('setDefaultValue', False, 'BOOLEAN'),
        ]}
        for i, (key, name) in enumerate(variable_names.items())
    ]
    guard = [
        equals(variable_names['mr_measurement_allowed'], 'true'),
        equals(variable_names['mr_consent_google'], 'true'),
        {'type': 'MATCH_REGEX', 'parameter': [
            parameter('arg0', '{{Page Hostname}}'),
            parameter('arg1', r'^(mrsewingfashion\.com|www\.mrsewingfashion\.com)$'),
        ]},
    ]

    def trigger(event, identifier):
        return {'triggerId': str(identifier), 'name': PREFIX + event, 'type': 'CUSTOM_EVENT',
                'customEventFilter': [equals('_event', event)], 'filter': guard}

    ready_trigger = trigger('mr_measurement_ready', 900100)
    triggers = [ready_trigger]
    tags = [
        {'tagId': '900201', 'name': PREFIX + 'Google tag AW-18587874562', 'type': 'googtag',
         'parameter': [parameter('tagId', tag_id)], 'firingTriggerId': ['900100'],
         'tagFiringOption': 'ONCE_PER_LOAD', 'consentSettings': extra_consent()},
        {'tagId': '900202', 'name': PREFIX + 'Conversion Linker', 'type': 'gclidw',
         'parameter': [parameter('enableCrossDomain', False, 'BOOLEAN')],
         'firingTriggerId': ['900100'], 'tagFiringOption': 'ONCE_PER_LOAD',
         'consentSettings': extra_consent()},
    ]
    for index, event in enumerate(EVENTS):
        row = actions[event]
        trigger_id = str(900101 + index)
        active = row['enabled'] and event != 'appointment_confirmed'
        if active:
            triggers.append(trigger(event, trigger_id))
        tags.append({
            'tagId': str(900301 + index), 'name': PREFIX + row['name'], 'type': 'awct',
            'parameter': [parameter('conversionId', conversion_id), parameter('conversionLabel', row['label']),
                          parameter('transactionId', '{{' + variable_names['event_id'] + '}}'),
                          parameter('enableConversionLinker', True, 'BOOLEAN'),
                          parameter('enableEnhancedConversion', False, 'BOOLEAN'),
                          parameter('enableProductReporting', False, 'BOOLEAN')],
            'firingTriggerId': [trigger_id] if active else [],
            'paused': not active, 'tagFiringOption': 'ONCE_PER_EVENT', 'consentSettings': extra_consent(),
        })
    result = {'exportFormatVersion': 2, 'containerVersion': {
        # Account/internal numeric container IDs are unknown, so not fabricated.
        # The operator selects the owner's existing destination during import.
        'container': {'name': 'Mr Sewing Fashion — prepared website measurement',
                      'publicId': container, 'usageContext': ['WEB']},
        'tag': tags, 'trigger': triggers, 'variable': variables,
        'builtInVariable': [{'type': 'PAGE_HOSTNAME', 'name': 'Page Hostname'}],
    }}
    validate(result)
    return result


def validate(value):
    """Validate internal identities, references and privacy invariants locally.

    This is not Google's import parser or proof of account publication.
    """
    version = value['containerVersion']
    if value.get('exportFormatVersion') != 2 or version['container']['publicId'] != 'GTM-WHR49M4D':
        raise ValueError('Unexpected GTM draft format/destination')
    for key, identifier in [('tag', 'tagId'), ('trigger', 'triggerId'), ('variable', 'variableId')]:
        rows = version[key]
        if len({r[identifier] for r in rows}) != len(rows) or len({r['name'] for r in rows}) != len(rows):
            raise ValueError('Duplicate GTM identifier/name')
    triggers = {r['triggerId'] for r in version['trigger']}
    for tag in version['tag']:
        if not set(tag.get('firingTriggerId', [])).issubset(triggers):
            raise ValueError('Tag references an unknown trigger')
    for rule in version['trigger']:
        if rule['type'] != 'CUSTOM_EVENT' or len(rule.get('filter', [])) != 3:
            raise ValueError('Every trigger needs explicit event, consent and official-host guards')
    return value


def outputs():
    source = json.loads((ROOT / '_data/advertising-measurement.json').read_text())
    return {OUTPUT: json.dumps(workspace(source), ensure_ascii=False, indent=2) + '\n'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    for target, content in outputs().items():
        if args.check:
            if not target.is_file() or target.read_text() != content:
                raise SystemExit('GTM draft is not synchronized with its registry: ' + str(target))
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content)
    print('PASS prepared GTM draft synchronized; no account import, publication or external receipt claimed')


if __name__ == '__main__':
    main()
