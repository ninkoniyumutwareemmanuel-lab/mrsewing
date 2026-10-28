/* Shared, keyboard-accessible design previews. No customer data is stored. */
(() => {
  const dialog = document.createElement('dialog');
  dialog.className = 'design-dialog';
  dialog.setAttribute('aria-labelledby', 'design-title');
  dialog.setAttribute('aria-describedby', 'design-description');
  dialog.innerHTML = `<button type="button" class="design-close" aria-label="Close design preview">×</button>
    <h2 id="design-title"></h2><img class="design-photo" alt=""><p class="design-description" id="design-description"></p>
    <div class="design-actions"><a class="design-enquiry" target="_blank" rel="noopener">Enquire About This Design on WhatsApp</a>
    <a class="design-booking" href="booking.html">Book Consultation</a><a href="contact.html">Contact Mr Sewing Fashion</a></div>`;
  document.body.append(dialog);
  let opener;
  dialog.querySelector('.design-close').addEventListener('click', () => dialog.close());
  dialog.addEventListener('click', event => { if (event.target === dialog) {
    const box = dialog.getBoundingClientRect();
    if (event.clientX < box.left || event.clientX > box.right || event.clientY < box.top || event.clientY > box.bottom) dialog.close();
  }});
  dialog.addEventListener('keydown', event => {
    if (event.key !== 'Tab') return;
    const controls = [...dialog.querySelectorAll('button, a[href]')];
    const first = controls[0], last = controls[controls.length - 1];
    if (event.shiftKey && document.activeElement === first) { event.preventDefault(); last.focus(); }
    else if (!event.shiftKey && document.activeElement === last) { event.preventDefault(); first.focus(); }
  });
  dialog.addEventListener('close', () => { if (opener?.isConnected) opener.focus(); });
  document.addEventListener('click', event => {
    const trigger = event.target.closest('.design-preview');
    if (!trigger) return;
    event.preventDefault();
    const card = trigger.closest('article, .photo-card, .work-card, .collection-card');
    const image = card?.querySelector('img');
    const file = trigger.dataset.designImage || image?.getAttribute('src');
    if (!file) return;
    opener = trigger;
    const title = card?.querySelector('h3, .photo-title-text')?.textContent.trim() || image?.alt || 'Mr. Sewing Design';
    const description = card?.querySelector('.work-desc, .photo-subtitle-text, .collection-content p')?.textContent.trim() || '';
    const photo = dialog.querySelector('.design-photo');
    // Encode spaces, including the existing leading space in the r24 filename.
    photo.src = new URL(encodeURI(file), location.href).href;
    photo.alt = title;
    dialog.querySelector('h2').textContent = title;
    dialog.querySelector('.design-description').textContent = description;
    const message = `Hello Mr. Sewing, I would like to enquire about ${title}: ${photo.src}`;
    dialog.querySelector('.design-booking').href = 'booking.html?design=' + encodeURIComponent(title) + '&photo=' + encodeURIComponent(file);
    dialog.querySelector('.design-enquiry').href = 'https://wa.me/250787411501?text=' + encodeURIComponent(message);
    dialog.showModal();
    dialog.querySelector('.design-close').focus();
  });
})();
