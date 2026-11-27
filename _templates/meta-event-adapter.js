/* Existing Meta dataset adapter. Unified consent and safe-context decisions
 * belong to customer-tracking.js. No advanced matching, CAPI, value or Purchase.
 * Queuing an SDK call does not establish platform receipt. */
(()=>{'use strict';
 const config=/*meta-event-config*/null;
 if(!config||config.productionEnabled!==true||!/^\d{5,30}$/.test(String(config.pixelId||'')))return;
 if(window.__mrMetaEventAdapter)return;
 const state={initialized:false,granted:false,blockedExistingPixel:false,scriptFailed:false};
 window.__mrMetaEventAdapter=state;
 const seen=new Set(),pixelId=String(config.pixelId);
 const services=new Set(['custom-tailoring','alterations','garment-care','mobile-fitting','vip']);
 const map={page_view:'PageView',design_view:'ViewContent',whatsapp_contact_click:'Contact',website_call_click:'Contact',quote_request_success:'Lead',lead_form_success:'Lead'};
 function eligible(){
  try{
   return window.top===window&&['mrsewingfashion.com','www.mrsewingfashion.com'].includes(location.hostname.toLowerCase())&&
    window.MrCustomerTracking?.consentGranted()===true&&window.MrCustomerTracking?.canTrack('meta')===true;
  }catch{return false;}
 }
 function initialize(){
  if(!eligible())return false;
  if(state.initialized){
   if(!state.granted){window.fbq('consent','grant');state.granted=true;}
   return true;
  }
  // An unknown account/container Pixel must be audited instead of initialized
  // again. The site retires its legacy loader when this adapter is installed.
  if(window.fbq||window._fbq){state.blockedExistingPixel=true;return false;}
  const fbq=function(){if(fbq.callMethod)fbq.callMethod.apply(fbq,arguments);else fbq.queue.push(arguments);};
  fbq.push=fbq;fbq.loaded=true;fbq.version='2.0';fbq.queue=[];
  window.fbq=fbq;if(!window._fbq)window._fbq=fbq;
  const script=document.createElement('script');script.async=true;script.src='https://connect.facebook.net/en_US/fbevents.js';
  script.onerror=()=>{state.scriptFailed=true;};
  // Disable Meta automatic event configuration before initialization. No
  // customer matching object or enhanced matching data is supplied to init.
  fbq('set','autoConfig',false,pixelId);
  fbq('consent','grant');
  fbq('init',pixelId);
  state.initialized=true;state.granted=true;
  try{document.head.appendChild(script);}catch{state.scriptFailed=true;return false;}
  return true;
 }
 window.addEventListener('mrsewing:tracking-consent',event=>{
  try{
   if(event.detail?.granted===false){
    if(state.initialized&&state.granted){window.fbq('consent','revoke');state.granted=false;}
    return;
   }
   if(event.detail?.granted===true)initialize();
  }catch{} // Advertising must never break a form or contact action.
 });
 window.addEventListener('mrsewing:customer-event',event=>{
  try{
   const value=event.detail;
   if(!value||typeof value!=='object'||!Object.hasOwn(map,value.eventName)||
      typeof value.eventId!=='string'||!/^[A-Za-z0-9._:-]{1,128}$/.test(value.eventId)||!eligible())return;
   const name=map[value.eventName],key=name+'|'+value.eventId;
   if(seen.has(key)||!initialize())return;
   const parameters={};
   if(name==='Contact')parameters.intent_channel=value.eventName==='whatsapp_contact_click'?'whatsapp':'telephone';
   if(name==='ViewContent')parameters.content_category='garment_design';
   if(name==='Lead'&&services.has(value.service))parameters.content_category=value.service;
   // Both quotation/general-lead inputs map to Lead and share this dedupe key;
   // root also chooses exactly one primary submission event.
   seen.add(key);
   window.fbq('track',name,parameters,{eventID:value.eventId});
  }catch{}
 });
})();
