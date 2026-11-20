"""Approved, versioned PDF policy publication and a progressively enhanced viewer.

The current document is selected explicitly. No legal text is extracted, inferred
or promoted from a PDF. Operational-source fingerprints require a recorded human
reconciliation before a changed document can be published.
"""
from copy import deepcopy
from datetime import date
from hashlib import sha256
from html import escape
import json
import os
from pathlib import Path, PurePosixPath
import re
import tempfile

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = '_data/policy-documents.json'
DOCUMENT_ID = 'terms-and-conditions'
MAX_PDF_BYTES = 20 * 1024 * 1024
VERSION = re.compile(r'[A-Za-z0-9][A-Za-z0-9._-]{0,79}\Z')
HASH = re.compile(r'[a-f0-9]{64}\Z')


def _fail(message):
    raise ValueError('Policy document: ' + message)


def _text(value, name, maximum=400):
    if not isinstance(value, str) or not value.strip() or len(value) > maximum or re.search(r'[\x00-\x1f\x7f]', value):
        _fail('provide a valid ' + name)
    return value.strip()


def _date(value, name):
    try:
        if not isinstance(value, str) or not re.fullmatch(r'\d{4}-\d{2}-\d{2}', value):
            raise ValueError
        date.fromisoformat(value)
    except (TypeError, ValueError):
        _fail('provide a valid ' + name)
    return value


def _relative(value, name):
    text = _text(value, name)
    p = PurePosixPath(text)
    if p.is_absolute() or '..' in p.parts or str(p) != text or '\\' in text:
        _fail('invalid ' + name)
    return text


def _file(root, relative):
    """Do not accept symlinks escaping the repository, even in source metadata."""
    path = root / relative
    if not path.resolve().is_relative_to(root.resolve()):
        _fail('source path leaves the repository')
    return path


def source_path(document_id, version):
    return '.github/policy-documents/' + document_id + '/' + version + '.pdf'


def public_path(document_id, version):
    return '/assets/policy-documents/' + document_id + '/' + version + '.pdf'


def _pdf(data):
    # This is an integrity/format boundary, not a security or accessibility audit.
    if not isinstance(data, bytes) or not 8 < len(data) <= MAX_PDF_BYTES or not data.startswith(b'%PDF-') or not data.rstrip().endswith(b'%%EOF'):
        _fail('the approved source must be a PDF of at most 20 MiB')


def _external_pdf(pdf_path, root):
    """Drafts/review copies must stay outside the deployed repository."""
    path = Path(pdf_path)
    if path.resolve().is_relative_to(root.resolve()):
        _fail('keep the unregistered PDF outside the repository until approved publication')
    if not path.is_file() or path.stat().st_size > MAX_PDF_BYTES:
        _fail('supply a readable external PDF of at most 20 MiB')
    if not path.name.lower().endswith('.pdf'):
        _fail('the original source filename must end in .pdf')
    data = path.read_bytes()
    _pdf(data)
    return data


def read_registry(root=ROOT):
    try:
        value = json.loads((root / REGISTRY).read_text())
    except (OSError, ValueError) as error:
        _fail('cannot read the document registry: ' + str(error))
    return value


def operational_fingerprints(root, document):
    paths = document.get('operationalSources')
    if not isinstance(paths, list) or not paths or len(paths) != len(set(paths)):
        _fail('list the authoritative operational sources once')
    output = {}
    for entry in paths:
        name = _relative(entry, 'operational source')
        if not name.startswith('_data/') or not name.endswith('.json') or name == REGISTRY:
            _fail('operational sources must identify authoritative JSON data, not the document registry')
        path = _file(root, name)
        if not path.is_file():
            _fail('missing operational source ' + name)
        output[name] = sha256(path.read_bytes()).hexdigest()
    return output


