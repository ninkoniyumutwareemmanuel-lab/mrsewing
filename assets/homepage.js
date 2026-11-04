/* Homepage interactions only; content is rendered in the initial HTML. */
/* Universal Event Delegation for Order Buttons & Slider Arrows */
    (function setupGlobalDelegation() {
      const modal = document.getElementById('orderModal');
      const agree = document.getElementById('termsAgree');
      const whatsapp = document.getElementById('whatsappBtn');
      const hint = document.getElementById('termsHint');
      const closeButton = document.getElementById('orderClose');
      const termsLink = document.getElementById('termsLink');
      let returnFocus = null;

      function openModal() {
        if (!modal) return;
        returnFocus = document.activeElement;
        modal.classList.add('open');
        modal.setAttribute('aria-hidden', 'false');
        if (closeButton) closeButton.focus();
      }
      function closeModal() {
        if (!modal) return;
        if (!modal.classList.contains('open')) return;
        modal.classList.remove('open');
        modal.setAttribute('aria-hidden', 'true');
        if (agree) agree.checked = false;
        if (whatsapp) whatsapp.setAttribute('aria-disabled', 'true');
        if (hint) hint.textContent = '';
        if (location.hash === '#orderModal') history.replaceState(null, '', location.pathname + location.search);
        if (returnFocus && returnFocus.isConnected) returnFocus.focus();
      }

      document.addEventListener('click', function (event) {
        // 1. Order modal button handler
        const button = event.target.closest && event.target.closest('.order-btn');
        if (button) {
          event.preventDefault();
          openModal();
          return;
        }

        // 2. Universal slider arrows handler
        const leftClick = event.target.closest('#slideLeft, .slide-left');
        const rightClick = event.target.closest('#slideRight, .slide-right');
        if (leftClick || rightClick) {
          event.preventDefault();
          const slider = document.getElementById('customersSlider') || document.querySelector('.customers-slider');
          if (slider) {
            const step = (slider.querySelector('.customer-card-slide')?.getBoundingClientRect().width || 280) + 18;
            slider.scrollBy({ left: leftClick ? -step : step, behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'instant' : 'smooth' });
          }
        }
      });

      if (agree) {
        agree.addEventListener('change', function () {
          if (whatsapp) whatsapp.setAttribute('aria-disabled', agree.checked ? 'false' : 'true');
          if (hint) hint.textContent = '';
        });
      }
      if (whatsapp) {
        whatsapp.addEventListener('click', function (event) {
          if (agree && !agree.checked) {
            event.preventDefault();
            if (hint) hint.textContent = 'Please agree to the Terms & Conditions to continue.';
          } else {
            closeModal();
          }
        });
      }
      if (termsLink) termsLink.addEventListener('click', closeModal);
      if (closeButton) closeButton.addEventListener('click', function (event) { event.preventDefault(); closeModal(); });
      if (modal) {
        modal.addEventListener('click', function (event) { if (event.target === modal) closeModal(); });
      }
      document.addEventListener('keydown', function (event) {
        if (!modal || !modal.classList.contains('open')) return;
        if (event.key === 'Escape') closeModal();
        if (event.key === 'Tab') {
          const focusable = [...modal.querySelectorAll('a[href],button,input')].filter(e => e.getClientRects().length);
          const first = focusable[0], last = focusable[focusable.length - 1];
          if (event.shiftKey && document.activeElement === first) { event.preventDefault(); last.focus(); }
          else if (!event.shiftKey && document.activeElement === last) { event.preventDefault(); first.focus(); }
        }
      });
      if (location.hash === '#orderModal') {
        openModal();
        // Native fragment navigation can otherwise move focus after setup.
        requestAnimationFrame(() => {
          if (modal && modal.classList.contains('open') && closeButton) closeButton.focus();
        });
      }
    })();

/* A disclosure menu: normal links and tab order, with a usable no-JS fallback. */
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
/* Homepage-only progressive enhancements; never change the standalone forms. */
(()=>{'use strict';
const dropdown=document.querySelector('.services-dropdown details');
document.addEventListener('keydown',e=>{if(e.key==='Escape'&&dropdown?.open){e.preventDefault();e.stopImmediatePropagation();dropdown.open=false;dropdown.querySelector('summary').focus();}},true);
document.addEventListener('click',e=>{if(dropdown?.open&&!dropdown.contains(e.target))dropdown.open=false;});
dropdown?.addEventListener('click',e=>{if(e.target.closest('a'))dropdown.open=false;});
const options=[...document.querySelectorAll('[data-option]')],panels=[...document.querySelectorAll('[data-option-panel]')];let current=0;
function show(index){current=(index+panels.length)%panels.length;options.forEach((e,i)=>e.setAttribute('aria-pressed',String(i===current)));panels.forEach((e,i)=>e.hidden=i!==current);const pos=document.querySelector('.option-position');if(pos)pos.textContent=`${current+1} / ${panels.length}`;}
options.forEach((button,i)=>{button.addEventListener('click',()=>show(i));button.addEventListener('keydown',e=>{if(['ArrowLeft','ArrowRight','Home','End'].includes(e.key)){e.preventDefault();show(e.key==='Home'?0:e.key==='End'?panels.length-1:current+(e.key==='ArrowRight'?1:-1));options[current].focus();}});});
document.querySelectorAll('[data-option-direction]').forEach(e=>e.addEventListener('click',()=>show(current+Number(e.dataset.optionDirection))));if(panels.length)show(0);
const form=document.getElementById('quotationForm');if(!form)return;const button=form.querySelector('[type=submit]'),phone=document.getElementById('quotePhone'),message=document.getElementById('quoteMessage'),status=document.getElementById('quoteStatus'),success=document.getElementById('quoteSuccess');let pending=false;const label=button.innerHTML;
function validate(){const value=phone.value.trim(),digits=value.replace(/\D/g,'').length;phone.setCustomValidity(/^[0-9+\-\s().]+$/.test(value)&&digits>=7&&digits<=15?'':'Enter a valid phone number including your country code.');message.setCustomValidity(message.value.trim()?'':'Please tell us what you need.');}
phone.addEventListener('input',validate);message.addEventListener('input',validate);
form.addEventListener('submit',async e=>{e.preventDefault();validate();if(pending||!form.reportValidity())return;if(form.elements.botcheck.value){status.textContent='We could not confirm your request. Please contact us directly.';return;}
const data=Object.fromEntries(new FormData(form));delete data.botcheck;const email=data['Email Address'].trim();data['Email Address']=email||'Not provided';if(email)data.replyto=email;data['Terms Consent']='Agreed';data['Customer Message']=message.value.trim();pending=true;button.disabled=true;button.textContent='Sending…';form.setAttribute('aria-busy','true');status.textContent='Sending your request. Please wait.';const controller=new AbortController(),timer=setTimeout(()=>controller.abort(),20000);
try{const response=await fetch(form.action,{method:'POST',headers:{'Content-Type':'application/json',Accept:'application/json'},body:JSON.stringify(data),signal:controller.signal});const result=await response.json();if(!response.ok||result.success!==true)throw new Error('Not confirmed');form.hidden=true;success.hidden=false;success.focus();}
catch(error){status.textContent=error.name==='AbortError'?'We could not confirm delivery before the connection timed out. Your request may have arrived. Please contact us on WhatsApp before trying again.':'We could not confirm your request. Your entries are preserved. Please try again or contact us directly on WhatsApp.';}
finally{clearTimeout(timer);pending=false;button.disabled=false;button.innerHTML=label;form.removeAttribute('aria-busy');}});
})();
