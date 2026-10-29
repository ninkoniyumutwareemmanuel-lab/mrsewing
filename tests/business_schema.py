#!/usr/bin/env python3
"""Validate local JSON-LD, business consistency and confirmed working hours.

Optional --vocabulary accepts Schema.org's official schemaorg-all-https.ttl to
check every declared type/property and its domain without network requests.
"""
import argparse
import json
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
BLOCK = re.compile(r'<script\b[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>', re.S | re.I)
BUSINESS_ID = 'https://mrsewingfashion.com/#organization'


def walk(value):
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from walk(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk(child)


def vocabulary_check(documents, path):
    text = path.read_text()
    chunks = re.findall(r'^schema:(\w+) a (.*?)(?=^schema:\w+ a |\Z)', text, re.S | re.M)
    classes = {name: block for name, block in chunks if block.startswith('rdfs:Class')}
    properties = {name: block for name, block in chunks if block.startswith('rdf:Property')}

    def terms(block, predicate):
        match = re.search(re.escape(predicate) + r'\s+(.*?)(?:;|\s+\.)', block, re.S)
        return set(re.findall(r'schema:(\w+)', match[1])) if match else set()

    def ancestors(name, seen=None):
        seen = set() if seen is None else seen
        if name in seen:
            return seen
        seen.add(name)
        for parent in terms(classes.get(name, ''), 'rdfs:subClassOf'):
            ancestors(parent, seen)
        return seen

    typed_nodes = 0
    for filename, document in documents:
        for node in walk(document):
            types = node.get('@type', [])
            types = types if isinstance(types, list) else [types]
            for name in types:
                assert name in classes, (filename, 'unknown type', name)
            inherited = set().union(*(ancestors(name) for name in types)) if types else set()
            for key in node:
                if key.startswith('@'):
                    continue
                assert key in properties, (filename, 'unknown property', key)
                domains = terms(properties[key], 'schema:domainIncludes')
                if types and domains:
                    assert inherited & domains, (filename, types, key, 'inappropriate property domain')
            typed_nodes += bool(types)
    print(f'PASS: {typed_nodes} typed nodes use recognized Schema.org types/properties and compatible property domains in the supplied official vocabulary.')


def main():
    args = argparse.ArgumentParser(description=__doc__)
    args.add_argument('--vocabulary', type=Path)
    options = args.parse_args()
    common = json.loads((ROOT / '_data/business.json').read_text())
    documents = []
    business_pages = []
    for path in sorted(ROOT.glob('*.html')):
        source = path.read_text()
        assert 'mrsewingfashiondesgner@gmail.com' not in source.lower(), path.name
        assert not re.search(r'Saturday (?:and|&amp;) Sunday.{0,30}(?:Booking / Call Required|by booking or call)', source, re.I), path.name
        for block in BLOCK.findall(source):
            document = json.loads(block)
            documents.append((path.name, document))
            count = 0
            for node in walk(document):
                assert node.get('@type') != 'Tailor', path.name
                assert node.get('@id') not in {'https://mrsewingfashion.com/#tailor', 'https://mrsewingfashion.com/#localbusiness'}, path.name
                if node.get('@id') != BUSINESS_ID or '@type' not in node:
                    continue
                count += 1
                if path.name == 'about.html':
                    assert node['@type'] == 'Organization'
                    for key in ['name', 'url', 'telephone', 'email', 'logo']:
                        assert node[key] == common[key], key
                    assert node['foundingDate'] == '2019'
                    assert node['parentOrganization']['name'] == 'NINKONIYUMUTWARE NEXUS LTD'
                    assert node['alternateName'] == 'Mr Sewing'
                    continue
                if path.name == 'contact.html':
                    assert node['@type'] == 'Organization'
                    for key in ['name', 'url', 'telephone', 'email', 'logo']:
                        assert node[key] == common[key], key
                    places = [n for n in walk(document) if n.get('@type') == 'Place']
                    assert len(places) == 2
                    main, mic = places
                    assert main['openingHoursSpecification'] == common['openingHoursSpecification']
                    assert main['specialOpeningHoursSpecification'] == common['specialOpeningHoursSpecification']
                    assert main['hasMap'] == 'https://maps.app.goo.gl/qz1GzkBunkmzVKXQ6?g_st=ac'
                    assert 'appointment only' in mic['description']
                    assert 'openingHoursSpecification' not in mic and 'hasMap' not in mic
                    assert 'https://youtube.com/@mr.sewingfashion' in node['sameAs']
                    continue
                assert node['@type'] == 'ClothingStore', path.name
                assert all(node.get(key) == value for key, value in common.items()), path.name
                assert 'geo' not in node and 'review' not in node and 'aggregateRating' not in node, path.name
                days = {}
                for hours in node['openingHoursSpecification']:
                    for day in hours['dayOfWeek']:
                        day = day.removeprefix('https://schema.org/')
                        assert day not in days, (path.name, 'duplicate day', day)
                        days[day] = (hours['opens'], hours['closes'])
                expected = {day:('09:00','17:00') for day in ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday']}
                assert days == expected, path.name
                assert 'Ordinary Saturday visits do not require an appointment' in node['disambiguatingDescription']
                assert 'Sunday: by appointment only' in node['disambiguatingDescription']
                assert len(node['specialOpeningHoursSpecification']) == 24
                from datetime import date, timedelta
                for exception in node['specialOpeningHoursSpecification']:
                    day = date.fromisoformat(exception['validFrom'])
                    assert exception['validThrough'] == day.isoformat()
                    assert day.weekday() == 5 and (day + timedelta(days=7)).month != day.month
                    assert (exception['opens'],exception['closes']) == ('12:00','17:00')
                assert 'advance appointment' in node['disambiguatingDescription']
            assert count <= 1, (path.name, 'duplicate business entity')
            if count:
                business_pages.append(path.name)
    assert len(business_pages) == len(set(business_pages)) == 11, business_pages
    assert common['telephone'] == '+250787411501'
    assert common['email'] == 'mrsewingfashiondesigner@gmail.com'
    assert all('Kigali' in address['addressLocality'] and address['addressCountry'] == 'RW' for address in common['address'])
    subprocess.run(['python3','scripts/sync_business_hours.py','--check'], cwd=ROOT, check=True)
    subprocess.run(['python3','scripts/sync_business_schema.py','--check'], cwd=ROOT, check=True)
    subprocess.run(['python3','scripts/build_homepage.py','--check'], cwd=ROOT, check=True)
    subprocess.run(['python3','scripts/build_contact.py','--check'], cwd=ROOT, check=True)
    print(f'PASS: {len(documents)} JSON-LD blocks parse; 11 public business entities preserve confirmed identity and hours; Contact separately qualifies workshop and appointment-only consultation locations.')
    if options.vocabulary:
        vocabulary_check(documents, options.vocabulary)


if __name__ == '__main__':
    main()
