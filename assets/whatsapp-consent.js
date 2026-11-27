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
   window.MrEnquiryMeasurement?.whatsappClick(e);
   e.preventDefault();e.stopImmediatePropagation();
   if(e.ctrlKey||e.metaKey||e.shiftKey||a.target==='_blank')window.open(url,'_blank','noopener');
   else location.assign(url);
 },true);
 if(location.pathname.replace(/\/+$/,'')==='/whatsapp'){const url=destination(location.href);if(url)location.replace(url);}
})();
