"""Single owner-approved public fact source; no private management material."""
import json
from html import escape
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def facts():
 data=json.loads((ROOT/'_data/customer-policy-facts.json').read_text())
 prices=json.loads((ROOT/'_data/suit-package-prices.json').read_text())['prices'];lines=[]
 for gender,label in [('men','Men’s ordinary suits'),('women','Women’s ordinary suits')]:
  rows=sorted([p for p in prices.values() if p['category']==gender and p.get('publicationApproved')],key=lambda p:p['tier'])
  lines.append(label+': '+ '; '.join('Tier '+str(p['tier'])+' — two-piece '+format(p['twoPieceRwf'],',')+' RWF, three-piece '+format(p['threePieceRwf'],',')+' RWF' for p in rows)+'.')
 tux=json.loads((ROOT/'_data/tuxedo-package-prices.json').read_text())
 lines.append('Men’s tuxedos, separate schedule: '+'; '.join('Tier '+str(p['tier'])+' — two-piece '+format(p['twoPieceRwf'],',')+' RWF, three-piece '+format(p['threePieceRwf'],',')+' RWF' for p in tux['tiers'])+'.')
 data['priceLines']=lines
 data['texts']['policySuitPrices']=' '.join(lines)+' These are complete garment starting prices, not fabric-only prices. Your selected fabric, design, inclusions and service requirements are reviewed before the final quotation is confirmed.'
 return data
def sections(service):
 f=facts();rows=[]
 if service in ['custom-tailoring','alterations','garment-care']:rows.append(('timing','Service Turnaround',f['texts'][f['services'][service]['timingTextKey']]))
 if service in ['custom-tailoring','alterations','garment-care']:rows.append(('charges','Express, after-hours and overnight',f['texts']['policyCharges']))
 if service=='custom-tailoring':
  rows.append(('prices','Starting Suit Prices',f['texts']['policySuitPrices']))
  rows.extend([('payments','Payments before production and release',' '.join(f['texts'][k] for k in ['policyDomesticPayment','policyInternationalPayment','policyPaymentVerification'])),('fabric','Customer-supplied fabric and design references',f['texts']['policyOwnFabric'])])
 if service in ['custom-tailoring','alterations']:rows.append(('corrections','Fitting and workmanship concerns','Report concerns promptly, preferably through official WhatsApp. The reporting guidance is within 72 hours after receipt or collection without limiting applicable customer rights. Mr Sewing assesses its own errors, corrects feasible errors without an additional tailoring charge and may provide a company-funded remake if proper correction is impossible. Customer-supplied measurement errors require an assessment; a replacement may need a separate quotation.'))
 if service in ['alterations','garment-care']:rows.append(('payment','Payment and garment assessment','Payment and balance arrangements are confirmed in your quotation before work starts. Full payment is required before release. Inspection determines suitability, work and the final price; not every garment or treatment can be accepted.'))
 if service in ['custom-tailoring','alterations','garment-care']:rows.append(('transport','Collection and delivery',f['texts']['policyTransport']+(' Initial standard cleaning, protective packaging and initial Kigali delivery remain included in the eligible standard custom-suit package.' if service=='custom-tailoring' else '')))
 if service=='mobile-fitting':rows.append(('mobile','Choose the appropriate mobile service',' '.join(f['texts'][k] for k in ['policyMobileMeasurement','policyMobileConsultation','policyMobileAssistance'])))
 if service in ['mobile-fitting','vip']:rows.append(('vip','Individually quoted VIP assistance',f['texts']['policyVIP']))
 return rows

def render(service):
 out=[]
 for id,title,text in sections(service):
  content=('<ul>'+''.join('<li>'+escape(line)+'</li>' for line in facts()['priceLines'])+'</ul><p>These are complete garment starting prices, not fabric-only prices. The final quotation follows review of your fabric, design and requirements.</p>') if id=='prices' else '<p>'+escape(text)+'</p>'
  out.append('<section class="release-section" id="service-info-'+id+'"><h2>'+escape(title)+'</h2>'+content+'</section>')
 return ''.join(out)
