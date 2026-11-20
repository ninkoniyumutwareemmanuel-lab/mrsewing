"""R51 effective media gates, filename reuse, empty categories and video fixtures.

No approved data is changed. A small temporary container tests metadata safety;
it does not claim real browser playback or a new publication permission.
"""
from pathlib import Path
from urllib.parse import unquote
from copy import deepcopy
from unittest.mock import patch
import hashlib
import json
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from media_library import image_items, published_items, facets, settings, inventory, media_id, validate_video, public_item, shop_image_items
from showroom import render, homepage_showcase, homepage_css, outputs
from build_collections import load
from project_catalog import projects
from selected_designs import image_url

items = published_items()
designs = load()[0]
assert len(items) == len(designs) == 28
assert {item['designId'] for item in items} == {design['id'] for design in designs}
assert all(item['mediaType'] == 'photograph' for item in items)
assert len([item for item in items if item['classification'] == 'our-work']) == 7
assert len([item for item in items if item['classification'] == 'reference-design']) == 21
assert not [item for item in items if item['classification'] == 'shop-product']
assert len(items) < sum(record['published'] for record in json.loads((ROOT / '_data/collection-designs.json').read_text())['designs'])
assert {item['mediaId'] for item in items} == {media_id(unquote(item['assetPath'])) for item in items}
# Encoded asset URLs are normalized before ID generation; source paths remain stable.
assert len({item['mediaId'] for item in items}) == len(items)
assert media_id('a/shared.jpg') != media_id('b/shared.jpg')

work_paths = {image['src'] for project in projects() for image in project['images']}
by_id = {item['designId']: item for item in items}
for item in items:
    from urllib.parse import unquote
    path = ROOT / unquote(item['assetPath']).lstrip('/')
    assert item['sha256'] == hashlib.sha256(path.read_bytes()).hexdigest()
    assert item['photographUrl'] == image_url(item['assetPath'])
    assert item['originalFilename'] == Path(item['originalPath']).name
    assert item['usageRights']['approved'] and item['usageRights']['evidenceRef']
    assert '/collections/designs/' in item['detailUrl'] and 'photo=' in item['detailUrl']
    assert (unquote(item['assetPath']) in work_paths) == (item['classification'] == 'our-work')
    assert item['sourceOrCreator'] == ('Mr Sewing Fashion' if item['classification'] == 'our-work' else None)
    if item.get('shopUrl'):
        assert item['shopUrl'].startswith('/shop/') and 'enquiry' not in item['classification']
    assert 'usageRights' not in public_item(item), 'Browser projection does not need internal evidence text'
assert by_id['MS-007']['audience'] == 'unclassified', 'Do not invent a gender for the unassigned reference'
assert all(by_id['MS-' + str(i).zfill(3)]['classification'] == 'reference-design' for i in range(29, 37))

groups = facets(items)
assert set(groups['audiences']) == {'men', 'women'}
assert set(groups['garments']) == {'suit', 'tuxedo'}
assert 'dress' not in groups['garments'] and 'shirt' not in groups['garments']
draft = {**items[0], 'publicationStatus': 'draft', 'garmentType': 'dress'}
archived = {**items[0], 'publicationStatus': 'archived', 'garmentType': 'shirt'}
unapproved = {**items[0], 'usageRights': {'approved': False}, 'garmentType': 'jumpsuit'}
assert facets(items + [draft, archived, unapproved]) == groups
approved_new_type = {**items[0], 'garmentType': 'dress'}
assert 'dress' in facets(items + [approved_new_type])['garments'], 'A reviewed new garment category activates from data'
approved_other_type = {**items[0], 'garmentType': 'jumpsuit'}
assert 'jumpsuit' in facets(items + [approved_other_type])['garments'], 'No one-fabric/one-category hardcoding'
home = settings(items)['homepage']
assert len(home['cards']) == 2 and len({card['mediaId'] for card in home['cards']}) == 2
assert {card['audience'] for card in home['cards']} == {'men', 'women'}
assert home['featuredMediaId'] in {item['mediaId'] for item in items if item['classification'] == 'our-work'}

inv = inventory()
# R53 owner upload commit adds exactly25photos and2videos; originals stay intact.
assert len(inv['images']) == 427 and len(inv['videos']) == 9
assert all(video['publicationStatus'] == 'held' for video in inv['videos'])
assert any(image['publicationStatus'] == 'supporting-derivative' for image in inv['images'])
assert sum(image['publicationStatus'] == 'published' for image in inv['images']) == 28
assert ['r19.jpeg', 's4.jpeg'] in inv['duplicateGroups']
assert ['r37.jpeg', 'r38.jpeg', 'r39.jpeg'] in inv['duplicateGroups']
assert ['neck.jepg.webp', 'neck.webp'] in inv['duplicateGroups']
for asset in inv['images'] + inv['videos']:
    path = ROOT / asset['storedAssetPath']
    assert path.is_file() and asset['bytes'] == path.stat().st_size
