#!/usr/bin/env python3
"""Build programme pages and publication-gated merchandise from one Git catalogue."""
import argparse,json,re
from html import escape,unescape
from pathlib import Path
from urllib.parse import quote
from shop_catalog import ROOT,load,route,STATUSES,categories as shop_categories,category_route
from shop_preview import enabled as preview_enabled,candidates as preview_candidates
from customer_site import frame
from site_seo import finalize,DOMAIN

def e(v):return escape(str(v),quote=True)
def a(url,text,button=False):return '<a href="'+e(url)+'"'+(' class="home-button home-button-gold"' if button else '')+'>'+e(text)+'</a>'
def faq(items):return '<section><h2>Questions &amp; Answers</h2>'+''.join('<details><summary>'+e(q)+'</summary><p>'+e(t)+'</p></details>' for q,t in items)+'</section>'
def common_fields():
 return '''<label for="fullName">Full name (required)</label><input id="fullName" name="Full Name" autocomplete="name" maxlength="160" required><label for="phone">Phone / WhatsApp (required)</label><input id="phone" name="Phone / WhatsApp" type="tel" autocomplete="tel" maxlength="40" required><label for="email">Email address (optional)</label><input id="email" name="Email Address" type="email" autocomplete="email" maxlength="254"><div class="trap" aria-hidden="true"><label>Leave empty<input name="botcheck" tabindex="-1" autocomplete="off"></label></div>'''
def consent(referral=False):
 return '<label class="consent"><input type="checkbox" name="Consent" value="Accepted" required><span>I have read '+(a('/referral-program/#conditions','the referral participation conditions')+' and ' if referral else '')+'the '+a('/terms-and-conditions/','Terms & Conditions')+' and '+a('/privacy-policy/','Privacy Policy')+'. I request human review; this does not confirm '+('participation or commission.' if referral else 'an order, reservation, final price or payment.')+'</span></label>'
def review(kind):
 return '<div class="actions"><button class="home-button home-button-gold" type="button" data-review disabled>Continue</button></div></div><section data-review-panel hidden><h3 tabindex="-1">Review Your Request</h3><dl data-review-details></dl><p>This is a request for review, not automatic approval.</p><div class="actions"><button type="button" class="home-button" data-edit>Edit</button><button type="submit" class="home-button home-button-gold" disabled>'+kind+'</button></div></section><p class="status" role="status" aria-live="polite" data-status></p><section data-success hidden tabindex="-1"></section></form>'
def form(kind,extra='',referral=False):
 return '<form method="post" action="/api/shop-request" data-commerce-form="'+kind+'" novalidate><div data-fields>'+common_fields()+extra+consent(referral)+review('Submit Participation Request' if referral else 'Submit Quotation Request' if kind=='quote' else 'Submit Purchase Request')
def page(url,title,desc,body,products=None,product=None):
 source=frame(url,title,desc,'<div class="commerce'+(' storefront' if url.startswith('/shop/') else '')+'">'+body+'<noscript><p class="notice">JavaScript is needed for cart and request submission. You can still read the information and use our Contact Us page for assistance.</p></noscript></div>')
 source=source.replace('</head>','<link rel="stylesheet" href="/assets/commerce.css"><script src="/assets/commerce.js" defer></script></head>',1)
 payload={'products':products if products is not None else []}
 if url.startswith('/shop/'):
  source=re.sub(r'(<nav class="customer-breadcrumb".*?</nav>)',lambda m:m[0].replace('href="/"','href="/shop/"'),source,count=1,flags=re.S)
  source=source.replace('</main>','<script type="application/json" id="shopData">'+json.dumps(payload,ensure_ascii=False).replace('<','\\u003c')+'</script></main>')
 if product:
  source=source.replace('property="og:type" content="website"','property="og:type" content="product"')
  image=DOMAIN+quote(product['socialImage'],safe='/');alt=next(i['alt'] for i in product['images'] if i['src']==product['socialImage'])
  for key in ['og:image','twitter:image']:
   source=re.sub(r'(<meta (?:property|name)="'+key+'" content=")[^"]*',lambda m:m[1]+e(image),source)
  for key in ['og:image:alt','twitter:image:alt']:
   source=re.sub(r'(<meta (?:property|name)="'+key+'" content=")[^"]*',lambda m:m[1]+e(alt),source)
  source=re.sub(r'<meta property="og:image:(?:width|height)"[^>]*>','',source)
  graph={'@context':'https://schema.org','@type':'Product','name':product['name'],'sku':product['id'],'description':product['description'],'image':[DOMAIN+quote(i['src'],safe='/') for i in product['images']],'url':DOMAIN+url,'category':product['category']}
  if product.get('priceRwf') is not None:graph['offers']={'@type':'Offer','priceCurrency':'RWF','price':product['priceRwf'],'availability':'https://schema.org/'+('InStock' if product['availability']=='Available in Stock' else 'OutOfStock'),'url':DOMAIN+url,'seller':{'@type':'Organization','name':'Mr Sewing Fashion'}}
  source=source.replace('</head>','<script type="application/ld+json">'+json.dumps(graph,ensure_ascii=False).replace('<','\\u003c')+'</script></head>')
 return finalize(source,ROOT/url.strip('/')/'index.html')
