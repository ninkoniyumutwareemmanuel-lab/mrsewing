"""Full-screen, mobile-readable staged Terms PDF viewer.

Renders the registered staging-review PDF as page images derived from its
checksum-verified bytes. Review authorization is not official activation.
Until official activation, quotation/consultation consent continues pointing
to the preserved current HTML Terms.
"""
import hashlib
import json
import re
import struct
from pathlib import Path
from html import escape

ROOT = Path(__file__).resolve().parents[1]
CURRENT_PATH = '/terms-and-conditions/current/'
PAGE_DIR = '/assets/policy-documents/terms-and-conditions/pages/'
RENDER_DPI = 160


def production_terms_html(route='/terms-and-conditions/', root=ROOT):
    """Return the preserved effective HTML for an unactivated production release.

    This is an export projection, never PDF approval or contractual activation.
    The staging reader stays unchanged. Only canonical/social/schema route
    metadata is normalized; the effective document body and its noindex status
    are preserved verbatim. A later activated document requires its own reviewed
    publication path rather than silently falling back to old terms.
    """
    if route not in ('/terms-and-conditions/', CURRENT_PATH):
        raise ValueError('Unsupported contractual Terms export route')
    root = Path(root)
    document = json.loads((root / '_data/policy-documents.json').read_text())['documents']['terms-and-conditions']
    if document.get('currentVersion') is not None:
        raise ValueError('Activated Terms need their explicitly reviewed publication workflow')
    source = (root / 'terms-and-conditions/current/index.html').read_text()
    current_url = 'https://mrsewingfashion.com' + CURRENT_PATH
    target_url = 'https://mrsewingfashion.com' + route
    canonicals = re.findall(r'<link\b(?=[^>]*\brel=["\']canonical["\'])[^>]*\bhref=["\']([^"\']+)["\'][^>]*>', source, re.I)
    if canonicals != [current_url] or 'Identity and scope' not in source or 'id="1"' not in source:
        raise ValueError('Current effective HTML Terms source could not be verified')
    if 'termsPdfDialog' in source or '/terms-and-conditions/1.2.pdf' in source:
        raise ValueError('A staging-review PDF cannot substitute for effective HTML Terms')
    source = re.sub(
        r'(<link\b(?=[^>]*\brel=["\']canonical["\'])[^>]*\bhref=["\'])[^"\']+(["\'])',
        lambda match: match[1] + target_url + match[2], source, flags=re.I)
    source = re.sub(
        r'(<meta\b(?=[^>]*\bproperty=["\']og:url["\'])[^>]*\bcontent=["\'])[^"\']+(["\'])',
        lambda match: match[1] + target_url + match[2], source, flags=re.I)

    def schema(match):
        def normalize(value):
            if isinstance(value, dict):
                return {key: normalize(item) for key, item in value.items()}
            if isinstance(value, list):
                return [normalize(item) for item in value]
            if isinstance(value, str) and value.startswith(current_url):
                return target_url + value[len(current_url):]
            return value
        value = normalize(json.loads(match[2]))
        return match[1] + json.dumps(value, ensure_ascii=False).replace('<', '\\u003c') + match[3]

    source = re.sub(r'(<script\b[^>]*type=["\']application/ld\+json["\'][^>]*>)(.*?)(</script>)',
                    schema, source, flags=re.I | re.S)
    return source


def received_version():
    document = json.loads((ROOT / '_data/policy-documents.json').read_text())['documents']['terms-and-conditions']
    if document['currentVersion'] is not None:
        raise ValueError('Staging PDF preview must not silently activate Terms')
    versions = document.get('receivedVersions', [])
    if not versions or [v['version'] for v in versions] not in (['1.0'], ['1.0','1.1'], ['1.0','1.2']):
        raise ValueError('Unexpected PDF receipt history')
    for candidate in versions:
        validate_receipt(candidate)
    return versions[-1]