def _received_versions(root, document, expected_sources, staged_files, allowed_pdf_paths, allow_stale_current=False):
    """Approved content may be staged without inventing its official effective date.

    This is not a second publication gate: these records cannot become the
    authoritative currentVersion. A dated, reconciled normal publication is
    still required for that. Every source/upload/public copy remains hashed.
    """
    records = document.get('receivedVersions', [])
    history = document.get('receiptHistory', [])
    if not isinstance(records, list) or not isinstance(history, list):
        _fail('received versions must be a list')
    seen = set()
    for version, historical in [(v, False) for v in records] + [(v, True) for v in history]:
        if not isinstance(version, dict):
            _fail('invalid received document')
        label = version.get('version')
        if not isinstance(label, str) or not VERSION.fullmatch(label) or label in seen:
            _fail('received version identifiers must be unique and filename-safe')
        seen.add(label)
        if version.get('documentId') != document['id'] or version.get('approvalStatus') != 'approved':
            _fail('received PDFs require actual owner content approval')
        if version.get('publicationStatus') != 'staging-review' or version.get('activationStatus') != 'awaiting-official-publication':
            _fail('received PDFs cannot bypass the official publication gate')
        if version.get('effectiveDate') is not None or version.get('effectiveDateBasis') != 'official-website-publication':
            _fail('do not invent an official effective date for a received document')
        _date(version.get('preparedDate'), 'document preparation date')
        _date(version.get('approvalDate'), 'received content approval date')
        _text(version.get('approvedBy'), 'received content approver')
        _text(version.get('sourceReference'), 'received content approval reference', 1000)
        filename = _text(version.get('sourceFilename'), 'received source filename', 180)
        if PurePosixPath(filename).name != filename or '\\' in filename or not filename.lower().endswith('.pdf'):
            _fail('preserve a received PDF basename')
        source = version.get('sourcePath')
        public = version.get('publishedPath')
        upload = version.get('originalUploadPath')
        if source != source_path(document['id'], label) or public != public_path(document['id'], label):
            _fail('use immutable received-document version paths')
        if upload != filename:
            _fail('received original upload must identify its exact root filename')
        fingerprint = version.get('sha256')
        if not isinstance(fingerprint, str) or not HASH.fullmatch(fingerprint):
            _fail('record a valid received PDF checksum')
        for relative in [source, upload]:
            data = staged_files.get(relative)
            if data is None:
                path = _file(root, relative)
                if not path.is_file():
                    _fail('missing received PDF ' + relative)
                data = path.read_bytes()
            _pdf(data)
            if sha256(data).hexdigest() != fingerprint:
                _fail('received PDF differs from its owner-approved content checksum')
            allowed_pdf_paths.add(relative)
        public_file = _file(root, public.lstrip('/'))
        if public_file.is_file() and sha256(public_file.read_bytes()).hexdigest() != fingerprint:
            _fail('received public review PDF differs from its approved source')
        allowed_pdf_paths.add(public.lstrip('/'))
        review = version.get('reconciliation')
        if not isinstance(review, dict) or review.get('status') != 'reviewed-awaiting-activation':
            _fail('record the technical review and remaining activation requirements')
        _text(review.get('reviewedBy'), 'technical document reviewer')
        _date(review.get('reviewedOn'), 'technical review date')
        _text(review.get('reference'), 'technical reconciliation reference', 1000)
        fingerprints = review.get('sourceFingerprints')
        if not isinstance(fingerprints, dict) or set(fingerprints) != set(expected_sources) or any(not isinstance(v, str) or not HASH.fullmatch(v) for v in fingerprints.values()):
            _fail('record every received-document operational comparison checksum')
        if not historical and document.get('currentVersion') is None and fingerprints != expected_sources and not allow_stale_current:
            _fail('received PDF operational comparison needs a fresh technical review')
        blockers = review.get('activationRequirements')
        if not isinstance(blockers, list) or not blockers:
            _fail('identify the precise received-document activation requirements')
        for requirement in blockers:
            _text(requirement, 'activation requirement', 1500)
    return records