def loyalty():
 body='<p class="home-eyebrow">For returning suit customers</p><h1>Loyalty Program</h1><p class="lead">A thank-you for choosing Mr Sewing Fashion again. Eligible customers receive a 3% discount beginning with their second separate qualifying suit purchase.</p><section class="panel"><span class="benefit">3%</span><h2>How eligibility works</h2><p>Your second separate qualifying suit purchase can qualify for the loyalty discount. Buying multiple suits in your first order does not automatically count as multiple separate purchases.</p><p>The programme covers qualifying men’s and women’s suits. Our team checks your purchase history and confirms eligibility before applying the benefit.</p></section><section><h2>Benefits &amp; Conditions</h2><ul><li>The discount does not automatically cover alterations, standalone garment care, accessories or unrelated services.</li><li>Customer discounts do not stack on the same suit. The single highest eligible customer discount applies.</li></ul></section>'
 body+=faq([('Does my first multi-suit order qualify as several purchases?','No. Multiple suits in one first order do not automatically count as separate qualifying purchases.'),('Can I combine loyalty with another suit discount?','Customer discounts cannot be stacked on the same suit. Our team applies the single highest eligible discount.'),('How do I check my eligibility?','Request a consultation and mention your previous qualifying suit purchase. Our team will review your eligibility.')])
 body+='<section><h2>Plan Your Next Suit</h2><p>Explore designs or ask our team to check your eligibility.</p><div class="actions">'+a('/mensuits/',"Men’s Suits",True)+a('/womensuits/',"Women’s Suits",True)+a('/booking/','Enquire About Eligibility',True)+'</div></section>'
 return page('/loyalty-program/','Loyalty Program','Learn about the 3% loyalty discount for qualifying repeat suit purchases at Mr Sewing Fashion in Kigali, Rwanda.',body)
def referral():
 body='<p class="home-eyebrow">Introduce someone new</p><h1>Referral Program</h1><p class="lead">Help a new customer discover Mr Sewing Fashion. Eligible customers and people who have never purchased from us can enquire about participating as referrers.</p><div class="grid"><section class="panel"><span class="benefit">6,000 RWF</span><h2>For the Referrer</h2><p>Per qualifying suit in the newly referred customer’s first qualifying order, subject to eligibility and verification.</p></section><section class="panel"><span class="benefit">2%</span><h2>For the New Customer</h2><p>A discount on qualifying suits in their first qualifying order. Customer discounts do not stack; the highest eligible discount applies.</p></section></div><section id="conditions"><h2>How Referrals Work</h2><ol><li>Enquire about participation and confirm the applicable conditions with our team.</li><li>The referrer must be identified before the new customer’s first deposit. Only one referrer can be attributed; self-referrals are not eligible.</li><li>Our team verifies the new customer and qualifying suit order.</li><li>Commission becomes earned only after the qualifying order is completed, fully paid and handed over.</li></ol><p>There is no repeat commission on that customer’s later orders. These benefits concern qualifying suits, not automatic rewards on unrelated services.</p><p>Our team will confirm the applicable payment arrangements and timing with you before participation is agreed. Submitting this form does not approve participation, create a referral code or issue a commission.</p></section>'
 body+=faq([('Do I need to be an existing customer?','No. Eligible people who have not purchased from Mr Sewing Fashion may also participate, subject to verification.'),('When should the referral be recorded?','Identify the referrer with our team before the new customer’s first deposit. Only one referrer is attributed, and self-referrals are excluded.'),('Will later orders earn another commission?','No. The commission applies only to qualifying suits in the new customer’s first qualifying order.'),('When does a reward qualify?','The qualifying order must be completed, fully paid and handed over. Our team verifies eligibility and confirms payment arrangements; applying does not guarantee a reward.')])
 body+='<section class="panel"><h2>Enquire About Participation</h2><p>Tell us how to contact you. Please do not submit someone else’s private contact details.</p>'+form('referral','<label for="existingCustomer">Are you an existing customer? (required)</label><select id="existingCustomer" name="Existing Customer" required><option value="">Select an option</option><option>Yes</option><option>No</option></select>',True)+'</section>'
 return page('/referral-program/','Referral Program','Refer eligible new suit customers to Mr Sewing Fashion. Learn about referral benefits and request participation in Kigali, Rwanda.',body)
