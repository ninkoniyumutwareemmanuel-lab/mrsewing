#!/usr/bin/env python3
"""R52 source/preservation checks against immutable reviewed R51 commit.

No live-site, enquiry-receipt or ranking assertions. Temporary fixtures remain
in memory; this test never rewrites approved business records or media.
"""
from pathlib import Path
from unittest.mock import patch
import copy
from urllib.parse import urlsplit,parse_qs
from html.parser import HTMLParser
import argparse,hashlib,json,re,subprocess,sys
ROOT=Path(__file__).resolve().parents[1]
BASE='749b21d99f0dacf21d260b1adfc3ebca52a76447'
OUT=Path('/workspace/review/r52-tailoring-first-2026-11-19')
sys.path.insert(0,str(ROOT/'tests'))
from r51_restructure import Page,PROTECTED
sys.path.insert(0,str(ROOT/'scripts'))
def git(*args):return subprocess.check_output(['git',*args],cwd=ROOT)
def old(path):return git('show',BASE+':'+path)
def sha(value):return hashlib.sha256(value).hexdigest()
def capture():
 files=[p.decode() for p in git('ls-tree','-r','--name-only','-z',BASE).split(b'\0') if p]
 media={};pages={};forms={}
 for path in files:
  content=None
  if re.search(r'\.(?:jpe?g|png|webp|avif|svg|gif|mp4|webm|ico)$',path,re.I):media[path]=sha(old(path))
  if path.endswith('.html') and not path.startswith('_templates/'):
   p=Page(old(path).decode());pages[path]=p.metadata()
   fields=[(tag,a.get('name')) for tag,a in p.tags if tag in {'input','textarea','select'} and a.get('name')]
   actions=[a.get('action','') for tag,a in p.tags if tag=='form']
   if actions:forms[path]={'fields':fields,'actions':actions}
 protected={p:sha(old(p)) for p in PROTECTED|{'_data/public-content-policy.json','_data/media-library-settings.json','_data/media-video-records.json','_data/policy-documents.json','functions/_lib/operational-facts.js','_redirects','sitemap.xml'}}
 result={'baseline':BASE,'media':media,'pages':pages,'forms':forms,'protected':protected}
 OUT.mkdir(parents=True,exist_ok=True);(OUT/'immutable-baseline.json').write_text(json.dumps(result,indent=2)+'\n')
 print('PASS R52 immutable baseline:',len(pages),'HTML,',len(media),'media,',len(forms),'forms')
 return result
class Anchors(HTMLParser):
 def __init__(self,text):super().__init__();self.anchors=[];self.feed(text)
 def handle_starttag(self,tag,attrs):
  if tag=='a':self.anchors.append(dict(attrs))
def rejected(call):
 try:call()
 except (AssertionError,ValueError):return
 raise AssertionError('Invalid reference was accepted')
