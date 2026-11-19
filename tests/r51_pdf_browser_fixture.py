#!/usr/bin/env python3
"""Produce an out-of-repository synthetic PDF viewer fixture for intercepted QA.

Never writes the actual document registry, publishes a company PDF or deploys.
"""
from copy import deepcopy
import importlib.util,json,sys,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=Path('/workspace/review/r51-restructure-2026-11-19')
sys.path.insert(0,str(ROOT/'scripts'))
import policy_documents as policy
from customer_site import frame
spec=importlib.util.spec_from_file_location('r51_policy_test_helpers',ROOT/'tests/policy_documents.py');helpers=importlib.util.module_from_spec(spec);spec.loader.exec_module(helpers)
actual=deepcopy(policy.validate_registry())
assert actual['documents'][policy.DOCUMENT_ID]['currentVersion'] is None
with tempfile.TemporaryDirectory(prefix='r51-pdf-browser-') as directory:
 base=Path(directory);root=base/'repository';(root/'_data').mkdir(parents=True)
 for name in actual['documents'][policy.DOCUMENT_ID]['operationalSources']:
  target=root/name;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes((ROOT/name).read_bytes())
 (root/policy.REGISTRY).write_text(json.dumps(actual))
 source=base/'synthetic-r51-fixture.pdf';source.write_bytes(helpers.fixture_pdf('browser only'))
 approved=helpers.approval(policy.review_template(source,'synthetic-browser','2026-11-19',root))
 record=policy.publish_document(source,approved,root,write=True)
 body='<section class="release-intro"><h1>Terms and Conditions</h1><p>Temporary synthetic viewer test, not company Terms.</p></section><section id="2"><p>LEGACY_TERM_SENTINEL_NOT_FOR_PDF</p></section>'
 content=policy.wrap_terms(body,root);assert 'LEGACY_TERM_SENTINEL_NOT_FOR_PDF' not in content
 html=frame('/terms-and-conditions/','Synthetic PDF viewer test','Temporary synthetic fixture, not company Terms.',content)
 # The existing Terms frame already includes the scoped viewer assets once.
 OUT.mkdir(parents=True,exist_ok=True);(OUT/'synthetic-pdf-viewer.html').write_text(html);(OUT/'synthetic-pdf-viewer.pdf').write_bytes(source.read_bytes());(OUT/'synthetic-pdf-viewer.json').write_text(json.dumps({'route':'/terms-and-conditions/?qa=synthetic-pdf','pdfPath':record['publishedPath'],'version':record['version'],'realCompanyDocument':False},indent=2)+'\n')
print('PASS synthetic PDF browser fixture saved outside repository; actual registry remains pending')
