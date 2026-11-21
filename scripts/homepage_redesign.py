"""R56 homepage: short tailoring-first layout from one authorized media registry.

The original R53 videos are only served after all existing safety/rights/poster
gates are satisfied. Uploaded reference images remain design inspiration;
homepage authorization never publishes them as Showroom or Shop merchandise.
"""
from collections import OrderedDict
from datetime import datetime, timezone
from html import escape
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
UPLOAD_COMMIT = 'ce98ee3991a43483357304b5fe9f2f0a83f7ae27'


def _load_json(name):
    return json.loads((ROOT / name).read_text())


def _valid_date(stamp):
    if not stamp:
        return None
    try:
        value = datetime.fromisoformat(stamp.replace('Z', '+00:00'))
        if value.tzinfo is None:
            return None
        return value.astimezone(timezone.utc).timestamp()
    except (ValueError, TypeError, AttributeError):
        return None


def source_families():
    """Newest verified upload batch first; stable fallback for unknown dates.

    Never treat image upload time as a garment manufacture or completion date.
    Within a family preserve the R53 image view order and colour variants.
    """
    records = _load_json('_data/collection-designs.json')['designs']
    eligible = []
    for source_index, design in enumerate(records):
        attestation = design.get('homepagePublication') or {}
        if not (attestation.get('approved') is True
                and attestation.get('approvalBasis') == 'owner-attested-commercial-use-rights'
                and attestation.get('evidenceRef') == 'R56_OWNER_PHOTOGRAPH_RIGHTS_2026-11-21'
                and design.get('rightsStatus') == 'approved'):
            continue
        if design.get('uploadCommit') != UPLOAD_COMMIT:
            raise ValueError('Unreviewed homepage photo batch in approved source projection')
        images = design.get('images', [])
        if not images:
            raise ValueError('Homepage-approved source has no actual image')
        for photo in images:
            src = photo.get('src', '')
            if not src.startswith('/') or not (ROOT / src.lstrip('/')).is_file():
                raise ValueError('Approved homepage reference file missing: ' + str(src))
            if not photo.get('alt') or not photo.get('width') or not photo.get('height'):
                raise ValueError('Photo has no meaningful accessible media metadata')
        family = design.get('family') or {}
        eligible.append({
            'group': family.get('id') or design['id'],
            'title': family.get('name') or design['name'],
            'designId': design['id'],
            'timestamp': _valid_date(design.get('homepageUploadTimestamp')),
            'images': images,
            'sourceIndex': source_index,
            'kind': 'reference',
        })
    if len(eligible) != 22:
        raise ValueError('Expected exactly 22 owner-authorized R53 designs for R56 homepage')
    families = OrderedDict()
    for record in eligible:
        key = record['group']
        if key not in families:
            families[key] = {
                'id': key, 'title': record['title'], 'timestamp': record['timestamp'],
                'sourceIndex': record['sourceIndex'], 'photos': []
            }
        elif record['timestamp'] != families[key]['timestamp']:
            raise ValueError('One family contains inconsistent upload dates')
        for photo in record['images']:
            families[key]['photos'].append({
                'src': photo['src'], 'alt': photo['alt'],
                'width': photo['width'], 'height': photo['height'],
                'designId': record['designId'], 'kind': 'reference',
                'family': key, 'title': record['title'],
            })
    groups = list(families.values())
    if sum(len(g['photos']) for g in groups) != 25:
        raise ValueError('Expected 25 authorized real photographs, grouped into their families')
    # All 25 are from the same verified 19 Nov 2026 upload commit.
    # Tie: preserve original R53 registry group order; no fictitious dates.
    groups.sort(key=lambda group: (
        0 if group['timestamp'] is not None else 1,
        -(group['timestamp'] or 0), group['sourceIndex']))
    return groups


def stable_legacy_families(limit=8):
    """The existing publication-gated loader is the authority for older work.

    Missing chronological dates are not invented; retain its stable order.
    """
    from build_collections import load
    designs = load()[0]
    groups = []
    for index, design in enumerate(designs[:limit]):
        photo = design['images'][0]
        groups.append({
            'id': design['id'], 'title': design['name'], 'timestamp': None,
            'sourceIndex': index, 'photos': [{
                'src': photo['src'], 'alt': photo['alt'],
                'width': photo['width'], 'height': photo['height'],
                'designId': design['id'], 'kind': 'existing-approved',
                'family': design['id'], 'title': design['name']
            }]
        })
    return groups


