#!/usr/bin/env python3
"""H01 metadata authority, propagation and escaping tests without generation."""
from copy import deepcopy
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from homepage_metadata import render_head


class Head(HTMLParser):
    def __init__(self, source):
        super().__init__()
        self.metas, self.links, self.titles = {}, [], []
        self.in_title = False
        self.feed(source)

    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        if tag == 'meta':
            key = attrs.get('name', attrs.get('property'))
            self.metas.setdefault(key, []).append(attrs.get('content'))
        if tag == 'link':
            self.links.append(attrs)
        if tag == 'title':
            self.in_title = True

    def handle_endtag(self, tag):
        if tag == 'title':
            self.in_title = False

    def handle_data(self, data):
        if self.in_title:
            self.titles.append(data)


def graph(source):
    return json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>', source, re.S)[1])


class HomepageMetadataTests(unittest.TestCase):
    def setUp(self):
        self.seo = json.loads((ROOT / '_data/public-page-seo.json').read_text())['/']
        self.business = json.loads((ROOT / '_data/business.json').read_text())
        self.media = json.loads((ROOT / '_data/homepage-media.json').read_text())

    def render(self, **updates):
        return render_head(seo=updates.get('seo', self.seo), business=updates.get('business', self.business), media=updates.get('media', self.media))

    def test_current_h01_metadata_and_business_projection(self):
        source = self.render()
        parsed = Head(source)
        self.assertEqual(''.join(parsed.titles), self.seo['title'])
        for field in ('description', 'og:description', 'twitter:description'):
            self.assertEqual(parsed.metas[field], [self.seo['description']])
        for field in ('og:title', 'twitter:title'):
            self.assertEqual(parsed.metas[field], [self.seo['title']])
        self.assertEqual([link['href'] for link in parsed.links if link['rel'] == 'canonical'], ['https://mrsewingfashion.com/'])
        self.assertEqual(parsed.metas['og:url'], ['https://mrsewingfashion.com/'])
        self.assertEqual(parsed.metas['og:image:width'], ['1244'])
        self.assertEqual(parsed.metas['og:image:height'], ['802'])
        self.assertEqual(graph(source)['@graph'][0]['publisher'], self.business)
        self.assertNotIn('keywords', parsed.metas)
        self.assertNotIn('SiteNavigationElement', source)  # no stale, independently maintained nav schema

    def test_one_seo_edit_reaches_all_homepage_metadata(self):
        seo = {'title': 'A fixture title & name', 'description': 'A fixture description <with> "quotes".'}
        parsed = Head(self.render(seo=seo))
        self.assertEqual(''.join(parsed.titles), seo['title'])
        for field in ('description', 'og:description', 'twitter:description'):
            self.assertEqual(parsed.metas[field], [seo['description']])
        for field in ('og:title', 'twitter:title'):
            self.assertEqual(parsed.metas[field], [seo['title']])

    def test_business_contact_hours_and_social_edits_propagate_without_mutation(self):
        business = deepcopy(self.business)
        business.update(name='Fixture business', telephone='+250700000000', email='fixture@example.invalid')
        business['sameAs'] = ['https://example.invalid/channel']
        business['openingHoursSpecification'][0]['opens'] = '10:30'
        before = deepcopy(business)
        source = self.render(business=business)
        publisher = graph(source)['@graph'][0]['publisher']
        self.assertEqual(publisher, before)
        self.assertEqual(Head(source).metas['author'], ['Fixture business'])
        self.assertEqual(graph(source)['@graph'][0]['name'], 'Fixture business')
        self.assertEqual(business, before)
        self.assertNotIn('+250787411501', source)

    def test_json_and_html_boundaries_are_safe(self):
        value = '</script><script>alert("fixture")</script>&'
        business = deepcopy(self.business)
        business['name'] = value
        source = self.render(seo={'title': value, 'description': value}, business=business)
        self.assertEqual(source.count('<script'), 1)
        self.assertEqual(source.count('</script>'), 1)
        self.assertEqual(graph(source)['@graph'][0]['publisher']['name'], value)
        self.assertEqual(''.join(Head(source).titles), value)
        self.assertEqual(Head(source).metas['description'], [value])

    def test_missing_and_unsafe_configuration_fails_before_publication(self):
        for key in ('title', 'description'):
            seo = dict(self.seo)
            seo[key] = ''
            with self.subTest(key=key), self.assertRaises(ValueError):
                self.render(seo=seo)
        for field in ('url', 'image'):
            for value in ('/relative', 'javascript:alert(1)', 'http://example.invalid/', 'https://u:p@example.invalid/'):
                business = deepcopy(self.business)
                business[field] = value
                with self.subTest(field=field, value=value), self.assertRaises(ValueError):
                    self.render(business=business)

    def test_effective_source_is_read_instead_of_legacy_title(self):
        with tempfile.TemporaryDirectory() as tmp:
            data = Path(tmp) / '_data'
            data.mkdir()
            (data / 'public-page-seo.json').write_text(json.dumps({'/': {'title': 'Effective fixture', 'description': 'Effective description'}}))
            (data / 'page-seo.json').write_text(json.dumps({'index.html': {'title': 'Obsolete fixture', 'description': 'Obsolete description'}}))
            (data / 'business.json').write_text(json.dumps(self.business))
            (data / 'homepage-media.json').write_text(json.dumps(self.media))
            source = render_head(tmp)
            self.assertIn('Effective fixture', source)
            self.assertNotIn('Obsolete fixture', source)

    def test_template_keeps_resources_and_no_competing_literal_seo(self):
        source = (ROOT / '_templates/homepage.html').read_text().split('</head>', 1)[0]
        for hook in ('{{head_metadata}}', '{{hero_preloads}}', '{{agent_discovery}}', '{{section_styles}}'):
            self.assertEqual(source.count(hook), 1)
        for text in ('data-legacy-url', 'location.search + location.hash', 'assets/homepage.js', 'name="viewport"', 'charset="UTF-8"'):
            self.assertIn(text, source)
        for text in ('<title>', 'name="description"', 'name="keywords"', 'rel="canonical"', 'application/ld+json'):
            self.assertNotIn(text, source)


if __name__ == '__main__':
    unittest.main()
