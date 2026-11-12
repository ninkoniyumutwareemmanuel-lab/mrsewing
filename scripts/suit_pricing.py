"""Authoritative ordinary suit prices are classified by audience/tier, independent of fabrics."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def catalogue():return json.loads((ROOT/'_data/suit-package-prices.json').read_text())
def rows(audience):return sorted((p for p in catalogue()['prices'].values() if p['category']==audience and p['publicationApproved']),key=lambda p:p['tier'])
def minimum(audience,key):return min(r[key] for r in rows(audience))
def starting_text(audience):
 label='Men’s' if audience=='men' else 'Women’s'
 return label+' ordinary suits start at '+format(minimum(audience,'twoPieceRwf'),',')+' RWF for two pieces and '+format(minimum(audience,'threePieceRwf'),',')+' RWF for three pieces. Final fabric, design and order requirements are confirmed in the quotation.'
def compact_benefits(tier):return ('3 cleanings' if tier<=2 else 'Initial cleaning')+' · Kigali delivery · Hanger & cover'+(' · Collection gift' if tier<=2 else '')
def all_benefits():return 'Every qualifying ordinary custom suit includes initial standard professional cleaning, initial delivery within Kigali, and a branded hanger and protective garment cover. Tuxedos retain their separate package eligibility and accessories.'
def cleaning_benefits():return 'Tiers 1 and 2 include three standard cleanings total: one initial cleaning and two follow-up sessions. The additional sessions are used within three months after receiving the garment, with the follow-up arrangements confirmed by our team. Each qualifying follow-up covers the suit and one shirt. Follow-up collection and delivery transport is customer-paid. Tiers 3 and 4 include the initial cleaning only; no additional complimentary follow-up cleaning is included.'
def gift_benefits():return 'Men’s Tier 1 includes a shirt and necktie; men’s Tier 2 includes a necktie or bow tie. Women’s Tiers 1 and 2 include an inner top. Tiers 3 and 4 do not include collection gifts. These are the approved collection gifts, not an unlimited entitlement; quantities for multi-suit orders are identified in the quotation, not multiplied automatically.'
