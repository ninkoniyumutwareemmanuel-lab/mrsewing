"""25Nov recovery: silent-only media, prepared metadata and About source preservation."""
from pathlib import Path
from copy import deepcopy
import hashlib,json,shutil,subprocess,sys,tempfile
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'scripts'))
from homepage_video_cards import verified_playback,render
records=json.loads((R/'_data/media-video-records.json').read_text())['videos']
assert len(records)==2 and render().count('<video')==2
for record in records:
 assert verified_playback(record),record['assetPath']
 with tempfile.TemporaryDirectory() as tmp:
  root=Path(tmp);p=deepcopy(record)
  for key in ['assetPath','posterPath']:
   path=root/p['playback'][key].lstrip('/');path.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(R/p['playback'][key].lstrip('/'),path)
  assert verified_playback(p,root)
  poster=root/p['playback']['posterPath'].lstrip('/');poster.unlink();assert verified_playback(p,root) is None
  shutil.copyfile(R/p['playback']['posterPath'].lstrip('/'),poster)
  clip=root/p['playback']['assetPath'].lstrip('/');shutil.copyfile(R/record['assetPath'].lstrip('/'),clip)
  p['playback']['sha256']=hashlib.sha256(clip.read_bytes()).hexdigest();p['playback']['bytes']=clip.stat().st_size
  assert verified_playback(p,root) is None,'Actual audio track must fail even if metadata calls the source silent'
  p['playback']['assetPath']='/assets/videos/../../private.mp4';assert verified_playback(p,root) is None
from build_about import render as about
html=about()
#26Nov owner-authorized About redesign replaces the former hero/CTA copy;
#protect verified business identity, all service destinations and approved values.
for text in ['Company Information','Our Mission','Our Vision','What We Stand For','NINKONIYUMUTWARE NEXUS LTD','/services/custom-tailoring/','/services/alterations/','/services/garment-care/','/services/mobile-fitting/','/services/vip/']:
 assert text in html,('Owner25NovAbout source lost',text)
designs=json.loads((R/'_data/collection-designs.json').read_text())['designs'];prepared=[d for d in designs if 152<=int(d['id'].split('-')[1])<=173]
assert len(prepared)==22 and sum(len(d['images']) for d in prepared)==25
assert all(d['rightsStatus']=='approved' and not d['published'] and d['publicationPermission']['approved'] for d in prepared)
byid={d['id']:d for d in prepared}
assert byid['MS-156']['family']['variant']['colour']=='Burgundy' and byid['MS-156']['images'][1]['originalPath']=='sovereign-gold-button-double-breasted-suit-01-olive.webp'
assert byid['MS-156']['metadataReviewStatus']=='visually_reviewed_pending_gallery_placement'
assert [i['catalogueNo'] for i in byid['MS-169']['images']]==[21,19,20]
print('PASS silent-only actual-track/hash/poster/path guards; current About source;22prepared25photos with R61 rights and preserved unpublished status/grouping')

from route_recovery import alias
from customer_site import outputs
files=outputs()
assert files[R/'why-choose/index.html']==files[R/'why-choose.html']
assert files[R/'showroom/index.html']==alias('/collections/','Showroom — Explore Clothing Designs',True)
assert 'u.searchParams.get("audience")' in files[R/'showroom/index.html']
assert 'u.search+u.hash' in files[R/'showroom/index.html']
assert '/happy-customers/ /our-work/ 301' in __import__('build_public_routes').outputs()[R/'_redirects']
from design_families import family_navigation
fixture=[]
for i,c in enumerate(['Black','Navy','Burgundy','Olive']):
 fixture.append({'id':'QA'+str(i),'slug':'qa-'+str(i),'name':'Temporary fixture','gender':'men','family':{'id':'qa-family','name':'Fictional family','variant':{'label':c}},'images':[{'src':'/qa-'+str(i)+'.jpeg'}]})
picture=lambda img:'<img src="'+img['src']+'" alt="Fixture">'
nav=family_navigation(fixture[0],fixture,picture)
assert nav.count('class="design-family-variant"')==4 and nav.count('aria-current="page"')==1
assert family_navigation(fixture[0],[fixture[0]],picture)==''
assert 'qa-4' not in family_navigation(fixture[0],fixture+[dict(fixture[0],id='QA4',published=False)],picture)
print('PASS recovered Showroom query compatibility/legacy destinations and publication-gated same-audience family navigation fixtures')

# Isolated fixtures prove QA exclusions cannot hide real unapproved website media.
from tempfile import TemporaryDirectory
from pathlib import Path
from build_collections import validate_inventory_paths
with TemporaryDirectory() as folder:
    fixture=Path(folder)
    target=fixture/'not-approved.png';target.write_bytes(b'qa fixture')
    try:
        validate_inventory_paths(fixture,set())
    except AssertionError as error:
        assert 'Uninventoried asset:' in str(error)
    else:
        raise AssertionError('Unregistered website image must fail inventory validation')
    validate_inventory_paths(fixture,{'not-approved.png'})
    target.unlink()
    for local in ['artifacts','node_modules','.wrangler']:
        (fixture/local).mkdir();(fixture/local/'tool-output.png').write_bytes(b'qa fixture')
    validate_inventory_paths(fixture,set())
print('PASS strict website asset inventory remains enforced after excluding local QA/dependency roots')
