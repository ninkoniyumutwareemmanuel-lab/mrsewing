/* Explicit per-visit acceptance. This does not record contractual acceptance or send a message. */
(()=>{'use strict';
 const official='https://wa.me/250787411501';
 function gate(raw){try{const u=new URL(raw,location.href);if(u.origin==='https://wa.me'&&u.pathname.replace(/\/$/,'')==='/250787411501'){const q=new URLSearchParams();const text=u.searchParams.get('text');if(text)q.set('text',text.slice(0,6000));return '/whatsapp/'+(q.size?'?'+q:'');}}catch(_){}return null;}
 document.addEventListener('click',e=>{const a=e.target.closest?.('a[href]');if(!a||a.getAttribute('aria-disabled')==='true')return;const url=gate(a.href);if(!url)return;e.preventDefault();e.stopImmediatePropagation();if(e.ctrlKey||e.metaKey||a.target==='_blank')window.open(url,'_blank','noopener');else location.assign(url);},true);
 const form=document.getElementById('whatsappConsentForm');if(!form)return;
 const checkbox=document.getElementById('whatsappTerms'),button=document.getElementById('continueWhatsApp');
 function reset(){checkbox.checked=false;button.disabled=true;}reset();addEventListener('pageshow',reset);
 checkbox.addEventListener('change',()=>{button.disabled=!checkbox.checked;});
 form.addEventListener('submit',e=>{e.preventDefault();if(!checkbox.checked||!form.reportValidity())return;const text=new URLSearchParams(location.search).get('text');const u=new URL(official);if(text)u.searchParams.set('text',text.slice(0,6000));location.assign(u.href);});
})();
