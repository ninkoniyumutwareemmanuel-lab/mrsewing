#!/usr/bin/env python3
"""R56 owner-approved tailoring-first homepage and photo-rights regressions."""
import json
import re
import sys
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from homepage_redesign import render,source_families,gallery_rows,stable_legacy_families,_allowed_video

class HomepageR56Tests(unittest.TestCase):
    def test_new_r53_photos_are_authorized_as_references_only(self):
        registry=json.loads((ROOT/'_data/collection-designs.json').read_text())
        new=[r for r in registry['designs'] if (r.get('homepagePublication') or {}).get('approved')]
        self.assertEqual(len(new),22)
        self.assertEqual(sum(len(d['images']) for d in new),25)
        for design in new:
            self.assertEqual(design['rightsStatus'],'approved')
            self.assertEqual(design['homepagePublication']['approvalBasis'],'owner-attested-commercial-use-rights')
            self.assertFalse(design['homepagePublication']['independentThirdPartyLicenseInspected'])
            self.assertEqual(design['published'],False,'Never auto-publish Shop or Showroom')
            self.assertEqual(design['classification'],'reference-design')
            self.assertEqual(design['homepageUploadTimestamp'],'2026-11-19T17:32:12Z')
        self.assertEqual(registry['nextId'],174)

    def test_grouped_photographs_and_burgundy_image12(self):
        groups=source_families()
        self.assertEqual(len(groups),17)
        self.assertEqual(sum(len(g['photos']) for g in groups),25)
        ids=[g['id'] for g in groups]
        self.assertEqual(len(ids),len(set(ids)))
        sovereign=next(g for g in groups if g['id']=='sovereign-gold-button-elegance')
        self.assertEqual(len(sovereign['photos']),5)
        records=json.loads((ROOT/'_data/collection-designs.json').read_text())['designs']
        burgundy=next(r for r in records if r['id']=='MS-156')
        olive=next(r for r in records if r['id']=='MS-157')
        self.assertEqual(burgundy['family']['variant']['label'],'Burgundy')
        self.assertIn('01-olive.webp',burgundy['images'][1]['originalPath'])
        self.assertNotEqual(olive['images'][0]['originalPath'],burgundy['images'][1]['originalPath'])
        heritage=next(g for g in groups if g['id']=='ivory-heritage-elegance')
        self.assertEqual(len(heritage['photos']),3)

    def test_newest_first_and_stable_unknown_date_order(self):
        first,second=gallery_rows()
        for lane in (first,second):
            timestamps=[g['timestamp'] for g in lane if g['timestamp'] is not None]
            self.assertEqual(timestamps,sorted(timestamps,reverse=True))
            self.assertIsNotNone(lane[0]['timestamp'])
            previous_undated=False
            for g in lane:
                if g['timestamp'] is None:previous_undated=True
                elif previous_undated:self.fail('Dated item placed after older undated item')
        self.assertEqual(sum(len(g['photos']) for lane in (first,second) for g in lane if g['timestamp'] is not None),25)
        self.assertEqual(len(stable_legacy_families()),8)
        from build_collections import load
        self.assertEqual(len(load()[0]),28,'Existing eligible Showroom set must stay at its R55 baseline')
        first_again,second_again=gallery_rows()
        self.assertEqual([[g['id'] for g in first],[g['id'] for g in second]],
                         [[g['id'] for g in first_again],[g['id'] for g in second_again]])

    def test_video_gates_remain_fully_closed(self):
        videos=json.loads((ROOT/'_data/media-video-records.json').read_text())['videos']
        self.assertEqual(len(videos),2)
        self.assertFalse(any(_allowed_video(v) for v in videos))
        for video in videos:
            self.assertFalse(video['usageRights']['approved'])
            self.assertFalse(video['metadataApproval']['approved'])
            self.assertIsNone(video['posterMediaId'])
        s=render()
        self.assertEqual(s.count('class="r56-showcase-card"'),2)
        self.assertNotIn('<video',s)
        self.assertNotIn('1024X768VIDEO.mp4',s)
        self.assertNotIn('1024X768black.mp4',s)

    def test_homepage_structure_and_consent(self):
        html=(ROOT/'index.html').read_text()
        self.assertEqual(len(re.findall(r'<h1\b',html)),1)
        self.assertIn('Professional <em>Tailor</em> in Kigali, Rwanda',html)
        self.assertIn('Send Your Design on WhatsApp',html)
        self.assertIn('data-whatsapp-modal',html)
        self.assertIn('Explore Clothing Designs',html)
        self.assertIn('Tailoring &amp; Clothing Services',html)
        self.assertIn('VIP Services',html)
        self.assertIn('/services/vip/',html)
        self.assertIn('data-direction="left"',html)
        self.assertIn('data-direction="right"',html)
        self.assertIn('data-r56-pause',html)
        self.assertEqual(html.count('data-home-gallery'),2)
        self.assertIn('id="supportForm"',html)
        self.assertIn('href="/terms-and-conditions/current/"',html)
        self.assertNotIn('Six Simple <em>Steps</em>',html)
        self.assertNotIn('Explore Your <em>Order Options</em>',html)
        self.assertNotIn('<video',html)
        self.assertNotIn('1024X768black.mp4',html)
        self.assertIn('rel="canonical" href="https://mrsewingfashion.com/"',html)
        self.assertIn('noindex',html.lower(),'staging noindex SEO remains enforced')
        self.assertIn('data-legacy-url',html)

    def test_usable_without_javascript_or_motion(self):
        css=(ROOT/'_templates/homepage-redesign.css').read_text()
        js=(ROOT/'_templates/homepage-redesign.js').read_text()
        self.assertIn('@media(prefers-reduced-motion:reduce)',css)
        self.assertIn('overflow-x:auto',css)
        self.assertIn('r56-move-left',css)
        self.assertIn('r56-move-right',css)
        self.assertIn('data-paused',js)
        self.assertIn('Resume motion',js)
        self.assertIn("e.key==='Escape'",js)

if __name__=='__main__':
    unittest.main()
