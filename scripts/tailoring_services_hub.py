"""Compatibility entry for older builder callers; S01 has one content owner."""
from custom_tailoring_landing import render


def content(service, hero, section=None, link=None):
    return render(service, hero)
