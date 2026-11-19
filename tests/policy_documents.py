#!/usr/bin/env python3
"""R51 approved-PDF workflow tests using temporary synthetic documents only."""
from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path
import re
import sys
from tempfile import TemporaryDirectory

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import policy_documents as policy


def rejects(callback, text=None):
    try:
        callback()
    except ValueError as error:
        if text:
            assert text in str(error), str(error)
        return
    raise AssertionError('Expected the invalid document/review to be rejected')


def fixture_pdf(label):
    """A valid one-page PDF saying only that it is a temporary test fixture."""
    content = ('BT /F1 12 Tf 30 140 Td (Temporary test fixture ' + label + ') Tj ET').encode()
    objects = [b'<< /Type /Catalog /Pages 2 0 R >>',
               b'<< /Type /Pages /Count 1 /Kids [3 0 R] >>',
               b'<< /Type /Page /Parent 2 0 R /MediaBox [0 0 300 200] /Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>',
               b'<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>',
               b'<< /Length ' + str(len(content)).encode() + b' >>\nstream\n' + content + b'\nendstream']
    data = b'%PDF-1.4\n'
    offsets = [0]
    for index, body in enumerate(objects, 1):
        offsets.append(len(data))
        data += str(index).encode() + b' 0 obj\n' + body + b'\nendobj\n'
    start = len(data)
    data += b'xref\n0 6\n0000000000 65535 f \n' + b''.join(('%010d 00000 n \n' % pos).encode() for pos in offsets[1:])
    return data + b'trailer\n<< /Size 6 /Root 1 0 R >>\nstartxref\n' + str(start).encode() + b'\n%%EOF\n'


def approval(record):
    value = deepcopy(record)
    value.update(approvalStatus='approved', approvedBy='Fictional test owner', approvalDate='2026-11-19', sourceReference='Synthetic test approval; not company Terms')
    value['reconciliation'].update(status='approved', reference='Synthetic operational review; not a legal approval', reviewedBy='Fictional test reviewer', reviewedOn='2026-11-19')
    return value


def write_registry(root, value):
    (root / policy.REGISTRY).write_text(json.dumps(value, indent=2) + '\n')


