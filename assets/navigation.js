/* Initialize shared navigation even when a page loads its header asynchronously. */
(() => {
  const style = document.createElement('style');
  style.textContent = `body header nav a, body #site-header nav a, body #header-container nav a { padding:10px 2px !important; font-size:max(.8rem, 1vw) !important; }
    body header nav, body #site-header nav, body #header-container nav { overflow:visible !important; } body header nav ul, body #site-header nav ul, body #header-container nav ul { flex-wrap:wrap !important; white-space:normal !important; }
    body header { flex-wrap:wrap !important; } header a:focus-visible { outline:2px solid #d4af37; outline-offset:3px; }
    @media(max-width:700px) { body header nav, body #site-header nav, body #header-container nav { width:100% !important; } body header nav a, body #site-header nav a, body #header-container nav a { min-height:44px; box-sizing:border-box; } }
    .customer-actions { font-size:.85rem; display:flex; flex-wrap:wrap; justify-content:center; gap:12px; padding:16px 4%; background:#141414; color:#d4af37; }
    @media(max-width:700px) { .customer-actions { display:grid; grid-template-columns:1fr 1fr; gap:4px; text-align:center; } }
    .customer-actions a { color:#d4af37; padding:10px; min-height:44px; box-sizing:border-box; }
    .customer-actions a:focus-visible { outline:2px solid #d4af37; }`;
  document.head.append(style);
  const actions = document.createElement('nav');
  actions.className = 'customer-actions';
  actions.setAttribute('aria-label', 'Customer actions');
  actions.innerHTML = '<a href="booking.html">Book Consultation</a><a href="suits.html">Enquire About a Design</a><a href="contact.html">Contact Mr Sewing Fashion</a><a href="https://wa.me/250787411501" target="_blank" rel="noopener">WhatsApp Contact</a>';
  document.body.append(actions);
  let queued = false;
  function update() {
    queued = false;
    document.querySelectorAll('header nav a').forEach(link => {
      const current = location.pathname.split('/').pop() || 'index.html';
      if (new URL(link.href).pathname.split('/').pop() === current) {
        link.setAttribute('aria-current', 'page'); link.classList.add('active');
      }
    });
    const header = document.querySelector('#site-header, #header-container, header');
    if (header && header.nextElementSibling !== actions) header.after(actions);
  }
  new MutationObserver(() => { if (!queued) { queued = true; queueMicrotask(update); } }).observe(document.body, { childList:true, subtree:true });
  update();
})();