def validate_registry(root=ROOT, registry=None, staged_files=None, allow_stale_current=False):
    """Validate every approved version and the active human reconciliation.

    Historical source fingerprints remain historical. Only the current document
    must match today's operational data. Staged bytes support a no-write dry run.
    """
    value = read_registry(root) if registry is None else registry
    if not isinstance(value, dict) or value.get('schemaVersion') != 1 or not isinstance(value.get('documents'), dict):
        _fail('unsupported registry format')
    if DOCUMENT_ID not in value['documents']:
        _fail('preserve the Terms and Conditions document registry')
    staged_files = staged_files or {}
    allowed_pdf_paths = set()
    for ident, document in value['documents'].items():
        if not isinstance(ident, str) or not re.fullmatch(r'[a-z][a-z0-9-]{1,79}', ident) or not isinstance(document, dict) or document.get('id') != ident:
            _fail('invalid document identity')
        _text(document.get('title'), 'document title', 180)
        if document.get('route') != '/' + ident + '/':
            _fail('preserve the stable document route')
        expected_sources = operational_fingerprints(root, document)
        received = _received_versions(root, document, expected_sources, staged_files, allowed_pdf_paths, allow_stale_current)
        anchors = document.get('legacyAnchors', [])
        if not isinstance(anchors, list) or len(set(anchors)) != len(anchors) or any(not isinstance(a, str) or not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_-]{0,99}', a) for a in anchors):
            _fail('invalid legacy section anchors')
        versions = document.get('versions')
        if not isinstance(versions, list):
            _fail('versions must be a list')
        current = document.get('currentVersion')
        if current is not None and any(v['version'] == current for v in received):
            _fail('a received review PDF cannot be the authoritative current document')
        if current is not None and (not isinstance(current, str) or not VERSION.fullmatch(current)):
            _fail('invalid current version')
        if current is None:
            _text(document.get('pendingNotice'), 'pending PDF notice', 1000)
        seen, published = set(), []
        for version in versions:
            if not isinstance(version, dict):
                _fail('invalid version record')
            label = version.get('version')
            if not isinstance(label, str) or not VERSION.fullmatch(label) or label in seen:
                _fail('version identifiers must be unique and filename-safe')
            previous = version.get('previousVersions', [])
            if not isinstance(previous, list) or len(previous) != len(set(previous)) or any(p not in seen for p in previous):
                _fail('previous-version references must identify preceding archived versions')
            seen.add(label)
            if version.get('documentId') != ident or version.get('approvalStatus') != 'approved':
                _fail('only explicitly approved document versions may be registered for publication')
            if version.get('publicationStatus') not in ['published', 'archived']:
                _fail('invalid publication status')
            if version['publicationStatus'] == 'published':
                published.append(label)
            _date(version.get('effectiveDate'), 'effective date')
            _date(version.get('lastUpdatedDate'), 'last updated date')
            _date(version.get('approvalDate'), 'approval date')
            _text(version.get('approvedBy'), 'approver')
            _text(version.get('sourceReference'), 'owner approval reference', 1000)
            filename = _text(version.get('sourceFilename'), 'original filename', 180)
            if PurePosixPath(filename).name != filename or '\\' in filename or not filename.lower().endswith('.pdf'):
                _fail('preserve a PDF basename as the original filename')
            source = version.get('sourcePath')
            if source != source_path(ident, label) or version.get('publishedPath') != public_path(ident, label):
                _fail('use immutable version-specific source and publication paths')
            allowed_pdf_paths.update([source, version['publishedPath'].lstrip('/')])
            path = _file(root, source)
            if source in staged_files:
                data = staged_files[source]
            elif path.is_file():
                data = path.read_bytes()
            else:
                _fail('missing approved PDF source ' + source)
            _pdf(data)
            fingerprint = version.get('sha256')
            if not isinstance(fingerprint, str) or not HASH.fullmatch(fingerprint) or sha256(data).hexdigest() != fingerprint:
                _fail('PDF checksum differs from its approval record')
            public = _file(root, version['publishedPath'].lstrip('/'))
            if public.is_file() and sha256(public.read_bytes()).hexdigest() != fingerprint:
                _fail('published PDF differs from its immutable approved source')
            review = version.get('reconciliation')
            if not isinstance(review, dict) or review.get('status') != 'approved':
                _fail('record the approved human review of contractual and operational rules')
            _text(review.get('reference'), 'reconciliation reference', 1000)
            _text(review.get('reviewedBy'), 'rule reviewer')
            _date(review.get('reviewedOn'), 'rule review date')
            fingerprints = review.get('sourceFingerprints')
            if not isinstance(fingerprints, dict) or not fingerprints or any(not isinstance(h, str) or not HASH.fullmatch(h) for h in fingerprints.values()):
                _fail('record the reviewed authoritative-source checksums')
            if label == current and fingerprints != expected_sources and not allow_stale_current:
                _fail('the current PDF and operational sources require a new human reconciliation; no silent publication')
        if published != ([current] if current is not None else []):
            _fail('the current pointer must identify exactly one approved published version')
    # A hidden folder or an unpublished registry flag does not make a static
    # file private. Reject stray PDFs before a normal site build can emit them.
    tooling = {'.git', '.wrangler', 'node_modules', '.venv', '__pycache__'}
    for folder, directories, filenames in os.walk(root):
        directories[:] = [name for name in directories if name not in tooling]
        for filename in filenames:
            path = Path(folder) / filename
            if path.suffix.lower() != '.pdf':
                continue
            relative = path.relative_to(root)
            if relative.as_posix() not in allowed_pdf_paths:
                _fail('unregistered PDF must be removed from the deployed repository: ' + relative.as_posix())
    return value


