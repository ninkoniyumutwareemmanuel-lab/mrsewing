#!/usr/bin/env python3
"""Assemble index.html from reusable section markup, without runtime HTML fetches.

No third-party dependencies. Standalone source pages are never modified.
Run after editing the dedicated _templates/homepage* files or resource helpers.
"""
from site_seo import finalize
import argparse
from html import unescape
from html.parser import HTMLParser
from pathlib import Path
import re
import struct
from homepage_resources import delivery, hero_preloads, CSS as RESOURCE_CSS
from build_clean_urls import DISCOVERY_LINKS
import shared_components as shared

ROOT = Path(__file__).resolve().parents[1]
# Owner requested a disconnected homepage while each page is rebuilt in sequence.
HOMEPAGE_VISUAL_REVIEW = False
# Source document, selected element, identifying attribute (if needed).
SECTIONS = {
    'header': ('_templates/homepage-header.html', 'header', None),
    'hero': ('_templates/homepage-sections.html', 'section', ('class', 'hero-section')),
    'customers': ('_templates/homepage-sections.html', 'section', ('class', 'customers-section home-section')),
    'process': ('_templates/homepage-sections.html', 'section', ('class', 'home-process home-section')),
    'benefits': ('_templates/homepage-sections.html', 'section', ('class', 'home-benefits home-section')),
    'services': ('_templates/homepage-sections.html', 'section', ('id', 'services')),
    'information': ('_templates/homepage-sections.html', 'section', ('id', 'customer-information')),
    'options': ('_templates/homepage-sections.html', 'section', ('id', 'order-options')),
    'programs': ('_templates/homepage-sections.html', 'div', ('id', 'programs')),
    'final': ('_templates/homepage-sections.html', 'section', ('class', 'home-final home-section')),
    'contact': ('_templates/homepage-sections.html', 'section', ('id', 'customer-support')),
    'footer': ('_templates/homepage-footer.html', 'footer', None),
}


class Section(HTMLParser):
    """Extract one balanced element verbatim; exclude its document's head/scripts."""
    def __init__(self, source, tag, identifier):
        super().__init__(convert_charrefs=False)
        self.source, self.tag, self.identifier = source, tag, identifier
        self.lines = source.splitlines(keepends=True)
        self.depth = 0
        self.start = None
        self.markup = None

    def char_offset(self):
        line, column = self.getpos()
        return sum(map(len, self.lines[:line - 1])) + column

    def handle_starttag(self, tag, attrs):
        if tag != self.tag or self.markup is not None:
            return
        if self.depth:
            self.depth += 1
        elif self.identifier is None or dict(attrs).get(self.identifier[0]) == self.identifier[1]:
            self.start = self.char_offset()
            self.depth = 1

    def handle_endtag(self, tag):
        if tag == self.tag and self.depth:
            self.depth -= 1
            if not self.depth:
                end = self.source.index('>', self.char_offset()) + 1
                self.markup = self.source[self.start:end]


def image_size(path):
    """Read intrinsic PNG/JPEG dimensions without re-encoding or dependencies."""
    data = path.read_bytes()
    if data[:8] == b'\x89PNG\r\n\x1a\n':
        return struct.unpack('>II', data[16:24])
    if data[:2] != b'\xff\xd8':
        raise ValueError(f'Expected PNG or JPEG: {path.name}')
    pos = 2
    sof = {0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF}
    while pos < len(data):
        if data[pos] != 0xFF:
            raise ValueError(f'Invalid JPEG marker: {path.name}')
        while data[pos] == 0xFF:
            pos += 1
        marker = data[pos]
        pos += 1
        length = struct.unpack('>H', data[pos:pos + 2])[0]
        if marker in sof:
            height, width = struct.unpack('>HH', data[pos + 3:pos + 7])
            return width, height
        pos += length
    raise ValueError(f'JPEG dimensions unavailable: {path.name}')


def reserve_image_space(match):
    tag = match.group(0)
    src = re.search(r'\bsrc="([^"]+)"', tag)
    if not src:
        raise ValueError('Homepage image needs an explicit src')
    path = ROOT / unescape(src[1])
    if not path.resolve().is_relative_to(ROOT):
        raise ValueError('Image must belong to this repository')
    width, height = image_size(path)
    if not re.search(r'\bwidth=', tag):
        tag = tag[:-1] + f' width="{width}" height="{height}">'
    if not re.search(r'\bdecoding=', tag):
        tag = tag[:-1] + ' decoding="async">'
    return tag


