#!/usr/bin/env python3
"""Preview-only projection/generation fixtures; no credentials or deploy calls."""
import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('rebuild_preview_builder', ROOT / 'scripts/build_rebuild_preview.py')
tool = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tool)


class RebuildPreviewBuildTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        (self.root / '_data').mkdir()
        (self.root / '_templates').mkdir()
        shutil.copyfile(ROOT / '_templates/rebuild-preview-worker.js', self.root / '_templates/rebuild-preview-worker.js')
        self.settings = json.loads((ROOT / '_data/rebuild-preview.json').read_text())
        self.save()

    def save(self):
        (self.root / '_data/rebuild-preview.json').write_text(json.dumps(self.settings))

    def tearDown(self):
        self.temp.cleanup()

    def test_root_worker_allowlist_excludes_hosting_source_and_uses_safe_projections(self):
        (self.root / 'index.html').write_text('<h1>Home</h1>')
        (self.root / 'robots.txt').write_text('Allow: /')
        files = {'index.html': b'<h1>Home</h1>', 'terms-and-conditions/index.html': b'<h1>Effective terms</h1>', 'robots.txt': b'Allow: /', '_headers': b'host rules', '_redirects': b'alias rules', '.nojekyll': b''}
        result = tool.outputs(self.root, branch='phase1/customer-journey-repairs', projection_fn=lambda **_: (files, []))
        self.assertEqual(set(p.name for p in result), {'_worker.js', '_routes.json'})
        worker = result[self.root / '_worker.js']
        self.assertIn('Effective terms', worker)
        self.assertNotIn('host rules', worker)
        self.assertNotIn('alias rules', worker)
        self.assertIn('"index.html":{"type":"text/html; charset=utf-8"}', worker)
        self.assertEqual(json.loads(result[self.root / '_routes.json']), {'version': 1, 'include': ['/*'], 'exclude': []})

    def test_main_unrelated_project_and_enquiry_activation_rejected(self):
        for branch in ('main', 'release/unapproved', 'detached'):
            with self.subTest(branch=branch), self.assertRaises(ValueError):
                tool.outputs(self.root, branch=branch)
        for key, value in [('project', 'mrsewingfashion'), ('submissionsEnabled', True), ('trackingEnabled', True), ('tokenSha256', 'not-a-hash')]:
            invalid = dict(self.settings, **{key: value})
            with self.subTest(key=key), self.assertRaises(ValueError):
                tool.validate(invalid, 'phase1/customer-journey-repairs')

    def test_absent_config_is_noop(self):
        (self.root / '_data/rebuild-preview.json').unlink()
        self.assertEqual(tool.outputs(self.root, branch='main'), {})


if __name__ == '__main__':
    unittest.main()