def shop_nav():return '<nav class="shop-nav" aria-label="Shop navigation">'+a('/shop/','Home')+'</nav>'
def photo(i,primary=False):
 sources=i.get('responsiveSources',[])
 responsive=(' srcset="'+e(', '.join(quote(x['src'],safe='/')+' '+str(x['width'])+'w' for x in sources))+'" sizes="(min-width:1000px) 520px, (min-width:650px) 50vw, 100vw"') if sources else ''
 return '<img src="'+e(quote(i['src'],safe='/'))+'" alt="'+e(i['alt'])+'" width="'+str(i['width'])+'" height="'+str(i['height'])+'" loading="'+('eager' if primary else 'lazy')+'" decoding="async" class="product-photo"'+responsive+'>'
def draft_card(p):
 return '<a class="product-card draft-card" href="'+route(p)+'" data-product-card data-name="'+e((p['name']+' '+p['description']).lower())+'" data-category="'+e(p['category'])+'" data-availability="" data-price="0"><span class="product-image-link">'+photo(p['images'][0])+'</span><div class="product-card-copy"><p class="product-category">'+e(p['category'])+'</p><h2>'+e(p['name'])+'</h2><p class="product-price-note">View details &amp; enquire</p></div></a>'
def draft_page(p,products):
 body=shop_nav()+category_nav(products,p['category'])+'<p>'+a('/shop/','Shop')+' / '+a(category_route(p['category']),p['category'])+'</p><div class="product-layout"><div>'+'<a data-enlarge href="'+e(quote(p['images'][0]['src'],safe='/'))+'" aria-label="Enlarge '+e(p['name'])+'">'+photo(p['images'][0],True)+'</a>'+'</div><div class="product-summary"><p class="product-category">'+e(p['category'])+'</p><h1>'+e(p['name'])+'</h1><p>'+e(p['description'])+'</p><p class="product-price-note">Contact us for the current price and available options.</p><button class="home-button" type="button" data-share-product="'+e(DOMAIN+route(p))+'">Share Product Link</button><p data-share-status role="status"></p><form data-shop-whatsapp-form data-product-name="'+e(p['name'])+'" data-product-url="'+e(DOMAIN+route(p))+'" data-product-id="'+e(p['id'])+'"><label for="enquiryQuantity">Requested quantity</label><input id="enquiryQuantity" name="quantity" type="number" min="1" max="999" step="1" value="1" required><label for="enquiryPayment">Preferred payment method</label><select id="enquiryPayment" name="payment"><option>Discuss with our team</option><option>Mobile Money</option><option>Bank Transfer</option><option disabled>Cryptocurrency — pending verification</option></select><label for="enquiryPreferences">Size, colour or other preferences (optional)</label><textarea id="enquiryPreferences" name="preferences" maxlength="1000" rows="3"></textarea><button class="home-button home-button-gold" type="submit">Enquire on WhatsApp</button><p data-shop-whatsapp-error role="status"></p></form><p>Review your enquiry in WhatsApp, then press Send. Our team will confirm availability, options and the final price. An enquiry does not reserve stock or confirm a purchase.</p></div></div><section><h2>You May Also Like</h2><div class="shop-grid">'+''+'</div></section>'
 # Related cards use the same catalogue, not a separate product list.
 related=[x for x in products if x['id']!=p['id'] and x['category']==p['category']][:4]
 body=body.replace('<section><h2>You May Also Like</h2><div class="shop-grid"></div></section>','<section><h2>You May Also Like</h2><div class="shop-grid">'+''.join(draft_card(x) for x in related)+'</div></section>')
 return noindex(page(route(p),p['name']+' | Mr Sewing Fashion Shop',p['description']+' Enquire on WhatsApp for confirmed options and pricing.',body))