UPLOAD_COMMIT = 'ce98ee3991a43483357304b5fe9f2f0a83f7ae27'
MEDIA_SUFFIXES = {'.jpg', '.jpeg', '.png', '.webp', '.avif', '.mp4', '.webm'}
uploaded = [name for name in subprocess.check_output(['git', 'diff-tree', '--no-commit-id', '--name-only', '-r', '--diff-filter=A', UPLOAD_COMMIT], cwd=ROOT, text=True).splitlines() if Path(name).suffix.lower() in MEDIA_SUFFIXES]
assert len(uploaded) == 27 and sum(Path(name).suffix.lower() == '.webp' for name in uploaded) == 25
# The precise owner-uploaded bytes are authorized additions, never permission to
# modify originals or promote the held records into customer-facing content.
for name in uploaded:
    assert (ROOT / name).read_bytes() == subprocess.check_output(['git', 'show', UPLOAD_COMMIT + ':' + name], cwd=ROOT), ('Uploaded original changed', name)
changes = subprocess.check_output(['git', 'diff', '--name-status', 'b2b8946882929da4ce7e0e01de4ba1511eed818a'], cwd=ROOT, text=True).splitlines()
for change in changes:
    status, name = change.split('\t', 1)
    if Path(name).suffix.lower() in MEDIA_SUFFIXES:
        assert status == 'A' and name in uploaded, ('Unauthorized original media change', status, name)


# Eligible Shop-only clothing is reusable without creating another Shop or
# inventing a tailoring design identity. All records below are memory fixtures.
raw_products=json.loads((ROOT/'_data/shop-products.json').read_text())['products']
stock=deepcopy(next(p for p in raw_products if p['category']=='Shirts'))
stock.update(id='R51_MEDIA_FIXTURE',slug='r51-media-fixture-shirt',publicationStatus='published',
             missingInformation=[],availability='Available in Stock',priceRwf=173000,priceApproved=True,
             stockQuantity=2,variations=[{'id':'R51_MEDIA_SIZE','size':'M','colour':'White','stockQuantity':2}],
             approval={'publicDisplay':True,'source':'Synthetic media fixture, never publication approval','date':'2026-11-19'},
             careInstructions='Temporary test only',orderingNotes='Temporary test only',specifications={})
for image in stock['images']:image.update(rightsApproved=True,approvalSource='Synthetic media fixture only')
fixture_source={'schemaVersion':1,'products':[stock]}
shop_only=shop_image_items(items,fixture_source)
assert len(shop_only)==1 and shop_only[0]['classification']=='shop-product'
assert shop_only[0]['garmentType']=='shirt' and shop_only[0]['audience']=='unclassified'
assert shop_only[0]['detailUrl']=='/shop/r51-media-fixture-shirt/'
assert 'designId' not in shop_only[0], 'Product images do not fabricate selected-design identities'
assert shop_only[0]['originalFilename']==Path(stock['images'][0]['src']).name
assert 'shirt' in facets(items+shop_only)['garments']
assert 'shop-product' in facets(items+shop_only)['classifications']
assert 'priceRwf' not in shop_only[0] and 'stockQuantity' not in shop_only[0], 'Shop stays the only inventory/price owner'
for state in ['draft','archived']:
    assert not shop_image_items(items,{'schemaVersion':1,'products':[{**stock,'publicationStatus':state}]})
for category in ['Clothes Hangers','Garment Covers','Footwear','Unreviewed Clothing Group']:
    assert not shop_image_items(items,{'schemaVersion':1,'products':[{**stock,'category':category}]})
unsafe=deepcopy(stock);unsafe['images'][0]['rightsApproved']=False
try:
    shop_image_items(items,{'schemaVersion':1,'products':[unsafe]})
    raise RuntimeError('Unapproved Shop photograph accepted')
except AssertionError:pass
classified={**stock,'category':'Reviewed Occasion Clothing','showroom':{'audience':'unclassified','garmentType':'dress','styleTags':['ceremony'],'metadataApproval':{'approved':True,'evidenceRef':'Synthetic manual category review','date':'2026-11-19'}}}
reviewed_items=shop_image_items(items,{'schemaVersion':1,'products':[classified]})
assert len(reviewed_items)==1 and 'dress' in facets(items+reviewed_items)['garments']
assert reviewed_items[0]['styleTags']==['ceremony']
conflicting={**classified,'category':"Men's Suits"}
try:
    shop_image_items(items,{'schemaVersion':1,'products':[conflicting]})
    raise RuntimeError('Conflicting approved product/category tags accepted')
