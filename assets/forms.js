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
  // Kigali dates are calendar dates, not browser-local time-zone instants.
  const dateInput = form.querySelector('#preferredDate');
  const timeInput = form.querySelector('#preferredTime');
  let validateHours = () => {};
  if (dateInput && timeInput && window.MrSewingHours) {
    const hours = window.MrSewingHours;
    const note = document.getElementById('business-hours-note') || document.createElement('p');
    note.id = 'business-hours-note'; note.setAttribute('role', 'status');
    note.style.cssText = 'color:#cccccc;font-size:.85rem;line-height:1.5;margin-top:8px';
    if (!note.isConnected) dateInput.insertAdjacentElement('afterend', note);
    dateInput.setAttribute('aria-describedby', [...new Set((dateInput.getAttribute('aria-describedby') || '').split(/\s+/).filter(Boolean).concat(note.id))].join(' '));
    timeInput.setAttribute('aria-describedby', [...new Set((timeInput.getAttribute('aria-describedby') || '').split(/\s+/).filter(Boolean).concat(note.id))].join(' '));
    validateHours = () => {
      timeInput.setCustomValidity(hours.timeAllowed(dateInput.value, timeInput.value) ? '' : 'On Umuganda, please choose a time between 12:00 PM and 5:00 PM; an advance appointment is required.');
    };
    const updateHours = () => {
      const day = hours.availability(dateInput.value);
      for (const option of timeInput.options) option.disabled = !hours.timeAllowed(dateInput.value, option.value);
      if (timeInput.selectedOptions[0]?.disabled) timeInput.value = [...timeInput.options].find(option => !option.disabled)?.value || '';
      note.textContent = !day ? 'Ordinary Saturdays: 9 AM–5 PM, no appointment needed. Umuganda: noon–5 PM by advance appointment. Sunday: by appointment only.'
        : day.kind === 'umuganda' ? 'Umuganda (last Saturday): 12 PM–5 PM, strictly by advance appointment. Please obtain confirmation before visiting; custom requests must also be within these hours.'
        : day.kind === 'sunday' ? 'Sunday is by appointment only, with no fixed opening hours. Your proposed time must be confirmed before visiting.'
        : day.kind === 'saturday' ? 'Saturday: 9 AM–5 PM. Ordinary Saturday visits do not require an appointment; you may still request a consultation.'
        : 'Monday–Friday: 9 AM–5 PM. Your booking request is subject to confirmation.';
      validateHours();
    };
    dateInput.addEventListener('change', updateHours);
    dateInput.addEventListener('input', updateHours);
    timeInput.addEventListener('change', validateHours);
    updateHours();
  }
  let pending = false;
  const label = button.textContent;
  form.addEventListener('submit', async event => {
    event.preventDefault();
    validateHours();
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