def render():
    template = (ROOT / '_templates/homepage.html').read_text().replace('{{agent_discovery}}', DISCOVERY_LINKS)
    styles = []
    for key, (filename, tag, identifier) in SECTIONS.items():
        source = (ROOT / filename).read_text()
        parser = Section(source, tag, identifier)
        parser.feed(source)
        if parser.markup is None:
            raise ValueError(f'Missing homepage section: {filename}')
        markup = parser.markup
        if key in ('header', 'footer'):
            from html import escape
            import json
            guides = json.loads((ROOT/'_data/homepage-guides.json').read_text())
            items = []
            for guide in guides:
                label = escape(guide['label'])
                if guide['href']:
                    assert (ROOT/guide['href'].strip('/')/'index.html').is_file(), 'Missing customer guide route'
                    items.append('<li><a href="'+escape(guide['href'], quote=True)+'">'+label+'</a></li>')
                else:
                    pending_class = 'footer-guide-pending' if key == 'footer' else 'nav-guide-pending'
                    span_class = 'pending-guide' if key == 'footer' else 'home-nav-pending'
                    items.append('<li class="'+pending_class+'"><span class="'+span_class+'" title="This guide will be developed separately">'+label+'</span></li>')
            markup = markup.replace('{{customer_guides}}', ''.join(items))
        if key == 'footer':
            markup = markup.replace('2026 Mr Sewing Fashion. All Rights Reserved.', '2026 NINKONIYUMUTWARE NEXUS LTD. All Rights Reserved.')
        if key == 'header':
            markup = markup.replace('<a href="/">Home</a>', '<a href="/" aria-current="page" class="active">Home</a>', 1)
        if re.search(r'<(?:head|meta|link|script|style)\b', markup, re.I):
            raise ValueError(f'Unexpected document metadata/script in section: {filename}')
        markup = re.sub(r'<img\b[^>]*>', reserve_image_space, markup)
        if key != 'header':
            markup = re.sub(r'<img\b(?![^>]*\bloading=)', '<img loading="lazy"', markup)
        markup = delivery(markup, key)
        template = template.replace('{{' + key + '}}', markup)
        section_styles = re.findall(r'<style[^>]*>(.*?)</style>', source, re.S)
        styles.extend(section_styles)
    from homepage_galleries import suit_section,moments_gallery
    template=template.replace('{{suit_collections}}',suit_section()).replace('{{moments_gallery}}',moments_gallery())
    styles.append((ROOT/'_templates/homepage-galleries.css').read_text())
    styles.append(RESOURCE_CSS)
    styles.append(shared.site_css())
    styles.append((ROOT/'_templates/homepage-motion.css').read_text())
    styles.append((ROOT/'_templates/homepage-phase1.css').read_text())
    template = template.replace('{{hero_preloads}}', hero_preloads())
    template = template.replace('{{section_styles}}', '\n'.join(styles))
    if re.search(r'{{\w+}}', template):
        raise ValueError('Unexpanded homepage template placeholder')
    if HOMEPAGE_VISUAL_REVIEW:
        from homepage_preview import disconnect
        template = disconnect(template)
    template = '\n'.join(line.rstrip() for line in template.splitlines()) + '\n'
    return '<!-- Generated by scripts/build_homepage.py; edit the template or source sections. -->\n<!-- Icons: Font Awesome Free 6.4.0, CC BY 4.0, Fonticons Inc.; assets/fontawesome-LICENSE.txt -->\n' + template


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='Fail if the generated homepage is out of date')
    args = parser.parse_args()
    output = finalize(render(), ROOT/'index.html')
    destination = ROOT / 'index.html'
    navigation = (shared.menu_script() + (ROOT/'_templates/homepage-preview.js').read_text() if HOMEPAGE_VISUAL_REVIEW else shared.menu_script() + (ROOT/'_templates/homepage-corrective.js').read_text() + (ROOT/'_templates/order-carousel.js').read_text() + (ROOT/'_templates/homepage-galleries.js').read_text())
    navigation_path = ROOT / 'assets/homepage.js'
    if args.check:
        if navigation_path.read_text() != navigation:
            raise SystemExit('Homepage navigation out of date; run build_homepage.py')
    else:
        navigation_path.write_text(navigation)
    if args.check:
        if destination.read_text() != output:
            raise SystemExit('Homepage is out of date. Run python3 scripts/build_homepage.py')
        print('PASS: generated homepage matches its template and section sources.')
    else:
        destination.write_text(output)
        print('Generated index.html; standalone section source pages are unchanged.')


if __name__ == '__main__':
    main()
