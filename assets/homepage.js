/* Homepage interactions only; content is rendered in the initial HTML. */
/* Universal Event Delegation for Order Buttons & Slider Arrows */
    (function setupGlobalDelegation() {
      const modal = document.getElementById('orderModal');
      const agree = document.getElementById('termsAgree');
      const whatsapp = document.getElementById('whatsappBtn');
      const hint = document.getElementById('termsHint');
      const closeButton = document.getElementById('orderClose');
      const termsLink = document.getElementById('termsLink');

      function openModal() {
        if (!modal) return;
        modal.classList.add('open');
        modal.setAttribute('aria-hidden', 'false');
      }
      function closeModal() {
        if (!modal) return;
        modal.classList.remove('open');
        modal.setAttribute('aria-hidden', 'true');
        if (agree) agree.checked = false;
        if (whatsapp) whatsapp.setAttribute('aria-disabled', 'true');
        if (hint) hint.textContent = '';
        if (location.hash === '#orderModal') history.replaceState(null, '', location.pathname + location.search);
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
            slider.scrollBy({ left: leftClick ? -280 : 280, behavior: 'smooth' });
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
      document.addEventListener('keydown', function (event) { if (event.key === 'Escape') closeModal(); });
      if (location.hash === '#orderModal') openModal();
    })();

/* A disclosure menu: normal links and tab order, with a usable no-JS fallback. */
(function setupHomepageMenu() {
  const button = document.querySelector('.home-menu-toggle');
  const menu = document.getElementById('home-navigation');
  if (!button || !menu) return;
  function setOpen(open, restoreFocus = false) {
    button.setAttribute('aria-expanded', String(open));
    menu.dataset.open = String(open);
    if (restoreFocus) button.focus();
  }
  button.addEventListener('click', () => setOpen(button.getAttribute('aria-expanded') !== 'true'));
  menu.addEventListener('click', event => { if (event.target.closest('a')) setOpen(false); });
  document.addEventListener('click', event => {
    if (!event.target.closest('.homepage-header')) setOpen(false);
  });
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && button.getAttribute('aria-expanded') === 'true') setOpen(false, true);
  });
  // Reset on the layout breakpoint only, not while mobile browser chrome resizes.
  matchMedia('(max-width: 1100px)').addEventListener('change', () => setOpen(false));
})();
