/* One consented measurement controller. GTM is the only Google transport.
 * No contact/form text, measurements, photos, money or arbitrary URLs in events. */
(()=>{'use strict';
 if(window.MrCustomerTracking)return;
 const config={"externalEventsEnabled":true,"attribution":{"storage":"per-tab sessionStorage only after fresh measurement consent","ttlMs":86400000,"pendingEventTtlMs":1800000,"keys":["gclid","gbraid","wbraid","fbclid","utm_source","utm_medium","utm_campaign","utm_content","utm_term"]},"contact":{"telephone":"+250787411501","email":"mrsewingfashiondesigner@gmail.com","directionsURLs":["https://maps.app.goo.gl/qz1GzkBunkmzVKXQ6?g_st=ac"]},"publicReferrerPaths":["/","/about/","/collections/","/collections/designs/ivory-elegance-shawl-tuxedo-black-tie/","/collections/designs/midnight-black-double-breasted-gold/","/collections/designs/ms-005/","/collections/designs/ms-006/","/collections/designs/ms-029/","/collections/designs/ms-030/","/collections/designs/ms-031/","/collections/designs/ms-032/","/collections/designs/ms-033/","/collections/designs/ms-034/","/collections/designs/ms-035/","/collections/designs/ms-036/","/collections/designs/ms-069/","/collections/designs/ms-083/","/collections/designs/ms-096/","/collections/designs/ms-117/","/collections/designs/ms-139/","/collections/designs/ms-140/","/collections/designs/ms-141/","/collections/designs/ms-142/","/collections/designs/ms-143/","/collections/designs/ms-144/","/collections/designs/ms-145/","/collections/designs/ms-146/","/collections/designs/rose-elegance-suit/","/collections/designs/royal-blue-executive-womens-three-piece/","/collections/designs/sky-blue-elegance-suit/","/contact/","/faq/","/guides/fabrics/","/loyalty-program/","/measurements/","/mensuits/","/mensuits/double-breasted/","/mensuits/kaunda/","/mensuits/single-breasted/","/mensuits/three-piece/","/mensuits/tuxedos-formalwear/","/our-work/","/our-work/blue-jacket-black-trousers/","/our-work/cobalt-blue-suit/","/our-work/light-grey-and-navy/","/our-work/off-white-graduation-suit/","/our-work/soft-ivory-tailoring/","/referral-program/","/services/alterations/","/services/custom-tailoring/","/services/garment-care/","/services/mobile-fitting/","/services/vip/","/womensuits/","/womensuits/double-breasted/","/womensuits/single-breasted/","/womensuits/skirt-suits/","/womensuits/three-piece/"],"gtm":{"containerId":"GTM-WHR49M4D","productionEnabled":true},"googleAds":{"enabled":true},"conversions":[{"event":"whatsapp_contact_click","enabled":true},{"event":"website_call_click","enabled":true},{"event":"appointment_confirmed","enabled":false},{"event":"directions_click","enabled":true},{"event":"quote_request_success","enabled":true},{"event":"lead_form_success","enabled":true}]};
 if(!config)return;
 const official=()=>['mrsewingfashion.com','www.mrsewingfashion.com'].includes(location.hostname.toLowerCase());
 const topLevel=window.top===window;
 const consentKey='mrsewing:measurement-consent:v2',attrKey='mrsewing:measurement-attribution:v1',pendingKey='mrsewing:measurement-pending:v1';
 const allowedServices=new Set(['custom-tailoring','alterations','garment-care','mobile-fitting','vip','shop']);
 const known=new Set(['page_view','service_view','design_view','design_selection','fabric_selection','request_started','request_step_completed','request_submission_failed','email_contact_click',...config.conversions.filter(c=>c.enabled).map(c=>c.event)]);
 const ttl=config.attribution.ttlMs,pendingTtl=config.attribution.pendingEventTtlMs;
 let initialURL=location.href;try{initialURL=performance.getEntriesByType('navigation')[0]?.name||initialURL;}catch{}
 function initialContextSafe(vendor){try{const u=new URL(initialURL);if(u.hash)return false;for(const[k,v]of [...u.searchParams]){if(k.startsWith('utm_')){if(!config.attribution.keys.includes(k)||!campaignValue(k,v))return false;u.searchParams.delete(k);}}return safeURL(u.href,vendor);}catch{return false;}}
 const received=new Set(),sentGoogle=new Set(),sentMeta=new Set(),pageIds={};
 let localStore,sessionStore;try{localStore=window.localStorage;}catch{}try{sessionStore=window.sessionStorage;}catch{}
 let memoryChoice=null,gtmStarted=false,banner=null,firstPageId=null;
 const uid=()=>{try{return crypto.randomUUID();}catch{return null;}};
 const store=(storage,key,value)=>{try{storage.setItem(key,JSON.stringify(value));return true;}catch{return false;}};
 const read=(storage,key)=>{try{return JSON.parse(storage.getItem(key)||'null');}catch{return null;}};
 const remove=(storage,key)=>{try{storage.removeItem(key);}catch{}};
 function consentGranted(){const c=memoryChoice||read(localStore,consentKey);return c?.version===2&&c.choice==='accepted';}
 function campaignValue(key,value){
  if(typeof value!=='string'||!value)return false;
  if(/clid$|^gbraid$|^wbraid$/.test(key))return /^[A-Za-z0-9_-]{5,256}$/.test(value);
  return /^[A-Za-z0-9_. -]{1,80}$/.test(value)&&!/\d{7,}|@|https?:|[<>]/i.test(value);
 }
 function privateDocument(){
  const route=location.pathname.toLowerCase().replace(/\.html$/,'/');
  if(/^\/(?:request|booking(?:-[a-z-]+)?|privacy-policy|terms-and-conditions|refund-policy|customer-support|measurement-submission|referral-program|staff|whatsapp|shop)(?:\/|$)/.test(route)||
     /\/(?:selected-designs|fabric|measurements)(?:\/|$)/.test(route)||
     /^\/services\/(?:custom-tailoring\/(?:special-order|standard-order|design-choice)|vip\/subscription)(?:\/|$)/.test(route))return true;
  try{return !!document.querySelector('#customerRequestForm,#submissionForm,#bookingForm,form[data-commerce-form],form[data-shop-whatsapp-form],form[data-request-form],form[data-quotation-form]');}catch{return true;}
 }
 function safeURL(raw,vendor){
  try{
   const u=new URL(raw,location.href);if(u.hash)return false;
   const keys=vendor==='google'?new Set(['gclid','gbraid','wbraid']):new Set(['fbclid']);
   for(const[k,v]of u.searchParams){if(k==='gender'&&['men','women','all'].includes(v))continue;if(!keys.has(k)||!campaignValue(k,v))return false;}
   return true;
  }catch{return false;}
 }
 function canTrack(vendor){
  if(!topLevel||!official()||!consentGranted()||privateDocument()||!initialContextSafe(vendor)||!safeURL(location.href,vendor))return false;
  // SDKs can read referrers independently; never rely only on custom URL fields.
  if(document.referrer){
   try{const r=new URL(document.referrer);if(r.hash)return false;
    if(r.origin===location.origin){if(!config.publicReferrerPaths.includes(r.pathname))return false;for(const[k,v]of r.searchParams)if(k!=='gender'||!['men','women','all'].includes(v))return false;}
    else if(r.pathname!=='/'||r.search)return false;
   }catch{return false;}
  }
  return true;
 }
 function captureAttribution(){
  if(!topLevel||!official()||!consentGranted())return;
  const previous=read(sessionStore,attrKey);
  let values=previous&&previous.time<=Date.now()&&Date.now()-previous.time<ttl?previous.values:{};
  if(!values||typeof values!=='object')values={};
  values=Object.fromEntries(Object.entries(values).filter(([k,v])=>config.attribution.keys.includes(k)&&campaignValue(k,v)));
  const url=new URL(location.href);let changed=false;
  for(const key of config.attribution.keys){
   const value=url.searchParams.get(key);if(value&&campaignValue(key,value))values[key]=value;
   // Campaign labels can contain customer-supplied words; keep them off SDK URLs.
   if(key.startsWith('utm_')&&url.searchParams.has(key)&&!privateDocument()){url.searchParams.delete(key);changed=true;}
  }
  if(Object.keys(values).length)store(sessionStore,attrKey,{time:previous?.time&&Date.now()-previous.time<ttl?previous.time:Date.now(),values});
  else remove(sessionStore,attrKey);
  if(changed)try{history.replaceState(history.state,'',url.pathname+url.search+url.hash);}catch{}
 }
 function command(){window.dataLayer=window.dataLayer||[];window.dataLayer.push(arguments);}
 function consentCommand(granted){granted=granted&&official();command('consent','update',{ad_storage:granted?'granted':'denied',ad_user_data:granted?'granted':'denied',ad_personalization:'denied',analytics_storage:'denied'});}
 function startGoogle(){
  if(gtmStarted||!canTrack('google')||!config.gtm.productionEnabled)return;
  gtmStarted=true;window.dataLayer=window.dataLayer||[];
  window.dataLayer.push({'gtm.start':Date.now(),event:'gtm.js'});
  const script=document.createElement('script');script.async=true;script.src='https://www.googletagmanager.com/gtm.js?id='+encodeURIComponent(config.gtm.containerId);
  script.referrerPolicy='no-referrer';document.head.appendChild(script);
  window.dataLayer.push({event:'mr_measurement_ready',mr_measurement_allowed:true,mr_consent_google:true});
 }
 function minimal(raw){
  if(!raw||!known.has(raw.eventName)||typeof raw.eventId!=='string'||!/^[A-Za-z0-9-]{5,80}$/.test(raw.eventId))return null;
  const value={eventName:raw.eventName,eventId:raw.eventId};
  if(allowedServices.has(raw.service))value.service=raw.service;
  if(['quotation','consultation','product'].includes(raw.kind))value.kind=raw.kind;
  if(['choose','advice','own'].includes(raw.fabricPreference))value.fabricPreference=raw.fabricPreference;
  if(Number.isInteger(raw.step)&&raw.step>=1&&raw.step<=6)value.step=raw.step;
  return value;
 }
 function deliver(value){
  const key=value.eventName+':'+value.eventId;let sent=false;
  if(config.gtm.productionEnabled&&config.googleAds.enabled&&canTrack('google')&&!sentGoogle.has(key)){
   startGoogle();sentGoogle.add(key);
   window.dataLayer.push({event:value.eventName,event_id:value.eventId,mr_measurement_allowed:true,mr_consent_google:true,
    ...(value.service?{service:value.service}:{}),...(value.kind?{request_kind:value.kind}:{}),
    ...(value.fabricPreference?{fabric_preference:value.fabricPreference}:{}),...(value.step?{request_step:value.step}:{})});
   sent=true;
  }
  if(canTrack('meta')&&!sentMeta.has(key)){
   sentMeta.add(key);window.dispatchEvent(new CustomEvent('mrsewing:customer-event',{detail:Object.freeze(value)}));sent=true;
  }
  return sent;
 }
 function flush(){
  const queue=read(sessionStore,pendingKey);remove(sessionStore,pendingKey);
  if(!Array.isArray(queue)||!consentGranted())return;
  const remaining=[];
  for(const row of queue){
   if(!row||row.time>Date.now()||Date.now()-row.time>pendingTtl)continue;
   const value=minimal(row.value);if(value&&!deliver(value))remaining.push({time:row.time,value});
  }
  if(remaining.length)store(sessionStore,pendingKey,remaining.slice(-30));
 }
 function signal(raw){
  const value=minimal(raw);if(!value||!consentGranted()||!official()||!topLevel)return false;
  const key=value.eventName+':'+value.eventId;if(received.has(key))return false;received.add(key);
  if(!deliver(value)&&['quote_request_success','lead_form_success','whatsapp_contact_click','website_call_click','directions_click'].includes(value.eventName)){
   const old=read(sessionStore,pendingKey),queue=Array.isArray(old)?old.filter(x=>x&&x.time<=Date.now()&&Date.now()-x.time<pendingTtl):[];
   queue.push({time:Date.now(),value});store(sessionStore,pendingKey,queue.slice(-30));
  }
  return true;
 }
 function relay(raw){
  try{const target=window.top.location.origin===location.origin?window.top:window;target.dispatchEvent(new target.CustomEvent('mrsewing:measurement-input',{detail:raw}));}catch{}
 }
 function interaction(eventName,event){
  if(event?.__mrContactMeasured)return;if(event)event.__mrContactMeasured=true;
  const eventId=uid();if(eventId)relay({eventName,eventId});
 }
 // One delegate for real calls, approved directions and email; WA uses its existing helper.
 document.addEventListener('click',event=>{
  const a=event.target.closest?.('a[href]');if(!a||a.getAttribute('aria-disabled')==='true')return;
  let u;try{u=new URL(a.href,location.href);}catch{return;}
  if(u.protocol==='tel:'&&u.pathname.replace(/\D/g,'')===config.contact.telephone.replace(/\D/g,''))interaction('website_call_click',event);
  else if(u.protocol==='mailto:'&&u.pathname.toLowerCase()===config.contact.email.toLowerCase())interaction('email_contact_click',event);
  else if(config.contact.directionsURLs.includes(u.href))interaction('directions_click',event);
 },true);
 window.MrCustomerTracking=Object.freeze({consentGranted,canTrack,externalTracking:official(),signal});
 function localSignals(){
  document.addEventListener('mrsewing:designselected',()=>relay({eventName:'design_selection',eventId:uid()}));
  document.addEventListener('mrsewing:fabricpreference',e=>relay({eventName:'fabric_selection',eventId:uid(),fabricPreference:e.detail?.choice==='now'?'choose':e.detail?.choice}));
  if(document.getElementById('customerRequestForm'))relay({eventName:'request_started',eventId:uid()});
 }
 if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',localSignals,{once:true});else localSignals();
 if(!topLevel)return; // Embedded enquiry documents never load vendor tags or their own banner.
 window.addEventListener('mrsewing:measurement-input',e=>signal(e.detail));
 window.addEventListener('mrsewing:whatsapp-click',e=>signal({eventName:'whatsapp_contact_click',eventId:e.detail?.eventId}));
 window.addEventListener('mrsewing:enquiry-accepted',e=>{
  const d=e.detail;if(d?.outcome!=='provider_accepted'||!['quotation','consultation','product'].includes(d.kind)||!allowedServices.has(d.service))return;
  signal({eventName:d.kind==='quotation'&&d.service==='custom-tailoring'?'quote_request_success':'lead_form_success',eventId:d.eventId,service:d.service,kind:d.kind});
 });
 function pageEvents(){
  if(!firstPageId)firstPageId=uid();if(firstPageId)signal({eventName:'page_view',eventId:firstPageId});
  const service=location.pathname.match(/^\/services\/(custom-tailoring|alterations|garment-care|mobile-fitting|vip)\/$/)?.[1];
  if(service)signal({eventName:'service_view',eventId:pageIds.service||(pageIds.service=uid()),service});
  if(/^\/collections\/designs\/[a-z0-9-]+\/$/.test(location.pathname)&&document.querySelector('[data-select-design]'))signal({eventName:'design_view',eventId:pageIds.design||(pageIds.design=uid())});
 }
 function close(){banner?.remove();banner=null;}
 function choose(choice){
  const was=consentGranted();memoryChoice={version:2,choice};const persisted=store(localStore,consentKey,memoryChoice);if(!persisted&&choice==='declined')remove(localStore,consentKey);close();
  consentCommand(choice==='accepted');
  window.dispatchEvent(new CustomEvent('mrsewing:tracking-consent',{detail:{granted:choice==='accepted'}}));
  if(choice==='accepted'){captureAttribution();startGoogle();pageEvents();flush();}
  else{remove(sessionStore,attrKey);remove(sessionStore,pendingKey);if(was&&(persisted||read(localStore,consentKey)?.choice!=='accepted'))location.reload();}
 }
 function openPreferences(){
  close();banner=document.createElement('section');banner.className='mr-tracking-consent';banner.setAttribute('role','region');banner.setAttribute('aria-label','Advertising cookie preferences');
  const title=document.createElement('h2');title.textContent='Your Privacy Choices';
  const p=document.createElement('p');p.textContent='Allow optional Google and Meta advertising measurement? Your choice does not affect our services. ';
  const link=document.createElement('a');link.href='/privacy-policy/';link.textContent='Privacy Policy';p.append(link);
  const controls=document.createElement('div');controls.className='mr-tracking-controls';
  for(const[label,value]of[['Reject','declined'],['Allow Measurement','accepted']]){
   const button=document.createElement('button');button.type='button';button.textContent=label;button.addEventListener('click',()=>choose(value));controls.append(button);
  }
  banner.append(title,p,controls);document.body.append(banner);
 }
 function ready(){
  const preview=location.hostname.endsWith('.pages.dev')&&new URLSearchParams(location.search).get('tracking_preview')==='1';
  const stage=location.hostname==='mrsewing-staging.pages.dev'||location.hostname.endsWith('.mrsewing-staging.pages.dev');
  if(official()||preview||stage){
   const manage=document.createElement('button');manage.type='button';manage.className='mr-cookie-manage';manage.textContent='Cookie preferences';manage.addEventListener('click',openPreferences);
   (document.querySelector('#site-footer,footer,.homepage-footer')||document.body).append(manage);
   if(!read(localStore,consentKey)&&!privateDocument()&&(official()||preview))openPreferences();
  }
  captureAttribution();
  if(consentGranted()){consentCommand(true);window.dispatchEvent(new CustomEvent('mrsewing:tracking-consent',{detail:{granted:true}}));startGoogle();pageEvents();flush();}
 }
 command('consent','default',{ad_storage:'denied',ad_user_data:'denied',ad_personalization:'denied',analytics_storage:'denied'});
 command('set','allow_enhanced_conversions',false);command('set','allow_ad_personalization_signals',false);command('set','ads_data_redaction',true);
 if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',ready,{once:true});else ready();
})();
