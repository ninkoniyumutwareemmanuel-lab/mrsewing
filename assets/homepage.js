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
