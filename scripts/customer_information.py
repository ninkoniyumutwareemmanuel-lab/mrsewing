"""Shared owner-confirmed customer facts. No supplier costs or draft retail rates."""
import json,re
from pathlib import Path
from html import escape
ROOT=Path(__file__).resolve().parents[1]
def information():
 data=json.loads((ROOT/'_data/customer-information.json').read_text());texts=__import__('customer_policies').facts()['texts']
 for key,ref in [('timing','policyTailoringTime'),('alterationTiming','policyAlterationTime'),('careTiming','policyCareTime'),('suitPayment','policyDomesticPayment')]:data[key]=texts[ref]
 return data
def cotton_table():
 from customer_policies import facts
 return '<p>'+escape(facts()['texts']['policyMensStarting']+' '+facts()['texts']['policyWomensStarting'])+' <a href="/services/custom-tailoring/#service-info-prices">View the tier pricing tables and included benefits</a>. Men’s tuxedos have a separate schedule.</p>'

def historical_cotton_table():
 return '<div class="tw"><table class="price-table"><caption>Cotton standard suit base prices — RWF</caption><thead><tr><th scope="col">Standard suit</th><th scope="col">Base price (RWF)</th></tr></thead><tbody>'+''.join('<tr><th scope="row">'+escape(row['garment'])+'</th><td>'+format(row['priceRwf'],',')+'</td></tr>' for row in information()['cotton'])+'</tbody></table></div>'
def expand(text):
 data=information();data.update(__import__('customer_policies').facts()['texts']);data['cotton_table']=cotton_table()
 for key,value in data.items():
  if isinstance(value,str):text=text.replace('{{'+key+'}}',value)
 assert not re.search(r'{{\w+}}',text),text
 return text
