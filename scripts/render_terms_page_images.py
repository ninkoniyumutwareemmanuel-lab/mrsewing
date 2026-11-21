#!/usr/bin/env python3
"""Render five pages of the immutable approved Terms PDF for mobile WebViews.

Manual build prerequisite for an R55 release: install poppler-utils (pdftoppm).
PNG image pixels are derived only from the verified approved PDF. The original
PDF and owner approvals remain untouched; this does not activate the policy.
"""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import struct
import subprocess
import sys
import tempfile

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from terms_reader import received_version, page_url, RENDER_DPI


def render_images(check=False):
    entry=received_version()
    count=entry['technicalInspection']['pages']
    source=ROOT/entry['sourcePath']
    destination=ROOT/'assets/policy-documents/terms-and-conditions/pages'
    executable=shutil.which('pdftoppm')
    if not executable:
        raise RuntimeError('Install poppler-utils / pdftoppm to generate genuine PDF page renders')
    with tempfile.TemporaryDirectory() as folder:
        prefix=Path(folder)/'terms'
        subprocess.run([executable,'-f','1','-l',str(count),'-r',str(RENDER_DPI),'-png',str(source),str(prefix)],check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        renders=sorted(Path(folder).glob('terms-*.png'),key=lambda p:int(p.stem.split('-')[-1]))
        if len(renders)!=count:
            raise ValueError('Expected %d original approved PDF pages; got %d' %(count,len(renders)))
        files=[]
        for number,image in enumerate(renders,1):
            raw=image.read_bytes()
            if not raw.startswith(b'\x89PNG\r\n\x1a\n') or raw[12:16]!=b'IHDR':
                raise ValueError('Invalid rendered PNG')
            width,height=struct.unpack('>II',raw[16:24])
            if (width,height)!=(1360,1760):
                raise ValueError('Unexpected PDF page dimensions: %r' % ((width,height),))
            name=Path(page_url(entry,number)).name
            target=destination/name
            if check:
                if not target.is_file() or target.read_bytes()!=raw:
                    raise ValueError('Stale Terms PDF page render '+name)
            else:
                destination.mkdir(parents=True,exist_ok=True)
                if not target.is_file() or target.read_bytes()!=raw:
                    target.write_bytes(raw)
            files.append({'page':number,'path':'/assets/policy-documents/terms-and-conditions/pages/'+name,
                          'width':width,'height':height,'sha256':hashlib.sha256(raw).hexdigest()})
        manifest={'sourcePdfSha256':entry['sha256'],'version':entry['version'],'publicationStatus':'staging-review',
                  'effectiveDate':None,'dpi':RENDER_DPI,'pages':files}
        text=json.dumps(manifest,ensure_ascii=False,indent=2)+'\n'
        target=destination/'manifest.json'
        if check:
            if not target.is_file() or target.read_text()!=text:
                raise ValueError('Stale Terms page-render manifest')
        else:
            if not target.is_file() or target.read_text()!=text:
                target.write_text(text)
    print('PASS: %d PDF-derived pages from immutable approved version %s; not activated' %(count,entry['version']))


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--check',action='store_true')
    args=parser.parse_args()
    render_images(args.check)
