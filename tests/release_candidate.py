#!/usr/bin/env python3
"""Verify the preparation artifact without publishing or changing business data."""
from pathlib import Path
import json
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from prepare_release_candidate import INTERNAL, path_for, prepare, projection


class ReleaseCandidateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.files, cls.excluded = projection()

    def test_public_boundary_and_effective_terms(self):
        from prelaunch_security_content import main_body
        self.assertGreater(len(self.files), 400)
        for name in self.files:
            self.assertFalse(set(Path(name).parts) & INTERNAL, name)
            self.assertFalse(name.endswith('.pdf'), name)
            self.assertNotIn('assets/policy-documents/', name)
        for name in ('index.html', 'mensuits/index.html', 'womensuits/index.html',
                     'collections/index.html', 'guides/fabrics/index.html',
                     'services/custom-tailoring/index.html', 'sitemap.xml', 'robots.txt'):
            self.assertIn(name, self.files)
        self.assertIn('header.html', list(self.files), 'Legacy Kaunda header fetch is a required public component')
        current = (ROOT / 'terms-and-conditions/current/index.html').read_text()
        for name in ('terms-and-conditions/index.html', 'terms-and-conditions.html'):
            self.assertEqual(main_body(self.files[name].decode()), main_body(current))
        self.assertEqual(self.files['terms-and-conditions/current/index.html'].decode(), current)
        self.assertNotIn('Staging-only R59 held', self.files['_redirects'].decode())
        headers = self.files['_headers'].decode()
        self.assertIn('https://mrsewing-staging.pages.dev/*', headers)
        self.assertNotIn('https://mrsewingfashion.com/*', headers)

    def test_staging_projection_keeps_exact_review_reader(self):
        files, _ = projection(mode='staging')
        name = 'terms-and-conditions/index.html'
        self.assertEqual(files[name], (ROOT / name).read_bytes())
        self.assertIn('assets/policy-documents/terms-and-conditions/1.2.pdf', list(files))
        self.assertIn('termsPdfDialog', files[name].decode())

    def test_missing_asset_fails_closed_and_output_preserves_previous(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder) / 'source'
            root.mkdir()
            (root / 'index.html').write_text('<img src="/missing.jpg" alt="test">')
            with self.assertRaisesRegex(ValueError, 'Missing public asset'):
                projection(root, mode='staging')
            (root / 'index.html').write_text('<main>Fixture</main>')
            with self.assertRaisesRegex(ValueError, 'outside'):
                prepare(root / 'output', mode='staging', root=root)
            output = Path(folder) / 'candidate'
            result = prepare(output, mode='staging', root=root)
            self.assertFalse(result['deploymentPerformed'])
            self.assertEqual(prepare(output, mode='staging', root=root, check=True), result)
            with self.assertRaisesRegex(ValueError, 'Preserve existing'):
                prepare(output, mode='staging', root=root)
            (output / 'public/private.json').write_text('{}')
            with self.assertRaisesRegex(ValueError, 'differs'):
                prepare(output, mode='staging', root=root, check=True)

    def test_runtime_is_separate_and_references_are_contained(self):
        with tempfile.TemporaryDirectory() as folder:
            output = Path(folder) / 'candidate'
            result = prepare(output)
            self.assertGreater(len(result['runtimeBuildInputs']), 10)
            for name in result['runtimeBuildInputs']:
                self.assertTrue((output / 'runtime' / name).is_file())
                self.assertFalse((output / 'public' / name).exists())
            self.assertEqual(len(result['publicFiles']), len(self.files))
            runtime_file = output / 'runtime' / result['runtimeBuildInputs'][0]
            runtime_file.write_text('// deliberately changed fixture')
            with self.assertRaisesRegex(ValueError, 'Runtime'):
                prepare(output, check=True)
        self.assertIsNone(path_for('/_data/business.json', 'index.html', ROOT))
        self.assertIsNone(path_for('https://unrelated.example/private.json', 'index.html', ROOT))
        with self.assertRaisesRegex(ValueError, 'escapes'):
            path_for('/../../outside.png', 'index.html', ROOT)


if __name__ == '__main__':
    unittest.main()
