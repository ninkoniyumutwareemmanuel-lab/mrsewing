/* WhatsApp chat opens directly; Terms are accessible in the site footer. */
(()=>{'use strict';let photo,opener;
function dialog(id,title){const d=document.createElement('dialog');d.id=id;d.className='customer-dialog';d.setAttribute('aria-labelledby',id+'-title');d.innerHTML='<button type="button" class="dialog-close" aria-label="Close dialog">Close</button><h2 id="'+id+'-title">'+title+'</h2>';d.querySelector('button').addEventListener('click',()=>d.close());d.addEventListener('close',()=>{opener?.focus({preventScroll:true});});document.body.append(d);return d;}
function openWhatsApp(text){const u=new URL('https://wa.me/250787411501');if(text)u.searchParams.set('text',String(text).slice(0,6000));window.open(u.href,'_blank','noopener');}
window.MrSewingWhatsApp={open:openWhatsApp};
/* Existing footer Policies menu remains the sole footer Terms navigation. */
document.addEventListener('click',e=>{
 const link=e.target.closest?.('[data-enlarge]');if(!link)return;const u=new URL(link.href,location.href);
 if(u.origin!==location.origin||!/^https?:$/.test(u.protocol))return;
 e.preventDefault();if(!photo){photo=dialog('measurementPhotoDialog','Measurement illustration');photo.append(document.createElement('img'));}
 opener=link;const img=photo.querySelector('img');img.src=u.href;img.alt=link.querySelector('img').alt;
 photo.querySelector('h2').textContent=link.getAttribute('aria-label').replace(/^Enlarge /,'');photo.showModal();photo.querySelector('button').focus();
},true);
})();

/* Optional Meta Pixel integration. Owner authorised placement on main.
   The owner-approved production flag and visitor consent system remain unchanged. */
(function () {
  "use strict";
  var config = /*meta-pixel-config*/null;
  if (!config || !config.productionEnabled || config.status !== "owner-approved-production") return;
  if (window.__mrSewingMetaPixelLoader) return;
  window.__mrSewingMetaPixelLoader = true;
  var tag = document.createElement("script");
  tag.src = "/assets/meta-pixel.js?v=compact-20261121";
  tag.async = true;
  tag.setAttribute("data-mr-meta-pixel", "");
  tag.dataset.pixelId = String(config.pixelId);
  tag.dataset.productionEnabled = "true";
  document.head.appendChild(tag);
})();

