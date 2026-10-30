"""Structured garment-care publication/pricing gates. Draft categories are never advertised."""
import json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def catalog():
    data=json.loads((ROOT/'_data/garment-care.json').read_text());assert data['currency']=='RWF';seen=set();published=[]
    for s in data['services']:
        assert re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*',s['slug']) and s['slug'] not in seen;seen.add(s['slug'])
        assert s['pricing']['currency']=='RWF'
        for row in s['pricing']['rows']:
            assert row.get('garmentType') and row.get('serviceType')
            if row.get('approved'):
                assert row.get('approvalEvidenceRef') and type(row.get('standardPriceRwf')) is int and row['standardPriceRwf']>0,'Approved RWF price must be positive and evidenced'
                for charge in row.get('additionalCharges',[]):
                    if charge.get('approved'):assert charge.get('approvalEvidenceRef') and charge.get('label') and type(charge.get('amountRwf')) is int and charge['amountRwf']>0
        timing=s['pricing']['standardTurnaround']
        if timing['approved']:assert timing.get('approvalEvidenceRef') and type(timing.get('minimum')) is int and timing['minimum']>0 and type(timing.get('maximum')) is int and timing['maximum']>=timing['minimum'] and timing['unit'] in ['hours','business_days','days']
        express=s['pricing']['express']
        if express['approved']:assert express.get('approvalEvidenceRef') and type(express.get('available')) is bool and (express.get('additionalChargeRwf') is None or type(express['additionalChargeRwf']) is int and express['additionalChargeRwf']>0)
        if not s['published']:continue
        assert s['availabilityConfirmed'] is True and s.get('confirmationEvidenceRef') and s['publicationApproved'] is True,'Care availability/publication confirmation required'
        assert s.get('description') and s['suitableGarments'] and s['process'] and s['customerPreparation'] and s['limitations'],'Care page needs complete approved information'
        published.append(s)
    return data,published

from html import escape

def care_information():
    return json.loads((ROOT/'_data/care-information.json').read_text())
def care_navigation():
    return '<nav class="care-subnav" aria-label="Garment care"><a href="/services/garment-care/">Care home</a><a href="/services/garment-care/services/">Services</a><a href="/services/garment-care/planning/#prices">Prices</a><a href="/services/garment-care/planning/#turnaround">Turnaround</a><a href="/services/garment-care/planning/#pickup-delivery">Pickup &amp; delivery</a></nav>'
def care_summary(category=None):
    info=care_information();pricing=info['pricingStatus'];timing=info['turnaroundStatus'];handover=info['arrangementsStatus']
    if category:
        if any(r.get('approved') for r in category['pricing']['rows']):pricing='Approved RWF rates for this service are listed below. Confirm the quote for your garment.'
        t=category['pricing']['standardTurnaround']
        if t['approved']:timing='Estimated '+str(t['minimum'])+'–'+str(t['maximum'])+' '+t['unit'].replace('_',' ')+'. Confirm for your garment.'
        handover=category.get('pickupDelivery') or handover
    return '<dl class="care-basic-summary">'+''.join('<div><dt>'+label+'</dt><dd>'+escape(text)+'</dd></div>' for label,text in [('Pricing',pricing),('Turnaround',timing),('Pickup & delivery',handover)])+'</dl>'