def noindex(source):
 return re.sub(r'(<meta name="robots" content=")[^"]*',r'\g<1>noindex, nofollow',source)
def card(p):return '<a class="product-card" href="'+route(p)+'" data-product-card data-name="'+e((p['name']+' '+p['description']).lower())+'" data-category="'+e(p['category'])+'" data-availability="'+p['availability']+'" data-price="'+str(p.get('priceRwf') or 0)+'">'+photo(p['images'][0])+'<h2>'+e(p['name'])+'</h2><p>'+e(p['availability'])+'</p>'+('<p class="price">RWF '+format(p['priceRwf'],',')+'</p>' if p.get('priceRwf') else '<p>Request a Quote</p>' if p['availability']=='Available on Orders' else '')+'</a>'
def category_nav(products,selected=None):
 return '<nav class="shop-categories" aria-label="Product categories">'+a('/shop/','All Products')+''.join('<a href="'+category_route(c)+'"'+(' aria-current="page"' if c==selected else '')+'>'+e(c)+'</a>' for c in shop_categories(products))+'</nav>'
def shop(products,selected=None,drafts=None):
 drafts=drafts or []
 display=products+drafts
 render=lambda p:draft_card(p) if p in drafts else card(p)
 body=shop_nav()+'<p class="home-eyebrow">Mr Sewing Fashion</p><h1>Online Shop</h1><p class="lead">Browse products and send a purchase request or ask for a quotation. Our team confirms availability and the final amount before any payment.</p>'
 categories=shop_categories(display)
 body+='<aside class="shop-banner" aria-label="Shop introduction"><p>Style for you. Care for your wardrobe.</p><small>Availability and final arrangements are confirmed by our team.</small></aside>'+category_nav(display,selected)
 if drafts:body+='<p class="shop-how">Find your item · Enquire on WhatsApp · Confirm details with our team</p>'
 body+='<div class="filters"><label>Search products<input id="shopSearch" type="search" maxlength="120"></label><label>Category<select id="shopCategory"><option value="">All categories</option>'+''.join('<option'+(' selected' if c==selected else '')+'>'+e(c)+'</option>' for c in categories)+'</select></label><label>Availability<select id="shopAvailability"><option value="">All availability</option>'+''.join('<option>'+s+'</option>' for s in STATUSES)+'</select></label><label>Sort by<select id="shopSort"><option value="name">Name A–Z</option><option value="price-asc">Price: low to high</option><option value="price-desc">Price: high to low</option></select></label></div><p id="shopCount" role="status">'+str(sum(not selected or p['category']==selected for p in display))+' products</p><section class="shop-grid" id="shopGrid" aria-label="Products">'+''.join(render(p).replace('data-product-card','data-product-card hidden',1) if selected and p['category']!=selected else render(p) for p in display)+'</section><section class="panel empty" id="shopEmpty"'+(' hidden' if display else '')+'><h2>'+('No matching products' if display else 'Our catalogue is being prepared')+'</h2><p>'+('Try another search or filter.' if display else 'No products are listed yet. Product details, photographs, prices and availability will appear here when the catalogue is ready. There are no products available to purchase through this catalogue at present.')+'</p></section><p class="notice">Submitting a purchase request does not reserve stock in real time or confirm an order. Please wait for verified payment instructions from Mr Sewing Fashion.</p>'
 if drafts:
  body=re.sub(r'<option>Available in Stock</option>.*?<option>Out of Stock</option>','',body)
  body=body.replace('<option value="">All availability</option>','<option value="">Confirm on WhatsApp</option>').replace('<option value="price-asc">Price: low to high</option><option value="price-desc">Price: high to low</option>','')
  body+='<section class="shop-assurance"><h2>Shop with Personal Assistance</h2><p>Choose a product to see its details, then enquire on WhatsApp. We confirm the available options, final amount and delivery or collection arrangements before you pay.</p><h3>Payment Options</h3><p>Mobile Money · Bank Transfer</p><p>Cryptocurrency: pending verification; not currently enabled. Payment instructions are provided individually after review.</p></section>'
 if selected:
  body=body.replace('<h1>Online Shop</h1>','<h1>'+e(selected)+'</h1>')
  return (noindex if drafts else lambda x:x)(page(category_route(selected),selected+' | Shop','Browse '+selected.lower()+' in the Mr Sewing Fashion catalogue. Availability and final purchase arrangements require confirmation.',body,products))
 return (noindex if drafts else lambda x:x)(page('/shop/','Online Shop','Browse the Mr Sewing Fashion product catalogue in Rwanda. Request availability and pricing, or submit a purchase request for approved in-stock products.',body,products))
