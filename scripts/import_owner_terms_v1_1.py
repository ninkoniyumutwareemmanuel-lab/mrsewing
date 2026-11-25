#!/usr/bin/env python3
"""Inspect the historical v1.1-named upload without misidentifying its contents.

The latest upload is actually Version 1.2. Its owner-authorized staging review
is registered separately; it is not proof of the missing approved Version 1.1.
This historical command no longer silently mutates the registry during builds.
"""
import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SOURCE='Mr_Sewing_Fashion_Terms_and_Conditions_v1.1_Uploaded.pdf'
# Historical attempted import expectation, preserved as evidence, not promoted
# to a verified approved-document fingerprint. No independent source was found.
HISTORICAL_EXPECTED='4ba45807fd3568002c116a5df1ab9677e13adb044b8b5888426d610a0fd1eb1c'


def inspect_upload():
    source=ROOT/SOURCE
    raw=source.read_bytes()
    if not raw.startswith(b'%PDF-'):
        raise ValueError('Uploaded file is not a PDF')
    text=subprocess.check_output(['pdftotext','-enc','UTF-8',str(source),'-']).decode('utf-8')
    info=subprocess.check_output(['pdfinfo',str(source)],text=True)
    fields={k.strip():v.strip() for line in info.splitlines() if ':' in line for k,v in [line.split(':',1)]}
    versions=sorted(set(re.findall(r'\bVERSION\s+(\d+\.\d+)\b',text)))
    headings=list(dict.fromkeys(re.findall(r'^(\d+)\.\s+([^\n]+)',text,re.M)))
    normalized=hashlib.sha256(' '.join(text.split()).encode()).hexdigest()
    return {'sourcePath':SOURCE,'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw),
            'pages':int(fields['Pages']),'declaredVersions':versions,'numberedSections':len(headings),
            'sectionHeadings':[number+'. '+title for number,title in headings],
            'normalizedCompleteTextSha256':normalized,'historicalExpectedTextSha256':HISTORICAL_EXPECTED,
            'matchesHistoricalExpectation':normalized==HISTORICAL_EXPECTED,
            'matchesRequestedV1_1Identity':versions==['1.1'] and len(headings)==14,
            'encrypted':not fields.get('Encrypted','').startswith('no'),
            'javascript':fields.get('JavaScript','no')!='no','forms':fields.get('Form','none'),
            'approvedLibraryCopyAvailable':False,'officialActivation':False}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check',action='store_true',help='Verify actual registered staging-review document; never activate or import v1.1')
    parser.add_argument('--inspect',action='store_true',help='Print full identity comparison and preserve all files')
    args=parser.parse_args()
    result=inspect_upload()
    if args.inspect:
        print(json.dumps(result,ensure_ascii=False,indent=2))
        return
    if args.check:
        from terms_reader import received_version,page_manifest
        entry=received_version()
        if entry['originalUploadPath']!=SOURCE or entry['sha256']!=result['sha256']:
            raise ValueError('Actual latest upload is not the registered staging-review document')
        if result['declaredVersions']!=[entry['version']] or result['pages']!=entry['technicalInspection']['pages']:
            raise ValueError('Registered document identity does not match the actual PDF contents')
        page_manifest(entry)
        print('PASS: actual uploaded Version '+entry['version']+' registered for staging review; not verified as v1.1 and not activated')
        return
    raise SystemExit('BLOCKED: this v1.1-named upload declares Version '+','.join(result['declaredVersions'])+
                     ' with '+str(result['numberedSections'])+' sections. The approved 14-section Version 1.1 source is unavailable. '
                     'No import or activation performed. Use --inspect or --check for read-only review verification.')


if __name__=='__main__':
    main()
