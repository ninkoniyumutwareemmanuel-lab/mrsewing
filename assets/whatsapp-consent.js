/* Open official WhatsApp chat directly; no Terms popup or checkbox gate. */
(()=>{'use strict';
 const official='https://wa.me/250787411501';
 function destination(raw){try{
   const u=new URL(raw,location.href);
   const sameSite=u.origin===location.origin&&u.pathname.replace(/\/+$/,'')==='/whatsapp';
   const direct=u.origin==='https://wa.me'&&u.pathname.replace(/\/+$/,'')==='/250787411501';
   if(!sameSite&&!direct)return null;
   const dest=new URL(official),text=u.searchParams.get('text');if(text)dest.searchParams.set('text',text.slice(0,6000));
   return dest.href;
 }catch(_){return null;}}
 document.addEventListener('click',e=>{
   const a=e.target.closest?.('a[href]');if(!a||a.getAttribute('aria-disabled')==='true')return;
   const url=destination(a.href);if(!url)return;
   e.preventDefault();e.stopImmediatePropagation();
   if(e.ctrlKey||e.metaKey||e.shiftKey||a.target==='_blank'){
     window.MrEnquiryMeasurement?.whatsappClick(e);
     window.open(url,'_blank','noopener');
     return;
   }
   // Preserve same-tab handoff; wait briefly only for consented, eligible Google measurement.
   // An independent fallback keeps WhatsApp usable if GTM is slow, blocked or unavailable.
   const measurement=window.MrEnquiryMeasurement;
   if(!measurement||!window.MrCustomerTracking?.canTrack('google')){
     measurement?.whatsappClick(e);
     location.assign(url);
     return;
   }
   let done=false,timer;
   const navigate=()=>{if(done)return;done=true;clearTimeout(timer);location.assign(url);};
   timer=setTimeout(navigate,500);
   try{if(!measurement.whatsappClick(e,navigate))navigate();}catch(_){navigate();}
 },true);
 if(location.pathname.replace(/\/+$/,'')==='/whatsapp'){const url=destination(location.href);if(url)location.replace(url);}
})();