def main():
    actual = policy.validate_registry()
    assert actual['documents'][policy.DOCUMENT_ID]['currentVersion'] is None, 'No actual approved PDF was supplied for R51'
    assert not list(ROOT.glob('.github/policy-documents/**/*.pdf')), 'This test must not add a pretend company PDF'
    body = '<nav aria-label="Breadcrumb">Home / Terms</nav><section class="release-intro"><h1>Terms &amp; Conditions</h1></section><section id="2"><h2>Existing online conditions</h2><p>Existing approved explanation stays readable while PDF is pending.</p></section><section id="5"><p>Appointment conditions</p></section>'
    pending = policy.wrap_terms(body)
    assert 'PDF edition is not available yet' in pending
    assert 'Existing approved explanation stays readable' in pending
    assert '<section id="2">' in pending and '<section id="5">' in pending
    assert '<h1>Terms and Conditions</h1>' in pending
    assert 'type="application/pdf"' not in pending and 'Download PDF' not in pending
    assert not any(path.suffix == '.pdf' for path in policy.outputs())

    with TemporaryDirectory(prefix='mrsewing-policy-fixture-') as directory:
        base = Path(directory)
        root = base / 'repository'
        (root / '_data').mkdir(parents=True)
        registry = deepcopy(actual)
        for name in registry['documents'][policy.DOCUMENT_ID]['operationalSources']:
            target = root / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes((ROOT / name).read_bytes())
        write_registry(root, registry)
        source = base / 'fictional-v1.pdf'
        source.write_bytes(fixture_pdf('one'))
        review = policy.review_template(source, 'fixture-v1', '2026-11-19', root)
        assert review['approvalStatus'] == review['reconciliation']['status'] == 'pending'
        before = (root / policy.REGISTRY).read_bytes()
        rejects(lambda: policy.publish_document(source, review, root, write=True), 'approved')
        assert not list(root.rglob('*.pdf')) and (root / policy.REGISTRY).read_bytes() == before
        approved = approval(review)
        wrong = deepcopy(approved)
        wrong['documentSha256'] = '0' * 64
        rejects(lambda: policy.publish_document(source, wrong, root, write=True), 'differs')
        wrong = deepcopy(approved)
        wrong['reconciliation']['sourceFingerprints'] = {'_data/business.json': '0' * 64}
        rejects(lambda: policy.publish_document(source, wrong, root), 'reconciliation')
        planned = policy.publish_document(source, approved, root)
        assert not list(root.rglob('*.pdf')), 'Dry run must not copy a document'
        record = policy.publish_document(source, approved, root, write=True)
        assert record == planned and record['version'] == 'fixture-v1'
        assert policy.current_document(root)['version'] == 'fixture-v1'
        source_path = root / record['sourcePath']
        public_path = root / record['publishedPath'].lstrip('/')
        assert source_path.read_bytes() == public_path.read_bytes() == source.read_bytes()
        assert sha256(source.read_bytes()).hexdigest() == record['sha256']
        active = policy.wrap_terms(body, root)
        assert 'Existing approved explanation stays readable' not in active, 'Do not keep a competing full HTML Terms body'
        assert active.count('<h1>') == 1
        assert 'data-policy-document-current="fixture-v1"' in active
        assert 'type="application/pdf"' in active and '<object data="' + record['publishedPath'] + '#view=FitH"' in active
        assert 'Open PDF separately' in active and 'Download PDF' in active and 'This browser cannot display' in active
        assert 'download="fictional-v1.pdf"' in active
        assert active.count('id="2"') == active.count('id="5"') == 1
        for ident in ['2', '5', '6', '7', '8', 'mobile-fees']:
            assert 'id="' + ident + '"' in active
        assert not re.search(r'#page=\d+', active), 'No invented PDF section-to-page mapping'
        assert policy.outputs(root)[public_path] == source.read_bytes()
        rejects(lambda: policy.publish_document(source, approved, root), 'immutable')
        public_path.write_bytes(fixture_pdf('tampered'))
        rejects(lambda: policy.validate_registry(root), 'published PDF differs')
        public_path.write_bytes(source.read_bytes())
        source_path.write_bytes(fixture_pdf('tampered source'))
        rejects(lambda: policy.validate_registry(root), 'checksum')
        source_path.write_bytes(source.read_bytes())

        # A new approved version changes one pointer and retains both originals.
        second = base / 'fictional-v2.pdf'
        second.write_bytes(fixture_pdf('two'))
        new_review = approval(policy.review_template(second, 'fixture-v2', '2026-11-20', root))
        second_record = policy.publish_document(second, new_review, root, write=True)
        updated = policy.validate_registry(root)['documents'][policy.DOCUMENT_ID]
        assert updated['currentVersion'] == 'fixture-v2'
        assert updated['versions'][0]['publicationStatus'] == 'archived'
        assert updated['versions'][1]['previousVersions'] == ['fixture-v1']
        assert source_path.read_bytes() == public_path.read_bytes() == source.read_bytes(), 'Historical approved files must remain recoverable'
        assert policy.wrap_terms(body, root).count(second_record['publishedPath']) >= 3
        assert len([p for p in policy.outputs(root) if p.suffix == '.pdf']) == 2

        # Changes to operational data never silently rewrite a PDF or its rules.
        fact = root / '_data/customer-policy-facts.json'
        fact.write_text(fact.read_text() + '\n')
        rejects(lambda: policy.validate_registry(root), 'new human reconciliation')
        third = base / 'fictional-v3.pdf'
        third.write_bytes(fixture_pdf('three'))
        reviewed_again = approval(policy.review_template(third, 'fixture-v3', '2026-11-21', root))
        policy.publish_document(third, reviewed_again, root, write=True)
        assert policy.current_document(root)['version'] == 'fixture-v3', 'A genuine replacement review can reconcile changed sources'
        assert json.loads((root / policy.REGISTRY).read_text())['documents'][policy.DOCUMENT_ID]['versions'][0]['reconciliation'] == record['reconciliation']

        stray = root / 'assets/drafts/unapproved.PDF'
        stray.parent.mkdir(parents=True)
        stray.write_bytes(fixture_pdf('not approved'))
        rejects(lambda: policy.outputs(root), 'unregistered PDF')
        stray.unlink()
        escaped = deepcopy(policy.read_registry(root))
        escaped['documents'][policy.DOCUMENT_ID]['versions'][0]['sourcePath'] = '../../outside.pdf'
        rejects(lambda: policy.validate_registry(root, escaped), 'immutable')
        current = policy.current_document(root)
        current_source = root / current['sourcePath']
        saved = current_source.read_bytes()
        current_source.unlink()
        current_source.symlink_to(source)
        rejects(lambda: policy.validate_registry(root), 'leaves the repository')
        current_source.unlink()
        current_source.write_bytes(saved)
        policy.validate_registry(root)

        # A failed final registry write keeps the old published pointer and
        # removes the new immutable files rather than leaving a partial update.
        fourth = base / 'fictional-v4.pdf'
        fourth.write_bytes(fixture_pdf('four'))
        fourth_review = approval(policy.review_template(fourth, 'fixture-v4', '2026-11-22', root))
        previous_registry = (root / policy.REGISTRY).read_bytes()
        replace = policy.os.replace
        try:
            policy.os.replace = lambda *_args: (_ for _ in ()).throw(OSError('Synthetic registry-write failure'))
            try:
                policy.publish_document(fourth, fourth_review, root, write=True)
            except OSError as error:
                assert 'Synthetic' in str(error)
            else:
                raise AssertionError('Expected synthetic filesystem failure')
        finally:
            policy.os.replace = replace
        assert (root / policy.REGISTRY).read_bytes() == previous_registry
        assert not (root / policy.source_path(policy.DOCUMENT_ID, 'fixture-v4')).exists()
        assert not (root / policy.public_path(policy.DOCUMENT_ID, 'fixture-v4').lstrip('/')).exists()
        assert not list((root / '_data').glob('.policy-registry-*.tmp'))
        policy.validate_registry(root)

    assert policy.current_document() is None
    print('PASS: pending/no-fake-PDF fallback, approved-only dry-run/publication, immutable replacement/history, exact anchors, open/download/embed fallback, fingerprints/conflicts, checksum/path/stray-PDF guards; temporary fixtures only')


if __name__ == '__main__':
    main()
