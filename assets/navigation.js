/* Initialize shared navigation even when a page loads its header asynchronously. */
(() => {
  const style = document.createElement('style');
  style.textContent = `body header nav a, body #site-header nav a, body #header-container nav a { padding:10px 2px !important; font-size:max(.8rem, 1vw) !important; }
    body header nav, body #site-header nav, body #header-container nav { overflow:visible !important; } body header nav ul, body #site-header nav ul, body #header-container nav ul { flex-wrap:wrap !important; white-space:normal !important; }
    body header { flex-wrap:wrap !important; } header a:focus-visible { outline:2px solid #d4af37; outline-offset:3px; }
    @media(max-width:700px) { body header nav, body #site-header nav, body #header-container nav { width:100% !important; } body header nav a, body #site-header nav a, body #header-container nav a { min-height:44px; box-sizing:border-box; } }
    `;
  document.head.append(style);
  let queued = false;
  function update() {
    queued = false;
    document.querySelectorAll('header nav a').forEach(link => {
      const current = location.pathname.split('/').pop() || 'index.html';
      if (new URL(link.href).pathname.split('/').pop() === current) {
        link.setAttribute('aria-current', 'page'); link.classList.add('active');
      }
    });
  }
  new MutationObserver(() => { if (!queued) { queued = true; queueMicrotask(update); } }).observe(document.body, { childList:true, subtree:true });
  update();
})();
