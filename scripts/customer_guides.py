"""Shared source-qualified fabric references and measurement illustrations; no stock/price invention."""
from pathlib import Path
from html import escape
from urllib.parse import quote
import json
ROOT=Path(__file__).resolve().parents[1]
def fabrics():return json.loads((ROOT/'_data/fabric-reference-catalogue.json').read_text())['fabrics']
def photos():return json.loads((ROOT/'_data/customer-guide-images.json').read_text())['images']
def image(key,sizes='(min-width: 1000px) 360px, (min-width: 600px) 45vw, 100vw'):
 d=photos()[key];variants=d['variants']+[{'src':d['src'],'width':d['width']}];src=variants[0]['src']
 return '<img src="'+quote(src,safe='/')+'" data-original="'+quote(d['src'],safe='/')+'" srcset="'+', '.join(quote(v['src'],safe='/')+' '+str(v['width'])+'w' for v in variants)+'" sizes="'+sizes+'" width="'+str(d['width'])+'" height="'+str(d['height'])+'" alt="'+escape(d['alt'],quote=True)+'" loading="lazy" decoding="async">'
def cards(category,selectable=False):
 out='<div class="fabric-grid">'
 for f in [f for f in fabrics() if f['category']==category]:
  ident='fabric-'+f['id'];out+='<article class="fabric-card" data-fabric-id="'+f['id']+'">'
  if selectable:out+='<label for="'+ident+'" class="fabric-selection-label"><input type="radio" id="'+ident+'" name="fabricRef" value="'+f['id']+'"> Select '+escape(f['name'])+'</label>'
  out+=image(f['image'])+'<div class="fabric-card-copy"><p class="fabric-tier">Tier '+str(f['tier'])+' / Quality '+str(f['tier'])+'</p><h3>'+escape(f['name'])+'</h3>'+'<p><a href="/services/custom-tailoring/#service-info-prices">View ordinary suit prices for Tier '+str(f['tier'])+' / Quality '+str(f['tier'])+'</a></p>'+'<p class="colour-enquiry"><span class="colour-swatch" role="img" aria-label="Ask us about available colours"></span>'+escape(f['colourStatus'])+'</p><p>'+escape(f['description'])+'</p></div></article>'
 return out+'</div>'
def fabric_guide():
 return '<section class="guide-collection" aria-labelledby="fabric-references-title"><h2 id="fabric-references-title">Choosing Your Fabric</h2><p>Explore approved fabric reference photographs and their assigned Tier / Quality. Several fabrics may share the same tier; an individual fabric name is not a separate suit-price schedule.</p><p>We recommend visiting our workshop to see and feel the fabrics and explore colours. Photographs may show colours differently.</p><p class="guide-notice">These are reference classifications, not certified fibre-composition claims or proof of current stock. We confirm exact fabric, colour, suitability and availability before your quotation is accepted.</p><p><a href="/services/custom-tailoring/#service-info-prices">View ordinary suit starting prices and benefits by Tier / Quality</a>. Special design requirements and the approved quotation process determine your final price.</p><h2>Men’s suit fabrics</h2>'+cards('men')+'<h2>Women’s suit fabrics</h2>'+cards('women')+'<p id="tuxedo-prices"><a href="/services/custom-tailoring/#tuxedo-prices">View the separate men’s tuxedo pricing schedule</a>.</p>'+fabric_request_notes()+'</section>'
def measurements():
 d=json.loads((ROOT/'_data/measurement-guide-images.json').read_text());out='<section class="guide-collection" aria-labelledby="measurement-photos-title"><h2 id="measurement-photos-title">Measurement Illustrations</h2><p class="guide-notice">Use these pictures to identify measurement areas. Illustrated tape numbers are not your measurements or a calibrated scale. Follow the instructions confirmed for your garment and ask for assistance if the starting point, path or endpoint is unclear.</p><div class="measurement-photo-grid">'
 for m in d['measurements']:out+='<figure class="measurement-photo" id="measure-'+m['id']+'">'+'<a class="measurement-enlarge" data-enlarge href="'+quote(photos()[m['image']]['src'],safe='/')+'" aria-label="Enlarge '+escape(m['title'])+' measurement illustration">'+image(m['image'])+'</a><figcaption><h3>'+escape(m['title'])+'</h3><p>'+escape(m['caption'])+'</p></figcaption></figure>'
 return out+'</div></section>'
def options():
 return ''.join('<optgroup label="'+('Men’s Suits' if category=='men' else 'Women’s Suits')+'">'+''.join('<option value="'+f['id']+'">'+escape(f['name'])+' — Tier '+str(f['tier'])+' (reference)</option>' for f in fabrics() if f['category']==category)+'</optgroup>' for category in ['men','women'])
def script():return '<script id="fabricReferenceData" type="application/json">'+json.dumps({f['id']:{k:f[k] for k in ['id','name','category','tier']} for f in fabrics()},ensure_ascii=False).replace('<','\\u003c')+'</script>'

def fabric_request_notes():
 from customer_policies import facts
 f=facts()
 return '<section id="fabric-service-notes"><h2>Express and children’s tailoring</h2><p>Express custom tailoring is estimated at 2–3 days, subject to feasibility, capacity and acceptance. The eligible Express surcharge is 35% of the quoted base. Necessary and agreed after-hours work adds 25% of the same base; together the surcharge is additive 60%. Confirm the final quotation and completion date before acceptance.</p><p>'+escape(f['texts']['policyChildren'])+'</p><p>'+escape(f['texts']['policyParentChild'])+'</p></section>'
