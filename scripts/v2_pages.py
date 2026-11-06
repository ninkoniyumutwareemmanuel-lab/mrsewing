"""V2 additions reuse existing frames, fields, provider and approved public records."""
import json,re
from html import escape
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def subscription_form():
 from customer_site import request_form
 source=request_form('support')
 source=source.replace('data-service=""','data-service="vip"').replace('<legend>Support topic</legend>','<legend>VIP Subscription Enquiry</legend>').replace('data-kind="support"','data-kind="subscription"').replace('Customer Support - Mr Sewing Fashion','VIP Subscription Enquiry - Mr Sewing Fashion')
 source=re.sub(r'<label for="requestService">.*?</select>','<input id="requestService" type="hidden" name="Service" value="vip">',source,count=1,flags=re.S)
 fields='''<fieldset class="subscription-requirements"><legend>Subscription Requirements</legend><label for="subscriptionType">Individual or family (required)</label><select id="subscriptionType" name="Subscription Type" required><option value="">Select an option</option><option>Individual</option><option>Family</option></select><label for="subscriptionPeople">Number of people requiring service (required)</label><input id="subscriptionPeople" name="Number of People" type="number" min="1" step="1" required><label for="subscriptionServices">Requested services (required)</label><select id="subscriptionServices" name="Requested Services" required><option value="">Select services</option><option>Garment Care &amp; Cleaning</option><option>Clothing Alterations &amp; Repairs</option><option>Garment Care &amp; Cleaning and Clothing Alterations &amp; Repairs</option></select><label for="subscriptionFrequency">Expected frequency (required)</label><input id="subscriptionFrequency" name="Expected Frequency" placeholder="For example, weekly or monthly" maxlength="200" required><label for="subscriptionLocation">Preferred location or handover arrangements (required)</label><input id="subscriptionLocation" name="Location or Handover" maxlength="300" required></fieldset>'''
 source=source.replace('<div><label for="requestMessage">',fields+'<div><label for="requestMessage">',1).replace('How Can We Help You?','Special garment-care requirements or additional information')
 source=source.replace('Submit Support Request','Submit Subscription Enquiry').replace('The submission service accepted your request. This is not confirmation of an order, appointment, production start, payment or refund approval. Our team will review the details.','The submission service accepted your subscription enquiry for review. This does not activate a subscription, confirm a contract or guarantee a quoted price. Our team will assess your requirements and contact you.')
 return source
def subscription_page():
 from customer_site import frame,intro
 from customer_navigation import breadcrumb
 body=breadcrumb([('Home','/'),('VIP Services','/services/vip/'),('VIP Subscription Enquiry',None)])+intro('VIP Subscription Enquiry','Request a personalised quotation for garment care and alterations for yourself or your family. Submitting this enquiry does not activate a subscription, confirm a contract or guarantee a price.')+subscription_form()
 return frame('/request/vip-subscription/','VIP Subscription Enquiry','Request an individually assessed garment-care and alterations subscription quotation in Kigali. No subscription or payment is activated.',body)
def media_page():
 from customer_site import frame,intro,section,link
 from customer_navigation import breadcrumb
 from project_catalog import projects
 business=json.loads((ROOT/'_data/business.json').read_text())
 body=breadcrumb([('Home','/'),('Media Kit',None)])+intro('Media Kit','Mr Sewing Fashion — tailoring and garment services in Kigali, Rwanda.')+section('About Mr Sewing Fashion','Mr Sewing Fashion is operated by NINKONIYUMUTWARE NEXUS LTD in Kigali, Rwanda. Discover our tailoring, alterations, garment care and individually assessed assistance services.')
 body+='<section class="release-section"><h2>Our Services</h2><ul>'
 from customer_site import data
 for s in data()['services']:body+='<li>'+link(s['route'],s['title'])+'</li>'
 body+='</ul></section><section class="release-section"><h2>A Look at Our Work</h2><div class="release-cards">'
 for p in projects()[:2]:
  i=p['images'][0];body+='<article class="release-card"><img src="'+escape(i['src'],quote=True)+'" alt="'+escape(i['alt'],quote=True)+'" width="'+str(i['width'])+'" height="'+str(i['height'])+'" loading="lazy"><h3>'+escape(p['title'])+'</h3>'+link('/our-work/'+p['slug']+'/','View Project')+'</article>'
 body+='</div><p>Contact us to discuss permission and approved materials before reproducing photographs or brand assets.</p></section>'
 body+=section('English–French Media Kit','A bilingual media kit is being prepared. The download will be available after the final document has been approved. No draft PDF is available for download.')+section('Media, Partnership & Collaboration Enquiries','For press information or a proposed collaboration, contact our team to discuss your request. No partnership or permission is implied by an enquiry.')
 body+='<p>'+link('mailto:'+business['email'],business['email'])+' · '+link('tel:'+business['telephone'],business['telephone'])+'</p><p>'+link(business['url'],'Official Website')+'</p>'
 return frame('/media-kit/','Media Kit','Verified company introduction, approved work and media enquiry contacts for Mr Sewing Fashion in Kigali. Bilingual PDF awaiting approval.',body)
