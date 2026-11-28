#!/usr/bin/env python3
"""New publication contract fixtures; no approved media data is edited."""
from copy import deepcopy
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from media_sorting import newest_first, verified_publication


def record(ident, stamp=None, category='men', published=True):
    return {'id': ident, 'published_at': stamp, 'published_at_evidence': 'Synthetic fixture only',
            'category': category, 'published': published, 'rightsStatus': 'approved',
            'images': [{'src': ident + '-front.jpg'}, {'src': ident + '-detail.jpg'}]}


class PublicationOrderTests(unittest.TestCase):
    def test_publication_order_before_pagination_filter_and_family_views(self):
        source = [record('unknown'), record('old', '2026-01-01T10:00:00+02:00'),
                  record('held', '2026-12-01T00:00:00Z', published=False),
                  record('new', '2026-11-28T12:00:00+02:00'),
                  record('women', '2026-11-28T11:00:00Z', category='women')]
        eligible = [x for x in source if x['published'] and x['rightsStatus'] == 'approved']
        ordered = newest_first(eligible)
        self.assertEqual([x['id'] for x in ordered], ['women', 'new', 'old', 'unknown'])
        self.assertEqual(ordered[:1][0]['id'], 'women')
        category = newest_first([x for x in eligible if x['category'] == 'men'])
        self.assertEqual(category[0]['id'], 'new')
        self.assertEqual(category[0]['images'], source[3]['images'])
        self.assertEqual(len(category[0]['images']), 2)
        self.assertNotIn('held', [x['id'] for x in ordered])
        self.assertIn('old', [x['id'] for x in ordered])

    def test_timezone_normalization_and_stable_identifier_ties(self):
        a = record('a', '2026-11-28T12:00:00+02:00')
        z = record('z', '2026-11-28T10:00:00Z')
        self.assertEqual(verified_publication(a), verified_publication(z))
        self.assertEqual([x['id'] for x in newest_first([z, a])], ['a', 'z'])
        self.assertEqual(newest_first([z, a]), newest_first([a, z]))

    def test_unknown_invalid_or_unproven_dates_keep_legacy_order(self):
        rows = [record('z'), record('a', '2026-11-28'), record('b', '2026-11-28T12:00:00')]
        no_evidence = record('c', '2026-11-28T12:00:00Z')
        no_evidence['published_at_evidence'] = ''
        rows.append(no_evidence)
        rows.append(record('invalid', '2026-02-30T12:00:00Z'))
        self.assertTrue(all(verified_publication(x) is None for x in rows))
        self.assertEqual(newest_first(rows), rows)

    def test_metadata_edits_do_not_republish_and_projection_uses_authority(self):
        a, b = record('a', '2026-11-27T10:00:00Z'), record('b', '2026-11-28T10:00:00Z')
        edited = deepcopy(a)
        edited.update(name='Revised description', updated_at='2026-12-01T00:00:00Z')
        self.assertEqual([x['id'] for x in newest_first([edited, b])], ['b', 'a'])
        projected = [{'id': 'a'}, {'id': 'b'}]
        self.assertEqual(newest_first(projected, {'a': edited, 'b': b}), list(reversed(projected)))
        self.assertEqual(projected, [{'id': 'a'}, {'id': 'b'}])

    def test_legacy_upload_is_fallback_and_not_claimed_publication(self):
        legacy = {'id': 'legacy', 'mediaDateAdded': '2026-11-30',
                  'mediaDateEvidence': 'Synthetic upload fixture', 'mediaDateBasis': 'verified-upload'}
        actual = record('publication', '2026-11-28T10:00:00Z')
        self.assertIsNone(verified_publication(legacy))
        self.assertEqual([x['id'] for x in newest_first([legacy, record('unknown'), actual])],
                         ['publication', 'legacy', 'unknown'])

    def test_actual_project_loader_gates_and_orders_whole_families(self):
        import project_catalog
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / '_data').mkdir()
            source = []
            for ident, stamp, published in [('older', '2026-11-27T12:00:00+02:00', True),
                                            ('held', '2026-12-01T12:00:00+02:00', False),
                                            ('newest', '2026-11-28T12:00:00+02:00', True)]:
                photo = '/' + ident + '.jpg'
                (root / photo.lstrip('/')).write_bytes(b'synthetic existence fixture')
                source.append({'slug': ident, 'title': ident, 'context': 'Private fixture',
                               'published': published, 'completedWorkEvidence': 'Synthetic fixture',
                               'published_at': stamp, 'published_at_evidence': 'Synthetic timestamp fixture',
                               'publicationPermission': {'approved': True, 'evidenceRef': 'Synthetic fixture'},
                               'images': [{'src': photo, 'alt': ident, 'width': 100, 'height': 150,
                                           'permissionEvidenceRef': 'Synthetic fixture',
                                           'projectAssociationEvidenceRef': 'Synthetic fixture'}]})
            (root / '_data/customer-projects.json').write_text(json.dumps({'projects': source}))
            with patch.object(project_catalog, 'ROOT', root):
                projects = project_catalog.projects()
            self.assertEqual([x['slug'] for x in projects], ['newest', 'older'])
            self.assertEqual(projects[0]['images'], source[2]['images'])


if __name__ == '__main__':
    unittest.main()
