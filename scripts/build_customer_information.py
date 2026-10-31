#!/usr/bin/env python3
"""Render existing policy/FAQ routes from shared customer facts and page content."""
import argparse,json,re
import service_information as offers
from html import escape
from html.parser import HTMLParser
from site_seo import ROOT,DOMAIN,finalize
from sync_page_seo import apply
from customer_information import expand
from faq_help import outputs as faq_outputs, plain, catalogue
def policy_main(data):
 title=escape(data['title']);out='<div class="page-title"><img src="/assets/images/mr-logo-480.webp" alt="Mr Sewing logo" class="about-logo" width="1244" height="802" decoding="async"><h1>'+title+'</h1><p>Mr Sewing · Kigali, Rwanda</p><span class="updated">Last updated: 31 October 2026</span></div><div class="box"><p>'+escape(data['intro'])+'</p></div>'
 out+='<nav class="box" aria-label="On this page"><h2>On this page</h2><ul>'+''.join('<li><a href="/'+data['route']+'/#'+s['id']+'">'+escape(s['title'])+'</a></li>' for s in data['sections'])+'</ul></nav>'
 for s in data['sections']:
  anchors=''.join('<span id="'+old+'"></span>' for old,new in data.get('legacyAnchors',{}).items() if new==s['id'])
  out+='<section class="sec" id="'+s['id']+'">'+anchors+'<h2>'+escape(s['title'])+'</h2>'+''.join('<p>'+expand(p)+'</p>' if p not in ['{{cotton_table}}','{{suit_price_table}}','{{alteration_table}}','{{care_price_table}}','{{gift_table}}'] else expand(p) for p in s['paragraphs'])+'</section>'
 return out

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
  source=source.replace('</style>',offers.styles()+'</style>',1)
  out[path]=finalize(apply(static_header(source),meta[path.name]),path)
 out.update(faq_outputs())
 return out

def main():
 p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');a=p.parse_args()
 for path,output in outputs().items():
  if a.check:
   if not path.exists() or path.read_text()!=output:raise SystemExit('Stale customer information: '+path.name)
  else:path.parent.mkdir(parents=True,exist_ok=True);path.write_text(output)
 print(f'PASS: policy outputs and FAQ help centre with {len(catalogue()[1])} topics / {len(catalogue()[3])} published answers '+('synchronized.' if a.check else 'generated.'))
if __name__=='__main__':main()
