#!/usr/bin/env python3
"""Prove shared footers/CSS and isolated homepage navigation without changing files."""
from pathlib import Path
from unittest.mock import patch
import re
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'scripts'))
import build_homepage
import build_contact
import build_about
import build_collections
import faq_help
from shared_components import ROOT, SHARED
home, contact = build_homepage.render(), build_contact.render()
designs, _ = build_collections.load()
def showroom():
    return build_collections.render('collections.html','all','Discover Your Signature Style.',designs)
def extract(html, tag):
    return re.search(r'<'+tag+r'\b.*?</'+tag+'>',html,re.S)[0]
from homepage_preview import disconnect
from build_homepage import HOMEPAGE_VISUAL_REVIEW
home_footer=extract(home,'footer')
assert 'Service Links' in home_footer and 'Customer Guides' in home_footer and 'Quick Information' in home_footer
assert 'NINKONIYUMUTWARE NEXUS LTD' in home_footer and 'footer-order-col' not in home_footer
assert extract(contact,'footer') == extract(build_about.render(),'footer') == extract(showroom(),'footer')
for path,html in faq_help.outputs().items():
 if path.suffix=='.html':assert extract(html,'footer')==extract(contact,'footer')
assert home.count('aria-label="YouTube"') == 1
assert ('href="https://youtube.com/@mr.sewingfashion"' in home) == (not HOMEPAGE_VISUAL_REVIEW)
assert contact.count('href="https://youtube.com/@mr.sewingfashion"') == 1
assert len(re.findall(r'href="/booking/"',extract(contact,'main'))) == 2
assert not re.search(r'<(?:a|button)\b', re.search(r'<section class="contact-hero.*?</section>',contact,re.S)[0])
read = Path.read_text
def injected(path,*args,**kwargs):
    value = read(path,*args,**kwargs)
    if path == SHARED/'header.html' or path == ROOT/'_templates/homepage-header.html':value=value.replace('<header ', '<header data-shared-probe="header" ',1)
    if path == SHARED/'footer.html' or path == ROOT/'_templates/homepage-footer.html':value=value.replace('<footer ', '<footer data-shared-probe="footer" ',1)
    if path == SHARED/'site.css':value+='\n.social-icons a { outline-offset:7px; }\n'
    return value
with patch.object(Path,'read_text',injected):
    for html in [build_homepage.render(),build_contact.render(),build_about.render(),showroom()]+[html for path,html in faq_help.outputs().items() if path.suffix=='.html']:
        assert 'data-shared-probe="header"' in html
        assert 'data-shared-probe="footer"' in html
        assert '.social-icons a { outline-offset:7px; }' in html
print('PASS: isolated homepage footer; shared footers unchanged elsewhere; header/footer/CSS propagate to the appropriate builders; Contact hero actions absent and two main booking links retained.')
