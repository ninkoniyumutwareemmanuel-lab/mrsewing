"""Preserve legacy WhatsApp URLs for client-side direct chat navigation."""
from html import escape,unescape
from urllib.parse import urlparse,parse_qs,urlencode
import re
def protect(source):
 def replacement(match):
  u=urlparse(unescape(match[2]));qs=parse_qs(u.query)
  if u.scheme!='https' or u.netloc!='wa.me' or u.path.rstrip('/')!='/250787411501':return match[0]
  text=qs.get('text',[''])[0][:6000]
  return 'href='+match[1]+escape('/whatsapp/'+('?' +urlencode({'text':text}) if text else ''),quote=True)+match[1]
 source=re.sub(r'href=([\"\'])(https://wa\.me/[^\"\']*)\1',replacement,source)
 source=re.sub(r'<script src="/assets/whatsapp-consent.js" defer></script>','',source)
 return source.replace('</head>','<script src="/assets/whatsapp-consent.js" defer></script></head>',1)
def page():
 from customer_site import frame,intro
 from customer_navigation import breadcrumb
 return frame('/whatsapp/','Continue to WhatsApp',"Open the official Mr Sewing Fashion WhatsApp chat. You decide whether to send a message.",breadcrumb([('Home','/'),('WhatsApp',None)])+intro('Continue to WhatsApp',"Chat directly with Mr Sewing Fashion about our services or a quotation.")+"<section class=\"release-section\"><p><a class=\"home-button home-button-gold\" href=\"https://api.whatsapp.com/send?phone=250787411501\" rel=\"noopener\">Open WhatsApp</a></p><p>Opening WhatsApp does not send a message or confirm an order. You decide whether to send the message in WhatsApp.</p><p>Read our <a href=\"/terms-and-conditions/\">Terms &amp; Conditions</a> and <a href=\"/privacy-policy/\">Privacy Policy</a> at any time.</p></section>")