def gallery_rows():
    """One main/legacy source, two opposite-motion views; never reverse DOM order."""
    new = source_families()
    old = stable_legacy_families()
    left, right = [], []
    for idx, group in enumerate(new):
        (left if idx % 2 == 0 else right).append(group)
    for idx, group in enumerate(old):
        (left if idx % 2 == 0 else right).append(group)
    for row in (left, right):
        dated = [group['timestamp'] for group in row if group['timestamp'] is not None]
        if dated != sorted(dated, reverse=True):
            raise ValueError('Homepage photo group order must be newest upload first')
        seen_undated = False
        for group in row:
            if group['timestamp'] is None:
                seen_undated = True
            elif seen_undated:
                raise ValueError('Undated old photographs must follow verified newer uploads')
    return left, right


def _img(photo, priority=False, media_card=False):
    src = escape(photo['src'], quote=True)
    alt = escape('Reference clothing design photograph: ' + photo['alt']
                 if photo['kind'] == 'reference' else photo['alt'], quote=True)
    dimensions = (' width="' + str(photo['width']) + '" height="' + str(photo['height']) + '"')
    return ('<img src="' + src + '" alt="' + alt + '"' + dimensions
            + ' loading="' + ('eager' if priority else 'lazy') + '" decoding="async"'
            + (' fetchpriority="high"' if priority else '')
            + '>')


def _allowed_video(video):
    """All approval conditions including silent media and poster must be explicit."""
    meta = video.get('metadataApproval') or {}
    usage = video.get('usageRights') or {}
    soundless = video.get('silentDerivative') or {}
    poster = video.get('approvedPoster') or {}
    if not (
        video.get('publicationStatus') == 'published'
        and usage.get('approved') is True
        and usage.get('evidenceRef')
        and meta.get('approved') is True
        and meta.get('evidenceRef')
        and video.get('posterMediaId')
        and soundless.get('audioStreams') == 0
        and soundless.get('verified') is True
        and poster.get('approved') is True
        and poster.get('sha256')
    ):
        return False
    for record in (soundless, poster):
        route = record.get('path', '')
        if not route.startswith('/assets/') or not (ROOT / route.lstrip('/')).is_file():
            return False
    return True


def _media_card(video, image):
    source_title = escape(video['title'], quote=True)
    if _allowed_video(video):
        src = escape(video['silentDerivative']['path'], quote=True)
        poster = escape(video['approvedPoster']['path'], quote=True)
        return ('<figure class="r56-showcase-card" aria-label="' + source_title + '">'
                '<video controls playsinline muted preload="none"'
                ' aria-label="' + source_title + '" poster="' + poster + '">'
                '<source src="' + src + '" type="video/mp4">'
                'Your browser cannot play this video.</video></figure>')
    return ('<figure class="r56-showcase-card"'
            ' aria-label="Approved clothing reference photograph">'
            + _img(image, priority=True) + '</figure>')


def video_preview():
    registry = _load_json('_data/media-video-records.json')
    videos = registry.get('videos', [])
    if len(videos) != 2:
        raise ValueError('R53 two-video review record not found')
    designs = _load_json('_data/collection-designs.json')['designs']
    lookup = {d['id']: d for d in designs}
    fallbacks = []
    for key in ('MS-169', 'MS-162'):
        d = lookup.get(key)
        if not d or not (d.get('homepagePublication') or {}).get('approved'):
            raise ValueError('R56 approved photo fallback not available: ' + key)
        fallbacks.append({**d['images'][0], 'kind': 'reference'})
    return ('<section class="r56-visual-showcase" aria-label="Clothing design visual showcase">'
            '<div class="home-shell r56-showcase-grid">'
            + ''.join(_media_card(video, photo) for video, photo in zip(videos, fallbacks))
            + '</div></section>')


