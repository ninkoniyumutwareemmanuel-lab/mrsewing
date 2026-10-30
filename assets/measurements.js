/* Progressive enhancement: ordinary image links work without JavaScript. */
(() => {
  const viewer = document.getElementById('measurement-viewer');
  if (!viewer || typeof viewer.showModal !== 'function') return;
  const image = viewer.querySelector('img');
  const caption = viewer.querySelector('p');
  const close = viewer.querySelector('button');
  let trigger;
  document.querySelectorAll('[data-measure-image]').forEach(link => {
    link.addEventListener('click', event => {
      if (event.button || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
      event.preventDefault();
      trigger = link;
      image.src = link.href;
      image.alt = link.querySelector('img').alt;
      caption.textContent = link.dataset.measureImage;
      viewer.showModal();
      document.documentElement.style.overflow = 'hidden';
      close.focus();
    });
  });
  close.addEventListener('click', () => viewer.close());
  viewer.addEventListener('click', event => { if (event.target === viewer) {
    const rect = viewer.getBoundingClientRect();
    if (event.clientX < rect.left || event.clientX > rect.right || event.clientY < rect.top || event.clientY > rect.bottom) viewer.close();
  }});
  viewer.addEventListener('close', () => {
    document.documentElement.style.overflow = '';
    trigger?.focus();
  });
})();
