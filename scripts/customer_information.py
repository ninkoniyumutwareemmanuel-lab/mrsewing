"""Shared owner-confirmed customer facts. No supplier costs or draft retail rates."""
import json,re
from pathlib import Path
from html import escape
ROOT=Path(__file__).resolve().parents[1]
def information():
 data=json.loads((ROOT/'_data/customer-information.json').read_text());texts=__import__('customer_policies').facts()['texts']
 for key,ref in [('timing','policyTailoringTime'),('alterationTiming','policyAlterationTime'),('careTiming','policyCareTime'),('suitPayment','policyDomesticPayment'),('standalonePayment','policyStandalonePayment'),('package','policyAllSuitBenefits'),('extras','policyGiftBenefits'),('higherCollections','policyCleaningBenefits')]:
  if ref in texts:data[key]=texts[ref]
 from business_settings import settings
 business=settings();data.update(officialPhone=business['phone'],officialPhoneDigits=business['phoneDigits'],officialWhatsApp='https://wa.me/'+business['phoneDigits'],officialTelephone='tel:'+business['phone'],officialEmail=business['email'])
 data['advancePercent']=__import__('customer_policies').facts()['payments']['domesticCustomAdvancePercent']
 data['balance']='Your balance is the accepted quotation total less payments already received.'
 data['delivery']=texts['policyCustomDelivery']+' '+texts['policyTransport']
 return data
def cotton_table():
 from customer_policies import facts
 return '<p>'+escape(facts()['texts']['policyMensStarting']+' '+facts()['texts']['policyWomensStarting'])+' <a href="/services/custom-tailoring/#service-info-prices">Explore suit quality tiers and included benefits</a>. Men’s tuxedo requirements and their quotation are assessed separately.</p>'

def historical_cotton_table():
 from public_content import service_prices_visible
 if not service_prices_visible():return cotton_table()
 return '<div class="tw"><table class="price-table"><caption>Cotton standard suit base prices — RWF</caption><thead><tr><th scope="col">Standard suit</th><th scope="col">Base price (RWF)</th></tr></thead><tbody>'+''.join('<tr><th scope="row">'+escape(row['garment'])+'</th><td>'+format(row['priceRwf'],',')+'</td></tr>' for row in information()['cotton'])+'</tbody></table></div>'
def expand(text):
 data=information();data.update(__import__('customer_policies').facts()['texts']);data['cotton_table']=cotton_table()
 for key,value in data.items():
  if isinstance(value,str):text=text.replace('{{'+key+'}}',value)
 assert not re.search(r'{{\w+}}',text),text
 return text
