/* Actual unified controller in synthetic DOMs. No vendor network is performed. */
'use strict';
const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
const config=JSON.parse(fs.readFileSync('_data/advertising-measurement.json'));
const source=fs.readFileSync('_templates/customer-tracking.js','utf8').replace('/*customer-tracking-config*/null',JSON.stringify(config));
function scenario(options={}){
 const base=new URL('https://'+(options.host||'mrsewingfashion.com')+(options.path||'/')+(options.query||''));
 const local=new Map(),session=new Map(Object.entries(options.session||{})),nodes=[],listeners={},windowListeners={},meta=[];
 if(options.choice)local.set('mrsewing:measurement-consent:v2',JSON.stringify({version:2,choice:options.choice}));
 if(options.oldChoice)local.set('mrsewing:meta-marketing-consent:v1',options.oldChoice);
 function storage(map){return{getItem:k=>map.get(k)??null,setItem(k,v){if(options.storageDenied)throw Error('Storage unavailable');map.set(k,v);},removeItem(k){map.delete(k);}};}
 const location={href:base.href,hostname:base.hostname,origin:base.origin,pathname:base.pathname,search:base.search,hash:base.hash,reloads:0,reload(){this.reloads++;}};
 function node(tag){const n={tag,children:[],listeners:{},style:{},setAttribute(k,v){this[k]=v;},addEventListener(k,v){this.listeners[k]=v;},append(...items){this.children.push(...items);},appendChild(item){this.children.push(item);return item;},remove(){this.removed=true;}};nodes.push(n);return n;}
 const head=node('head'),body=node('body'),form=options.form?{id:'customerRequestForm'}:null;
 const document={readyState:'loading',referrer:options.referrer||'',head,body,createElement:node,getElementById:id=>id==='customerRequestForm'?form:null,querySelector:s=>s.startsWith('#customerRequestForm')&&form?form:null,addEventListener(k,fn){(listeners[k]||=[]).push(fn);}};
 class Event{constructor(type,options){this.type=type;this.detail=options?.detail;}}
 const window={localStorage:storage(local),sessionStorage:storage(session),location,CustomEvent:Event,
  addEventListener(k,fn){(windowListeners[k]||=[]).push(fn);},dispatchEvent(e){if(e.type==='mrsewing:customer-event')meta.push(e.detail);for(const fn of windowListeners[e.type]||[])fn(e);}};
 window.top=window;
 const history={state:null,replaceState(_state,_title,url){const u=new URL(url,location.href);Object.assign(location,{href:u.href,pathname:u.pathname,search:u.search,hash:u.hash});}};
 let n=0;const context={window,document,location,history,crypto:{randomUUID:()=>('synthetic-event-'+(++n))},URL,URLSearchParams,CustomEvent:Event,Date,performance:{getEntriesByType:()=>[{name:options.initialURL||base.href}]}};
 vm.runInNewContext(source,context);for(const fn of listeners.DOMContentLoaded||[])fn();
 const event=(type,detail)=>window.dispatchEvent(new Event(type,{detail}));
 return{window,context,location,local,session,nodes,head,listeners,meta,event,events:()=>window.dataLayer.filter(x=>x?.event),
  choose(label){const button=nodes.filter(n=>n.tag==='button'&&n.textContent===label&&!n.removed).at(-1);assert(button,label+' button');button.listeners.click();},
  click(href){const a={href,getAttribute:()=>null},e={target:{closest:()=>a}};for(const fn of listeners.click||[])fn(e);return e;}};
}
for(const host of['mrsewing-staging.pages.dev','test.mrsewing-staging.pages.dev','localhost','unrelated.example']){
 const s=scenario({host,choice:'accepted'});assert.equal(s.head.children.filter(x=>x.src).length,0);assert.equal(s.events().length,0);assert.equal(s.meta.length,0);for(const c of s.window.dataLayer.filter(x=>x[0]==='consent'))assert.equal(c[2].ad_storage,'denied');
}
for(const choice of[null,'declined']){const s=scenario({choice});assert.equal(s.head.children.filter(x=>x.src).length,0);assert.equal(s.events().length,0);}
const old=scenario({oldChoice:'accepted'});assert.equal(old.head.children.filter(x=>x.src).length,0);assert(old.nodes.some(n=>n.textContent==='Allow Measurement'));
const opted=scenario();opted.choose('Allow Measurement');assert.equal(opted.head.children.filter(x=>x.src).length,1);assert.equal(opted.head.children.find(x=>x.src).src,'https://www.googletagmanager.com/gtm.js?id=GTM-WHR49M4D');
const commands=opted.window.dataLayer.filter(x=>!x.event).map(x=>Array.from(x));assert.equal(commands[0][0],'consent');assert.equal(commands[0][1],'default');for(const v of Object.values(commands[0][2]))assert.equal(v,'denied');
const update=commands.find(x=>x[1]==='update');assert.equal(update[2].ad_storage,'granted');assert.equal(update[2].ad_user_data,'granted');assert.equal(update[2].ad_personalization,'denied');assert.equal(update[2].analytics_storage,'denied');
assert.equal(opted.events().filter(x=>x.event==='page_view').length,1);
opted.event('mrsewing:enquiry-accepted',{eventId:'synthetic-positive',kind:'quotation',service:'custom-tailoring',outcome:'provider_accepted',name:'NEVER FORWARD',email:'private@example.invalid',photo:'private'});
opted.event('mrsewing:enquiry-accepted',{eventId:'synthetic-positive',kind:'quotation',service:'custom-tailoring',outcome:'provider_accepted'});
assert.equal(opted.events().filter(x=>x.event==='quote_request_success').length,1);assert.equal(opted.events().filter(x=>x.event==='lead_form_success').length,0);
assert(!JSON.stringify(opted.events()).includes('private@example.invalid'));assert(!JSON.stringify(opted.meta).includes('NEVER FORWARD'));
opted.event('mrsewing:enquiry-accepted',{eventId:'synthetic-service',kind:'quotation',service:'alterations',outcome:'provider_accepted'});
assert.equal(opted.events().filter(x=>x.event==='lead_form_success').length,1);
assert.equal(opted.window.MrCustomerTracking.signal({eventName:'appointment_confirmed',eventId:'synthetic-appointment'}),false);
assert.equal(opted.window.MrCustomerTracking.signal({eventName:'Purchase',eventId:'synthetic-purchase'}),false);
for(const [path,form]of[['/request/',false],['/booking.html',false],['/privacy-policy/',false],['/shop/',false],['/future-request/',true]]){
 const s=scenario({path,form,choice:'accepted'});assert.equal(s.head.children.filter(x=>x.src).length,0,path);assert.equal(s.events().length,0,path);
}
for(const query of['?email=private%40example.invalid','?flow=private','?gclid=unsafe%40value','?gclid=abcdefgh&fbclid=abcdefgh','?utm_campaign=private%40example.invalid']){
 const s=scenario({choice:'accepted',query});assert.equal(s.head.children.filter(x=>x.src).length,0,query);assert.equal(s.meta.length,0,query);
}
const rewrittenPrivate=scenario({choice:'accepted',initialURL:'https://mrsewingfashion.com/?email=private%40example.invalid'});assert.equal(rewrittenPrivate.events().length,0);assert.equal(rewrittenPrivate.meta.length,0);
const google=scenario({choice:'accepted',query:'?gclid=SyntheticGoogleClick&utm_source=google&utm_campaign=synthetic-release'});
assert.equal(google.location.search,'?gclid=SyntheticGoogleClick');assert.equal(google.head.children.filter(x=>x.src).length,1);assert.equal(google.meta.length,0);
const captured=JSON.parse(google.session.get('mrsewing:measurement-attribution:v1'));assert.equal(captured.values.gclid,'SyntheticGoogleClick');assert.equal(captured.values.utm_campaign,'synthetic-release');assert(!JSON.stringify(google.events()).includes('SyntheticGoogleClick'));
const facebook=scenario({choice:'accepted',query:'?fbclid=SyntheticFacebookClick&utm_source=facebook'});assert.equal(facebook.head.children.filter(x=>x.src).length,0);assert(facebook.meta.some(x=>x.eventName==='page_view'));
const filtered=scenario({choice:'accepted',path:'/collections/',query:'?gender=men'});assert.equal(filtered.head.children.filter(x=>x.src).length,1);const fromFilter=scenario({choice:'accepted',path:'/collections/designs/ms-031/',referrer:'https://mrsewingfashion.com/collections/?gender=women'});assert.equal(fromFilter.head.children.filter(x=>x.src).length,1);
const unsafeRef=scenario({choice:'accepted',referrer:'https://mrsewingfashion.com/request/?email=private'});assert.equal(unsafeRef.events().length,0);assert.equal(unsafeRef.meta.length,0);
const privatePage=scenario({choice:'accepted',path:'/request/'});privatePage.event('mrsewing:enquiry-accepted',{eventId:'synthetic-pending',kind:'quotation',service:'custom-tailoring',outcome:'provider_accepted'});assert.equal(privatePage.events().length,0);const queued=JSON.parse(privatePage.session.get('mrsewing:measurement-pending:v1'));assert.equal(queued.length,1);
const recovered=scenario({choice:'accepted',session:Object.fromEntries(privatePage.session)});assert.equal(recovered.events().filter(x=>x.event==='quote_request_success').length,1);assert(!recovered.session.has('mrsewing:measurement-pending:v1'));
const stale=JSON.parse(JSON.stringify(queued));stale[0].time=Date.now()-1800001;const expired=scenario({choice:'accepted',session:{'mrsewing:measurement-pending:v1':JSON.stringify(stale)}});assert.equal(expired.events().filter(x=>x.event==='quote_request_success').length,0);
const contacts=scenario({choice:'accepted'});contacts.click('tel:+250787411501');contacts.click('tel:+250000000000');contacts.click(config.contact.directionsURLs[0]);contacts.click('https://maps.app.goo.gl/unapproved');assert.equal(contacts.events().filter(x=>x.event==='website_call_click').length,1);assert.equal(contacts.events().filter(x=>x.event==='directions_click').length,1);
const wa=scenario({choice:'accepted'});wa.event('mrsewing:whatsapp-click',{eventId:'synthetic-wa',interaction:'whatsapp_contact_click',text:'NEVER'});assert.equal(wa.events().filter(x=>x.event==='whatsapp_contact_click').length,1);assert(!JSON.stringify(wa.events()).includes('NEVER'));
const withdrawal=scenario({choice:'accepted'});withdrawal.window.MrCustomerTracking.signal({eventName:'page_view',eventId:'synthetic-before'});withdrawal.nodes.find(x=>x.textContent==='Cookie preferences').listeners.click();withdrawal.choose('Reject');const before=withdrawal.events().length;withdrawal.event('mrsewing:whatsapp-click',{eventId:'synthetic-after'});assert.equal(withdrawal.events().length,before);assert.equal(withdrawal.location.reloads,1);assert.equal(withdrawal.session.size,0);
const denied=scenario({storageDenied:true});denied.choose('Reject');assert.equal(denied.events().length,0);
const identity=opted.window.MrCustomerTracking;vm.runInNewContext(source,opted.context);assert.equal(identity,opted.window.MrCustomerTracking);
console.log('PASS unified tracking: fresh consent/defaultdeny/withdrawal, exact GTM bootstrap once, staging/unsafe URL/referrer/forms suppression, campaign TTL storage and clean URL, success-only mutually exclusive primary/dedupe, approved contact clicks, pending-safe-page queue/expiry, no PII/values/enhanced data. Synthetic SDK intent only; actual accounts/receipt NOT TESTED.');
