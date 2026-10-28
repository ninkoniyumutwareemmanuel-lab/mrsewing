/* Shared consultation/measurement submission controller. */
(() => {
  const form = document.querySelector('#bookingForm, #submissionForm');
  if (!form) return;
  const selection = new URLSearchParams(location.search);
  if (selection.get('design')) {
    const design = selection.get('design').slice(0, 300);
    const summary = document.createElement('p');
    summary.textContent = 'Design enquiry: ' + design;
    form.prepend(summary);
    for (const [name, value] of [['Selected Design', design], ['Selected Photograph', selection.get('photo') || '']]) {
      const input = document.createElement('input');
      input.type = 'hidden'; input.name = name; input.value = value.slice(0, 2000); form.append(input);
    }
  }
  const button = form.querySelector('button[type="submit"]');
  const terms = form.querySelector('#agreeTerms, #formTermsAgree');
  const success = document.getElementById('successBox');
  const status = document.createElement('p');
  status.setAttribute('role', 'status');
  status.setAttribute('aria-live', 'polite');
  status.style.color = '#d4af37';
  form.append(status);
  const phone = form.querySelector('#phone');
  if (phone) {
    const validatePhone = () => {
      const value = phone.value.trim();
      const count = value.replace(/\D/g, '').length;
      phone.setCustomValidity(/^[0-9+\-\s().]+$/.test(value) && count >= 7 && count <= 15 ? '' : 'Please enter a valid phone number starting with your country code.');
    };
    phone.addEventListener('input', validatePhone);
    validatePhone();
  }
  let pending = false;
  const label = button.textContent;
  form.addEventListener('submit', async event => {
    event.preventDefault();
    if (pending || !form.reportValidity() || (terms && !terms.checked)) return;
    if (form.id === 'submissionForm') {
      const hasSize = document.getElementById('standardSize').value.trim();
      const hasMeasurement = Array.from({ length:12 }, (_, i) => document.getElementById('m' + (i + 1))).some(input => input.value.trim());
      const sizingError = document.getElementById('sizingErrorMsg');
      sizingError.style.display = hasSize || hasMeasurement ? 'none' : 'block';
      if (!hasSize && !hasMeasurement) {
        status.textContent = 'Please provide a standard size or at least one measurement.';
        document.getElementById('standardSize').focus();
        return;
      }
    }
    const data = Object.fromEntries(new FormData(form));
    const emailField = form.id === 'submissionForm' ? 'Email' : 'Email Address';
    const email = (data[emailField] || '').trim();
    data[emailField] = email || 'Not provided';
    if (email) data.replyto = email;
    if ('Customer Message' in data && !data['Customer Message'].trim()) data['Customer Message'] = 'No message provided';
    pending = true;
    button.disabled = true;
    button.textContent = 'Sending…';
    form.setAttribute('aria-busy', 'true');
    status.textContent = 'Sending your request. Please wait.';
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 20000);
    try {
      const response = await fetch(form.action, {
        method:'POST', headers:{ 'Content-Type':'application/json', Accept:'application/json' },
        body:JSON.stringify(data), signal:controller.signal
      });
      const result = await response.json();
      if (!response.ok || result.success !== true) throw new Error('Submission not confirmed');
      form.hidden = true;
      form.style.display = 'none';
      success.style.display = 'block';
      success.setAttribute('role', 'status');
      success.setAttribute('tabindex', '-1');
      success.focus();
    } catch (error) {
      status.textContent = error.name === 'AbortError'
        ? 'We could not confirm delivery before the connection timed out. Your request may have arrived. Please contact us on WhatsApp before trying again.'
        : 'We could not confirm your request. Your entries are preserved. Please try again or contact us directly on WhatsApp.';
    } finally {
      clearTimeout(timeout);
      pending = false;
      form.removeAttribute('aria-busy');
      button.disabled = !!terms && !terms.checked;
      button.textContent = label;
    }
  });
  // Changing consent must not unlock a request already being sent.
  terms?.addEventListener('change', () => { button.disabled = pending || !terms.checked; });
})();