def main():
 parser=argparse.ArgumentParser();parser.add_argument('--capture-baseline',action='store_true');args=parser.parse_args()
 if args.capture_baseline:capture();return
 baseline=json.loads((OUT/'immutable-baseline.json').read_text()) if (OUT/'immutable-baseline.json').exists() else capture()
 assert git('branch','--show-current').decode().strip()=='phase1/customer-journey-repairs'
 for p,d in baseline['protected'].items():assert sha((ROOT/p).read_bytes())==d,('protected source changed',p)
 for p,d in baseline['media'].items():assert sha((ROOT/p).read_bytes())==d,('originalmedia changed',p)
 overrides=json.loads((ROOT/'_data/public-page-seo.json').read_text())
 intentional={'index.html':'/','services/custom-tailoring/index.html':'/services/custom-tailoring/','services/custom-tailoring/special-order/index.html':'/services/custom-tailoring/special-order/'}
 for alias in ['service-standard.html','service-standard/index.html','service-cmt.html','service-cmt/index.html','service-sketches.html','service-sketches/index.html']:intentional[alias]='/services/custom-tailoring/'
 for p,metadata in baseline['pages'].items():
  assert (ROOT/p).is_file(),('route removed',p)
  actual=Page((ROOT/p).read_text()).metadata()
  for key,value in metadata.items():
   if p=='request/custom-tailoring/index.html' and key in {'title','description','h1'}:
    expected={'title':['Request Tailoring Services | Mr Sewing Fashion, Kigali'],'description':['Tell Mr Sewing Fashion about your tailoring services requirements for assessment and quotation.'],'h1':['Request Tailoring Services']}
    assert actual[key]==expected[key],(p,key,actual[key]);continue
   if p in intentional and key in {'title','description'}:assert actual[key]==[overrides[intentional[p]][key]],(p,key,actual[key]);continue
   if p in {'services/custom-tailoring/standard-order/index.html','services/custom-tailoring/design-choice/index.html'} and key=='h1':
    assert actual[key]==['Suit Tailoring'],(p,key,actual[key]);continue
   if p in intentional and key=='h1':
    expect={'index.html':'Professional Tailor in Kigali, Rwanda','services/custom-tailoring/index.html':'Tailoring Services','services/custom-tailoring/special-order/index.html':'Special Tailoring Request'}.get(p,'Tailoring Services')
    assert actual[key]==[expect],(p,key,actual[key]);continue
   assert actual[key]==value,('unapprovedmetadata',p,key,value,actual[key])
 for p,form in baseline['forms'].items():
  page=Page((ROOT/p).read_text());fields=[(tag,a.get('name')) for tag,a in page.tags if tag in {'input','textarea','select'} and a.get('name')]
  assert fields==[tuple(x) for x in form['fields']] and [a.get('action','') for tag,a in page.tags if tag=='form']==form['actions'],('formchanged',p)
 before=json.loads(old('_data/customer-release.json'));after=json.loads((ROOT/'_data/customer-release.json').read_text())
 for s in after['services']:
  prior=next(x for x in before['services'] if x['id']==s['id'])
  if s['id']=='custom-tailoring':assert {k:v for k,v in s.items() if k not in {'title','intro'}}=={k:v for k,v in prior.items() if k not in {'title','intro'}}
  else:assert s==prior,('other servicechanged',s['id'])
 assert before['pages']==after['pages'],'Contractual/service-information pages changed unexpectedly'
 home=(ROOT/'index.html').read_text();service=(ROOT/'services/custom-tailoring/index.html').read_text()
 assert home.count('class="home-showcase-card"')==2 and home.count('class="home-showcase-feature"')==1
 assert '<video' not in home[home.index('class="home-fashion-showcase"'):home.index('id="hero-section"')],'unapproved video'
 assert 'Have a Design in Mind?' in home and 'Attach your photograph' in home
 for label in ['Suit Tailoring','Special Tailoring','Alterations &amp; Repairs']:assert label in service,label
 assert service.count('class="tailoring-category-card ')==3
 from tailoring_positioning import whatsapp_action,settings
 config=settings();a=Anchors(whatsapp_action()).anchors[0]
 assert 'data-whatsapp-modal' in a and a['data-tailoring-whatsapp']=='homepage-showcase'
 assert parse_qs(urlsplit(a['href']).query)['text']==[config['whatsapp']['message']]
 modified=copy.deepcopy(config);modified['whatsapp']['label']='Fictional changed action label'
 with patch('tailoring_positioning.settings',return_value=modified):assert 'Fictional changed action label' in whatsapp_action()
 refs=json.loads((ROOT/'_data/request-reference-allowlist.json').read_text());ident=next(iter(refs));record=refs[ident]
 a=Anchors(whatsapp_action(context='design-detail',design=ident,photo=record['images'][0]['src'],detail=record['route'])).anchors[0]
 assert a['data-tailoring-photo']==record['images'][0]['src'] and a['data-tailoring-detail']==record['route']
 rejected(lambda:whatsapp_action(design='NOT-APPROVED'))
 rejected(lambda:whatsapp_action(design=ident,photo='/not-approved.jpeg'))
 rejected(lambda:whatsapp_action(design=ident,detail='/wrong-design/'))
 rejected(lambda:whatsapp_action(design=ident,photo='https://example.invalid/'+record['images'][0]['src'].lstrip('/')))
 rejected(lambda:whatsapp_action(context='bad" onclick="x'))
 from r51_restructure import faq_consistency,shop_price_fixture,shared_controller_contract
 faq_consistency();shop_price_fixture();shared_controller_contract()
 print('PASS R52 source/media/Shop/internalprices/policy/forms/routes/indexing preservation; approved scopedmetadata and CTAreference validation')
if __name__=='__main__':main()