def current_document(root=ROOT, document_id=DOCUMENT_ID):
    document = validate_registry(root)['documents'].get(document_id)
    if document is None:
        _fail('unknown document ' + document_id)
    return next((v for v in document['versions'] if v['version'] == document['currentVersion']), None)


def _intro_prefix(body):
    # Existing customer_site.intro() is a single, non-nested section.
    match = re.search(r'<section\b[^>]*class="[^"]*\brelease-intro\b[^"]*"[^>]*>.*?</section>', body, re.S)
    return body[:match.end()] if match else ''


def wrap_terms(body, root=ROOT):
    """Keep the approved HTML fallback until an approved PDF actually exists."""
    registry = validate_registry(root)
    document = registry['documents'][DOCUMENT_ID]
    version = next((v for v in document['versions'] if v['version'] == document['currentVersion']), None)
    prefix = _intro_prefix(body)
    prefix_length = len(prefix)
    if prefix:
        prefix = re.sub(r'(<h1\b[^>]*>).*?(</h1>)', lambda m: m[1] + escape(document['title']) + m[2], prefix, count=1, flags=re.S)
    elif version is not None:
        prefix = '<section class="release-intro"><h1>' + escape(document['title']) + '</h1></section>'
    if version is None:
        notice = '<aside class="policy-document-pending" aria-label="PDF availability"><p>' + escape(document['pendingNotice']) + '</p></aside>'
        received = document.get('receivedVersions', [])
        if received:
            review = received[-1]
            panel = _viewer(review, document, review_mode=True)
            return prefix + notice + panel + '<h2 class="policy-current-online-heading">Current Online Terms</h2>' + body[prefix_length:]
        return prefix + notice + body[prefix_length:]
    # Do not duplicate the legacy full terms beneath the authoritative PDF.
    anchor_ids = list(dict.fromkeys(document.get('legacyAnchors', []) + re.findall(r'\bid="([^"<>]+)"', body[prefix_length:])))
    anchors = ''.join('<span class="policy-document-anchor" data-policy-document-anchor id="' + escape(ident, quote=True) + '" aria-hidden="true"></span>' for ident in anchor_ids)
    return prefix + anchors + _viewer(version, document)


