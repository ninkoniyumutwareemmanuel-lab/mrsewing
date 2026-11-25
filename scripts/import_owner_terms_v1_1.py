#!/usr/bin/env python3
"""Staging-only import of the owner's uploaded v1.1. Fail closed on text mismatch."""
import hashlib, json, subprocess, shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
REG=ROOT/'_data/policy-documents.json'
EXPECTED='4ba45807fd3568002c116a5df1ab9677e13adb044b8b5888426d610a0fd1eb1c'
SOURCE='Mr_Sewing_Fashion_Terms_and_Conditions_v1.1_Uploaded.pdf'
data=json.loads(REG.read_text())
doc=data['documents']['terms-and-conditions']
assert doc['currentVersion'] is None, 'Do not activate Terms on staging'
if doc['receivedVersions'][-1]['version']=='1.1':
    print('Version 1.1 already registered; immutable source checked by reader')
    raise SystemExit(0)
src=ROOT/SOURCE
raw=src.read_bytes()
assert raw.startswith(b'%PDF-'), 'Uploaded file is not a PDF'
text=subprocess.check_output(['pdftotext','-enc','UTF-8',str(src),'-']).decode('utf-8')
fingerprint=hashlib.sha256(' '.join(text.split()).encode()).hexdigest()
print('Uploaded normalized text SHA-256:',fingerprint,flush=True)
assert fingerprint==EXPECTED,'Uploaded document text differs from the owner-approved v1.1 PDF; no reader replacement performed'
info=subprocess.check_output(['pdfinfo',str(src)],text=True)
fields={k.strip():v.strip() for line in info.splitlines() if ':' in line for k,v in [line.split(':',1)]}
assert fields.get('Pages')=='6' and fields.get('Encrypted','').startswith('no'), 'Expected six unencrypted PDF pages'
assert fields.get('JavaScript','no')=='no' and fields.get('Form','none')=='none', 'Unexpected active PDF content'
source='.github/policy-documents/terms-and-conditions/1.1.pdf'
published='/assets/policy-documents/terms-and-conditions/1.1.pdf'
for target in (source,published.lstrip('/')):
    dst=ROOT/target
    dst.parent.mkdir(parents=True,exist_ok=True)
    shutil.copyfile(src,dst)
sha=hashlib.sha256(raw).hexdigest()
entry={'documentId':'terms-and-conditions','version':'1.1','approvalStatus':'approved','approvedBy':'Business owner','approvalDate':'2026-11-25','sourceReference':'Owner approved v1.1 and confirmed uploaded six-page document. Normalized complete text matched approved PDF.','publicationStatus':'staging-review','activationStatus':'awaiting-official-publication','effectiveDate':None,'effectiveDateBasis':'official-website-publication','preparedDate':'2026-11-25','originalUploadPath':SOURCE,'technicalInspection':{'pages':6,'bytes':len(raw),'pdfVersion':fields.get('PDF version'),'encrypted':False,'javascript':False,'forms':'none','selectableText':True,'legalReviewClaim':'No completed legal review is asserted.'},'reconciliation':{'status':'reviewed-awaiting-activation','reference':'Complete normalized text matched owner-approved v1.1; prior v1.0 receipt preserved. Existing effective consent remains unchanged.'},'sourceFilename':'Mr_Sewing_Fashion_Terms_and_Conditions_v1.1_Approved.pdf','sourcePath':source,'publishedPath':published,'sha256':sha}
doc['receivedVersions'].append(entry)
doc['authority']='Owner approved version 1.1 on 25 November 2026 for staging review. No official activation.'
REG.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
from render_terms_page_images import render_images
render_images()
inventory_path=ROOT/'_data/collection-image-inventory.json'
inventory=json.loads(inventory_path.read_text())
known={r['originalImagePath'] for r in inventory['images']}
for n in range(1,7):
    p='assets/policy-documents/terms-and-conditions/pages/1.1-%02d.png'%n
    assert (ROOT/p).is_file()
    if p not in known:
        inventory['images'].append({'originalImagePath':p,'sourceOriginal':p,'designId':None,'galleryLocation':None,'groupedWithOtherPhotographs':False,'provenance':'not_a_design_record','rightsStatus':'not_assessed_non_garment','missing':False,'excludedReason':'Approved Terms PDF page raster; document reader asset, not a garment reference or Shop product.','legacyReferences':['scripts/render_terms_page_images.py']})
inventory_path.write_text(json.dumps(inventory,ensure_ascii=False,indent=2)+'\n')
print('PASS: exact normalized approved text verified; six PDF page images generated; not activated')
