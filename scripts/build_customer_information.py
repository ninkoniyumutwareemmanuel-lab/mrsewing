#!/usr/bin/env python3
"""Render existing policy/FAQ routes from shared customer facts and page content."""
import argparse,json,re
from html import escape
from html.parser import HTMLParser
from site_seo import ROOT,DOMAIN,finalize
from sync_page_seo import apply
from customer_information import expand
class Plain(HTMLParser):
 def __init__(self,text):super().__init__();self.parts=[];self.feed(text)
 def handle_data(self,s):self.parts.append(s)
def plain(text):return ' '.join(' '.join(Plain(text).parts).split())
def policy_main(data):
 title=escape(data['title']);out='<div class="page-title"><img src="/assets/images/mr-logo-480.webp" alt="Mr Sewing logo" class="about-logo" width="1244" height="802" decoding="async"><h1>'+title+'</h1><p>Mr Sewing Fashion Designer · Kigali, Rwanda</p><span class="updated">Last updated: 30 October 2026</span></div><div class="box"><p>'+escape(data['intro'])+'</p></div>'
 out+='<nav class="box" aria-label="On this page"><h2>On this page</h2><ul>'+''.join('<li><a href="/'+data['route']+'/#'+s['id']+'">'+escape(s['title'])+'</a></li>' for s in data['sections'])+'</ul></nav>'
 for s in data['sections']:
  anchors=''.join('<span id="'+old+'"></span>' for old,new in data.get('legacyAnchors',{}).items() if new==s['id'])
  out+='<section class="sec" id="'+s['id']+'">'+anchors+'<h2>'+escape(s['title'])+'</h2>'+''.join('<p>'+expand(p)+'</p>' if p!='{{cotton_table}}' else expand(p) for p in s['paragraphs'])+'</section>'
 return out

def faq_content(categories):
 out='<div class="facts" id="facts"><div class="fact"><b>70%</b><span>Advance before production</span></div><div class="fact"><b>Balance</b><span>Before suit cleaning &amp; delivery</span></div><div class="fact"><b>Full payment</b><span>Before garment release</span></div></div>'
 out+='<div class="toolbar" id="toolbar"><nav class="chips" aria-label="FAQ topics">'+''.join('<a href="/faq/#'+c['id']+'">'+escape(c['title'])+'</a>' for c in categories)+'</nav><div class="tools"><button type="button" id="expandAll">Expand all</button><button type="button" id="collapseAll">Collapse all</button></div></div>'
 for c in categories:
  out+='<section class="faq-category" id="'+c['id']+'"><h2>'+escape(c['title'])+'</h2>'+''.join('<details><summary>'+escape(q['question'])+'</summary><div class="faq-content">'+expand(q['answer'])+'</div></details>' for q in c['questions'])+'</section>'
 return out+'<div class="no-results" id="noResults" hidden><p>No questions match your search. Try another word, or ask us directly on WhatsApp.</p></div><section class="help"><h2>Discuss your request.</h2><p>Contact the team for a quotation or to confirm arrangements.</p><div class="help-btns"><a class="btn btn-wa" href="https://wa.me/250787411501?text=Hello%20Mr%20Sewing%2C%20I%20have%20a%20customer%20information%20question." target="_blank" rel="noopener">Ask on WhatsApp</a><a class="btn btn-line" href="/booking/">Request a consultation</a></div><p><a href="/terms-and-conditions/">Terms &amp; Conditions</a> · <a href="/refund-policy/">Refund &amp; Cancellation Policy</a> · <a href="/privacy-policy/">Privacy Policy</a></p></section>'
def static_header(source):
    # Reuse the exact legacy header and deferred-navigation styles at first paint.
    header=(ROOT/'header.html').read_text()
    nav=re.search(r'style.textContent = `(.*?)`;', (ROOT/'assets/navigation.js').read_text(),re.S)[1]
    return source.replace('{{header}}',header).replace('</head>','<style data-static-navigation>'+nav+'</style></head>',1)

def outputs():
 meta=json.loads((ROOT/'_data/page-seo.json').read_text());pages=json.loads((ROOT/'_data/policy-pages.json').read_text());out={}
 for slug,data in pages.items():
  path=ROOT/(slug+'.html');data={**data,'route':slug};source=(ROOT/'_templates'/(slug+'.html')).read_text().replace('{{content}}',policy_main(data))
  # Keep the existing restrained policy style and provide a responsive price table.
  source=source.replace('</style>','.tw{overflow-x:auto}.price-table{width:100%;border-collapse:collapse}.price-table th,.price-table td{padding:12px;text-align:left;border-bottom:1px solid #444}.price-table caption{text-align:left;padding:12px 0;color:#d4af37}section{scroll-margin-top:90px}</style>',1)
  out[path]=finalize(apply(static_header(source),meta[path.name]),path)
 cats=json.loads((ROOT/'_data/customer-faqs.json').read_text());path=ROOT/'faq.html'
 schema={'@context':'https://schema.org','@type':'FAQPage','@id':DOMAIN+'/faq/#faq','url':DOMAIN+'/faq/','name':'Frequently Asked Questions','mainEntity':[{'@type':'Question','name':q['question'],'acceptedAnswer':{'@type':'Answer','text':plain(expand(q['answer']))}} for c in cats for q in c['questions']]}
 source=(ROOT/'_templates/faq.html').read_text().replace('{{content}}',faq_content(cats)).replace('{{faq_schema}}','<script type="application/ld+json">'+json.dumps(schema,ensure_ascii=False).replace('<','\\u003c')+'</script>')
 out[path]=finalize(apply(static_header(source),meta[path.name]),path)
 return out

def main():
 p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');a=p.parse_args()
 for path,output in outputs().items():
  if a.check:
   if path.read_text()!=output:raise SystemExit('Stale customer information: '+path.name)
  else:path.write_text(output)
 print('PASS: four existing policy/FAQ pages, shared Cotton prices/payment sequence and FAQ schema '+('synchronized.' if a.check else 'generated.'))
if __name__=='__main__':main()