def product_page(p,products):
 body=shop_nav()+category_nav(products,p['category'])+'<p>'+a(category_route(p['category']),p['category'])+' / '+e(p['name'])+'</p><div class="product-layout"><div>'+photo(p['images'][0],True)+'<div class="photo-strip">'+''.join(photo(i) for i in p['images'][1:])+'</div></div><div><h1>'+e(p['name'])+'</h1><p>'+e(p['description'])+'</p><p>'+e(p['availability'])+'</p>'+('<p class="price">RWF '+format(p['priceRwf'],',')+'</p>' if p.get('priceRwf') else '')+'<p>Product ID: '+e(p['id'])+'</p><form id="productSelection" data-product-id="'+e(p['id'])+'"><label for="productVariation">Size / Colour</label><select id="productVariation" required><option value="">Select a size and colour</option>'+''.join('<option value="'+e(v['id'])+'"'+(' disabled' if p['availability']=='Available in Stock' and v['stockQuantity']==0 else '')+'>'+e(v['size']+' / '+v['colour'])+(' — '+str(v['stockQuantity'])+' available' if p['availability']=='Available in Stock' else '')+'</option>' for v in p['variations'])+'</select><label for="productQuantity">Quantity</label><input id="productQuantity" type="number" min="1" step="1" value="1" required><div class="actions"><button type="submit" class="home-button home-button-gold"'+(' disabled' if p['availability']=='Out of Stock' else '')+'>'+('Add to Cart' if p['availability']=='Available in Stock' else 'Request a Quote' if p['availability']=='Available on Orders' else 'Out of Stock')+'</button></div><p id="productStatus" role="status"></p></form><p>Recorded availability is subject to confirmation; requests do not reserve stock.</p></div></div><section><h2>Product Specifications</h2><dl>'+''.join('<dt>'+e(k)+'</dt><dd>'+e(v)+'</dd>' for k,v in p['specifications'].items())+'</dl><h2>Care Instructions</h2><p>'+e(p['careInstructions'])+'</p><h2>Ordering Notes</h2><p>'+e(p['orderingNotes'])+'</p></section>'
 if p['availability']=='Available on Orders':body+='<dialog id="quoteDialog" aria-labelledby="quoteTitle"><button type="button" class="home-button dialog-close" data-close>Close</button><h2 id="quoteTitle">Request a Quote</h2><p id="quoteContext"></p>'+form('quote','<label for="quoteRequirements">Additional requirements (optional)</label><textarea id="quoteRequirements" name="Additional Requirements" maxlength="2000" rows="3"></textarea>')+'</dialog>'
 return page(route(p),p['seoTitle'],p['seoDescription'],body,products,p)
