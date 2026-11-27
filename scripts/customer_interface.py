"""Approved interface wording, separate from prices and operational policies."""
import json
import re
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def labels():
    data = json.loads((ROOT / '_data/customer-interface-labels.json').read_text())
    assert data['schemaVersion'] == 1
    return data


def action(key):
    return labels()['actions'][key]


def service_name(key):
    return labels()['services'][key]


def navigation_labels(markup):
    """Normalize only exact service navigation links, never prose or policies."""
    for service, name in labels()['services'].items():
        path = '/services/' + service + '/'
        markup = re.sub(r'(<a\b[^>]*href="' + re.escape(path) + r'"[^>]*>)[^<]*(</a>)',
                        lambda match: match[1] + escape(name) + match[2], markup)
    return markup
