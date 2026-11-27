/* Generated from the approved shared menu controller. */
/* Shared navigation: native links/disclosures plus a focus-safe mobile menu. */
(function setupHomepageMenu() {
  const button = document.querySelector('.home-menu-toggle');
  const menu = document.getElementById('home-navigation');
  if (!button || !menu) return;
  const mobile = matchMedia('(max-width: 1099px)');
  const disclosures = [...menu.querySelectorAll('details')];
  const background = new Map();
  const backdrop = document.createElement('div');
  backdrop.className = 'home-nav-backdrop';
  backdrop.hidden = true;
  backdrop.setAttribute('aria-hidden', 'true');
  document.body.append(backdrop);
  function open() { return mobile.matches && button.getAttribute('aria-expanded') === 'true'; }
  function setBackground(blocked) {
    if (blocked) {
      for (const node of document.querySelectorAll('main,body>footer,#site-footer,.selected-design-bar')) {
        if (background.has(node)) continue;
        background.set(node, node.inert);
        node.inert = true;
      }
    } else {
      for (const [node, inert] of background) node.inert = inert;
      background.clear();
    }
  }
  function setOpen(value, restoreFocus = false) {
    const show = value && mobile.matches;
    button.setAttribute('aria-expanded', String(show));
    button.setAttribute('aria-label', show ? 'Close navigation' : 'Open navigation');
    menu.dataset.open = String(show);
    backdrop.hidden = !show;
    document.documentElement.classList.toggle('home-navigation-open', show);
    if (show) {
      const bottom = menu.closest('.homepage-header')?.getBoundingClientRect().bottom || 110;
      menu.style.setProperty('--home-nav-top', Math.max(0, bottom) + 'px');
    } else {
      for (const disclosure of disclosures) disclosure.open = false;
    }
    setBackground(show);
    if (restoreFocus) button.focus({ preventScroll: true });
  }
  for (const disclosure of disclosures) {
    const summary = disclosure.querySelector('summary');
    if (!summary) continue;
    summary.setAttribute('aria-expanded', String(disclosure.open));
    disclosure.addEventListener('toggle', () => {
      summary.setAttribute('aria-expanded', String(disclosure.open));
      if (disclosure.open) for (const other of disclosures) if (other !== disclosure) other.open = false;
    });
    disclosure.addEventListener('keydown', event => {
      if (event.key === 'Escape' && disclosure.open) {
        event.preventDefault(); event.stopPropagation();
        disclosure.open = false; summary.focus();
      } else if (event.target === summary && ['ArrowDown', 'ArrowUp'].includes(event.key)) {
        event.preventDefault(); disclosure.open = true;
        const links = [...disclosure.querySelectorAll('a[href]')];
        (event.key === 'ArrowDown' ? links[0] : links.at(-1))?.focus();
      }
    });
  }
  button.addEventListener('click', () => setOpen(!open()));
  backdrop.addEventListener('click', () => setOpen(false, true));
  menu.addEventListener('click', event => {
    const link = event.target.closest('a');
    if (!link) return;
    setOpen(false);
    const url = new URL(link.href, location.href);
    if (url.pathname === location.pathname && url.hash) {
      const section = document.getElementById(decodeURIComponent(url.hash.slice(1)));
      const target = section && (section.querySelector('h1,h2') || section);
      if (target) {
        target.tabIndex = -1;
        requestAnimationFrame(() => target.focus({ preventScroll: true }));
      }
    }
  });
  document.addEventListener('click', event => {
    if (!menu.contains(event.target) && !button.contains(event.target)) setOpen(false);
  });
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && open()) { event.preventDefault(); setOpen(false, true); return; }
    if (event.key !== 'Tab' || !open()) return;
    const targets = [button, ...menu.querySelectorAll('a[href],summary,button:not([disabled])')]
      .filter(node => node.getClientRects().length && !node.closest('[inert]'));
    const current = targets.indexOf(document.activeElement);
    // The toggle follows the nav in DOM order; explicitly keep a logical loop
    // rather than allowing Tab to leave the menu or skip its first link.
    event.preventDefault();
    const next = current < 0 ? (event.shiftKey ? targets.length - 1 : 0)
      : (current + (event.shiftKey ? -1 : 1) + targets.length) % targets.length;
    targets[next]?.focus();
  });
  mobile.addEventListener('change', () => setOpen(false));
  addEventListener('pageshow', () => setOpen(false));
})();

function legacyOrderBookmark(){if(location.hash==="#orderModal")location.replace("/#orderModal");}
addEventListener("hashchange",legacyOrderBookmark);legacyOrderBookmark();