/* Until activation, consent links use the currently effective HTML Terms. */
(()=>{'use strict';const fix=()=>document.querySelectorAll('form a[href="/terms-and-conditions/"],[data-terms-consent] a[href="/terms-and-conditions/"]').forEach(a=>{a.href='/terms-and-conditions/current/';});if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',fix,{once:true});else fix();})();

/* R65: keep the original quotation and consultation request pages/logic,
   but show their form areas in same-origin native-dialog iframe pop-ups.
   Direct links still work when JavaScript is disabled. */
(()=>{'use strict';
 if(window.self!==window.top)return; // Never nest a popup inside the form iframe.
 let popup,frame,closeButton,titleNode,loadingNode,opener;
 const supported=path=>path==='/booking/'||path==='/booking.html'||path==='/request/'||path==='/request.html'||/^\/request\/[^/]+\/$/.test(path);
 const kind=path=>path.startsWith('/booking')?'consultation':'quotation';
 const isRequestForm=path=>path.startsWith('/request/')||path==='/request.html'||path.startsWith('/booking/');
 const frameStyle=`
 html{scroll-behavior:auto!important;scroll-padding-top:0!important}
 body{margin:0!important;padding:0!important;min-height:0!important;overflow:auto!important}
 body>#site-header,#site-header,body>.homepage-header,body>footer,body>#site-footer,
 body>.skip-link,.customer-breadcrumb,.release-intro,.request-progress{display:none!important}
 #main-content{padding:0!important;margin:0!important;min-height:0!important}
 #main-content>.home-shell.release-main{max-width:100%!important;width:100%!important;margin:0!important;padding:12px 13px 28px!important}
 #main-content .release-section{max-width:none!important;margin:0!important;padding:clamp(14px,3vw,26px)!important}
 #main-content .release-section:first-of-type{margin-top:0!important}
 #main-content h2#request-title{margin-top:0!important}
 @media(max-width:599px){#main-content>.home-shell.release-main{padding:8px 7px 20px!important}
 #main-content .release-section{padding:13px!important}}
 `;
 function makeDialog(){
   popup=document.createElement('dialog');
   popup.id='mrCustomerFormPopup';popup.className='mr-customer-form-popup';
   popup.setAttribute('aria-labelledby','mrCustomerPopupTitle');
   const header=document.createElement('div');header.className='mr-customer-popup-header';
   titleNode=document.createElement('h2');titleNode.id='mrCustomerPopupTitle';
   closeButton=document.createElement('button');closeButton.type='button';
   closeButton.className='mr-customer-popup-close';closeButton.textContent='×';closeButton.setAttribute('aria-label','Close form');
   header.append(titleNode,closeButton);
   const body=document.createElement('div');body.className='mr-customer-popup-body';
   loadingNode=document.createElement('p');loadingNode.className='mr-customer-popup-loading';loadingNode.setAttribute('role','status');
   loadingNode.textContent='Opening your form…';
   frame=document.createElement('iframe');frame.id='mrCustomerFormFrame';
   frame.title='Mr Sewing Fashion request form';frame.setAttribute('referrerpolicy','same-origin');
   frame.setAttribute('loading','eager');frame.style.visibility='hidden';
   body.append(loadingNode,frame);popup.append(header,body);
   closeButton.addEventListener('click',()=>popup.close());
   popup.addEventListener('close',()=>{
     if(opener?.isConnected)opener.focus({preventScroll:true});
   });
   frame.addEventListener('load',()=>{
     if(!popup.open)return;
     try{
       const doc=frame.contentDocument,win=frame.contentWindow;
       if(!doc||!win||win.location.origin!==location.origin||!isRequestForm(win.location.pathname))throw Error('Unrelated page');
       const form=doc.getElementById('customerRequestForm');
       if(!form)throw Error('Request form not found');
       doc.getElementById('mrEmbeddedFormStyles')?.remove();
       const style=doc.createElement('style');style.id='mrEmbeddedFormStyles';style.textContent=frameStyle;
       doc.head.appendChild(style);
       doc.querySelectorAll('a[href]').forEach(link=>{
         const u=new URL(link.href,win.location.href);
         // Policy, design-gallery and other navigation open outside the popup.
         if(u.origin!==location.origin||!isRequestForm(u.pathname)){
           link.target='_blank';link.rel='noopener noreferrer';
         }
       });
       doc.addEventListener('keydown',event=>{
         if(event.key==='Escape'){
           event.preventDefault();event.stopImmediatePropagation();popup.close();
         }
       },true);
       const actualKind=form.dataset.kind||kind(win.location.pathname);
       titleNode.textContent=actualKind==='consultation'?'Book a Consultation':actualKind==='quotation'?'Request a Quotation':actualKind==='subscription'?'Subscription Enquiry':'Service Enquiry';
       frame.title=titleNode.textContent+' — existing Mr Sewing Fashion form';
       loadingNode.hidden=true;frame.style.visibility='visible';
     }catch(_){
       loadingNode.textContent='This form could not open in the pop-up. Use its regular page instead.';
       loadingNode.hidden=false;frame.style.visibility='hidden';
       if(!loadingNode.querySelector('a')){
         const a=document.createElement('a');a.href=frame.src;a.textContent='Open form page';a.style.marginLeft='8px';loadingNode.append(a);
       }
     }
   });
   document.body.append(popup);
 }
 function open(link,url){
   if(!popup)makeDialog();
   opener=link;
   titleNode.textContent=kind(url.pathname)==='consultation'?'Book a Consultation':'Request a Quotation';
   loadingNode.textContent='Opening your form…';loadingNode.hidden=false;
   frame.style.visibility='hidden';
   const src=new URL(url.href);src.searchParams.set('popup','1');
   frame.src=src.pathname+src.search+src.hash;
   if(!popup.open)popup.showModal();
   closeButton.focus({preventScroll:true});
 }
 document.addEventListener('click',event=>{
   if(event.defaultPrevented||event.button!==0||event.ctrlKey||event.metaKey||event.altKey||event.shiftKey)return;
   const link=event.target.closest?.('a[href]');
   if(!link||link.hasAttribute('download')||(link.target&&link.target!=='_self'))return;
   let url;try{url=new URL(link.href,location.href);}catch{return;}
   if(url.origin!==location.origin||!supported(url.pathname))return;
   event.preventDefault();open(link,url);
 },true);
})();
