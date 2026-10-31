#!/usr/bin/env python3
"""No unconfirmed care categories, invented prices, hidden charges or turnaround claims."""
import sys,json,copy
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import garment_care as care
import build_journey as journey
from build_public_routes import public_routes
source,published=care.catalog();assert not published and len(source['services'])==6
root=care.ROOT;page=(root/'services/garment-care/index.html').read_text()
assert 'AI-generated' in page and 'Paid suit cleaning — RWF' in page and '40,000' in page and '67,500' in page
for category in source['services']:
 assert category['title'] not in page
 assert '/services/garment-care/'+category['slug']+'/' not in public_routes()
 assert not (root/'services/garment-care'/category['slug']).exists()
read=Path.read_text
base=copy.deepcopy(source)
def trial(data,should_pass=False):
 def override(path,*a,**k):return json.dumps(data) if path==root/'_data/garment-care.json' else read(path,*a,**k)
 with patch.object(Path,'read_text',override):
  try:result=care.catalog()
  except (AssertionError,KeyError):
   assert not should_pass;return
  assert should_pass,'Unapproved care data was accepted'
  return result
x=copy.deepcopy(base);x['services'][0]['published']=True;trial(x)
x['services'][0].update(availabilityConfirmed=True,confirmationEvidenceRef='test evidence',publicationApproved=True);trial(x)
# Test-only complete record stays in memory. Never write fictional examples/prices to the website.
s=x['services'][0];s.update(description='Test fixture only',suitableGarments=['Fixture garment'],process=['Fixture step'],customerPreparation=['Fixture preparation'],limitations=['Fixture limitation'])
trial(x,True)
row={'garmentType':'Fixture garment','serviceType':'Fixture treatment','standardPriceRwf':12345,'approved':False,'approvalEvidenceRef':None,'additionalCharges':[],'notes':None};s['pricing']['rows']=[row]
with patch.object(Path,'read_text',lambda p,*a,**k:json.dumps(x) if p==root/'_data/garment-care.json' else read(p,*a,**k)):
 html=journey.care_page(next(v for v in journey.services() if v['id']=='garment-care'),s)
 assert '<table' not in html and '12,345' not in html
row['approved']=True;trial(x)
row['approvalEvidenceRef']='test approval';row['standardPriceRwf']=0;trial(x)
row['standardPriceRwf']=12345;trial(x,True)
with patch.object(Path,'read_text',lambda p,*a,**k:json.dumps(x) if p==root/'_data/garment-care.json' else read(p,*a,**k)):
 html=journey.care_page(next(v for v in journey.services() if v['id']=='garment-care'),s)
 assert 'RWF 12,345' in html and '<caption>Approved care prices' in html
s['pricing']['standardTurnaround'].update(approved=True,minimum=1,maximum=3);trial(x)
s['pricing']['standardTurnaround']['approvalEvidenceRef']='test timing';trial(x,True)
s['pricing']['express'].update(approved=True,available=True);trial(x)
assert source['currency']=='RWF'
print('PASS: six care categories stay unpublished; availability/publication/completeness gates, positive evidenced RWF rates, withheld unapproved prices and confirmed-only turnaround/express controls.')