def cart(products):
 body=shop_nav()+'<h1>Your Cart</h1><p>Review your selections before requesting a purchase. Stock and final amounts are subject to business confirmation; no payment is collected here.</p><p>Cart contents are saved in this browser when storage is available. Contact and delivery details are not saved in the cart.</p><section id="cartItems" aria-label="Cart items"></section><p id="cartTotal" class="price"></p><p id="cartStatus" role="status"></p><section id="checkout" hidden><h2>Purchase Request</h2>'+form('purchase','<label for="deliveryAddress">Delivery location or collection preference (required)</label><textarea id="deliveryAddress" name="Delivery or Collection" autocomplete="street-address" maxlength="1000" required></textarea><label for="paymentMethod">Preferred payment method (required)</label><select id="paymentMethod" name="Preferred Payment Method" required><option value="">Select a preference</option><option>Bank Transfer</option><option>Mobile Money</option><option disabled>Cryptocurrency — not available</option></select><small>Payment instructions and any delivery charges will be confirmed individually. Do not pay before receiving verified instructions. Cryptocurrency is not currently available.</small><label for="purchaseNotes">Additional information (optional)</label><textarea id="purchaseNotes" name="Additional Information" maxlength="2000"></textarea>')+'</section>'
 return page('/shop/cart/','Cart & Purchase Request','Review your Mr Sewing Fashion shopping cart and submit a purchase request for availability and final amount confirmation.',body,products)
def routes():return ['/loyalty-program/','/referral-program/','/shop/','/shop/cart/']+[route(p) for p in load()]+[category_route(c) for c in shop_categories()]
def outputs(products=None):
 ps=load() if products is None else products
 drafts=preview_candidates() if products is None and preview_enabled() else []
 out={ROOT/'loyalty-program/index.html':loyalty(),ROOT/'referral-program/index.html':referral(),ROOT/'shop/index.html':shop(ps,drafts=drafts),ROOT/'shop/cart/index.html':cart(ps)}
 for p in ps:out[ROOT/route(p).strip('/')/'index.html']=product_page(p,ps)
 for p in drafts:out[ROOT/route(p).strip('/')/'index.html']=draft_page(p,ps+drafts)
 for c in shop_categories(ps+drafts):out[ROOT/category_route(c).strip('/')/'index.html']=shop(ps,c,drafts)
 # Server-only preview snapshot: independent of unverified CI preview variables.
 # The Pages route enforces the exact staging project hostname on every request.
 review=preview_candidates()
 preview_pages={'/shop/':shop(ps,drafts=review)}
 for draft in review:preview_pages[route(draft)]=draft_page(draft,ps+review)
 for category in shop_categories(ps+review):preview_pages[category_route(category)]=shop(ps,category,review)
 out[ROOT/'functions/_lib/shop-preview-pages.js']='// Generated server-only staging presentation; never a purchasable catalogue.\nexport const pages='+json.dumps(preview_pages,ensure_ascii=False).replace('<','\\u003c')+';\n'
 out[ROOT/'assets/commerce.css']=(ROOT/'_templates/commerce.css').read_text();out[ROOT/'assets/commerce.js']=(ROOT/'_templates/commerce.js').read_text()
 # Server-only module: reuse the existing publishable provider key, never create/alter provider credentials.
 template=(ROOT/'_templates/homepage-quotation.html').read_text();key=unescape(re.search(r'name="access_key" value="([^"]+)"',template)[1])
 out[ROOT/'functions/_lib/shop-runtime.js']='// Generated from the approved catalogue and existing provider configuration.\nexport const products='+json.dumps(ps,ensure_ascii=False).replace('<','\\u003c')+';\nexport const providerKey='+json.dumps(key)+';\n'
 return out
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--check',action='store_true');args=parser.parse_args();out=outputs()
 manifest=ROOT/'_data/shop-generated-pages.json';paths=[str(p.relative_to(ROOT)) for p in out if p.suffix=='.html'];previous=json.loads(manifest.read_text()) if manifest.exists() else []
 for old in set(previous)-set(paths):
  path=ROOT/old
  assert old.startswith('shop/') and old.endswith('/index.html'),'Unsafe generated page cleanup'
  if args.check and path.exists():raise SystemExit('Stale withdrawn product '+old)
  if not args.check:path.unlink(missing_ok=True)
 out[manifest]=json.dumps(paths,indent=2)+'\n'
 for path,value in out.items():
  if args.check:
   assert path.exists() and path.read_text()==value,'Stale commerce output: '+str(path)
  else:path.parent.mkdir(parents=True,exist_ok=True);path.write_text(value)
 print('Shop draft preview: '+('enabled for verified staging build' if preview_enabled() else 'disabled; published products only'))
 print('PASS: programme pages and '+str(len(load()))+' verified merchandise products '+('synchronized' if args.check else 'generated'))
