"""The existing customer-information builder's shared FAQ renderer and search catalogue."""
import json,re
from html import escape
from html.parser import HTMLParser
from urllib.parse import urlencode
from site_seo import ROOT,DOMAIN,finalize
from sync_page_seo import apply
from service_information import styles as offer_styles
from customer_information import expand
from build_homepage import reserve_image_space
from homepage_resources import delivery,CSS as ICON_CSS
from build_clean_urls import DISCOVERY_LINKS,legacy_script
import shared_components as shared
class Plain(HTMLParser):
 def __init__(self,text):super().__init__();self.parts=[];self.feed(text)
 def handle_data(self,s):self.parts.append(s)
def plain(text):return ' '.join(' '.join(Plain(text).parts).split())
def catalogue():
 data=json.loads((ROOT/'_data/customer-faqs.json').read_text());topics=[t for t in data['topics'] if t.get('published',True)];qs=data['questions'];slugs=set();owners={}
 for t in topics:
  assert re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*',t['slug']) and t['slug'] not in slugs;slugs.add(t['slug'])
  assert t['title'] and t['description'] and t['destination'].startswith('/')
  t['questions']=[id for id in t['questions'] if qs[id].get('published',True)]
  assert t['questions'],'Empty FAQ topic must remain unpublished'
  for id in t['questions']:
   assert re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*',id) and id not in owners;owners[id]=t['slug']
   assert qs[id]['question'] and expand(qs[id]['answer'])
 for t in topics:assert all(s in slugs and s!=t['slug'] for s in t['related'])
 return data,topics,qs,owners
def route(topic):return '/faq/'+topic['slug']+'/'
def routes():return [route(t) for t in catalogue()[1]]
def icon(name):
 paths={
 'arrow':'<path d="M5 19 19 5M5 5h14v14"/>',
 'needle':'<path d="m5 19 13-13c3-3 5 0 2 3L7 22M16 8l2 2M4 4l6 6"/>',
 'rings':'<circle cx="8" cy="13" r="6"/><circle cx="16" cy="13" r="6"/><path d="m8 7 4-5 4 5"/>',
 'cap':'<path d="m2 8 10-5 10 5-10 5Z M6 10v7c4 3 8 3 12 0v-7M22 8v9"/>',
 'pin':'<path d="M20 10c0 6-8 12-8 12S4 16 4 10a8 8 0 1 1 16 0Z"/><circle cx="12" cy="10" r="3"/>',
 'scissors':'<circle cx="6" cy="6" r="3"/><circle cx="6" cy="18" r="3"/><path d="m8 8 13 13M8 16 21 3"/>',
 'clock':'<circle cx="12" cy="12" r="9"/><path d="M12 6v6l4 2"/>',
 'hanger':'<path d="M9 6a3 3 0 1 1 4 3v2l9 7v3H2v-3l9-7"/>',
 'grid':'<rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/>',
 'ruler':'<path d="m3 17 14-14 4 4L7 21ZM13 7l3 3M9 11l3 3M5 15l3 3"/>',
 'receipt':'<path d="M5 2h14v20l-3-2-4 2-4-2-3 2ZM8 7h8M8 11h8M8 15h4"/>',
 'calendar':'<rect x="3" y="5" width="18" height="16" rx="1"/><path d="M7 2v6M17 2v6M3 11h18M7 15h3M14 15h3"/>',
 'truck':'<path d="M2 5h12v12H2ZM14 9h4l4 5v3h-8"/><circle cx="6" cy="18" r="3"/><circle cx="18" cy="18" r="3"/>',
 'chat':'<path d="M21 11c0 5-4 8-9 8H8l-6 3 2-6a8 8 0 0 1-1-5c0-5 4-8 9-8s9 3 9 8Z M7 10h10M7 14h6"/>',
 'shield':'<path d="m12 2 9 4v6c0 5-9 10-9 10S3 17 3 12V6ZM8 12l3 3 5-6"/>',
 'search':'<circle cx="10" cy="10" r="7"/><path d="m15 15 6 6"/>',
 'close':'<path d="m5 5 14 14M19 5 5 19"/>'}
 assert name in paths,name
 return '<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">'+paths[name]+'</svg>'
