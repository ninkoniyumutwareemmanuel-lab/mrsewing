"""R51 media projections. Existing publication records remain authoritative.

This module never treats a raw collection `published` flag as permission. Images
come from the existing effective collection/project gates. New video permissions
have their own empty-by-default registry; merely finding a file cannot publish it.
"""
from pathlib import Path
from urllib.parse import quote, unquote, urlencode
from datetime import date
from math import isfinite
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[1]
DOMAIN = 'https://mrsewingfashion.com'
CLASSIFICATIONS = {'reference-design': 'Reference Design', 'our-work': 'Our Work', 'shop-product': 'Shop Product'}
AUDIENCES = {'men': "Men's clothing", 'women': "Women's clothing"}
GARMENTS = {'suit': 'Suits', 'tuxedo': 'Tuxedos', 'shirt': 'Shirts', 'dress': 'Dresses', 'trousers': 'Trousers', 'skirt': 'Skirts', 'jacket': 'Jackets', 'coat': 'Coats', 'other': 'Other clothing'}
STYLE_LABELS = {'single-breasted': 'Single-breasted', 'double-breasted': 'Double-breasted', 'three-piece': 'Three-piece', 'tuxedos-formalwear': 'Tuxedos & formalwear', 'skirt-suits': 'Skirt suits', 'kaunda': 'Kaunda'}


def media_id(path):
    """Path identity, not basename identity: duplicate filenames stay distinct."""
    return 'MEDIA-' + hashlib.sha256(path.lstrip('/').encode('utf-8')).hexdigest()[:24]


def _read(name, root=ROOT):
    return json.loads((root / '_data' / name).read_text())


def _local(path, root=ROOT):
    assert isinstance(path, str) and path.startswith('/') and not path.startswith('//'), 'Local media path required'
    candidate = (root / unquote(path).lstrip('/')).resolve()
    assert candidate.is_relative_to(root.resolve()) and candidate.is_file(), 'Missing or unsafe media file'
    return candidate


def _friendly(value):
    return re.sub(r'\s*[—·-]\s*MS-\d+\b', '', value).strip()



# Exact approved product categories provide only their explicit garment/audience
# meaning. Unknown categories need a separate reviewed Showroom classification;
# filenames never determine whether a product is clothing.
SHOP_CLOTHING_CATEGORIES = {
    "men's suits": ('men', 'suit'), "women's suits": ('women', 'suit'),
    'shirts': ('unclassified', 'shirt'), "men's shirts": ('men', 'shirt'),
    "women's shirts": ('women', 'shirt'), 'dresses': ('unclassified', 'dress'),
    'trousers': ('unclassified', 'trousers'), 'skirts': ('unclassified', 'skirt'),
    'jackets': ('unclassified', 'jacket'), 'coats': ('unclassified', 'coat'),
    'tuxedos': ('unclassified', 'tuxedo'), "men's tuxedos": ('men', 'tuxedo'),
}
SHOP_NON_CLOTHING_CATEGORIES = {'clothes hangers', 'hangers', 'garment covers', 'footwear', 'accessories'}