def _viewer(version, document, review_mode=False):
    source = (ROOT / '_templates/policy-document.html').read_text()
    values = {
        'version': version['version'],
        'effective_date': 'on official website publication — date not yet set' if review_mode else date.fromisoformat(version['effectiveDate']).strftime('%d %B %Y'),
        'updated_date': ' · Prepared ' + date.fromisoformat(version['preparedDate']).strftime('%d %B %Y') if review_mode else ' · Updated ' + date.fromisoformat(version['lastUpdatedDate']).strftime('%d %B %Y'),
        'pdf_url': version['publishedPath'],
        'filename': version['sourceFilename'],
        'title': document['title']
    }
    for key, value in values.items():
        source = source.replace('{{' + key + '}}', escape(value, quote=True))
    if re.search(r'{{\w+}}', source):
        _fail('unresolved document-viewer placeholder')
    if review_mode:
        source = source.replace('data-policy-document-current=', 'data-policy-document-review=')
        source = source.replace('Read the official document', 'Review the owner-approved PDF')
        source = source.replace('Existing section links open this document; use its contents or search to locate the relevant terms.', 'The PDF content is owner-approved. Its official effective date has not been set; the current online Terms remain below during this transition.')
    return source


def outputs(root=ROOT):
    """Generated approved assets only; do not create a fake or pending PDF."""
    registry = validate_registry(root)
    out = {root / 'assets/policy-document.css': (ROOT / '_templates/policy-document.css').read_text(),
           root / 'assets/policy-document.js': (ROOT / '_templates/policy-document.js').read_text()}
    for document in registry['documents'].values():
        for version in document['versions']:
            # Stable version URLs remain recoverable for past agreed quotations.
            # Only the explicitly selected current document is linked in the viewer.
            out[root / version['publishedPath'].lstrip('/')] = _file(root, version['sourcePath']).read_bytes()
        for version in document.get('receivedVersions', []):
            out[root / version['publishedPath'].lstrip('/')] = _file(root, version['sourcePath']).read_bytes()
    return out


def review_template(pdf_path, version, effective_date, root=ROOT):
    registry = validate_registry(root, allow_stale_current=True)
    if not isinstance(version, str) or not VERSION.fullmatch(version):
        _fail('choose a filename-safe version')
    _date(effective_date, 'effective date')
    data = _external_pdf(pdf_path, root)
    document = registry['documents'][DOCUMENT_ID]
    return {'documentId': DOCUMENT_ID, 'version': version, 'effectiveDate': effective_date,
            'lastUpdatedDate': date.today().isoformat(), 'documentSha256': sha256(data).hexdigest(),
            'approvalStatus': 'pending', 'approvedBy': '', 'approvalDate': '', 'sourceReference': '',
            'reconciliation': {'status': 'pending', 'reference': '', 'reviewedBy': '', 'reviewedOn': '',
                               'sourceFingerprints': operational_fingerprints(root, document)}}


