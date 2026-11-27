/* First-party integration signals only. No network, cookies, storage, tag or
 * dataLayer transport. Google Ads/GA4/GTM activation is separately configured
 * and verified; these events alone do not establish advertising measurement. */
(()=>{'use strict';
 if(window.MrEnquiryMeasurement)return;
 const forms=new WeakMap(),clicks=new WeakSet();
 const kinds=new Set(['quotation','consultation']);
 const services=new Set(['custom-tailoring','alterations','garment-care','mobile-fitting','vip']);
 const id=()=>{try{return crypto.randomUUID();}catch{return null;}};
 function emit(name,detail){
  try{
   let target=window;
   try{if(window.top.location.origin===location.origin)target=window.top;}catch{}
   // Dispatch exactly once in the top same-origin document. Never postMessage
   // to an arbitrary parent or include form data, URLs, referrers or messages.
   target.dispatchEvent(new target.CustomEvent(name,{detail:Object.freeze(detail)}));
   return true;
  }catch{return false;} // Measurement must never break a customer action.
 }
 function providerAccepted(form,kind,service){
  if(!form||form.id!=='customerRequestForm'||!kinds.has(kind)||!services.has(service))return false;
  if(forms.has(form))return false;
  const eventId=id();if(!eventId)return false;
  forms.set(form,eventId);
  return emit('mrsewing:enquiry-accepted',{eventId,kind,service,outcome:'provider_accepted'});
 }
 function whatsappClick(event,onGoogleComplete){
  if(event&&typeof event==='object'){
   if(clicks.has(event))return false;
   clicks.add(event);
  }
  const eventId=id();if(!eventId)return false;
  return emit('mrsewing:whatsapp-click',{eventId,interaction:'whatsapp_contact_click',...(typeof onGoogleComplete==='function'?{onGoogleComplete}:{})});
 }
 function support(form,eventName,step){
  if(!form||form.id!=='customerRequestForm'||!kinds.has(form.dataset?.kind)||
    !['request_step_completed','request_submission_failed'].includes(eventName))return false;
  const eventId=id();if(!eventId)return false;
  return emit('mrsewing:measurement-input',{eventName,eventId,...(Number.isInteger(step)&&step>=1&&step<=6?{step}:{})});
 }
 function productAccepted(form,kind){
  if(!form?.matches?.('form[data-commerce-form]')||!['quote','purchase'].includes(kind)||forms.has(form))return false;
  const eventId=id();if(!eventId)return false;forms.set(form,eventId);
  return emit('mrsewing:enquiry-accepted',{eventId,kind:'product',service:'shop',outcome:'provider_accepted'});
 }
 window.MrEnquiryMeasurement=Object.freeze({providerAccepted,whatsappClick,support,productAccepted,externalTracking:false});
})();
