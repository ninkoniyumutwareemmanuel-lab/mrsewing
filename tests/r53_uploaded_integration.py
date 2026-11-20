#!/usr/bin/env python3
"""R53 uploaded originals, gated design families/video preparation and real PDF.

Assertions use the actual owner-upload commit; synthetic publication fixtures
exist only in memory and never change an approved business/media record.
"""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import parse_qs,urlsplit
from copy import deepcopy
from unittest.mock import patch
import hashlib,json,subprocess,sys
ROOT=Path(__file__).resolve().parents[1]
UPLOAD='ce98ee3991a43483357304b5fe9f2f0a83f7ae27'
PRIOR='812aaca489bec127308520dce166b9298419d9d2'
OUT=Path('/workspace/review/r53-uploaded-integration-2026-11-19')
sys.path.insert(0,str(ROOT/'scripts'))
def git(*args):return subprocess.check_output(['git',*args],cwd=ROOT)
def sha(value):return hashlib.sha256(value).hexdigest()
def read(path):return json.loads((ROOT/path).read_text())
class Links(HTMLParser):
 def __init__(self,text):super().__init__();self.links=[];self.feed(text)
 def handle_starttag(self,tag,attrs):
  if tag=='a':self.links.append(dict(attrs))
def main():
 OUT.mkdir(parents=True,exist_ok=True)
 assert git('branch','--show-current').decode().strip()=='phase1/customer-journey-repairs'
 uploads=[p.decode() for p in git('diff-tree','--no-commit-id','--name-only','-r','--diff-filter=A','-z',UPLOAD).split(b'\0') if p]
 assert len(uploads)==28
 for path in uploads:assert (ROOT/path).read_bytes()==git('show',UPLOAD+':'+path),('Uploaded original changed',path)
 photographs=[p for p in uploads if p.endswith('.webp')];assert len(photographs)==25
 videos=[p for p in uploads if p.endswith('.mp4')];assert set(videos)=={'1024X768VIDEO.mp4','1024X768black.mp4'}
 old=read('_data/collection-designs.json');prior=json.loads(git('show',PRIOR+':_data/collection-designs.json'));prior_by={r['id']:r for r in prior['designs']}
 by_id={r['id']:r for r in old['designs']};new=[r for r in old['designs'] if r['id'] not in prior_by]
 assert len(new)==22 and {r['id'] for r in new}=={'MS-'+str(i) for i in range(152,174)}
 for ident,record in prior_by.items():assert by_id[ident]==record,('Existing design changed',ident)
 assert old['nextId']==174
 registry=read('_data/collection-id-registry.json');oldregistry=json.loads(git('show',PRIOR+':_data/collection-id-registry.json'))
 for ident,anchor in oldregistry.items():assert registry[ident]==anchor
 assert {i['originalPath'] for r in new for i in r['images']}==set(photographs)
 assert sum(len(r['images']) for r in new)==25
 assert len({r['family']['id'] for r in new})==17
 categories=read('_data/suit-reference-categories.json');oldcategories=json.loads(git('show',PRIOR+':_data/suit-reference-categories.json'))
 assert categories['categories']==oldcategories['categories'] and categories['references']==oldcategories['references']
 assert set(categories['preparedAssignments'])=={r['id'] for r in new}
 from PIL import Image
 for r in new:
  assert r['published'] is False and r['rightsStatus']=='review_required'
  assert r['classification']=='reference-design' and r['provenance']=='design_inspiration'
  assert r['publicationBlockers'] and r['sources'] and r['metadataEvidence']
  assert r['sourceOrCreator'] is None
  assert r['proposedCategoryId'] in {c['id'] for c in categories['categories']}
  assert registry[r['id']]==r['sourceAnchor']==r['images'][0]['originalPath']
  for image in r['images']:
   assert image['src']=='/'+image['originalPath'] and image['alt'].strip()
   with Image.open(ROOT/image['originalPath']) as opened:assert opened.size==(image['width'],image['height'])
 assert by_id['MS-156']['family']['variant']['colour']=='Burgundy'
 assert [i['catalogueNo'] for i in by_id['MS-156']['images']]==[5,12]
 assert by_id['MS-156']['metadataReviewStatus']=='owner_correction_required'
 assert len(by_id['MS-157']['images'])==1 and by_id['MS-157']['catalogueNumbers']==[6]
 assert by_id['MS-161']['metadataReviewStatus']=='visually_reviewed_pending_owner_publication'
 assert by_id['MS-161']['editorialReview']['status']=='completed' and len(by_id['MS-161']['publicationBlockers'])==1
 assert by_id['MS-161']['id']!=by_id['MS-166']['id']
 assert [i['catalogueNo'] for i in by_id['MS-169']['images']]==[21,19,20]
 # Effective publication and quotation gates remain unchanged.
 from build_collections import load
 from media_library import published_items,inventory
 published,_=load();assert len(published)==28 and not ({r['id'] for r in published}&{r['id'] for r in new})
 media=published_items();assert len(media)==28 and all(r['mediaType']=='photograph' for r in media)
 refs=read('_data/request-reference-allowlist.json');assert not set(refs).intersection(r['id'] for r in new)
 inv=inventory();assert len(inv['images'])==427 and len(inv['videos'])==9
 for image in inv['images']:
  if image['storedAssetPath'] in photographs:assert image['publicationStatus']=='held' and not image['activeInShowroom']
 # The existing family renderer is tested with explicit in-memory approvals only.
 from design_families import family_navigation
 def fixture(r):
  result=deepcopy(r);result.update(published=True,rightsStatus='approved',metadataReviewStatus='approved',publicationBlockers=[]);return result
 black,navy=fixture(by_id['MS-154']),fixture(by_id['MS-155'])
 picture=lambda image:'<img src="'+image['src']+'" alt="Fixture reference">'
 assert family_navigation(by_id['MS-154'],new,picture)==''
 html=family_navigation(black,[black,navy,navy,by_id['MS-156'],{**navy,'id':'FEMALE_FIXTURE','gender':'women'}],picture)
 links=Links(html).links;assert len(links)==2 and sum(a.get('aria-current')=='page' for a in links)==1
 assert 'Black' in html and 'Navy Blue' in html and 'Burgundy' not in html
 (OUT/'family-fixture.html').write_text('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>R53 synthetic family QA</title><style>'+ (ROOT/'_templates/collections.css').read_text()+'</style></head><body><main><h1>Synthetic approved-family fixture</h1><p>Temporary QA only; uploaded company photographs remain held.</p>'+html+'</main></body></html>')
 for link,record in zip(links,[black,navy]):
  query=parse_qs(urlsplit(link['href']).query);assert query['design']==[record['id']] and query['photo']==['https://mrsewingfashion.com'+record['images'][0]['src']]
 assert family_navigation(black,[black,{**navy,'images':black['images']}],picture)==''
 ivory=fixture(by_id['MS-169'])
 from selected_designs import design_media
 # Future-approved three-view source is preserved by the existing allowlist
 # builder; no held record is added to the real runtime allowlist.
 for image in ivory['images']:image['url']='https://mrsewingfashion.com'+image['src']
 with patch('build_collections.load',return_value=([ivory],{})):
  candidate=design_media()[ivory['id']]
  assert [i['url'] for i in candidate['images']]==['https://mrsewingfashion.com'+i['src'] for i in ivory['images']]
  assert len(candidate['images'])==3
 # Uploaded-video metadata is verified against real local probes, not filenames.
 from media_library import validate_video
 video_records=read('_data/media-video-records.json')['videos'];assert len(video_records)==2
 for r in video_records:
  assert r['publicationStatus']=='draft' and r['usageRights']['approved'] is False and r['metadataApproval']['approved'] is False
  assert r['posterMediaId'] is None and r['publicationBlockers']
  assert r['classification']=='reference-design' and r['audience']=='men'
  assert validate_video(r,media) is None
  path=ROOT/r['assetPath'].lstrip('/');probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)]))
  stream=next(s for s in probe['streams'] if s['codec_type']=='video');technical=r['technicalReview']
  assert (stream['width'],stream['height'])==(technical['width'],technical['height'])==(720,1280)
  assert technical['sha256']==sha(path.read_bytes()) and technical['bytes']==path.stat().st_size
  assert technical['fastStart'] is True and technical['decodeCheck'].startswith('passed')
  assert abs(float(probe['format']['duration'])-r['durationSeconds'])<0.02
 home=read('_data/media-library-settings.json')['homepage'];oldhome=json.loads(git('show',PRIOR+':_data/media-library-settings.json'))['homepage']
 assert home['cards']==oldhome['cards'] and home['featuredMediaId']==oldhome['featuredMediaId']
 pending=home['pendingVideoShowcase'];assert pending['status']=='held_awaiting_approvals' and {c['assetPath'] for c in pending['cards']}=={r['assetPath'] for r in video_records}
 # The actual approved PDF is integrated as a review document without inventing
 # the future official-publication date or replacing current contractual text.
 document=read('_data/policy-documents.json')['documents']['terms-and-conditions'];assert document['currentVersion'] is None
 received=document['receivedVersions'];assert len(received)==1
 pdf=received[0];assert pdf['version']=='1.0' and pdf['approvalStatus']=='approved' and pdf['publicationStatus']=='staging-review'
 assert pdf['effectiveDate'] is None and pdf['effectiveDateBasis']=='official-website-publication' and pdf['preparedDate']=='2026-11-19'
 assert pdf['technicalInspection']['companyRegistrationDate'] is None and pdf['technicalInspection']['preparationDateIsNotRegistrationDate'] is True
 assert pdf['technicalInspection']['pages']==5 and pdf['technicalInspection']['selectableText'] is True
 for path in [pdf['originalUploadPath'],pdf['sourcePath'],pdf['publishedPath'].lstrip('/')]:assert sha((ROOT/path).read_bytes())==pdf['sha256']
 extracted=subprocess.check_output(['pdftotext','-layout',str(ROOT/pdf['originalUploadPath']),'-']).decode()
 normalized=' '.join(extracted.lower().split())
 assert 'preparation date is not' in normalized and 'date of publication' in normalized
 rendered=(ROOT/'terms-and-conditions/index.html').read_text()
 assert 'data-policy-document-review="1.0"' in rendered and 'data-policy-document-current=' not in rendered
 assert pdf['publishedPath']+'#view=FitH' in rendered and 'download=' in rendered
 assert 'operational reconciliation' in rendered and 'current online Terms' in rendered
 # No operational business facts or production settings are changed by receipt.
 for path in ['_data/customer-policy-facts.json','_data/customer-release.json','_data/customer-information.json','_data/customer-faqs.json','_data/suit-package-prices.json','_data/tuxedo-package-prices.json','_data/shop-products.json','_data/shop-public-enquiries.json','_headers','_redirects','robots.txt','CNAME','_data/public-api.json']:
  assert (ROOT/path).read_bytes()==git('show',PRIOR+':'+path),('Protected source changed',path)
 evidence={'status':'PASS','baseline':UPLOAD,'registeredDesignsAndVariants':22,'families':17,'uploadedPhotos':25,'eligiblePublicPhotos':28,'newPhotosVisible':0,'heldNewPhotos':25,'preparedVideos':2,'activeVideos':0,'pdfPages':5,'pdfContentApproved':True,'pdfCurrentVersion':None,'pdfReviewViewer':True,'originalUploadsUnchanged':True,'actualDeployedVerification':False,'realMessagesOrSubmissions':False}
 (OUT/'source.json').write_text(json.dumps(evidence,indent=2)+'\n')
 print('PASS R53 actual25photos/22records/17families/rightsheld/variant+3viewfixtures/2verifiedheldvideos/realapprovedPDFreview/noinventeddate/preservedfacts')
if __name__=='__main__':main()
