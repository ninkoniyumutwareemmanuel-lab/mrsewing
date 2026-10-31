/* Native disclosures work without JavaScript; direct answer links open their answer. */
(() => {
  function openAnswer() {
    let id;
    try { id = decodeURIComponent(location.hash.slice(1)); } catch { return; }
    const answer = id && document.getElementById(id);
    if (answer && answer.matches('details.faq-question')) answer.open = true;
  }
  openAnswer();
  addEventListener('hashchange', openAnswer);
})();
