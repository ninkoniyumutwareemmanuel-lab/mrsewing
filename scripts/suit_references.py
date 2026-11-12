"""R4 matching suit-reference landings and gated category galleries; no product/stock fiction."""
from pathlib import Path
from html import escape
from urllib.parse import urlencode
import json
from customer_navigation import breadcrumb
ROOT=Path(__file__).resolve().parents[1]
BASE='/services/custom-tailoring/'
def model():return json.loads((ROOT/'_data/suit-reference-categories.json').read_text())
def categories():return model()['categories']
def category_by_id():return {c['id']:c for c in categories()}
def assignment(ident):return next((c for c in categories() if ident in c['designIds']),None)
def references(category,designs):
 pool={d['id']:d for d in designs}
 assert all(ident in pool for ident in category['designIds']),'Category must not publish an unapproved photograph'
 return [pool[ident] for ident in category['designIds']]
def landing_route(gender):return '/mensuits/' if gender=='men' else '/womensuits/'
def label(gender):return "Men's Suits" if gender=='men' else "Women's Suits"
def category_label(c):return ("Men's " if c['gender']=='men' else "Women's ")+c['title']
def href(c,design):
 from build_collections import design_route
 return design_route(design)+'?'+urlencode({'category':c['gender'],'suitCategory':c['id'],'design':design['id'],'order':'standard'})
def wrap(route,title,description,body,pending=False):
 from customer_site import frame
 html=frame(route,title,description,'<div class="suit-reference-view">'+body+'</div>',kind='CollectionPage')
 html=html.replace('</head>','<link rel="stylesheet" href="/assets/suit-references.css"></head>')
 if pending:html=html.replace('<main ','<main data-publication-hold ',1)
 return html
def landing(gender,designs):
 from build_collections import picture,SIZES
 title=label(gender);route=landing_route(gender)
 description="Explore our men's suit styles. Choose a category to discover designs for your custom-tailored garment." if gender=='men' else "Explore our women's tailored suit styles. Choose a category to discover designs for your preferred look."
 body='<header class="suit-intro">'+breadcrumb([('Custom Tailoring & Suits',BASE),(title,None)])+'<h1>'+escape(title)+'</h1><p>'+escape(description)+'</p></header><section aria-labelledby="suit-styles-heading"><h2 id="suit-styles-heading">Explore Suit Styles</h2><div class="suit-category-grid">'
 for c in [c for c in categories() if c['gender']==gender]:
  refs=references(c,designs);cover=next((r for r in refs if r['id']==c['coverDesignId']),None)
  photo=picture({**cover['images'][0],'position':'50% 0%'}).replace(SIZES,'(min-width: 700px) 560px, 100vw') if cover else '<div class="suit-photo-pending"><span>Reference photograph pending</span></div>'
  body+='<a class="suit-category-card" href="'+c['route']+'?category='+gender+'&amp;suitCategory='+c['id']+'">'+photo+'<div class="suit-category-copy"><h3>'+escape(c['title'])+'</h3><p>'+escape(c['description'])+'</p><span class="suit-open">Open category <span aria-hidden="true">→</span></span>'+('<small>Approved photographs are not yet available.</small>' if not refs else '')+'</div></a>'
 return wrap(route,title,description,body+'</div></section>')
def gallery(c,designs):
 from build_collections import picture,SIZES
 refs=references(c,designs);title=category_label(c);body='<header class="suit-intro">'+breadcrumb([('Custom Tailoring & Suits',BASE),(label(c['gender']),landing_route(c['gender'])),(c['title'],None)])+'<h1>'+escape(title)+'</h1><p>'+escape(c['description'])+' Photographs are references, not ready-made stock or confirmed fabric availability.</p></header>'
 if refs:
  body+='<section aria-labelledby="reference-heading"><h2 id="reference-heading">Choose a Reference</h2><p class="suit-instructions">Select a photograph to view its details, then continue to fabric preferences or advice.</p><div class="suit-design-grid">'
  for d in refs:
   info=model()['references'][d['id']];body+='<article class="suit-design-item"><a class="suit-design-card" data-design-id="'+d['id']+'" href="'+escape(href(c,d),quote=True)+'">'+picture(d['images'][0]).replace(SIZES,'(min-width: 700px) 560px, 100vw')+'<div class="suit-category-copy"><h3>'+escape(info['label'])+'</h3><p>Reference '+d['id']+'</p>'+('<p class="same-garment-note">Same garment as '+('MS-006' if d['id']=='MS-005' else 'MS-005')+', photographed from another view.</p>' if d['id'] in ['MS-005','MS-006'] else '')+'<span class="suit-open">View Design <span aria-hidden="true">→</span></span></div></a><button type="button" class="home-button home-button-gold" data-select-design="'+d['id']+'">Select This Design</button></article>'
  body+='</div></section>'
 else:body+='<section class="suit-empty" aria-labelledby="references-pending-heading"><h2 id="references-pending-heading">Approved Reference Photographs Pending</h2><p>There are no approved photographs for this category in the current preview. This does not indicate stock availability. Return to '+escape(label(c['gender']))+' to explore other categories or send your own design through Special Order.</p></section>'
 return wrap(c['route'],title,c['description']+' Browse design references for an individually assessed tailoring quotation.',body,pending=not refs)
def outputs(designs):
 out={ROOT/'mensuits.html':landing('men',designs),ROOT/'womensuits.html':landing('women',designs)}
 out.update({ROOT/c['route'].strip('/')/'index.html':gallery(c,designs) for c in categories()});out[ROOT/'assets/suit-references.css']=(ROOT/'_templates/suit-references.css').read_text()
 return out
