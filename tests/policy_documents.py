#!/usr/bin/env python3
"""Approved-PDF workflow and received-review gates; mutations use temporary fixtures."""
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
    document = actual['documents'][policy.DOCUMENT_ID]
    assert document['currentVersion'] is None, 'Official activation awaits its real publication date and operational reconciliation'
    received = document.get('receivedVersions', [])
    assert len(received) == 1 and received[0]['approvalStatus'] == 'approved'
    assert received[0]['effectiveDate'] is None and received[0]['effectiveDateBasis'] == 'official-website-publication'
    assert received[0]['preparedDate'] == '2026-11-19'
    assert received[0]['technicalInspection']['companyRegistrationDate'] is None
    body = '<nav aria-label="Breadcrumb">Home / Terms</nav><section class="release-intro"><h1>Terms &amp; Conditions</h1></section><section id="2"><h2>Existing online conditions</h2><p>Existing approved explanation stays readable while PDF is pending.</p></section><section id="5"><p>Appointment conditions</p></section>'
    pending = policy.wrap_terms(body)
    assert 'owner-approved PDF' in pending
    assert 'Existing approved explanation stays readable' in pending
    assert '<section id="2">' in pending and '<section id="5">' in pending
    assert '<h1>Terms and Conditions</h1>' in pending
    assert 'type="application/pdf"' in pending and 'Download PDF' in pending
    assert 'data-policy-document-review="1.0"' in pending
    assert 'data-policy-document-current' not in pending
    assert 'date not yet set' in pending
    for record in received:
        uploaded = (ROOT / record['originalUploadPath']).read_bytes()
        assert sha256(uploaded).hexdigest() == record['sha256']
        assert policy.outputs()[ROOT / record['publishedPath'].lstrip('/')] == uploaded

    with TemporaryDirectory(prefix='mrsewing-policy-fixture-') as directory:
        base = Path(directory)
        root = base / 'repository'
        (root / '_data').mkdir(parents=True)
        registry = deepcopy(actual)
        registry['documents'][policy.DOCUMENT_ID]['receivedVersions'] = []
        registry['documents'][policy.DOCUMENT_ID]['pendingNotice'] = 'The PDF edition is not available yet. You can read the current Terms and Conditions below.'
        for name in registry['documents'][policy.DOCUMENT_ID]['operationalSources']:
            target = root / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes((ROOT / name).read_bytes())
        write_registry(root, registry)
        plain_pending = policy.wrap_terms(body, root)
        assert 'PDF edition is not available yet' in plain_pending
        assert 'type="application/pdf"' not in plain_pending and 'Download PDF' not in plain_pending
        assert not any(path.suffix == '.pdf' for path in policy.outputs(root))
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

        # A received PDF with genuine content-approval metadata can be reviewed
        # without assigning a fake effective date or replacing current Terms.
        received_root = base / 'received-repository'
        (received_root / '_data').mkdir(parents=True)
        for name in registry['documents'][policy.DOCUMENT_ID]['operationalSources']:
            target = received_root / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes((ROOT / name).read_bytes())
        write_registry(received_root, registry)
        uploaded_source = base / 'received-fixture.pdf'
        uploaded_source.write_bytes(fixture_pdf('received'))
        (received_root / uploaded_source.name).write_bytes(uploaded_source.read_bytes())
        received_review = deepcopy(received[0])
        for key in ['sourcePath', 'publishedPath', 'sha256', 'sourceFilename']:
            received_review.pop(key, None)
        received_review.update(version='received-fixture', originalUploadPath=uploaded_source.name,
                               documentSha256=sha256(uploaded_source.read_bytes()).hexdigest(),
                               approvedBy='Fictional test owner', sourceReference='Synthetic received-content approval; not company publication')
        received_review['reconciliation']['sourceFingerprints'] = policy.operational_fingerprints(received_root, registry['documents'][policy.DOCUMENT_ID])
        wrong = deepcopy(received_review)
        wrong['approvalStatus'] = 'pending'
        rejects(lambda: policy.receive_document(uploaded_source, wrong, received_root), 'content approval')
        wrong = deepcopy(received_review)
        wrong['effectiveDate'] = '2026-11-19'
        rejects(lambda: policy.receive_document(uploaded_source, wrong, received_root), 'effective date')
        before = (received_root / policy.REGISTRY).read_bytes()
        plan = policy.receive_document(uploaded_source, received_review, received_root)
        assert (received_root / policy.REGISTRY).read_bytes() == before
        record_received = policy.receive_document(uploaded_source, received_review, received_root, write=True)
        assert record_received == plan
        assert policy.current_document(received_root) is None
        view_received = policy.wrap_terms(body, received_root)
        assert 'data-policy-document-review="received-fixture"' in view_received
        assert 'Existing approved explanation stays readable' in view_received
        assert 'Open PDF separately' in view_received and 'Download PDF' in view_received
        assert policy.outputs(received_root)[received_root / record_received['publishedPath'].lstrip('/')] == uploaded_source.read_bytes()
        wrong_registry = deepcopy(policy.read_registry(received_root))
        wrong_registry['documents'][policy.DOCUMENT_ID]['currentVersion'] = 'received-fixture'
        rejects(lambda: policy.validate_registry(received_root, wrong_registry), 'authoritative current')
        (received_root / uploaded_source.name).write_bytes(fixture_pdf('tampered received upload'))
        rejects(lambda: policy.validate_registry(received_root), 'content checksum')
        (received_root / uploaded_source.name).write_bytes(uploaded_source.read_bytes())
        rejects(lambda: policy.receive_document(uploaded_source, received_review, received_root), 'immutable received version')
        stray_received = received_root / 'unapproved.pdf'
        stray_received.write_bytes(fixture_pdf('stray'))
        rejects(lambda: policy.validate_registry(received_root), 'unregistered PDF')
        stray_received.unlink()
        policy.validate_registry(received_root)
        activation = policy.activation_review_template('received-fixture', policy.date.today().isoformat(), received_root)
        assert 'approvalStatus' not in activation, 'Received content approval does not need to be requested again'
        rejects(lambda: policy.activate_received_document('received-fixture', activation, received_root), 'confirmed actual')
        activation['officialPublication'].update(status='confirmed', reference='Synthetic official-publication event for fixture only')
        activation['reconciliation'].update(status='approved', reference='Synthetic activation reconciliation only', reviewedBy='Fictional test reviewer', reviewedOn=policy.date.today().isoformat())
        wrong = deepcopy(activation)
        wrong['documentSha256'] = '0' * 64
        rejects(lambda: policy.activate_received_document('received-fixture', wrong, received_root), 'exact owner-approved')
        wrong = deepcopy(activation)
        future = policy.date(policy.date.today().year + 1, 1, 1).isoformat()
        wrong['effectiveDate'] = wrong['officialPublication']['date'] = future
        rejects(lambda: policy.activate_received_document('received-fixture', wrong, received_root), 'future planned')
        wrong = deepcopy(activation)
        wrong['reconciliation']['sourceFingerprints']['_data/business.json'] = '0' * 64
        rejects(lambda: policy.activate_received_document('received-fixture', wrong, received_root), 'new human reconciliation')
        wrong = deepcopy(activation)
        wrong['effectiveDate'] = wrong['officialPublication']['date'] = '2026-11-18'
        rejects(lambda: policy.activate_received_document('received-fixture', wrong, received_root), 'cannot precede')
        before = (received_root / policy.REGISTRY).read_bytes()
        unchanged_files = {p: p.read_bytes() for p in received_root.rglob('*.pdf')}
        active_plan = policy.activate_received_document('received-fixture', activation, received_root)
        assert (received_root / policy.REGISTRY).read_bytes() == before
        replace = policy.os.replace
        try:
            policy.os.replace = lambda *_args: (_ for _ in ()).throw(OSError('Synthetic activation-write failure'))
            try:
                policy.activate_received_document('received-fixture', activation, received_root, write=True)
            except OSError as error:
                assert 'Synthetic' in str(error)
            else:
                raise AssertionError('Expected synthetic activation write failure')
        finally:
            policy.os.replace = replace
        assert (received_root / policy.REGISTRY).read_bytes() == before
        assert not list((received_root / '_data').glob('.policy-registry-*.tmp'))
        activated = policy.activate_received_document('received-fixture', activation, received_root, write=True)
        assert activated == active_plan and activated['version'] == 'received-fixture'
        assert activated['approvalDate'] == received_review['approvalDate'] and activated['sourceReference'] == received_review['sourceReference']
        activated_document = policy.validate_registry(received_root)['documents'][policy.DOCUMENT_ID]
        assert activated_document['currentVersion'] == 'received-fixture'
        assert activated_document['receivedVersions'] == []
        assert activated_document['receiptHistory'] == [record_received]
        assert all(p.read_bytes() == data for p, data in unchanged_files.items()), 'Activation must reuse exact immutable PDF paths and bytes'
        assert 'data-policy-document-current="received-fixture"' in policy.wrap_terms(body, received_root)
        assert 'Existing approved explanation stays readable' not in policy.wrap_terms(body, received_root)
        replacement = base / 'after-received-fixture.pdf'
        replacement.write_bytes(fixture_pdf('after received'))
        replacement_review = approval(policy.review_template(replacement, 'after-received', '2026-11-20', received_root))
        policy.publish_document(replacement, replacement_review, received_root, write=True)
        replaced_document = policy.validate_registry(received_root)['documents'][policy.DOCUMENT_ID]
        assert replaced_document['receiptHistory'] == [record_received]
        assert replaced_document['currentVersion'] == 'after-received'
        assert all(p.read_bytes() == data for p, data in unchanged_files.items())

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
    print('PASS: actual approved received-PDF review with unset official effective date/current Terms preserved; pending fallback, approved-only publication, immutable history, exact anchors, viewer/open/download, fingerprints/conflicts/checksum/path/stray-PDF guards; all mutations temporary fixtures')


if __name__ == '__main__':
    main()
