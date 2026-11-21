"""Consent-gated Meta Pixel installer (one authoritative config)."""
from html import escape
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]

def script_tag():
    config = json.loads((ROOT / "_data/meta-pixel.json").read_text(encoding="utf-8"))
    pixel_id = str(config["pixelId"])
    if not re.fullmatch(r"[0-9]{10,25}", pixel_id):
        raise ValueError("Invalid Meta Pixel ID")
    if config.get("productionEnabled") not in (True, False):
        raise ValueError("Invalid Meta tracking approval state")
    if config["productionEnabled"] and config.get("status") != "owner-approved-production":
        raise ValueError("Meta Pixel cannot be activated without owner approval")
    return ('<script src="/assets/meta-pixel.js?v=staging-20261121" defer '
            'data-mr-meta-pixel data-pixel-id="' + escape(pixel_id, quote=True) +
            '" data-production-enabled="' + str(config["productionEnabled"]).lower() +
            '"></script>')