def publication_plan(pdf_path, review, root=ROOT):
    """Build and validate the entire replacement in memory before writing anything."""
    registry = deepcopy(validate_registry(root, allow_stale_current=True))
    if not isinstance(review, dict) or review.get('documentId') != DOCUMENT_ID:
        _fail('use a review record for Terms and Conditions')
    document = registry['documents'][DOCUMENT_ID]
    version = review.get('version')
    if not isinstance(version, str) or not VERSION.fullmatch(version) or any(v['version'] == version for v in document['versions']):
        _fail('use a new immutable version; never overwrite a historical version')
    data = _external_pdf(pdf_path, root)
    if review.get('documentSha256') != sha256(data).hexdigest():
        _fail('the supplied PDF differs from the reviewed document')
    archive = source_path(DOCUMENT_ID, version)
    if _file(root, archive).exists():
        _fail('the version source already exists; do not overwrite it')
    record = {key: deepcopy(review.get(key)) for key in ['documentId', 'version', 'effectiveDate', 'lastUpdatedDate', 'approvalStatus', 'approvedBy', 'approvalDate', 'sourceReference', 'reconciliation']}
    record.update(sourceFilename=Path(pdf_path).name, sourcePath=archive, publishedPath=public_path(DOCUMENT_ID, version),
                  sha256=sha256(data).hexdigest(), publicationStatus='published', previousVersions=[v['version'] for v in document['versions']])
    for old in document['versions']:
        old['publicationStatus'] = 'archived'
    document['versions'].append(record)
    document['currentVersion'] = version
    validate_registry(root, registry, staged_files={archive: data})
    return registry, record, data


def publish_document(pdf_path, review, root=ROOT, write=False):
    """Publish an approved replacement locally; never commit, push or deploy.

    Validate before creating any file. The registry pointer is replaced last;
    failed writes remove newly created files and keep the previous pointer.
    """
    registry, record, data = publication_plan(pdf_path, review, root)
    if not write:
        return record
    return _write_document_plan(root, registry, record, data)


def receive_document(pdf_path, review, root=ROOT, write=False):
    """Register an already uploaded owner-approved PDF for explicit staging review.

    The original upload remains byte-identical, while immutable archive/public
    copies are generated. This cannot assign currentVersion or an effective date.
    Normal publication still requires completed operational activation review.
    """
    registry = deepcopy(read_registry(root))
    if not isinstance(review, dict) or review.get('documentId') != DOCUMENT_ID:
        _fail('use a received review record for Terms and Conditions')
    document = registry['documents'][DOCUMENT_ID]
    label = review.get('version')
    prior = document.get('receivedVersions', []) + document.get('receiptHistory', []) + document['versions']
    if not isinstance(label, str) or not VERSION.fullmatch(label) or any(v['version'] == label for v in prior):
        _fail('use a new immutable received version')
    data = _external_pdf(pdf_path, root)
    if review.get('documentSha256') != sha256(data).hexdigest():
        _fail('the supplied PDF differs from the received approval record')
    record = deepcopy(review)
    record.pop('documentSha256')
    record.update(sourceFilename=Path(pdf_path).name, sourcePath=source_path(DOCUMENT_ID, label), publishedPath=public_path(DOCUMENT_ID, label), sha256=sha256(data).hexdigest())
    if document.get('currentVersion') is not None:
        _fail('review a new received PDF without replacing the existing authoritative version')
    document.setdefault('receivedVersions', []).append(record)
    document['pendingNotice'] = 'An owner-approved PDF is available for staging review below. Its official effective date is the date of publication on the official website; the current online Terms remain available during operational reconciliation.'
    document['authority'] = 'Owner R53 corrective instruction,19 November2026: supplied PDF content is approved. Staging review is not official production publication; retain the current online Terms until the effective date and operational scope are reconciled.'
    validate_registry(root, registry, staged_files={record['sourcePath']: data})
    if not write:
        return record
    return _write_document_plan(root, registry, record, data)


