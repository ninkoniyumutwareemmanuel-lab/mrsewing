(function setupHomepageMenu() {
  const button = document.querySelector('.home-menu-toggle');
  const menu = document.getElementById('home-navigation');
  if (!button || !menu) return;
  function setOpen(open, restoreFocus = false) {
    button.setAttribute('aria-expanded', String(open));
    button.setAttribute('aria-label', open ? 'Close navigation' : 'Open navigation');
    menu.dataset.open = String(open);
    if (restoreFocus) button.focus();
  }
  button.addEventListener('click', () => setOpen(button.getAttribute('aria-expanded') !== 'true'));
  menu.addEventListener('click', event => {
    const link = event.target.closest('a');
    if (!link) return;
    setOpen(false);
    // In-page navigation must not leave focus inside the now-hidden dropdown.
    const url = new URL(link.href, location.href);
    if (url.pathname === location.pathname && url.hash) {
      const section = document.getElementById(decodeURIComponent(url.hash.slice(1)));
      const target = section && (section.querySelector('h1,h2') || section);
      if (target) {
        target.tabIndex = -1;
        // Let the native fragment navigation finish before placing focus.
        requestAnimationFrame(() => target.focus({ preventScroll:true }));
      }
    }
  });
  document.addEventListener('click', event => {
    if (!menu.contains(event.target) && !button.contains(event.target)) setOpen(false);
  });
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && button.getAttribute('aria-expanded') === 'true') setOpen(false, true);
  });
  // Reset on the layout breakpoint only, not while mobile browser chrome resizes.
  matchMedia('(max-width: 1099px)').addEventListener('change', () => setOpen(false));
})();

