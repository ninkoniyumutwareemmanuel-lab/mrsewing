#!/usr/bin/env python3
"""Publication safety tests for the optional, owner-approved About profile."""
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'scripts'))
from build_about import leadership_section


class LeadershipPublication(unittest.TestCase):
    def fixture(self):
        return {'published':True, 'approvalStatus':'approved',
            'name':'Fictional Test Person', 'title':'Approved Test Title',
            'biography':'Fictional test biography, not company information.',
            'portrait':{'path':'assets/images/logo-icon.png', 'alt':'Synthetic test reference',
                'width':32, 'height':32, 'publicationApproved':True}}

    def test_current_incomplete_record_is_not_customer_content(self):
        record = json.loads((ROOT/'_data/about-leadership.json').read_text())
        self.assertFalse(record['published'])
        self.assertEqual(leadership_section(record), '')

    def test_unapproved_publication_fails_closed(self):
        record = self.fixture()
        record['approvalStatus'] = 'pending-owner-content'
        with self.assertRaises(ValueError):
            leadership_section(record)

    def test_incomplete_required_content_fails_closed(self):
        for key in ('name', 'title', 'biography'):
            record = self.fixture()
            record[key] = None
            with self.subTest(key=key), self.assertRaises(ValueError):
                leadership_section(record)

    def test_unauthorized_and_external_portraits_are_rejected(self):
        for changed in ({'publicationApproved':False}, {'path':'../../etc/passwd'},
                        {'path':'https://example.test/portrait.jpg'}, {'alt':''}, {'width':0}):
            record = self.fixture()
            record['portrait'].update(changed)
            with self.subTest(change=changed), self.assertRaises(ValueError):
                leadership_section(record)

    def test_approved_plain_text_is_escaped(self):
        record = self.fixture()
        record['name'] = '<script>test</script>'
        record['biography'] = 'Text & <strong>not HTML</strong>'
        record['motivation'] = 'Optional approved statement.'
        rendered = leadership_section(record)
        self.assertIn('&lt;script&gt;test&lt;/script&gt;', rendered)
        self.assertIn('Text &amp; &lt;strong&gt;not HTML&lt;/strong&gt;', rendered)
        self.assertNotIn('<script>', rendered)
        self.assertIn('Optional approved statement.', rendered)
        self.assertNotIn('{{', rendered)


if __name__ == '__main__':
    unittest.main()
