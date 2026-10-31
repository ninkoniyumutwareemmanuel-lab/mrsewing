"""Shared owner-confirmed customer facts. No supplier costs or draft retail rates."""
import json,re
from pathlib import Path
from html import escape
ROOT=Path(__file__).resolve().parents[1]
def information():return json.loads((ROOT/'_data/customer-information.json').read_text())
def cotton_table():
 return '<div class="tw"><table class="price-table"><caption>Cotton standard suit base prices — RWF</caption><thead><tr><th scope="col">Standard suit</th><th scope="col">Base price (RWF)</th></tr></thead><tbody>'+''.join('<tr><th scope="row">'+escape(row['garment'])+'</th><td>'+format(row['priceRwf'],',')+'</td></tr>' for row in information()['cotton'])+'</tbody></table></div>'
def table(caption,headers,rows,kind=''):
 return '<div class="tw" tabindex="0" role="region" aria-label="'+escape(caption,quote=True)+'"><table class="price-table '+kind+'"><caption>'+escape(caption)+'</caption><thead><tr>'+''.join('<th scope="col">'+escape(h)+'</th>' for h in headers)+'</tr></thead><tbody>'+''.join('<tr><th scope="row">'+escape(str(row[0]))+'</th>'+''.join('<td>'+escape(str(v))+'</td>' for v in row[1:])+'</tr>' for row in rows)+'</tbody></table></div>'
def suit_price_table():
 return table('Standard suit prices — RWF',['Collection','Men two-piece','Men three-piece','Women two-piece','Women three-piece'],[[r['name']]+[format(v,',') for v in r['pricesRwf']] for r in information()['collections']],'suit-prices')
def alteration_table():
 return table('Alterations — starting prices in RWF',['Garment / assessed service','Starting price'],[[r['service'],'From '+format(r['startingPriceRwf'],',')] for r in information()['alterations']])
def care_price_table():
 return table('Paid suit cleaning — RWF',['Suit','Standard','Express (+35%)'],[[r['garment'],format(r['standardPriceRwf'],','),format(r['expressPriceRwf'],',')] for r in information()['paidSuitCleaning']])
def expand(text):
 data=information();data['cotton_table']=cotton_table();data['suit_price_table']=suit_price_table();data['alteration_table']=alteration_table();data['care_price_table']=care_price_table()
 for key,value in data.items():
  if isinstance(value,str):text=text.replace('{{'+key+'}}',value)
 assert not re.search(r'{{\w+}}',text),text
 return text
