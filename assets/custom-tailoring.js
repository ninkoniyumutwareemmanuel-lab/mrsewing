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

/* Dedicated tailoring-page enhancements; no uploads and no automatic order creation. */
(()=>{'use strict';
const dropdown=document.querySelector('.services-dropdown details');
document.addEventListener('keydown',e=>{if(e.key==='Escape'&&dropdown?.open){e.preventDefault();e.stopImmediatePropagation();dropdown.open=false;dropdown.querySelector('summary').focus();}},true);
document.addEventListener('click',e=>{if(dropdown?.open&&!dropdown.contains(e.target))dropdown.open=false;});
dropdown?.addEventListener('click',e=>{if(e.target.closest('a'))dropdown.open=false;});
const form=document.getElementById('specialOrderForm');if(!form)return;
const button=document.getElementById('specialSubmit'),status=document.getElementById('specialStatus'),success=document.getElementById('specialSuccess'),phone=document.getElementById('specialPhone'),name=document.getElementById('specialName'),description=document.getElementById('specialDescription'),locationField=document.getElementById('specialLocation'),date=document.getElementById('specialDate');let pending=false;
const today=new Date(),minimum=[today.getFullYear(),String(today.getMonth()+1).padStart(2,'0'),String(today.getDate()).padStart(2,'0')].join('-');date.min=minimum;
function validate(){const digits=phone.value.replace(/\D/g,'').length;phone.setCustomValidity(/^[0-9+\-\s().]+$/.test(phone.value.trim())&&digits>=7&&digits<=15?'':'Enter a valid phone number including your country code.');for(const [el,message]of [[name,'Please enter your name.'],[description,'Please describe your garment or design.'],[locationField,'Please enter your country or location.']])el.setCustomValidity(el.value.trim()?'':message);date.setCustomValidity(date.value&&date.value<minimum?'Please select today or a future date, or leave this preference empty.':'');}
for(const el of [phone,name,description,locationField,date])el.addEventListener('input',validate);
form.addEventListener('submit',async e=>{e.preventDefault();validate();if(pending||!form.reportValidity())return;if(form.elements.botcheck.value){status.textContent='We could not confirm your enquiry. Please contact Customer Support.';return;}
const data=Object.fromEntries(new FormData(form));delete data.botcheck;for(const key of Object.keys(data))if(typeof data[key]==='string')data[key]=data[key].trim();if(data['Email Address'])data.replyto=data['Email Address'];else data['Email Address']='Not provided';data['Entry Page']=location.origin+location.pathname;data['Reference Files']='No files attached. Online uploads are not enabled.';
pending=true;button.disabled=true;button.textContent='Submitting…';form.setAttribute('aria-busy','true');status.textContent='Sending your design enquiry. Please wait.';const controller=new AbortController(),timer=setTimeout(()=>controller.abort(),20000);
try{const response=await fetch(form.action,{method:'POST',headers:{'Content-Type':'application/json',Accept:'application/json'},body:JSON.stringify(data),signal:controller.signal});const result=await response.json();if(!response.ok||result.success!==true)throw new Error('Not confirmed');form.hidden=true;success.hidden=false;success.focus();}
catch(error){status.textContent=error.name==='AbortError'?'We could not confirm delivery before the connection timed out. Your enquiry may have arrived. Please contact Customer Support before submitting again.':'We could not confirm your enquiry. Your entries are preserved. Please try again or contact Customer Support.';}
finally{clearTimeout(timer);pending=false;button.disabled=false;button.textContent='Submit Design Request';form.removeAttribute('aria-busy');}
});button.disabled=false;
})();
