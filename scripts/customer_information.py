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
 return '<p>Ordinary suit starting prices are shown in the Fabric Guide: men’s two-piece from 200,000 RWF and three-piece from 250,000 RWF; women’s two-piece from 150,000 RWF and three-piece from 200,000 RWF. Men’s tuxedos have a separate schedule. Confirm fabric, design, inclusions and the final quotation before acceptance.</p>'

def historical_cotton_table():
 return '<div class="tw"><table class="price-table"><caption>Cotton standard suit base prices — RWF</caption><thead><tr><th scope="col">Standard suit</th><th scope="col">Base price (RWF)</th></tr></thead><tbody>'+''.join('<tr><th scope="row">'+escape(row['garment'])+'</th><td>'+format(row['priceRwf'],',')+'</td></tr>' for row in information()['cotton'])+'</tbody></table></div>'
def expand(text):
 data=information();data.update(__import__('customer_policies').facts()['texts']);data['cotton_table']=cotton_table()
 for key,value in data.items():
  if isinstance(value,str):text=text.replace('{{'+key+'}}',value)
 assert not re.search(r'{{\w+}}',text),text
 return text