def validate_receipt(entry):
    """Validate every retained receipt; a new upload cannot hide a damaged archive."""
    expected_approval = 'approved-for-staging-review' if entry['version']=='1.2' else 'approved'
    if (entry['approvalStatus'] != expected_approval
            or entry['publicationStatus'] != 'staging-review'
            or entry['activationStatus'] != 'awaiting-official-publication'
            or entry['effectiveDate'] is not None):
        raise ValueError('Terms publication state changed unexpectedly')
    if entry['publishedPath'] != '/assets/policy-documents/terms-and-conditions/'+entry['version']+'.pdf':
        raise ValueError('Unreviewed Terms PDF source')
    fingerprint = entry['sha256']
    for name in (entry['originalUploadPath'], entry['sourcePath'], entry['publishedPath'].lstrip('/')):
        path = ROOT / name
        if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != fingerprint:
            raise ValueError('Terms PDF checksum/path mismatch: ' + name)
    pages = entry['technicalInspection']['pages']
    if pages != {'1.0':5,'1.1':6,'1.2':6}[entry['version']]:
        raise ValueError('Unexpected approved PDF page count')
    if entry['version']=='1.2' and (entry['technicalInspection'].get('declaredVersion')!='1.2'
                                  or entry['technicalInspection'].get('numberedSections')!=20):
        raise ValueError('Uploaded Version 1.2 identity changed unexpectedly')


def page_url(version, number):
    return PAGE_DIR + version['version'] + '-%02d.png' % number


def page_manifest(entry):
    manifest = json.loads((ROOT / 'assets/policy-documents/terms-and-conditions/pages/manifest.json').read_text())
    pages=entry['technicalInspection']['pages']
    if (manifest.get('sourcePdfSha256')!=entry['sha256'] or manifest.get('version')!=entry['version']
            or manifest.get('publicationStatus')!='staging-review' or manifest.get('effectiveDate') is not None
            or len(manifest.get('pages',[]))!=pages):
        raise ValueError('Terms page manifest does not match the registered PDF')
    for number,item in enumerate(manifest['pages'],1):
        if item.get('page')!=number or item.get('path')!=page_url(entry,number):
            raise ValueError('Terms page order/path mismatch')
        raw=(ROOT/item['path'].lstrip('/')).read_bytes()
        if (not raw.startswith(b'\x89PNG\r\n\x1a\n') or raw[12:16]!=b'IHDR'
                or struct.unpack('>II',raw[16:24])!=(item['width'],item['height'])
                or hashlib.sha256(raw).hexdigest()!=item['sha256']):
            raise ValueError('Terms page image checksum/dimensions mismatch')
    return manifest


def render():
    entry = received_version()
    href = escape(entry['publishedPath'], quote=True)
    filename = escape(entry['sourceFilename'], quote=True)
    pages = entry['technicalInspection']['pages']
    manifest = page_manifest(entry)
    dimensions = {p['page']:(p['width'],p['height']) for p in manifest['pages']}
    document_pages = ''.join(
        '<li class="terms-popup-page" data-page="' + str(i) + '">'
        '<img src="' + escape(page_url(entry, i), quote=True)
        + '" width="' + str(dimensions[i][0]) + '" height="' + str(dimensions[i][1]) + '" loading="' + ('eager' if i == 1 else 'lazy')
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
        'This Version ' + escape(entry['version']) + ' PDF is authorized for staging review, not the officially effective Terms.'
        ' Customer consent continues to use the existing online Terms.</p>'
        '<div class="terms-popup-toolbar" role="toolbar" aria-label="PDF reader controls">'
        '<span class="terms-popup-document-icon" aria-hidden="true">'
        '<svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor"'
        ' stroke-width="1.7"><path d="M6 2h8l5 5v15H6z"/><path d="M14 2v6h5"/>'
        '<path d="M9 14h7M9 17h5"/></svg></span>'
        '<span class="terms-popup-filename" title="' + filename + '">' + filename + '</span>'
        '<a class="terms-popup-icon" href="' + href + '" target="_blank" rel="noopener noreferrer"'
        ' aria-label="Open the staging-review PDF in a new tab" title="Open PDF">'
        '<svg viewBox="0 0 24 24" width="23" height="23" fill="none" stroke="currentColor"'
        ' stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round">'
        '<path d="M14 3h7v7M10 14L21 3M21 13v8H3V3h8"/></svg></a>'
        '<a class="terms-popup-icon" href="' + href + '" download="' + filename
        + '" aria-label="Download the original staging-review PDF" title="Download PDF">'
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
