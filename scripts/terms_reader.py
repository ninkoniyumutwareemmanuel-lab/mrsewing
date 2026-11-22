"""Full-screen, mobile-readable staged Terms PDF viewer.

Only renders the exact approved R53 PDF as page images derived from its
checksum-verified bytes. The PDF is NOT yet the legally active online Terms.
Until official activation, quotation/consultation consent continues pointing
to the preserved current HTML Terms.
"""
import hashlib
import json
from pathlib import Path
from html import escape

ROOT = Path(__file__).resolve().parents[1]
CURRENT_PATH = '/terms-and-conditions/current/'
PAGE_DIR = '/assets/policy-documents/terms-and-conditions/pages/'
RENDER_DPI = 160


def received_version():
    document = json.loads((ROOT / '_data/policy-documents.json').read_text())['documents']['terms-and-conditions']
    if document['currentVersion'] is not None:
        raise ValueError('Staging PDF preview must not silently activate Terms')
    versions = document.get('receivedVersions', [])
    if len(versions) != 1:
        raise ValueError('Expected one owner-approved PDF receipt')
    entry = versions[0]
    if (entry['approvalStatus'] != 'approved'
            or entry['publicationStatus'] != 'staging-review'
            or entry['activationStatus'] != 'awaiting-official-publication'
            or entry['effectiveDate'] is not None):
        raise ValueError('Terms publication state changed unexpectedly')
    if entry['publishedPath'] != '/assets/policy-documents/terms-and-conditions/1.0.pdf':
        raise ValueError('Unreviewed Terms PDF source')
    fingerprint = entry['sha256']
    for name in (entry['originalUploadPath'], entry['sourcePath'], entry['publishedPath'].lstrip('/')):
        path = ROOT / name
        if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != fingerprint:
            raise ValueError('Terms PDF checksum/path mismatch: ' + name)
    pages = entry['technicalInspection']['pages']
    if pages != 5:
        raise ValueError('Unexpected approved PDF page count')
    return entry


def page_url(version, number):
    return PAGE_DIR + version['version'] + '-%02d.png' % number


def render():
    entry = received_version()
    href = escape(entry['publishedPath'], quote=True)
    filename = escape(entry['sourceFilename'], quote=True)
    pages = entry['technicalInspection']['pages']
    document_pages = ''.join(
        '<li class="terms-popup-page" data-page="' + str(i) + '">'
        '<img src="' + escape(page_url(entry, i), quote=True)
        + '" width="1360" height="1760" loading="' + ('eager' if i == 1 else 'lazy')
        + '" decoding="async" alt="Terms and Conditions PDF, page ' + str(i)
        + ' of ' + str(pages) + '">'
        '</li>' for i in range(1, pages + 1))
    return (
        '<section class="terms-popup-host" aria-label="Terms and Conditions document">'
        '<h1 class="terms-popup-visually-hidden">Terms and Conditions</h1>'
        '<dialog id="termsPdfDialog" class="terms-popup" open'
        ' aria-label="Terms and Conditions full-screen PDF reader"'
        ' aria-describedby="termsPopupLegalStatus">'
        '<p class="terms-popup-visually-hidden" id="termsPopupLegalStatus">'
        'This owner-approved PDF is for staging review, not the officially effective Terms.'
        ' Customer consent continues to use the existing online Terms.</p>'
        '<div class="terms-popup-toolbar" role="toolbar" aria-label="PDF reader controls">'
        '<span class="terms-popup-document-icon" aria-hidden="true">'
        '<svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor"'
        ' stroke-width="1.7"><path d="M6 2h8l5 5v15H6z"/><path d="M14 2v6h5"/>'
        '<path d="M9 14h7M9 17h5"/></svg></span>'
        '<span class="terms-popup-filename" title="' + filename + '">' + filename + '</span>'
        '<a class="terms-popup-icon" href="' + href + '" target="_blank" rel="noopener noreferrer"'
        ' aria-label="Open the approved PDF in a new tab" title="Open PDF">'
        '<svg viewBox="0 0 24 24" width="23" height="23" fill="none" stroke="currentColor"'
        ' stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round">'
        '<path d="M14 3h7v7M10 14L21 3M21 13v8H3V3h8"/></svg></a>'
        '<a class="terms-popup-icon" href="' + href + '" download="' + filename
        + '" aria-label="Download the original approved PDF" title="Download PDF">'
        '<svg viewBox="0 0 24 24" width="23" height="23" fill="none"'
        ' stroke="currentColor" stroke-width="1.9" stroke-linecap="round"'
        ' stroke-linejoin="round"><path d="M12 3v13m-5-5 5 5 5-5"/>'
        '<path d="M4 17v4h16v-4"/></svg></a>'
        '<button type="button" class="terms-popup-icon terms-popup-zoom" data-terms-zoom-out'
        ' aria-label="Zoom out" title="Zoom out">'
        '<svg viewBox="0 0 24 24" width="22" height="22" fill="none"'
        ' stroke="currentColor" stroke-width="1.9" stroke-linecap="round">'
        '<circle cx="10.5" cy="10.5" r="6.5"/><path d="M7 10.5h7M16 16l5 5"/></svg></button>'
        '<button type="button" class="terms-popup-icon terms-popup-zoom" data-terms-zoom-in'
        ' aria-label="Zoom in" title="Zoom in">'
        '<svg viewBox="0 0 24 24" width="22" height="22" fill="none"'
        ' stroke="currentColor" stroke-width="1.9" stroke-linecap="round">'
        '<circle cx="10.5" cy="10.5" r="6.5"/><path d="M7 10.5h7M10.5 7v7M16 16l5 5"/></svg></button>'
        '<button type="button" class="terms-popup-icon terms-popup-close" data-terms-close'
        ' aria-label="Close PDF reader" title="Close and return to website">'
        '<svg viewBox="0 0 24 24" width="26" height="26" fill="none"'
        ' stroke="currentColor" stroke-width="2" stroke-linecap="round">'
        '<path d="M5 5l14 14M19 5 5 19"/></svg></button>'
        '</div>'
        '<div class="terms-popup-scroll" data-terms-scroll role="region"'
        ' aria-label="Scrollable PDF pages" tabindex="0">'
        '<ol class="terms-popup-pages" data-terms-pages>'
        + document_pages + '</ol>'
        '</div>'
        '<div class="terms-popup-page-count" aria-live="polite" aria-atomic="true">'
        '<span data-terms-page-number>1</span> / ' + str(pages) + '</div>'
        '<noscript><a href="' + href + '">Open the PDF directly</a></noscript>'
        '</dialog></section>'
        '<script src="/assets/terms-reader.js?v=r55-20261121" defer></script>'
    )
