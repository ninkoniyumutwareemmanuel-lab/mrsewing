/* Generated from _templates/shared/navigation.js. */
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

/* Preserve legacy order bookmarks using the existing homepage flow. */
if (location.hash === "#orderModal") location.replace("/#orderModal");
/* Native service disclosure, populated from the header component at build time. */
(()=>{'use strict';for(const menu of document.querySelectorAll('[data-service-picker]')){const summary=menu.querySelector('summary'),links=[...menu.querySelectorAll('a')];summary.setAttribute('aria-expanded',String(menu.open));menu.addEventListener('toggle',()=>summary.setAttribute('aria-expanded',String(menu.open)));menu.addEventListener('keydown',e=>{if(e.key==='Escape'&&menu.open){e.preventDefault();menu.open=false;summary.focus();return;}if(e.target===summary&&['ArrowDown','ArrowUp'].includes(e.key)){e.preventDefault();menu.open=true;(e.key==='ArrowDown'?links[0]:links.at(-1)).focus();return;}const current=links.indexOf(document.activeElement);if(current<0)return;const target=e.key==='Home'?0:e.key==='End'?links.length-1:e.key==='ArrowDown'?(current+1)%links.length:e.key==='ArrowUp'?(current+links.length-1)%links.length:-1;if(target>=0){e.preventDefault();links[target].focus();}});document.addEventListener('click',e=>{if(!menu.contains(e.target))menu.open=false;});menu.addEventListener('click',e=>{if(e.target.closest('a'))menu.open=false;});}})();
