"""Static links require explicit consent even before any dynamic click handler runs."""
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
 return frame('/whatsapp/','Continue to WhatsApp','Review the Terms & Conditions before opening the official Mr Sewing Fashion WhatsApp conversation.',breadcrumb([('Home','/'),('WhatsApp',None)])+intro('Continue to WhatsApp','Please review the Terms & Conditions before starting your conversation with Mr Sewing Fashion.')+'<form id="whatsappConsentForm" class="release-section"><label class="quote-consent" for="whatsappTerms"><input id="whatsappTerms" type="checkbox" required autocomplete="off"><span>I agree to the <a href="/terms-and-conditions/" target="_blank" rel="noopener">Terms &amp; Conditions</a>.</span></label><button id="continueWhatsApp" type="submit" class="home-button home-button-gold" disabled>Continue to WhatsApp</button><p>Opening WhatsApp does not submit a quotation request or confirm an order. You choose whether to send the message in WhatsApp.</p><noscript><p>JavaScript is required to continue to WhatsApp here. You can call <a href="tel:+250787411501">+250 787 411 501</a> for assistance.</p></noscript></form>')