def activate_received_document(version, review, root=ROOT, write=False):
    """Activate the same approved bytes after a real official publication event.

    No date or operational review is inferred. Receipt history and PDF paths
    remain intact. Only an atomic registry replacement is required; a failure
    leaves the previous received/current state and every PDF unchanged.
    """
    registry = deepcopy(validate_registry(root, allow_stale_current=True))
    document = registry['documents'][DOCUMENT_ID]
    received = next((v for v in document.get('receivedVersions', []) if v['version'] == version), None)
    if received is None or any(v['version'] == version for v in document['versions']):
        _fail('select an unactivated approved received version')
    if not isinstance(review, dict) or review.get('documentId') != DOCUMENT_ID or review.get('version') != version:
        _fail('use the activation review for this exact received version')
    if review.get('documentSha256') != received['sha256']:
        _fail('activation must preserve the exact owner-approved received PDF')
    publication = review.get('officialPublication')
    if not isinstance(publication, dict) or publication.get('status') != 'confirmed':
        _fail('record the confirmed actual official website publication event')
    official_date = _date(publication.get('date'), 'actual official publication date')
    if date.fromisoformat(official_date) > date.today():
        _fail('official publication must be an actual event, not a future planned date')
    if official_date < max(received['preparedDate'], received['approvalDate']):
        _fail('official publication cannot precede preparation or content approval')
    _text(publication.get('reference'), 'official publication evidence', 1000)
    if review.get('effectiveDate') != official_date:
        _fail('effective date must equal the actual official website publication date')
    record = {key: deepcopy(review.get(key)) for key in ['documentId', 'version', 'effectiveDate', 'lastUpdatedDate', 'reconciliation']}
    # Content approval already exists; do not demand or fabricate a second one.
    record.update({key: deepcopy(received[key]) for key in ['approvalStatus', 'approvedBy', 'approvalDate', 'sourceReference']})
    record.update({key: deepcopy(received[key]) for key in ['sourceFilename', 'sourcePath', 'publishedPath', 'sha256']})
    record.update(publicationStatus='published', previousVersions=[v['version'] for v in document['versions']], officialPublication=deepcopy(publication), receiptVersion=version)
    for old in document['versions']:
        old['publicationStatus'] = 'archived'
    document.setdefault('receiptHistory', []).append(deepcopy(received))
    document['receivedVersions'] = [v for v in document['receivedVersions'] if v['version'] != version]
    document['versions'].append(record)
    document['currentVersion'] = version
    validate_registry(root, registry)
    if not write:
        return record
    target, temporary = root / REGISTRY, None
    try:
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=target.parent, prefix='.policy-registry-', suffix='.tmp', delete=False) as stream:
            temporary = Path(stream.name)
            stream.write(json.dumps(registry, ensure_ascii=False, indent=2) + '\n')
        os.replace(temporary, target)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)
    return record


def activation_review_template(version, official_date, root=ROOT):
    registry = validate_registry(root, allow_stale_current=True)
    document = registry['documents'][DOCUMENT_ID]
    received = next((v for v in document.get('receivedVersions', []) if v['version'] == version), None)
    if received is None:
        _fail('select an approved received version for activation review')
    _date(official_date, 'official publication date to verify')
    return {'documentId': DOCUMENT_ID, 'version': version, 'documentSha256': received['sha256'],
            'effectiveDate': official_date, 'lastUpdatedDate': received['preparedDate'],
            'officialPublication': {'status': 'pending', 'date': official_date, 'reference': ''},
            'reconciliation': {'status': 'pending', 'reference': '', 'reviewedBy': '', 'reviewedOn': '',
                               'sourceFingerprints': operational_fingerprints(root, document)}}


def _write_document_plan(root, registry, record, data):
    targets = [_file(root, record['sourcePath']), _file(root, record['publishedPath'].lstrip('/'))]
    if any(path.exists() for path in targets):
        _fail('an immutable source or public version already exists')
    created, temporary = [], None
    try:
        for path in targets:
            path.parent.mkdir(parents=True, exist_ok=True)
            with path.open('xb') as stream:
                created.append(path)
                stream.write(data)
        target = root / REGISTRY
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=target.parent, prefix='.policy-registry-', suffix='.tmp', delete=False) as stream:
            temporary = Path(stream.name)
            stream.write(json.dumps(registry, ensure_ascii=False, indent=2) + '\n')
        os.replace(temporary, target)
    except BaseException:
        for path in reversed(created):
            path.unlink(missing_ok=True)
        if temporary is not None:
            temporary.unlink(missing_ok=True)
        raise
    return record