def contact(title,path):
 return '<a class="faq-primary" href="https://wa.me/250787411501?'+escape(urlencode({'text':'Hello Mr Sewing! I have a question about '+title+'.\n'+DOMAIN+path}),quote=True)+'" target="_blank" rel="noopener">Ask Mr Sewing <span aria-hidden="true">↗</span></a>'
def search_data():
 data,topics,qs,_=catalogue()
 return {'synonyms':data['synonyms'],'entries':[{'id':id,'question':qs[id]['question'],'topic':t['title'],'url':route(t)+'#'+id,'answer':plain(expand(qs[id]['answer'])),'keywords':t.get('keywords',[])+qs[id].get('keywords',[])} for t in topics for id in t['questions']]}
def hub(topics,data):
 out='<section class="faq-intro" aria-labelledby="faq-heading"><p class="home-eyebrow">Mr Sewing help centre</p><h1 id="faq-heading">How can we help?</h1><p>Choose a topic or search for an answer.</p></section>'
 out+='<form class="faq-search" id="faq-search" role="search" aria-label="Search all FAQ topics" action="/faq/" method="get"><label for="faq-query">Search every topic and answer</label><div class="faq-search-box">'+icon('search')+'<input type="search" id="faq-query" name="q" placeholder="Try payments, fittings or delivery" autocomplete="off" maxlength="160" aria-controls="faq-results" aria-describedby="faq-search-hint"><button type="button" id="faq-clear" aria-label="Clear FAQ search" hidden>'+icon('close')+'</button></div><p id="faq-search-hint" class="faq-search-hint">Search questions, service topics and practical customer guidance.</p></form><noscript><p>Choose a topic below to browse its answers. Search is available when JavaScript is enabled.</p></noscript>'
 out+='<section id="faq-results" aria-labelledby="faq-results-title" hidden><h2 id="faq-results-title">Search results</h2><p id="faq-search-status" class="faq-search-status" role="status" aria-live="polite" aria-atomic="true"></p><ol class="faq-result-list" id="faq-result-list"></ol><div class="faq-empty" id="faq-empty" hidden><p>No answers match your search. Try another word or ask us about your request.</p>'+contact('a customer enquiry','/faq/')+'</div></section>'
 out+='<nav class="faq-grid" id="faq-topics" aria-label="FAQ topics">'
 for t in topics:
  old=''.join('<span id="'+id+'" aria-hidden="true"></span>' for id,dest in data['legacyFragments'].items() if dest.split('#')[0]==t['slug'])
  out+='<a class="faq-card" href="'+route(t)+'">'+old+'<span class="faq-icon">'+icon(t['icon'])+'</span><h2>'+escape(t['title'])+'</h2><p>'+escape(t['description'])+'</p><small>'+str(len(t['questions']))+' answers <span aria-hidden="true">↗</span></small></a>'
 out+='</nav><aside class="faq-contact"><p>Need an assessment or quotation? Share your garment or service needs with the team.</p>'+contact('a customer enquiry','/faq/')+'</aside>'
 out+='<script type="application/json" id="faq-search-data">'+json.dumps(search_data(),ensure_ascii=False).replace('<','\\u003c')+'</script><script type="application/json" id="faq-legacy-data">'+json.dumps({id:'/faq/'+dest.split('#')[0]+'/'+('#'+dest.split('#')[1] if '#' in dest else '') for id,dest in data['legacyFragments'].items()}).replace('<','\\u003c')+'</script>'
 return out

