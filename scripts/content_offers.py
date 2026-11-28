"""Shared, inactive offer-card foundation; this module is not a quote engine.

The homepage may call render() now: it emits nothing. Offer publishing remains
disabled until an approved trusted-clock publication/expiry mechanism exists.
Static HTML does not expire itself and a browser clock is never authoritative.

One benefitRef resolves to an existing approved pricing/benefit authority through
a caller-supplied resolver. Never copy rates into this registry, auto-stack,
apply discounts, change accepted quotations or infer eligibility from placement.
Clock-injected functions below support private fixtures and future integration.
"""
from __future__ import annotations

from datetime import datetime
from html import escape
import json
from pathlib import Path
import re
from urllib.parse import urlsplit
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
KIGALI = ZoneInfo('Africa/Kigali')
STATUSES = {'draft', 'scheduled', 'active', 'paused', 'expired', 'archived'}
SCOPE_KEYS = ('serviceIds', 'categoryIds', 'itemIds')


def _timestamp(value):
    if not isinstance(value, str) or not re.fullmatch(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:Z|[+-]\d{2}:\d{2})', value):
        raise ValueError('Offer timestamps need an explicit date, time and timezone')
    try:
        stamp = datetime.fromisoformat(value.replace('Z', '+00:00'))
    except ValueError as error:
        raise ValueError('Invalid offer timestamp') from error
    if stamp.utcoffset() is None:
        raise ValueError('Offer timezone is required')
    return stamp.astimezone(KIGALI)


def validate(offer, resolve_benefit):
    """Validate one record without publishing it or changing any price."""
    if not isinstance(offer, dict):
        raise ValueError('Offer must be a record')
    for field in ('id', 'revision', 'title', 'description', 'terms', 'benefitRef'):
        if not isinstance(offer.get(field), str) or not offer[field].strip():
            raise ValueError('Offer requires ' + field)
    if not re.fullmatch(r'[a-zA-Z0-9][a-zA-Z0-9_-]*', offer['id']):
        raise ValueError('Offer needs a stable ID')
    if offer.get('status') not in STATUSES or offer.get('publicationStatus') not in ('draft', 'approved'):
        raise ValueError('Invalid offer status')
    if 'value' in offer or 'discountValue' in offer or 'price' in offer:
        raise ValueError('Resolve the existing benefit authority; do not duplicate its value')
    start, end = _timestamp(offer.get('startsAt')), _timestamp(offer.get('endsAt'))
    if start >= end:
        raise ValueError('Offer end must follow its start')
    scope = offer.get('scope')
    if not isinstance(scope, dict) or set(scope) - set(SCOPE_KEYS):
        raise ValueError('Explicit service/category/item scope is required')
    for key in SCOPE_KEYS:
        values = scope.get(key, [])
        if not isinstance(values, list) or not all(isinstance(v, str) and v.strip() for v in values) or len(values) != len(set(values)):
            raise ValueError('Invalid offer scope')
    if not any(scope.get(key) for key in SCOPE_KEYS):
        raise ValueError('Unscoped offers are not supported')
    placements = offer.get('placements')
    if not isinstance(placements, list) or not placements or not all(isinstance(v, str) and v.strip() for v in placements):
        raise ValueError('Explicit display placements are required')
    terms_url = offer.get('termsUrl', '')
    parsed = urlsplit(terms_url)
    if not terms_url.startswith('/') or terms_url.startswith('//') or parsed.scheme or parsed.netloc or '..' in parsed.path.split('/') or '\\' in terms_url or any(ord(c) < 32 for c in terms_url):
        raise ValueError('Terms link must be a local public route')
    benefit = resolve_benefit(offer['benefitRef'])
    if not isinstance(benefit, dict) or benefit.get('approved') is not True:
        raise ValueError('Benefit authority has not been approved')
    kind, value = benefit.get('type'), benefit.get('value')
    if isinstance(value, bool):
        raise ValueError('Invalid benefit value')
    if kind == 'percentage':
        if not isinstance(value, (int, float)) or not 0 < value <= 100:
            raise ValueError('Invalid approved percentage')
    elif kind == 'fixed-rwf':
        if not isinstance(value, int) or value <= 0 or benefit.get('currency') != 'RWF':
            raise ValueError('Fixed benefits require positive whole RWF')
    elif kind == 'benefit':
        if value is not None or not isinstance(benefit.get('publicDescription'), str):
            raise ValueError('A nonmonetary benefit needs approved descriptive text')
    else:
        raise ValueError('Unsupported benefit type')
    return start, end, benefit


def eligible(offer, *, now, placement, service_id=None, category_id=None, item_id=None, resolve_benefit):
    """Pure eligibility. now must be a caller's trusted aware server instant.

    Every nonempty scope axis must match. Placement alone cannot grant a benefit.
    Invalid records fail closed. Inclusive start and exclusive end use Kigali.
    """
    if not isinstance(now, datetime) or now.utcoffset() is None:
        raise ValueError('A trusted timezone-aware clock is required')
    try:
        start, end, _ = validate(offer, resolve_benefit)
    except (ValueError, KeyError, TypeError):
        return False
    if offer['publicationStatus'] != 'approved' or offer['status'] not in ('active', 'scheduled'):
        return False
    if not start <= now.astimezone(KIGALI) < end or placement not in offer['placements']:
        return False
    selected = {'serviceIds': service_id, 'categoryIds': category_id, 'itemIds': item_id}
    return all(not offer['scope'].get(key) or selected[key] in offer['scope'][key] for key in SCOPE_KEYS)


def select_offer(offers, **context):
    """Fail closed on overlapping applicable offers; never invent stacking rules."""
    matches = [offer for offer in offers if eligible(offer, **context)]
    return matches[0] if len(matches) == 1 else None


def preview_card(offer, **context):
    """Render a private review card only when this explicit context is eligible."""
    if not eligible(offer, **context):
        return ''
    return ('<aside class="content-offer" aria-labelledby="offer-' + escape(offer['id'], quote=True) + '">'
            '<h3 id="offer-' + escape(offer['id'], quote=True) + '">' + escape(offer['title']) + '</h3>'
            '<p>' + escape(offer['description']) + '</p><p>' + escape(offer['terms']) + '</p>'
            '<a href="' + escape(offer['termsUrl'], quote=True) + '">Offer conditions</a></aside>')


def render(placement='H01', registry=None):
    """Safe homepage hook. Publication is deliberately unavailable in Phase 1.

    A future authenticated owner workflow must establish expiry, scope and quote
    consistency before this guard is changed. It cannot be enabled with a flag.
    """
    data = registry if registry is not None else json.loads((ROOT / '_data/content-offers.json').read_text())
    if data.get('schemaVersion') != 1 or not isinstance(data.get('offers'), list):
        raise ValueError('Invalid offer registry')
    if data.get('publishingEnabled') is not False:
        raise ValueError('Offer publishing needs a verified trusted-clock expiry workflow')
    return ''
