#!/usr/bin/env python3
"""Prove both V2 builds consume one header/footer/CSS source without changing files."""
from pathlib import Path
from unittest.mock import patch
import re
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'scripts'))
import build_homepage
import build_contact
import build_about
from shared_components import ROOT, SHARED
home, contact = build_homepage.render(), build_contact.render()
def extract(html, tag):
    return re.search(r'<'+tag+r'\b.*?</'+tag+'>',html,re.S)[0]
assert extract(home,'footer') == extract(contact,'footer') == extract(build_about.render(),'footer')
assert home.count('href="https://youtube.com/@mr.sewingfashion"') == 1
assert contact.count('href="https://youtube.com/@mr.sewingfashion"') == 1
assert len(re.findall(r'href="/booking/"',extract(contact,'main'))) == 2
assert not re.search(r'<(?:a|button)\b', re.search(r'<section class="contact-hero.*?</section>',contact,re.S)[0])
read = Path.read_text
def injected(path,*args,**kwargs):
    value = read(path,*args,**kwargs)
    if path == SHARED/'header.html':value=value.replace('<header ', '<header data-shared-probe="header" ',1)
    if path == SHARED/'footer.html':value=value.replace('<footer ', '<footer data-shared-probe="footer" ',1)
    if path == SHARED/'site.css':value+='\n.social-icons a { outline-offset:7px; }\n'
    return value
with patch.object(Path,'read_text',injected):
    for html in [build_homepage.render(),build_contact.render(),build_about.render()]:
        assert 'data-shared-probe="header"' in html
        assert 'data-shared-probe="footer"' in html
        assert '.social-icons a { outline-offset:7px; }' in html
print('PASS: identical rendered V2 footers; header/footer/CSS changes propagate to all three V2 builders; Contact hero actions absent and two main booking links retained.')