def featured_cards():
    return '''<section class="r56-primary-section r56-section" id="services" aria-labelledby="r56-primary-heading">
<div class="home-shell"><div class="r56-section-heading">
<p class="r56-eyebrow">Tailoring comes first</p>
<h2 id="r56-primary-heading">How can we help you?</h2>
<p>Choose your tailoring journey. We discuss your design and confirm a quotation before an order.</p>
</div>
<div class="r56-primary-grid">
<a class="r56-primary-card" href="/services/custom-tailoring/">
<img src="/hero-custom-tailoring.webp" width="1536" height="1024" loading="lazy" decoding="async" alt="Ivory suit jacket photographed on a mannequin">
<div class="r56-primary-card-copy"><p class="r56-eyebrow">Our main service</p>
<h3>Tailoring &amp; Clothing Services</h3>
<p>Explore custom clothing, suit designs and professional garment services.</p>
<span class="r56-link">Explore tailoring <span aria-hidden="true">→</span></span></div></a>
<a class="r56-primary-card r56-primary-card-vip" href="/services/vip/">
<img src="/hero-vip-services.webp" width="1536" height="1030" loading="lazy" decoding="async" alt="Approved premium suit consultation setting with tailoring accessories">
<div class="r56-primary-card-copy"><p class="r56-eyebrow">Personal assistance</p>
<h3>VIP Services</h3>
<p>Discuss a tailored service arrangement and individual quotation with our team.</p>
<span class="r56-link">Explore VIP services <span aria-hidden="true">→</span></span></div></a>
</div></div></section>'''


def craft_feature():
    return '''<section class="r56-feature-section" aria-labelledby="r56-craft-title"><div class="home-shell r56-feature-frame">
<figure><img src="/hero-alterations.webp" width="1000" height="571" loading="lazy" decoding="async" alt="Tailor adjusting a dark jacket on a mannequin"></figure>
<div class="r56-feature-content">
<p class="r56-eyebrow">Craft and fit</p><h2 id="r56-craft-title">Made around your measurements.</h2>
<p>Bring your design or explore clothing inspiration. We discuss the details before confirming your quotation.</p>
<a href="/services/custom-tailoring/" class="home-button home-button-gold">Explore Tailoring Services <span aria-hidden="true">→</span></a>
</div></div></section>'''


def _gallery_card(photo, duplicate=False):
    return ('<figure class="r56-gallery-card" data-design-family="'
            + escape(photo['family'], quote=True) + '" data-design-id="'
            + escape(photo['designId'], quote=True) + '"'
            + (' aria-hidden="true"' if duplicate else '') + '>'
            + _img(photo)
            + '<figcaption>' + escape(photo['title']) + '</figcaption></figure>')


def _gallery_panel(groups, number, direction):
    photos = [p for group in groups for p in group['photos']]
    if not photos:
        raise ValueError('Homepage gallery has no authorized pictures')
    cards = ''.join(_gallery_card(p) for p in photos)
    copies = ''.join(_gallery_card(p, duplicate=True) for p in photos)
    seconds = max(125, len(photos) * 13)
    name = ('First' if number == 1 else 'Second') + ' clothing design photograph row'
    return ('<div class="r56-gallery-panel" data-home-gallery>'
            '<div class="r56-gallery-actions"><h3>' + ('Design inspiration' if number == 1 else 'More clothing designs')
            + '</h3><button type="button" class="r56-gallery-control"'
            ' aria-label="Pause or resume '+ name.lower() + '"'
            ' aria-pressed="false" data-r56-pause hidden>Pause motion</button></div>'
            '<div class="r56-gallery" data-direction="' + direction
            + '" data-paused="false" aria-label="' + escape(name, quote=True)
            + ' — newest upload references first" role="region" tabindex="0">'
            '<div class="r56-gallery-track" style="--r56-duration:' + str(seconds) + 's">'
            '<div class="r56-gallery-group">' + cards + '</div>'
            '<div class="r56-gallery-group" aria-hidden="true">' + copies + '</div>'
            '</div></div></div>')


def galleries():
    first, second = gallery_rows()
    return ('''<section class="r56-galleries-section r56-section" id="suit-collections" aria-labelledby="r56-galleries-title">
<div class="home-shell">
<div class="r56-section-heading">
<p class="r56-eyebrow">Clothing inspiration</p>
<h2 id="r56-galleries-title">Discover tailoring possibilities.</h2>
<p>Explore real photo references and discuss the style you would like made.</p>
</div><span id="customers-section" class="visually-hidden" aria-hidden="true"></span>'''
            + _gallery_panel(first, 1, 'left')
            + _gallery_panel(second, 2, 'right')
            + '''<div class="r56-galleries-footer"><a href="/collections/">Explore All Clothing Designs <span aria-hidden="true">→</span></a></div></div></section>''')


def quick_links():
    return '''<nav class="r56-quick-links" id="process-section" aria-label="More Mr Sewing customer information">
<div class="home-shell r56-quick-grid">
<a href="/our-process/">How It Works</a>
<a href="/our-work/">Our Work</a>
<a href="/faq/">FAQs</a>
<a href="/shop/">Shop</a>
</div></nav>'''


def render():
    return video_preview() + featured_cards() + craft_feature() + galleries() + quick_links()