/* Contextual text requests with explicit review. No upload, payment or order backend. */
document.addEventListener('DOMContentLoaded',()=>{'use strict';const context=window.mrRequestContext;const names={'custom-tailoring':'Custom Tailoring & Suits','alterations':'Clothing Alterations & Repairs','garment-care':'Garment Care & Cleaning','mobile-fitting':'Mobile Tailoring, Styling & Event Assistance'};
for(const line of document.querySelectorAll('[data-context-line]')){const s=context?.read()||{};line.textContent=`Service Experience: ${s.experience==='vip'?'VIP Service':'Standard Service'}. Design order and priority are separate choices.`;}
const form=document.getElementById('customerRequestForm');if(!form)return;
const $=id=>document.getElementById(id),kind=form.dataset.kind,service=$('requestService'),experience=$('requestExperience'),order=$('requestOrder'),priority=$('requestPriority'),design=$('requestDesign'),after=$('requestAfterHours'),status=$('requestStatus'),review=$('requestReview'),success=$('requestSuccess'),reviewButton=$('reviewRequest'),edit=$('editRequest'),send=$('sendRequest'),choices=JSON.parse($('requestDesigns').textContent);let pending=false,fingerprint='';
const saved=context?.read()||{};if(service)service.value=names[saved.service]?saved.service:'custom-tailoring';if(experience)experience.value=saved.experience==='vip'?'vip':'standard';if(order)order.value=saved.order==='special'?'special':'standard';if(priority)priority.value=saved.priority==='express'?'express':'standard';if(design)design.value=saved.design||'';if(after)after.checked=saved.afterHours==='yes';
function update(){if(!service)return;const custom=service.value==='custom-tailoring';for(const block of document.querySelectorAll('[data-custom-only]')){block.hidden=!custom;for(const e of block.querySelectorAll('input,select'))e.disabled=!custom;}
const standard=custom&&order?.value==='standard';for(const block of document.querySelectorAll('[data-standard-design]')){block.hidden=!standard;for(const e of block.querySelectorAll('input'))e.disabled=!standard;}
for(const block of document.querySelectorAll('[data-upload-notice]'))block.hidden=!(custom&&order?.value==='special');for(const block of document.querySelectorAll('[data-measurement]')){block.hidden=service.value==='garment-care';for(const e of block.querySelectorAll('select'))e.disabled=block.hidden;}
if(experience){$('priority-guidance').textContent=experience.value==='vip'?'VIP Express and after-hours assistance is assessed within the individually agreed VIP quotation, subject to feasibility and scope. Standard-Service surcharges are not automatically applied.':priority.value==='express'&&after.checked?'For Standard Service, Express plus standard after-hours requests carry the approved combined 60% of the original quoted service price (base × 1.60), subject to confirmation.':priority.value==='express'?'For Standard Service, Express Priority adds 35% of the original quoted service price, subject to capacity and confirmation.':after.checked?'For Standard Service, work 17:00–22:00 Kigali time is subject to availability and a 25% surcharge on the original quoted service price.':'Standard Priority follows the individually agreed scheduling arrangements. Preferred dates are not confirmed completion times.';context?.update({service:service.value,experience:experience.value,order:order?.value,priority:priority.value,design:design?.value,afterHours:after.checked?'yes':'no'});const u=new URL(location.href);for(const [k,v]of Object.entries(context?.read()||{}))u.searchParams.set(k,v);history.replaceState(null,'',u.pathname+u.search+u.hash);}}
for(const e of [service,experience,order,priority,after])e?.addEventListener('change',update);update();
function valid(){const phone=$('requestPhone'),digits=phone.value.replace(/\D/g,'').length;phone.setCustomValidity(/^[0-9+\-\s().]+$/.test(phone.value.trim())&&digits>=7&&digits<=15?'':'Enter a valid phone number including your country code.');for(const e of [$('requestName'),$('requestMessage'),$('requestLocation')].filter(Boolean))e.setCustomValidity(e.value.trim()?'':'Please complete this field.');
if(!form.reportValidity())return false;if(kind==='quotation'&&service.value==='custom-tailoring'&&order.value==='standard'&&!choices[design.value]){status.textContent='Choose a published website design before reviewing a Standard Order, or choose Special Order for your own inspiration.';design.closest('div').querySelector('a').focus();return false;}return true;}
for(const e of form.querySelectorAll('input,textarea'))e.addEventListener('input',()=>e.setCustomValidity(''));
function payload(){const d=Object.fromEntries(new FormData(form));delete d.botcheck;for(const k of Object.keys(d))if(typeof d[k]==='string')d[k]=d[k].trim();if(service)d.Service=names[service.value];if(experience)d['Service Experience']=experience.value==='vip'?'VIP Service':'Standard Service';if(order&&!order.disabled)d['Design Order Type']=order.value==='special'?'Special Order':'Standard Order';if(priority)d['Order Priority']=priority.value==='express'?'Express Priority':'Standard Priority';if(design&&!design.disabled)d['Design Name']=choices[design.value];if(d['Email Address'])d.replyto=d['Email Address'];d['Entry Page']=location.origin+location.pathname;d['Request Type']=kind;d['Reference Files']='None — uploads are disabled';return d;}
function startReview(){status.textContent='';if(!valid())return;const d=payload();fingerprint=JSON.stringify(d);const dl=$('reviewDetails');dl.replaceChildren();for(const [k,v]of Object.entries(d)){if(['access_key','subject','from_name','replyto','Entry Page','Request Type'].includes(k)||!v)continue;const dt=document.createElement('dt'),dd=document.createElement('dd');dt.textContent=k;dd.textContent=v;dl.append(dt,dd);}form.hidden=true;review.hidden=false;$('review-title').focus();}
reviewButton.addEventListener('click',startReview);edit.addEventListener('click',()=>{review.hidden=true;form.hidden=false;(service||$('requestName')).focus();});reviewButton.disabled=false;
form.addEventListener('submit',async e=>{e.preventDefault();if(pending)return;if(!fingerprint||review.hidden){startReview();return;}if(!valid()||fingerprint!==JSON.stringify(payload())){status.textContent='Your request changed. Review the current details before submitting.';review.hidden=true;form.hidden=false;fingerprint='';return;}if(form.elements.botcheck.value){status.textContent='We could not confirm your request. Please contact Customer Support.';return;}
pending=true;send.disabled=true;edit.disabled=true;send.textContent='Sending…';status.textContent='Sending your request for human review.';const controller=new AbortController(),timer=setTimeout(()=>controller.abort(),20000);
try{const r=await fetch(form.action,{method:'POST',headers:{'Content-Type':'application/json',Accept:'application/json'},body:JSON.stringify(payload()),signal:controller.signal});const result=await r.json();if(!r.ok||result.success!==true)throw Error('Not confirmed');review.hidden=true;form.hidden=true;success.hidden=false;success.focus();}
catch(error){status.textContent=error.name==='AbortError'?'We could not confirm delivery before the timeout. Your request may have arrived. Contact Customer Support before trying again.':'We could not confirm your request. Your entries are preserved. Edit the request or try again, or contact Customer Support.';}
finally{clearTimeout(timer);pending=false;send.disabled=false;edit.disabled=false;send.textContent=kind==='refund'?'Submit Refund Request':kind==='support'?'Submit Support Request':'Submit for Quotation';}
});
});
