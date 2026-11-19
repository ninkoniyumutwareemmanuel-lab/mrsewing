"""Build-time shared identity/navigation projection; approved facts keep their existing owners.

No private settings are held here. Business identity/contact: business.json;
locations/social: contact-v2.json; hours: business-hours.json; legal operator:
customer-information.json. Navigation labels/ordering: site-navigation.json.
"""
from pathlib import Path
from html import escape
import json,re
ROOT=Path(__file__).resolve().parents[1]
def read(name):return json.loads((ROOT/'_data'/name).read_text())
def settings():
 b=read('business.json');c=read('contact-v2.json');h=read('business-hours.json');info=read('customer-information.json')
 digits=re.sub(r'\D','',b['telephone']);assert re.fullmatch(r'\d{7,15}',digits),'Invalid approved phone configuration'
 assert re.fullmatch(r'[A-Za-z0-9_.+\-]+@[A-Za-z0-9.\-]+',b['email']),'Invalid approved email configuration'
 return {'name':b['name'],'company':info['company'],'phone':b['telephone'],'phoneDigits':digits,'email':b['email'],'locations':c,'hours':h}
def guides():
 return [{**g,'href':'/guides/fabrics/' if g['label']=='Fabric Guide' else g.get('href')} for g in read('homepage-guides.json')]
def services():return read('customer-release.json')['services']
def anchor(href,label):return '<a href="'+escape(href,quote=True)+'">'+escape(label)+'</a>'
def services_disclosure():
 return '<details><summary>Services <span aria-hidden="true">⌄</span></summary><ul>'+''.join('<li>'+anchor(s['route'],s['title'])+'</li>' for s in services())+'</ul></details>'
def guide_items(footer=False):
 out=[]
 for g in guides():
  if g['href']:out.append('<li>'+anchor(g['href'],g['label'])+'</li>')
  else:out.append('<li class="'+('footer-guide-pending' if footer else 'nav-guide-pending')+'"><span class="'+('pending-guide' if footer else 'home-nav-pending')+'" title="This guide will be developed separately">'+escape(g['label'])+'</span></li>')
 return ''.join(out)
def main_navigation(current='/'):
 out=[]
 for item in read('site-navigation.json')['main']:
  if item.get('type')=='services':out.append('<li class="services-dropdown">'+services_disclosure()+'</li>')
  elif item.get('type')=='guides':out.append(guide_items())
  else:
   a=anchor(item['href'],item['label'])
   if item['href']==current:a=a.replace('>',' aria-current="page">',1)
   out.append('<li>'+a+'</li>')
 return ''.join(out)
def navigation_schema():
 items=[i for i in read('site-navigation.json')['main'] if i.get('href')]
 return {'names':[i['label'] for i in items],'urls':['https://mrsewingfashion.com'+i['href'] for i in items]}
def footer_columns():
 nav=read('site-navigation.json')
 service_list=''.join('<li>'+anchor(s['route'],s['title'])+'</li>' for s in services())
 quick=''.join('<li>'+anchor(i['href'],i['label'])+'</li>' for i in nav['quickInformation'])
 policies='<li><details class="footer-policy-list"><summary>Policies</summary><ul>'+''.join('<li>'+anchor(i['href'],i['label'])+'</li>' for i in nav['policies'])+'</ul></details></li>'
 return '<div class="footer-col"><h3>Service Links</h3><ul>'+service_list+'</ul></div><div class="footer-col"><h3>Customer Guides</h3><ul>'+guide_items(True)+'</ul></div><div class="footer-col"><h3>Quick Information</h3><ul>'+quick+policies+'</ul></div>'
def social_links():
 icons={'facebook':'facebook-f','instagram':'instagram','tiktok':'tiktok','youtube':'youtube'}
 return ''.join('<a href="'+escape(settings()['locations']['social'][name],quote=True)+'" target="_blank" rel="noopener" aria-label="'+name.title()+'"><i class="fab fa-'+icon+'"></i></a>' for name,icon in icons.items())
def expand(markup,current='/'):
 s=settings();h=s['hours'];loc=s['locations']['mainWorkshop']
 values={'main_navigation':main_navigation(current),'footer_columns':footer_columns(),'business_social_links':social_links(),'business_name':s['name'],'business_company':s['company'],'business_phone':s['phone'],'business_phone_digits':s['phoneDigits'],'business_email':s['email'],'business_header_location':'Kigali Main Workshop · '+loc.get('shortAddress',loc['streetAddress']),'business_header_hours':'Mon–Sat '+h['regularOpen']+'–'+h['regularClose']+' · Umuganda: '+h['umugandaOpen']+'–'+h['umugandaClose']+' by advance appointment · Sunday: by appointment only'}
 html_keys={'main_navigation','footer_columns','business_social_links'}
 for key,value in values.items():markup=markup.replace('{{'+key+'}}',value if key in html_keys else escape(value,quote=True))
 return markup

def client_text(source):
 """Expand only validated public contact constants in generated JavaScript."""
 s=settings()
 for key,value in [('business_phone',s['phone']),('business_phone_digits',s['phoneDigits']),('business_email',s['email'])]:source=source.replace('{{'+key+'}}',value)
 return source
