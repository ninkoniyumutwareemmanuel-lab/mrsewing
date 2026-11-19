"""Authoritative ordinary suit prices are classified by audience/tier, independent of fabrics."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def catalogue():return json.loads((ROOT/'_data/suit-package-prices.json').read_text())
def rows(audience):return sorted((p for p in catalogue()['prices'].values() if p['category']==audience and p['publicationApproved']),key=lambda p:p['tier'])
def minimum(audience,key):return min(r[key] for r in rows(audience))
def starting_text(audience, public=True):
 label='Men’s' if audience=='men' else 'Women’s'
 from public_content import service_prices_visible
 if public and not service_prices_visible():return label+' ordinary suits are individually quoted after reviewing the quality tier, fabric, design and order requirements.'
 return label+' ordinary suits start at '+format(minimum(audience,'twoPieceRwf'),',')+' RWF for two pieces and '+format(minimum(audience,'threePieceRwf'),',')+' RWF for three pieces. Final fabric, design and order requirements are confirmed in the quotation.'
def compact_benefits(tier):
 data=catalogue()['benefitsByTier'][str(tier)]
 total=data['standardCleaningsTotal']
 return (str(total)+' cleanings' if total>1 else 'Initial cleaning')+' · Kigali delivery · Hanger & cover'+(' · Collection gift' if any(data['collectionGifts'].values()) else '')
def all_benefits():
 labels=catalogue()['benefitConditions']['allTiers']
 return 'Every qualifying ordinary custom suit includes '+', '.join(label[0].lower()+label[1:] for label in labels)+'. Tuxedos retain their separate package eligibility and accessories.'
def cleaning_benefits():
 data=catalogue();conditions=data['benefitConditions'];tiers=data['benefitsByTier']
 enhanced=[key for key,row in tiers.items() if row['standardCleaningsTotal']>1]
 initial=[key for key,row in tiers.items() if row['standardCleaningsTotal']==1]
 total=tiers[enhanced[0]]['standardCleaningsTotal'] if enhanced else 1
 return 'Tiers '+ ' and '.join(enhanced)+' include '+str(total)+' standard cleanings total: one initial cleaning and '+str(conditions['followUpSessions'])+' follow-up sessions. The additional sessions are used within '+str(conditions['followUpWindowMonthsAfterReceipt'])+' months after receiving the garment, with follow-up arrangements confirmed by our team. Each qualifying follow-up covers the '+conditions['followUpCoverage']+'. Follow-up collection and delivery transport is '+conditions['followUpTransport']+'. Tiers '+' and '.join(initial)+' include the initial cleaning only; no additional complimentary follow-up cleaning is included.'
def gift_benefits():
 data=catalogue();parts=[]
 for audience,label in [('men','Men’s'),('women','Women’s')]:
  for tier,row in data['benefitsByTier'].items():
   gift=row['collectionGifts'].get(audience)
   if gift:parts.append(label+' Tier '+tier+' includes '+gift+'.')
 no_gift=[tier for tier,row in data['benefitsByTier'].items() if not any(row['collectionGifts'].values())]
 parts.append('Tiers '+' and '.join(no_gift)+' do not include collection gifts. These are the approved collection gifts, not an unlimited entitlement; quantities for multi-suit orders are identified in the quotation, not multiplied automatically.')
 return ' '.join(parts)
