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
/* Visual-only review: presentation controls work; navigation and submissions do not. */
(()=>{'use strict';
document.addEventListener('click',e=>{if(e.target.closest('[data-preview-link]')){e.preventDefault();e.stopImmediatePropagation();}},true);
document.addEventListener('submit',e=>{e.preventDefault();},true);
const dropdown=document.querySelector('.services-dropdown details');
document.addEventListener('keydown',e=>{if(e.key==='Escape'&&dropdown?.open){e.preventDefault();e.stopImmediatePropagation();dropdown.open=false;dropdown.querySelector('summary').focus();}},true);
document.addEventListener('click',e=>{if(dropdown?.open&&!dropdown.contains(e.target))dropdown.open=false;});
const buttons=[...document.querySelectorAll('[data-option]')],panels=[...document.querySelectorAll('[data-option-panel]')];let current=0;
function show(index){current=(index+panels.length)%panels.length;buttons.forEach((e,i)=>e.setAttribute('aria-pressed',String(i===current)));panels.forEach((e,i)=>e.hidden=i!==current);const pos=document.querySelector('.option-position');if(pos)pos.textContent=`${current+1} / ${panels.length}`;}
buttons.forEach((b,i)=>{b.addEventListener('click',()=>show(i));b.addEventListener('keydown',e=>{if(['ArrowLeft','ArrowRight','Home','End'].includes(e.key)){e.preventDefault();show(e.key==='Home'?0:e.key==='End'?panels.length-1:current+(e.key==='ArrowRight'?1:-1));buttons[current].focus();}});});
document.querySelectorAll('[data-option-direction]').forEach(b=>b.addEventListener('click',()=>show(current+Number(b.dataset.optionDirection))));if(panels.length)show(0);
document.querySelectorAll('#slideLeft,#slideRight').forEach(b=>b.addEventListener('click',()=>{const slider=document.getElementById('customersSlider');if(slider){const step=(slider.querySelector('.customer-card-slide')?.getBoundingClientRect().width||280)+18;slider.scrollBy({left:b.id==='slideLeft'?-step:step,behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'instant':'smooth'});}}));
})();