def _shop_clothing_tags(product):
    category = product['category'].strip().casefold().replace('’', "'")
    if category in SHOP_NON_CLOTHING_CATEGORIES:
        return None
    reviewed = product.get('showroom')
    if reviewed is not None:
        assert isinstance(reviewed, dict), 'Reviewed Shop media metadata must be a record'
        approval = reviewed.get('metadataApproval', {})
        assert approval.get('approved') is True and approval.get('evidenceRef'), 'Additional Shop media classification requires real approval evidence'
        assert isinstance(approval.get('date'),str) and re.fullmatch(r'\d{4}-\d{2}-\d{2}',approval['date']), 'Shop media review requires an approval date'
        date.fromisoformat(approval['date'])
        assert reviewed.get('audience') in [*AUDIENCES, 'unclassified']
        assert re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', reviewed.get('garmentType', '')), 'Reviewed clothing tag required'
        tags = reviewed.get('styleTags', [])
        assert isinstance(tags, list) and all(isinstance(tag, str) and re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', tag) for tag in tags)
        known=SHOP_CLOTHING_CATEGORIES.get(category)
        if known:
            assert reviewed['garmentType']==known[1], 'Reviewed Shop garment tag conflicts with its approved product category'
            if known[0]!='unclassified':assert reviewed['audience']==known[0], 'Reviewed Shop audience conflicts with its approved product category'
        return reviewed['audience'], reviewed['garmentType'], list(dict.fromkeys(tags))
    known = SHOP_CLOTHING_CATEGORIES.get(category)
    return (*known, []) if known else None


def _shop_picture(image):
    # Adapt approved Shop image metadata to the existing picture component.
    # There is no image copy, generated stock promise or new photograph.
    candidates = [v for v in image.get('responsiveSources', []) if not v['src'].lower().endswith('.avif')]
    candidates += [{'src': image['src'], 'width': image['width']}]
    unique = {v['src']: v for v in candidates}
    candidates = sorted(unique.values(), key=lambda v: v['width'])
    avifs = [v for v in image.get('responsiveSources', []) if v['src'].lower().endswith('.avif')]
    return {'src': quote(image['src'], safe='/'), 'thumb': quote(candidates[0]['src'], safe='/'),
            'srcset': ', '.join(quote(v['src'], safe='/') + ' ' + str(v['width']) + 'w' for v in candidates),
            'avif': ', '.join(quote(v['src'], safe='/') + ' ' + str(v['width']) + 'w' for v in avifs),
            'alt': image['alt'], 'width': image['width'], 'height': image['height'], 'position': 'center'}


def shop_image_items(existing=(), source=None):
    """Reuse only fully published, rights-approved clothing product images.

    Enquiry-only drafts do not qualify. Existing design/project image records
    keep their classification and Shop association instead of being duplicated.
    Tests may pass a temporary in-memory catalogue; real records are never edited.
    """
    from shop_catalog import load, route
    seen = {unquote(item['assetPath']).lstrip('/') for item in existing}
    result = []
    for product in load(source):
        tags = _shop_clothing_tags(product)
        if tags is None:
            continue
        audience, garment, styles = tags
        for index, image in enumerate(product['images']):
            path = _local(image['src'])
            relative = path.relative_to(ROOT).as_posix()
            if relative in seen:
                continue
            seen.add(relative)
            result.append({
                'mediaId': media_id(relative), 'originalFilename': path.name,
                'originalPath': relative, 'assetPath': quote('/' + relative, safe='/'),
                'title': product['name'], 'mediaType': 'photograph', 'garmentType': garment,
                'audience': audience, 'styleTags': styles, 'sourceOrCreator': None,
                'usageRights': {'approved': True, 'evidenceRef': image['approvalSource'], 'authority': '_data/shop-products.json'},
                'classification': 'shop-product', 'classificationLabel': CLASSIFICATIONS['shop-product'],
                'publicationStatus': 'published', 'detailUrl': route(product),
                'photographUrl': DOMAIN + quote('/' + relative, safe='/'),
                'projectUrl': None, 'shopUrl': route(product),
                'shopAssociation': {'id': product['id'], 'scope': 'Published Shop listing; price, availability and purchase conditions belong to the Shop'},
                'alternativeText': image['alt'], 'image': _shop_picture(image),
                'uploadMetadata': image.get('uploadMetadata'), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
                'sourceRecord': {'file': '_data/shop-products.json', 'id': product['id'], 'imageIndex': index},
            })
    return result


def image_items():
    from build_collections import load, design_route
    from project_catalog import projects
    from suit_references import assignment, model
    from selected_designs import image_url
    from public_enquiries import approved as enquiry_products
    from shop_catalog import load as sale_products, route as shop_route

    eligible, _ = load()
    raw = {d['id']: d for d in _read('collection-designs.json')['designs']}
    labels = model()['references']
    work = {unquote(i['src']): p for p in projects() for i in p['images']}
    # A matching link reuses an already approved Shop display. It is not a new
    # stock, price, checkout or Showroom-photo publication approval.
    shop = enquiry_products() + sale_products()
    shop_photos = {}
    for product in shop:
        for image in product['images']:
            shop_photos.setdefault(unquote(image['src']), product)
    result = []
    for design in eligible:
        record = raw[design['id']]
        category = assignment(design['id'])
        for index, image in enumerate(design['images']):
            original = record['images'][index]['originalPath']
            asset = unquote(image['src'])
            project = work.get(asset)
            product = shop_photos.get(asset)
            kind = 'our-work' if project else 'reference-design'
            styles = list(dict.fromkeys(([category['slug']] if category else []) + record['styles']))
            permission = project['publicationPermission'] if project else record.get('publicationPermission', {})
            evidence = permission.get('evidenceRef') or record.get('provenanceEvidence') or '; '.join(record.get('sources', []))
            assert evidence, 'Existing approved media must retain its source evidence'
            path = _local(image['src'])
            result.append({
                'mediaId': media_id(asset), 'originalFilename': Path(original).name,
                'originalPath': original, 'assetPath': image['src'],
                'title': _friendly(labels.get(design['id'], {}).get('label') or design['name']),
                'mediaType': 'photograph', 'garmentType': record.get('garmentType') or ('suit' if category else ''),
                'audience': category['gender'] if category else design['gender'], 'styleTags': styles,
                'sourceOrCreator': 'Mr Sewing Fashion' if project else None,
                'usageRights': {'approved': True, 'evidenceRef': evidence, 'authority': '_data/customer-projects.json' if project else '_data/collection-designs.json'},
                'classification': kind, 'classificationLabel': CLASSIFICATIONS[kind],
                'publicationStatus': 'published', 'designId': design['id'],
                'detailUrl': design_route(design) + '?' + urlencode({'design': design['id'], 'photo': image_url(image['src'])}),
                'photographUrl': image_url(image['src']),
                'projectUrl': '/our-work/' + project['slug'] + '/' if project else None,
                'shopUrl': shop_route(product) if product else None,
                'shopAssociation': {'id': product['id'], 'scope': 'Existing listing; availability and quotation require confirmation'} if product else None,
                'alternativeText': image['alt'], 'image': image,
                'uploadMetadata': None, 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
                'sourceRecord': {'file': '_data/collection-designs.json', 'id': design['id'], 'imageIndex': index},
            })
    result.extend(shop_image_items(result))
    ids = [item['mediaId'] for item in result]
    assert len(ids) == len(set(ids)), 'One physical path needs one canonical media record'
    return result


def validate_video(record, photographs, projects_by_slug=None, shop_by_id=None, root=ROOT):
    """Return a public video only after separate rights and metadata approval.

    Called at build time, never on public page requests. Tests use temporary files
    and records; no video currently has publication approval in the repository.
    """
    assert isinstance(record, dict) and record.get('publicationStatus') in ['draft', 'published', 'archived']
    if record['publicationStatus'] != 'published':
        return None
    for field in ['usageRights', 'metadataApproval']:
        approval = record.get(field, {})
        assert approval.get('approved') is True and isinstance(approval.get('evidenceRef'), str) and approval['evidenceRef'].strip() and re.fullmatch(r'\d{4}-\d{2}-\d{2}', approval.get('date', '')), 'Video rights and classification need explicit approval'
        try:
            date.fromisoformat(approval['date'])
        except ValueError as error:
            raise AssertionError('Video approval needs a valid date') from error
    assert record.get('classification') in CLASSIFICATIONS
    assert record.get('audience') in [*AUDIENCES, 'unclassified']
    assert re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', record.get('garmentType', '')), 'Reviewed garment tag required'
    assert isinstance(record.get('title'), str) and record['title'].strip()
    assert isinstance(record.get('alternativeText'), str) and record['alternativeText'].strip()
    assert isinstance(record.get('styleTags'), list) and all(re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', tag) for tag in record['styleTags'])
    assert type(record.get('durationSeconds')) in [int, float] and isfinite(record['durationSeconds']) and record['durationSeconds'] > 0
    path = _local(record.get('assetPath'), root)
    assert path.suffix.lower() in ['.mp4', '.webm'], 'Supported local video container required'
    posters = {item['mediaId']: item for item in photographs}
    assert record.get('posterMediaId') in posters, 'A published, approved photograph is required as poster'
    if record['classification'] == 'our-work':
        assert record.get('projectSlug') in (projects_by_slug or {}), 'Approved genuine project association required'
    if record['classification'] == 'shop-product':
        assert record.get('shopProductId') in (shop_by_id or {}), 'Published sale product association required'
    if record.get('designId'):
        assert record['designId'] in {item['designId'] for item in photographs if item.get('designId')}, 'Existing approved design association required'
    poster = posters[record['posterMediaId']]
    relative = str(path.relative_to(root))
    if record['classification']=='shop-product':
        from shop_catalog import route
        detail_url=route(shop_by_id[record['shopProductId']])
    elif record.get('designId'):
        detail_url=next(item['detailUrl'] for item in photographs if item.get('designId')==record['designId'])
    elif record['classification']=='our-work':
        detail_url='/our-work/'+record['projectSlug']+'/'
    else:detail_url='/showroom/'
    return {
        **record, 'mediaId': media_id(relative), 'originalFilename': path.name,
        'originalPath': relative, 'assetPath': '/' + quote(relative, safe='/'),
        'mediaType': 'video', 'classificationLabel': CLASSIFICATIONS[record['classification']],
        'poster': poster, 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
        'detailUrl': detail_url,
        'sourceRecord': {'file': '_data/media-video-records.json', 'assetPath': record['assetPath']},
        'uploadMetadata': record.get('uploadMetadata'),
    }


def published_items():
    photographs = image_items()
    from project_catalog import projects
    from shop_catalog import load as products
    source = _read('media-video-records.json')
    assert source.get('schemaVersion') == 1 and isinstance(source.get('videos'), list)
    videos = [item for record in source['videos'] if (item := validate_video(record, photographs, {p['slug']: p for p in projects()}, {p['id']: p for p in products()}))]
    items = photographs + videos
    assert len(items) == len({item['mediaId'] for item in items}), 'Duplicate media paths/IDs'
    return items


def facets(items=None):
    items = published_items() if items is None else items
    allowed = [item for item in items if item.get('publicationStatus') == 'published' and item.get('usageRights', {}).get('approved') is True]
    return {
        'audiences': {key: label for key, label in AUDIENCES.items() if any(item['audience'] == key for item in allowed)},
        'garments': {key: GARMENTS.get(key, key.replace('-', ' ').title()) for key in sorted({item['garmentType'] for item in allowed if item['garmentType']})},
        'styles': {key: STYLE_LABELS.get(key, key.replace('-', ' ').title()) for key in sorted({tag for item in allowed for tag in item['styleTags']})},
        'classifications': {key: label for key, label in CLASSIFICATIONS.items() if any(item['classification'] == key for item in allowed)},
    }


def settings(items=None):
    items = published_items() if items is None else items
    data = _read('media-library-settings.json')
    assert data.get('schemaVersion') == 1
    available = {item['mediaId']: item for item in items}
    home = data['homepage']
    assert len(home['cards']) == 2 and {card['audience'] for card in home['cards']} == {'men', 'women'}
    for card in home['cards']:
        assert card['mediaId'] in available and available[card['mediaId']]['audience'] == card['audience'], 'Home feature requires an eligible media item for the selected audience'
    assert home['featuredMediaId'] in available, 'Home feature must remain publication-approved'
    pending=home.get('pendingVideoShowcase')
    if pending is not None:
        assert pending.get('status')=='held_awaiting_approvals', 'Pending videos cannot silently activate'
        registered={record['assetPath']:record for record in _read('media-video-records.json')['videos']}
        cards=pending.get('cards',[])
        assert len(cards)==2 and len({card['assetPath'] for card in cards})==2
        for card in cards:
            assert card.get('activationStatus')=='held' and card['assetPath'] in registered
            record=registered[card['assetPath']]
            assert record['publicationStatus']=='draft' and card['audience']==record['audience']
            assert card['fallbackMediaId'] in available and available[card['fallbackMediaId']]['mediaType']=='photograph'
            assert available[card['fallbackMediaId']]['audience']==card['audience'], 'Fallback must retain the actual audience'
            path=_local(record['assetPath']);review=record.get('technicalReview',{})
            assert review.get('status')=='verified' and review.get('bytes')==path.stat().st_size
            assert review.get('sha256')==hashlib.sha256(path.read_bytes()).hexdigest(), 'Prepared video bytes changed after review'
            assert all(type(review.get(key)) is int and review[key]>0 for key in ['width','height'])
            assert record.get('publicationBlockers'), 'Held video needs a precise activation blocker'
    return data


def public_item(item):
    """Only eligible customer-facing records enter browser JSON."""
    keys = ['mediaId', 'originalFilename', 'assetPath', 'title', 'mediaType', 'garmentType', 'audience', 'styleTags', 'classification', 'classificationLabel', 'publicationStatus', 'designId', 'detailUrl', 'photographUrl', 'projectUrl', 'shopUrl', 'alternativeText']
    return {key: item.get(key) for key in keys if key in item}


def inventory():
    """Recoverable hashes and original paths; assets remain in Git, not copied."""
    raw = _read('collection-image-inventory.json')
    items = published_items()
    published = {unquote(item['assetPath']).lstrip('/'): item for item in items}
    original_to_item = {item.get('originalPath'): item for item in items}
    supporting = {}
    for item in items:
        if item['mediaType'] != 'photograph':
            continue
        image = item['image']
        paths = [image['thumb']] + [entry.strip().split()[0] for key in ['srcset', 'avif'] for entry in image.get(key, '').split(',') if entry.strip()]
        for relative in paths:
            supporting[unquote(relative).lstrip('/')] = item
    images = []
    hashes = {}
    for record in raw['images']:
        relative = record['originalImagePath']
        path = ROOT / relative
        assert path.is_file(), 'Media inventory must not hide a missing original'
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        hashes.setdefault(digest, []).append(relative)
        item = published.get(relative) or original_to_item.get(relative)
        derivative = supporting.get(relative) if not item else None
        images.append({
            'mediaId': media_id(relative), 'originalFilename': path.name,
            'storedAssetPath': relative, 'sha256': digest, 'bytes': path.stat().st_size,
            'sourceOriginal': record.get('sourceOriginal'), 'designId': record.get('designId'),
            'publicationStatus': 'published' if item else 'supporting-derivative' if derivative else 'held',
            'activeInShowroom': bool(item or derivative),
            'parentMediaId': derivative['mediaId'] if derivative else None,
            'classification': (item or derivative)['classification'] if item or derivative else None,
            'rightsStatus': 'approved' if item or derivative else record.get('rightsStatus'),
            'sourceRecord': '_data/collection-image-inventory.json',
            'reason': None if item else 'Responsive derivative of an approved original; not an independent gallery item' if derivative else record.get('excludedReason') or 'Not an eligible published clothing original; preserved for review',
        })
    videos = []
    for path in sorted(ROOT.rglob('*')):
        if not path.is_file() or any(part in ['.git', '.wrangler', 'node_modules'] for part in path.parts) or path.suffix.lower() not in ['.mp4', '.webm']:
            continue
        relative = str(path.relative_to(ROOT)); item = published.get(relative)
        videos.append({'mediaId': media_id(relative), 'originalFilename': path.name, 'storedAssetPath': relative, 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(), 'bytes': path.stat().st_size, 'publicationStatus': 'published' if item else 'held', 'reason': None if item else 'No separate video publication and classification approval recorded'})
    identities = [asset['mediaId'] for asset in images + videos]
    assert len(identities) == len(set(identities)), 'Inventory paths and media identities must be unique'
    return {'schemaVersion': 1, 'assetPolicy': 'Originals retained in place and in Git history; hashes identify duplicates without deleting them.', 'sourceAuthorities': ['_data/collection-designs.json', '_data/customer-projects.json', '_data/collection-image-inventory.json', '_data/media-video-records.json', '_data/shop-products.json'], 'images': images, 'videos': videos, 'duplicateGroups': [paths for paths in hashes.values() if len(paths) > 1]}


def inventory_markdown(data=None):
    data = inventory() if data is None else data
    def cell(text):
        return str(text).replace('|', '\\|').replace('\n', ' ')
    result = ['# Recoverable media inventory', '', 'Generated from the existing media and permission records; do not edit this report. No original file is moved, deleted or duplicated.', '', f'{len(data["images"])} image assets and {len(data["videos"])} video files retained. Only the effective publication gates can activate an item.', '', '| ID | Original filename | Stored path | Status | SHA256 |', '| --- | --- | --- | --- | --- |']
    for item in data['images'] + data['videos']:
        result.append('| ' + ' | '.join(cell(item[key]) for key in ['mediaId', 'originalFilename', 'storedAssetPath', 'publicationStatus', 'sha256']) + ' |')
    result += ['', '## Identical-file groups — retained, not deleted', '']
    for paths in data['duplicateGroups']:
        result.append('- ' + ', '.join('`' + path + '`' for path in paths))
    return '\n'.join(result) + '\n'
