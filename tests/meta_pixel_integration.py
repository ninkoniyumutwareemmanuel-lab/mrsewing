#!/usr/bin/env python3
"""Safe source checks for optional Meta Pixel (no network calls)."""
from pathlib import Path
import json
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from meta_pixel import script_tag
config = json.loads((ROOT / "_data/meta-pixel.json").read_text())
assert config["pixelId"] == "29683883327873735"
assert config["productionEnabled"] is False
assert 'data-production-enabled="false"' in script_tag()
source = (ROOT / "assets/meta-pixel.js").read_text()
assert "Allow tracking" in source and "Decline" in source
assert "meta_pixel_preview" in source
assert 'window.fbq("track", "PageView")' in source
assert "facebook.com/tr?" not in source
assert "meta_pixel_script_tag()" in (ROOT / "scripts/site_seo.py").read_text()
print("PASS: Meta Pixel staged, disabled by default, and consent gated")
