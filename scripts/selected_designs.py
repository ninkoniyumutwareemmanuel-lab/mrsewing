"""Publication-gated photograph references shared by collections, fabric and quotation."""
from urllib.parse import quote,unquote
DOMAIN='https://mrsewingfashion.com'
def image_url(src):
 assert src.startswith('/') and not src.startswith('//'),'Local approved photograph required'
 return DOMAIN+quote(unquote(src),safe='/')
def design_media():
 from build_collections import load,design_name,design_route
 from suit_references import model
 labels=model()['references'];out={}
 for d in load()[0]:
  images=[{k:i[k] for k in ['src','alt','width','height']}|{'url':image_url(i['src'])} for i in d['images']]
  out[d['id']]={'name':labels.get(d['id'],{}).get('label') or design_name(d),'image':images[0]['src'],'images':images,'route':design_route(d)}
 return out
