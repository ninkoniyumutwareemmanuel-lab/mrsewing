/* Isolated conversion handoff regression: actual scripts, fake DOM/timers, no vendor traffic. */
'use strict';
const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
const config=JSON.parse(fs.readFileSync('_data/advertising-measurement.json','utf8'));
const controller=fs.readFileSync('_templates/customer-tracking.js','utf8').replace('/*customer-tracking-config*/null',JSON.stringify(config));
const helper=fs.readFileSync('_templates/enquiry-measurement.js','utf8');
const handoff=fs.readFileSync('_templates/whatsapp-consent.js','utf8');
function scenario({choice='accepted',query='',path='/',referrer='',host='mrsewingfashion.com'}={}){
 const base=new URL('https://'+host+path+query),local=new Map(),session=new Map(),handlers={},winHandlers={},assigned=[],opened=[],timers=new Map();
 if(choice)local.set('mrsewing:measurement-consent:v2',JSON.stringify({version:2,choice}));
 const storage=m=>({getItem:k=>m.get(k)??null,setItem:(k,v)=>m.set(k,v),removeItem:k=>m.delete(k)});
 const location={href:base.href,origin:base.origin,hostname:base.hostname,pathname:base.pathname,search:base.search,hash:base.hash,assign:u=>assigned.push(u),replace:u=>assigned.push(u)};
 const node=()=>({children:[],setAttribute(){},addEventListener(){},append(...items){this.children.push(...items);},appendChild(x){this.children.push(x);return x;}});
 const head=node(),body=node();
 const document={head,body,readyState:'complete',referrer,querySelector:()=>null,getElementById:()=>null,createElement:node,addEventListener:(k,fn)=>(handlers[k]||=[]).push(fn)};
 class CustomEvent{constructor(type,options){this.type=type;this.detail=options?.detail;}}
 const window={location,CustomEvent,localStorage:storage(local),sessionStorage:storage(session),open:(...args)=>opened.push(args),addEventListener:(k,fn)=>(winHandlers[k]||=[]).push(fn),dispatchEvent:e=>{for(const fn of winHandlers[e.type]||[])fn(e);}};
 window.top=window;
 let next=0,timerId=0;
 const context={window,document,location,CustomEvent,URL,URLSearchParams,Date,performance:{getEntriesByType:()=>[{name:base.href}]},crypto:{randomUUID:()=>('synthetic-'+(++next))},history:{state:null,replaceState(){}},setTimeout:(fn,delay)=>{assert.equal(delay,500);timers.set(++timerId,fn);return timerId;},clearTimeout:id=>timers.delete(id)};
 for(const source of [handoff,controller,helper])vm.runInNewContext(source,context);
 function click(href='/whatsapp/?text=Hello%20%26%20thanks',target='',modifier=false){
  let prevented=false,stopped=false;const a={href:new URL(href,base.href).href,target,getAttribute:()=>null};
  const e={target:{closest:()=>a},ctrlKey:modifier,preventDefault(){prevented=true;},stopImmediatePropagation(){stopped=true;}};
  for(const fn of handlers.click||[]){fn(e);if(stopped)break;}return prevented;
 }
 return{window,head,assigned,opened,timers,click,events:(name='whatsapp_contact_click')=>window.dataLayer.filter(x=>x?.event===name),expire(){for(const fn of [...timers.values()])fn();}};
}
const normal=scenario();assert(normal.click());assert.equal(normal.assigned.length,0);assert.equal(normal.events().length,1);
const event=normal.events()[0];assert.equal(event.eventTimeout,500);assert.equal(typeof event.eventCallback,'function');assert(!JSON.stringify(event).includes('Hello'));
event.eventCallback();normal.expire();event.eventCallback();assert.equal(normal.assigned.length,1);
const url=new URL(normal.assigned[0]);assert.equal(url.hostname,'wa.me');assert.equal(url.pathname,'/250787411501');assert.equal(url.searchParams.get('text'),'Hello & thanks');
const timeout=scenario();timeout.click();timeout.expire();timeout.events()[0].eventCallback();assert.equal(timeout.assigned.length,1);assert.equal(timeout.events().length,1);
for(const choice of ['declined',null]){const s=scenario({choice});s.click();assert.equal(s.assigned.length,1);assert.equal(s.events().length,0);assert.equal(s.head.children.length,0);assert.equal(s.timers.size,0);}
const blank=scenario();blank.click('/whatsapp/','_blank');assert.equal(blank.opened.length,1);assert.equal(blank.assigned.length,0);assert.equal(blank.events().length,1);assert.equal(blank.events()[0].eventCallback,undefined);
const modifier=scenario();modifier.click('/whatsapp/','',true);assert.equal(modifier.opened.length,1);assert.equal(modifier.events().length,1);
const unavailable=scenario();delete unavailable.window.MrEnquiryMeasurement;unavailable.click();assert.equal(unavailable.assigned.length,1);
const wrong=scenario();assert.equal(wrong.click('https://wa.me/250000000000'),false);assert.equal(wrong.events().length,0);
for(const query of ['?gtm_debug=x','?gtm_debug=1795792019533']){const s=scenario({query});s.click();assert.equal(s.events().length,1);assert.equal(s.head.children.length,1);s.click('tel:+250787411501');assert.equal(s.events('website_call_click').length,1);}
const fromDebug=scenario({referrer:'https://mrsewingfashion.com/?gtm_debug=x'});fromDebug.click();assert.equal(fromDebug.events().length,1);
for(const options of [{query:'?gtm_debug=private%40example.invalid'},{query:'?gtm_debug=x&gtm_debug=x'},{query:'?gtm_debug=x&email=private%40example.invalid'},{query:'?gtm_debug=x',choice:'declined'},{query:'?gtm_debug=x',path:'/request/'},{query:'?gtm_debug=x',host:'mrsewing-staging.pages.dev'}]){const s=scenario(options);s.click();assert.equal(s.events().length,0);assert.equal(s.head.children.length,0);assert.equal(s.assigned.length,1);}
console.log('PASS WhatsApp: GTM callback and bounded fallback, exact destination, consent, new-tab/modifier behavior, strict debug markers, telephone event, unsafe context and staging suppression. No vendor requests.');
