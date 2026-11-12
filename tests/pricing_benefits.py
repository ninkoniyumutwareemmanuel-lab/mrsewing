"""R37 source and current-content audit; no historical records or runtime fixtures modified."""
from pathlib import Path
import sys,json,re,subprocess,copy
from html.parser import HTMLParser
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'scripts'))
from suit_pricing import catalogue,rows
from customer_information import expand
from faq_help import search_data
from customer_guides import cards,fabrics
expected={'men':[(600000,800000),(400000,550000),(300000,400000),(250000,300000)],'women':[(500000,550000),(350000,400000),(220000,270000),(150000,200000)]}
for audience,prices in expected.items():assert [(p['twoPieceRwf'],p['threePieceRwf']) for p in rows(audience)]==prices
assert all(k==p['category']+'-tier-'+str(p['tier']) for k,p in catalogue()['prices'].items())
assert (R/'_data/tuxedo-package-prices.json').read_bytes()==subprocess.check_output(['git','show','0a446ad:_data/tuxedo-package-prices.json'],cwd=R)
assert 'mensOrdinaryPrices' not in json.loads((R/'_data/custom-tailoring-page.json').read_text())
assert all(f['category']+'-tier-'+str(f['tier']) in catalogue()['prices'] for f in fabrics())
# A second fabric in the same tier renders by classification, without a price key or numeric schedule.
import customer_guides as guides
original=guides.fabrics;extra=copy.deepcopy(fabrics()[1]);extra['id']='synthetic-second-fabric-same-tier'
try:
 guides.fabrics=lambda:original()+[extra]
 html=cards('men');assert 'synthetic-second-fabric-same-tier' in html and 'suit-package-prices' not in html
finally:guides.fabrics=original
faq=json.loads((R/'_data/customer-faqs.json').read_text());required=['suit-package','suit-tier-differences','suit-complimentary-cleanings','suit-cleaning-window','suit-followup-shirt','suit-benefit-transport','higher-collections','fabric-tier-pricing','bulk-order-discount','parent-child-offer','payment-verification']
for id in required:assert id in faq['questions'] and '{{' not in expand(faq['questions'][id]['answer'])
for id,text in [('suit-cleaning-window','three months'),('suit-followup-shirt','one shirt'),('suit-benefit-transport','customer-paid'),('bulk-order-discount','highest-priced'),('parent-child-offer','automatically'),('payment-verification','pending transactions')]:assert text in expand(faq['questions'][id]['answer'])
class Text(HTMLParser):
 def __init__(self):super().__init__();self.parts=[];self.skip=0
 def handle_starttag(self,t,a):
  if t in ['script','style']:self.skip+=1
 def handle_endtag(self,t):
  if t in ['script','style']:self.skip=max(0,self.skip-1)
 def handle_data(self,s):
  if not self.skip:self.parts.append(s)
files=subprocess.check_output(['git','ls-files','*.html'],cwd=R,text=True).splitlines();old=[]
for file in files:
 p=Text();p.feed((R/file).read_text());text=' '.join(p.parts)
 for pattern in [r'650,000\s*RWF',r'450,000\s*RWF',r'320,000\s*RWF',r'men[’\x27]s.{0,100}three-piece.{0,25}250,000',r'three-piece.{0,20}from 250,000']:
  m=re.search(pattern,text,re.I)
  if m:old.append((file,m.group()))
assert not old,old
for file in ['guides/fabrics/index.html','services/custom-tailoring/fabric/index.html']:
 source=(R/file).read_text();assert 'class="suit-package-prices"' not in source and 'Two-Piece Starting Price:' not in source and 'Three-Piece Starting Price:' not in source
 assert 'RWF 600,000' not in source and 'RWF 800,000' not in source
# No invented public product Offers; all source-linked FAQ destinations still exist.
for e in search_data()['entries']:
 from urllib.parse import urlsplit,unquote
 u=urlsplit(e['source']);p=R/'index.html' if u.path=='/' else R/u.path.strip('/')/'index.html';assert p.is_file(),e['source']
 if u.fragment:assert 'id="'+unquote(u.fragment)+'"' in p.read_text(),e['source']
report={'ordinaryPrices':expected,'ordinaryAmounts':16,'tuxedoAmounts':4,'obsoleteMensPriceReferences':old,'currentHtmlFilesAudited':len(files),'faqSubjects':required,'multipleFabricsPerTier':'PASS','historicalRecords':'not scanned/replaced'}
Path('/workspace/review/pricing-benefits-2026-11-12/source-audit.json').write_text(json.dumps(report,indent=2))
print('PASS16ordinary+4tuxprices/oneTierSource/multipleFabricsPerTier/11FAQsubjects/currentHTMLobsolete-priceaudit/noFabricSuitSchedule/sourceLinks')
