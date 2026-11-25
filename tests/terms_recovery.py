#!/usr/bin/env python3
"""Recovery25Nov: actual PDF identity, fail-closed import and immutable reader data."""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import terms_reader as reader
from import_owner_terms_v1_1 import inspect_upload


class TermsRecoveryTests(unittest.TestCase):
    def test_full_uploaded_identity_is_not_approved_v1_1(self):
        report=inspect_upload()
        self.assertEqual(report['declaredVersions'],['1.2'])
        self.assertEqual(report['pages'],6)
        self.assertEqual(report['numberedSections'],20)
        self.assertFalse(report['matchesHistoricalExpectation'])
        self.assertFalse(report['matchesRequestedV1_1Identity'])
        self.assertFalse(report['approvedLibraryCopyAvailable'])
        self.assertFalse(report['encrypted'])
        self.assertFalse(report['javascript'])
        self.assertEqual(report['forms'],'none')
        self.assertEqual(report['sha256'],'d12476d31e6ac6d2943a6f18c2577774b5905f985ca9d8d5521624a5f4a77cb0')
        self.assertEqual(report['normalizedCompleteTextSha256'],'5c7123f88ea7971cb38c9d5dea052167041d50ba42763316b14af59ba57b7d45')

    def test_old_unconditional_import_cannot_claim_v1_1(self):
        target=ROOT/'_data/policy-documents.json'
        before=target.read_bytes()
        result=subprocess.run([sys.executable,str(ROOT/'scripts/import_owner_terms_v1_1.py')],capture_output=True,text=True)
        self.assertNotEqual(result.returncode,0)
        self.assertIn('BLOCKED',result.stderr)
        self.assertIn('Version 1.2',result.stderr)
        self.assertEqual(target.read_bytes(),before)

    def test_registered_review_is_exact_upload_and_never_activation(self):
        doc=json.loads((ROOT/'_data/policy-documents.json').read_text())['documents']['terms-and-conditions']
        entry=reader.received_version()
        self.assertEqual([e['version'] for e in doc['receivedVersions']],['1.0','1.2'])
        self.assertEqual(entry['approvalStatus'],'approved-for-staging-review')
        self.assertIsNone(doc['currentVersion'])
        self.assertIsNone(entry['effectiveDate'])
        for key in ('originalUploadPath','sourcePath','publishedPath'):
            self.assertEqual(hashlib.sha256((ROOT/entry[key].lstrip('/')).read_bytes()).hexdigest(),entry['sha256'])
        manifest=reader.page_manifest(entry)
        self.assertEqual([p['page'] for p in manifest['pages']],[1,2,3,4,5,6])
        self.assertEqual(manifest['rendering'],{'widthPixels':1360})

    def test_mutated_page_manifest_or_pdf_fails_in_temporary_fixture(self):
        data=json.loads((ROOT/'_data/policy-documents.json').read_text())
        entry=data['documents']['terms-and-conditions']['receivedVersions'][-1]
        manifest_path=Path('assets/policy-documents/terms-and-conditions/pages/manifest.json')
        manifest=json.loads((ROOT/manifest_path).read_text())
        with tempfile.TemporaryDirectory() as folder:
            fixture=Path(folder)
            paths={'_data/policy-documents.json',str(manifest_path)}
            for record in data['documents']['terms-and-conditions']['receivedVersions']:
                paths.update(record[k].lstrip('/') for k in ('originalUploadPath','sourcePath','publishedPath'))
            paths.update(p['path'].lstrip('/') for p in manifest['pages'])
            for path in paths:
                target=fixture/path;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/path,target)
            with patch.object(reader,'ROOT',fixture):
                reader.received_version();reader.page_manifest(entry)
                path=fixture/manifest['pages'][0]['path'].lstrip('/')
                original=path.read_bytes();path.write_bytes(original+b'tamper')
                with self.assertRaisesRegex(ValueError,'checksum'):reader.page_manifest(entry)
                path.write_bytes(original)
                invalid=json.loads(json.dumps(manifest));invalid['pages'][1]['page']=1
                (fixture/manifest_path).write_text(json.dumps(invalid))
                with self.assertRaisesRegex(ValueError,'order/path'):reader.page_manifest(entry)
                (fixture/manifest_path).write_text(json.dumps(manifest))
                old=data['documents']['terms-and-conditions']['receivedVersions'][0]
                path=fixture/old['sourcePath'];path.write_bytes(path.read_bytes()+b'tamper')
                with self.assertRaisesRegex(ValueError,'checksum/path'):reader.received_version()


if __name__=='__main__':unittest.main()