def topic_content(t,topics,qs):
 path=route(t)
 out='<nav class="faq-breadcrumb" aria-label="Breadcrumb"><a href="/">Home</a><span aria-hidden="true">/</span><a href="/faq/">All FAQ topics</a><span aria-hidden="true">/</span><span>'+escape(t['title'])+'</span></nav><section class="faq-intro" aria-labelledby="faq-heading"><p class="home-eyebrow">Mr Sewing help centre</p><h1 id="faq-heading">'+escape(t['title'])+' FAQs</h1><p>'+escape(t['description'])+'</p></section><div class="faq-topic-layout"><div class="faq-questions">'
 for id in t['questions']:
  q=qs[id];out+='<details class="faq-question" id="'+id+'"><summary><h2>'+escape(q['question'])+'</h2></summary><div class="faq-answer">'+expand(q['answer'])+'<br><a class="faq-permalink" href="'+path+'#'+id+'">Link to this answer <span class="visually-hidden">: '+escape(q['question'])+'</span></a></div></details>'
 out+='</div><aside class="faq-side"><h2>Your next step.</h2><p>Discuss your needs with the team for an assessment, quotation or confirmation of arrangements.</p>'+contact(t['title'],path)+'<a class="faq-side-link" href="'+t['destination']+'">View related '+('service' if t['destination'].startswith('/services/') else 'information')+' <span aria-hidden="true">↗</span></a><a class="faq-side-link" href="/faq/">All FAQ topics</a></aside></div>'
 byslug={x['slug']:x for x in topics};out+='<nav class="faq-related" aria-label="Related FAQ topics"><h2>Related topics</h2><div class="faq-related-links">'+''.join('<a href="'+route(byslug[s])+'">'+escape(byslug[s]['title'])+'</a>' for s in t['related'])+'</div></nav>'
 return out

def render(path,title,description,content,schema,legacy=False):
 source=(ROOT/'_templates/faq.html').read_text();vals={'title':escape(title,quote=True),'description':escape(description,quote=True),'route':path,'styles':shared.component_css()+'\n'+ICON_CSS+'\n'+(ROOT/'_templates/faq.css').read_text()+'\n'+offer_styles(),'header':delivery(re.sub(r'<img\b[^>]*>',reserve_image_space,shared.header('/faq/')),'header'),'footer':delivery(shared.footer(),'footer'),'content':content.replace('<span aria-hidden="true">↗</span>',icon('arrow')),'schema':json.dumps(schema,ensure_ascii=False).replace('<','\\u003c'),'discovery':DISCOVERY_LINKS,'legacy':legacy_script('faq.html') if legacy else ''}
 for k,v in vals.items():source=source.replace('{{'+k+'}}',v)
 assert not re.search(r'{{\w+}}',source)
 return finalize(source,ROOT/'faq.html' if legacy else ROOT/path.strip('/')/'index.html')
def outputs():
 data,topics,qs,_=catalogue();seo=json.loads((ROOT/'_data/page-seo.json').read_text())['faq.html'];out={}
 schema={'@context':'https://schema.org','@type':'CollectionPage','name':seo['title'],'description':seo['description'],'url':DOMAIN+'/faq/','isPartOf':{'@id':DOMAIN+'/#website'},'mainEntity':{'@type':'ItemList','itemListElement':[{'@type':'ListItem','position':n+1,'name':t['title'],'url':DOMAIN+route(t)} for n,t in enumerate(topics)]}}
 out[ROOT/'faq.html']=render('/faq/',seo['title'],seo['description'],hub(topics,data),schema,True)
 for t in topics:
  path=route(t);title=t['title']+' FAQs | Mr Sewing Fashion, Kigali';desc=t['description']+' Find practical answers from Mr Sewing and the next step for your enquiry.'
  schema={'@context':'https://schema.org','@type':'FAQPage','@id':DOMAIN+path+'#faq','name':title,'description':desc,'url':DOMAIN+path,'isPartOf':{'@id':DOMAIN+'/faq/'},'mainEntity':[{'@type':'Question','name':qs[id]['question'],'acceptedAnswer':{'@type':'Answer','text':plain(expand(qs[id]['answer']))}} for id in t['questions']],'breadcrumb':{'@type':'BreadcrumbList','itemListElement':[{'@type':'ListItem','position':1,'name':'Home','item':DOMAIN+'/'},{'@type':'ListItem','position':2,'name':'FAQs','item':DOMAIN+'/faq/'},{'@type':'ListItem','position':3,'name':t['title'],'item':DOMAIN+path}]}}
  out[ROOT/path.strip('/')/'index.html']=render(path,title,desc,topic_content(t,topics,qs),schema)
 out[ROOT/'assets/faq-help.js']=shared.menu_script()+'\n'+(ROOT/'_templates/faq-help.js').read_text()
 # Guard obsolete generated topics rather than silently publishing withdrawn answers.
 stale=set((ROOT/'faq').glob('*/index.html'))-{ROOT/route(t).strip('/')/'index.html' for t in topics}
 assert not stale,'Unpublished FAQ topic output requires review: '+str(stale)
 return out
