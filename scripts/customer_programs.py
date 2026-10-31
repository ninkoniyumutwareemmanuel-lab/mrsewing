"""Existing program routes, rendered from the shared approved customer facts and FAQs."""
import json,re
from html import escape
from html.parser import HTMLParser
from site_seo import ROOT
from build_journey import page
import service_information as offers
from customer_information import expand

class Plain(HTMLParser):
 def __init__(self,text):super().__init__();self.parts=[];self.feed(text)
 def handle_data(self,s):self.parts.append(s)
def plain(s):return ' '.join(' '.join(Plain(s).parts).split())

def render(route):
 data=json.loads((ROOT/'_data/customer-faqs.json').read_text());topic=next(t for t in data['topics'] if t.get('route')==route);q=data['questions']
 loyalty=route=='/loyalty-program/'
 title='Loyalty Program & Second-Purchase Gifts' if loyalty else 'Salesperson Referral Program'
 description='Understand Mr Sewing’s suit-only loyalty discount, separate-purchase counting and collection-specific second-purchase gifts in Kigali.' if loyalty else 'Understand Mr Sewing’s first-time buyer referral discount, code timing, qualifying suit commissions and salesperson payment windows.'
 content='<nav class="journey-back" aria-label="Breadcrumb"><a href="/">Home</a> / <a href="/faq/">Help centre</a> / <span>'+escape(title)+'</span></nav><section class="preparation-intro"><p class="home-eyebrow">'+('Returning purchases, recognised' if loyalty else 'Introduce a first-time suit customer')+'</p><h1>'+escape(title)+'</h1><p>'+('3% off suits from the third separate qualifying purchase, with collection-specific gifts on the second qualifying purchase.' if loyalty else 'A defined buyer benefit and salesperson commission for qualifying first-time customer suit orders.')+'</p></section>'
 if loyalty:
  content+=offers.section('From your third qualifying purchase','{{loyaltySummary}}')+offers.section('Second-purchase gifts','{{gift_table}} {{giftTerms}}')+offers.discounts()+offers.section('Confirm your order history','{{loyaltyVerification}}')
  content+='<nav class="offer-links" aria-label="Related benefits"><a href="/services/garment-care/#included-cleaning-benefits">Included cleaning benefits</a><a href="/referral-program/">Salesperson referral program</a></nav>'
 else:
  content+=offers.section('For first-time buyers','{{referralBuyer}}')+offers.section('Before you pay an advance','Record your chosen salesperson’s code with the team before the advance payment. Discuss the complete quotation and any express, mobile or accessory charges before payment.')+offers.section('Suit-only discount calculation','{{discountRules}}')
  content+='<section class="program-participant" id="salesperson-guidance" aria-labelledby="participant-title"><p class="home-eyebrow">Participant guidance</p><h2 id="participant-title">For salespeople</h2>'
  content+=offers.section('Qualifying suits and codes','{{referralCommission}}')+offers.section('When commission becomes payable','{{referralEligibility}}')+offers.section('Payment windows and carried orders','{{referralWindows}}')+offers.section('Participation and payout arrangements','Contact Mr Sewing about participation and an assigned code. This website does not issue codes or process commission payments. {{referralPayment}}')+'</section>'
 content+='<section class="program-faq" aria-labelledby="program-faq-title"><h2 id="program-faq-title">Questions about this program</h2>'
 for ident in topic['questions']:
  item=q[ident];content+='<details class="faq-question" id="'+ident+'"><summary>'+escape(item['question'])+'</summary><div class="program-answer">'+expand(item['answer'])+'<a class="home-text-link" href="'+route+'#'+ident+'">Link to this answer</a></div></details>'
 content+='</section><nav class="help-related" aria-label="Continue exploring"><a href="/faq/">All FAQ topics</a><a href="/faq/prices-packages-payments/">Prices &amp; payments</a><a href="/contact/">Contact Mr Sewing</a></nav>'
 schema={'mainEntity':[{'@type':'Question','name':q[i]['question'],'acceptedAnswer':{'@type':'Answer','text':plain(expand(q[i]['answer']))}} for i in topic['questions']]}
 source=page(route,title+' | Mr Sewing',description,content,'FAQPage',schema)
 source=source.replace('</style>','\n'+offers.styles()+'\n'+(ROOT/'_templates/completion.css').read_text()+'\n'+(ROOT/'_templates/preparation.css').read_text()+'\n'+(ROOT/'_templates/customer-programs.css').read_text()+'</style>',1)
 return source.replace('</body>','<script src="/assets/customer-programs.js" defer></script></body>')