except AssertionError:pass
reused=deepcopy(stock);original=items[0];reused['category']="Men's Suits";reused['images']=[{'src':unquote(original['assetPath']),'alt':original['alternativeText'],'width':original['image']['width'],'height':original['image']['height'],'rightsApproved':True,'approvalSource':'Synthetic duplicate-path test'}];reused['socialImage']=reused['images'][0]['src']
assert not shop_image_items(items,{'schemaVersion':1,'products':[reused]}), 'An approved design/product shared path remains one media record'
# Exercise the actual loader integration without changing the Shop source file.
import shop_catalog
real_shop_load=shop_catalog.load
def fixture_load(source=None):return real_shop_load(fixture_source if source is None else source)
with patch('shop_catalog.load',side_effect=fixture_load):
    combined=image_items()
    assert len(combined)==29 and len([m for m in combined if m['classification']=='shop-product'])==1
    from showroom import _card
    product_card=_card(next(m for m in combined if m['classification']=='shop-product'))
    assert 'showroom-shop-link' in product_card and 'showroom-design-link' not in product_card
    assert 'Shop Product' in product_card and '/shop/r51-media-fixture-shirt/' in product_card
    assert '173,000' not in product_card and '173000' not in product_card
assert len(published_items())==28, 'Fixtures never publish or alter the real empty sale catalogue'

with tempfile.TemporaryDirectory() as temporary:
    base = Path(temporary)
    (base / 'reviewed-video.mp4').write_bytes(b'\x00\x00\x00\x18ftypmp42temporary fixture only')
    record = {'assetPath': '/reviewed-video.mp4', 'title': 'Fictional reviewed video', 'alternativeText': 'Fictional suit video metadata test', 'audience': 'men', 'garmentType': 'suit', 'styleTags': ['single-breasted'], 'classification': 'reference-design', 'publicationStatus': 'draft', 'durationSeconds': 15, 'posterMediaId': items[0]['mediaId'], 'usageRights': {'approved': False, 'evidenceRef': None, 'date': None}, 'metadataApproval': {'approved': False, 'evidenceRef': None, 'date': None}}
    assert validate_video(record, items, root=base) is None
    record['publicationStatus'] = 'published'
    try:
        validate_video(record, items, root=base)
        raise AssertionError('Missing video approval must fail')
    except AssertionError as error:
        assert str(error) != 'Missing video approval must fail'
    for field in ['usageRights', 'metadataApproval']:
        record[field] = {'approved': True, 'evidenceRef': 'Synthetic fixture, never a publication approval', 'date': '2026-11-19'}
    video = validate_video(record, items, root=base)
    assert validate_video({**record,'designId':items[0]['designId']},items+shop_only,root=base)['detailUrl']==items[0]['detailUrl']
    assert validate_video({**record,'classification':'shop-product','shopProductId':stock['id']},items+shop_only,shop_by_id={stock['id']:stock},root=base)['detailUrl']=='/shop/r51-media-fixture-shirt/'
    assert video['mediaType'] == 'video' and video['poster']['mediaId'] == items[0]['mediaId']
    for patch in [{'assetPath': 'https://foreign.invalid/movie.mp4'}, {'posterMediaId': 'held'}, {'classification': 'our-work', 'projectSlug': 'invented'}, {'classification': 'shop-product', 'shopProductId': 'draft'}]:
        try:
            validate_video({**record, **patch}, items, root=base)
            raise RuntimeError('Unsafe video fixture accepted')
        except AssertionError:
            pass
    assert validate_video({**record, 'publicationStatus': 'archived'}, items, root=base) is None

page = render()
assert page.count('<h1>') == 1 and '<h1>Clothing Showroom</h1>' in page
assert page.count('class="showroom-card"') == len(items)
assert page.count('class="announcement-bar"') == 1
assert 'value="dress"' not in page and 'value="shirt"' not in page
assert 'm-kaundasuits3.jpeg' in page and 'Reference Design' in page and 'Our Work' in page
assert '<video' not in page and 'ready-made stock' in page
assert all(item['originalFilename'].replace('&', '&amp;').replace('"', '&quot;').replace("'", '&#x27;') in page for item in items)
showcase = homepage_showcase()
assert showcase.count('class="home-showcase-card"') == 2
assert showcase.count('class="home-showcase-feature"') == 1
assert '<video' not in showcase and 'Reference Design' in showcase and 'Our Work' in showcase
assert '/showroom/?audience=men' in showcase and '/showroom/?audience=women' in showcase
assert 'home-fashion-showcase' in homepage_css()
assert ROOT / 'showroom/index.html' in outputs()
print('PASS effective28media/7genuine21reference/rightsheldlegacy/427images9heldvideos/hashrecovery/duplicatefilenames/nonemptyfacets/manualvideogates/eligibleShopclothingfixtures/no2ndShop/homefeatures/exactdesignphotos/nooriginalchanges')
