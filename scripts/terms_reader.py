"""Document-first preview for the approved R53 PDF, without activating it.

The archived received-version registry is retained intact. The R53 technical
fingerprints apply to R53 staging, not automatically to the newer main copy.
Any official activation still requires a fresh reviewed source reconciliation.
"""
import hashlib
import json
from pathlib import Path
from html import escape

ROOT = Path(__file__).resolve().parents[1]
CURRENT_PATH = '/terms-and-conditions/current/'


def received_version():
    document = json.loads((ROOT / '_data/policy-documents.json').read_text())['documents']['terms-and-conditions']
    if document['currentVersion'] is not None:
        raise ValueError('R54 staging reader is not an official PDF activation')
    versions = document.get('receivedVersions', [])
    if len(versions) != 1:
        raise ValueError('Expected exactly one R53 approved received Terms PDF')
    entry = versions[0]
    if (entry['approvalStatus'] != 'approved' or entry['publicationStatus'] != 'staging-review'
            or entry['activationStatus'] != 'awaiting-official-publication' or entry['effectiveDate'] is not None):
        raise ValueError('Terms publication/approval status changed; review before rendering')
    url = entry['publishedPath']
    if url != '/assets/policy-documents/terms-and-conditions/1.0.pdf':
        raise ValueError('Unexpected unreviewed Terms PDF source')
    expected = entry['sha256']
    for filename in (entry['originalUploadPath'], entry['sourcePath'], url.lstrip('/')):
        source = (ROOT / filename)
        if not source.is_file() or hashlib.sha256(source.read_bytes()).hexdigest() != expected:
            raise ValueError('Approved PDF missing or checksum does not match: ' + filename)
    return entry


def render():
    entry = received_version()
    href = escape(entry['publishedPath'], quote=True)
    filename = escape(entry['sourceFilename'], quote=True)
    return (
        '<section class="terms-document-shell" aria-label="Terms and Conditions document reader">'
        '<h1 class="terms-document-a11y">Terms and Conditions</h1>'
        '<nav class="terms-document-toolbar" aria-label="Terms document actions">'
        '<div class="terms-document-state"><strong>Approved PDF · Staging review only.</strong> '
        'This PDF is not yet the officially effective website version. '
        '<a href="' + CURRENT_PATH + '">Read the current online Terms for customer consent</a>.</div>'
        '<div class="terms-document-actions">'
        '<a href="' + href + '" target="_blank" rel="noopener">Open PDF<span class="terms-document-a11y"> (new tab)</span></a>'
        '<a href="' + href + '" download="' + filename + '">Download PDF</a>'
        '</div></nav>'
        '<div class="terms-document-viewport">'
        '<object type="application/pdf" data="' + href + '#view=FitH" '
        'aria-label="Approved Terms PDF — staging review, not yet effective" tabindex="0">'
        '<p class="terms-document-fallback">This browser cannot display the document here. '
        '<a href="' + href + '" target="_blank" rel="noopener">Open the PDF directly</a> '
        'or use Download PDF above.</p></object></div>'
        '<p class="terms-document-a11y">On some mobile browsers, Open PDF provides a better reading experience.</p>'
        '</section>'
        '<script src="/assets/terms-reader.js" defer></script>'
    )
