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
  out+=image(f['image'])+'<div class="fabric-card-copy"><p class="fabric-tier">Tier '+str(f['tier'])+' / Quality Level — working reference</p><h3>'+escape(f['name'])+'</h3><p class="fabric-price">Starting price (RWF): <strong>Price on request</strong></p><p class="colour-enquiry"><span class="colour-swatch" role="img" aria-label="Colour availability unverified"></span>'+escape(f['colourStatus'])+'</p><p>'+escape(f['description'])+'</p><p class="fabric-disclaimer">'+escape(f['availability'])+'</p></div></article>'
 return out+'</div>'
def fabric_guide():
 return '<section class="guide-collection" aria-labelledby="fabric-references-title"><h2 id="fabric-references-title">Fabric References</h2><p class="guide-notice">These pictures are illustrative references, not photographs of verified Mr Sewing stock. Tier labels below are working reference categories pending company-source confirmation. They do not certify fibre composition or current availability. Price on request is not a fabric-only or complete suit-package price; your quotation confirms the actual scope.</p><h2>Men’s suit fabric references</h2>'+cards('men')+'<h2>Women’s suit fabric references</h2>'+cards('women')+'</section>'
def measurements():
 d=json.loads((ROOT/'_data/measurement-guide-images.json').read_text());out='<section class="guide-collection" aria-labelledby="measurement-photos-title"><h2 id="measurement-photos-title">Measurement Illustrations</h2><p class="guide-notice">Use these pictures to identify measurement areas. Illustrated tape numbers are not your measurements or a calibrated scale. Follow the instructions confirmed for your garment and ask for assistance if the starting point, path or endpoint is unclear.</p><div class="measurement-photo-grid">'
 for m in d['measurements']:out+='<figure class="measurement-photo" id="measure-'+m['id']+'">'+image(m['image'])+'<figcaption><h3>'+escape(m['title'])+'</h3><p>'+escape(m['caption'])+'</p></figcaption></figure>'
 return out+'</div></section>'
def options():
 return ''.join('<optgroup label="'+('Men’s Suits' if category=='men' else 'Women’s Suits')+'">'+''.join('<option value="'+f['id']+'">'+escape(f['name'])+' — Tier '+str(f['tier'])+' (reference)</option>' for f in fabrics() if f['category']==category)+'</optgroup>' for category in ['men','women'])
def script():return '<script id="fabricReferenceData" type="application/json">'+json.dumps({f['id']:{k:f[k] for k in ['id','name','category','tier']} for f in fabrics()},ensure_ascii=False).replace('<','\\u003c')+'</script>'
