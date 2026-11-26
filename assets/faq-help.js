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

/* FAQ answers remain readable without repeated copy/source button groups. */

/* Local FAQ enhancement: native links/details remain useful without JavaScript. */
(() => {
  'use strict';
  function revealAnswer() {
    let id; try { id = decodeURIComponent(location.hash.slice(1)); } catch (_) { return; }
    const target = document.getElementById(id);
    if (target && target.matches('.faq-question')) {
      target.open = true;
      requestAnimationFrame(() => target.scrollIntoView({block:'start'}));
    }
  }
  revealAnswer();
  addEventListener('hashchange', revealAnswer);
  const form = document.getElementById('faq-search');
  if (!form) return;
  const legacy = JSON.parse(document.getElementById('faq-legacy-data').textContent);
  function restoreBookmark() {
    let hash; try { hash = decodeURIComponent(location.hash.slice(1)); } catch (_) { return; }
    if (legacy[hash]) location.replace(legacy[hash] + (location.search && !legacy[hash].includes('#') ? location.search : ''));
  }
  restoreBookmark(); addEventListener('hashchange', restoreBookmark);
  const data = JSON.parse(document.getElementById('faq-search-data').textContent);
  const query = document.getElementById('faq-query'), clear = document.getElementById('faq-clear'), cards = document.getElementById('faq-topics');
  const results = document.getElementById('faq-results'), list = document.getElementById('faq-result-list'), status = document.getElementById('faq-search-status'), empty = document.getElementById('faq-empty');
  const basic = value => value.normalize('NFKD').replace(/[\u0300-\u036f]/g,'').toLowerCase().replace(/[^a-z0-9]+/g,' ').trim();
  const aliases = data.synonyms.flatMap(group => group.map(term => ({term:basic(term), canonical:basic(group[0])}))).sort((a,b) => b.term.length-a.term.length);
  const normalise = value => {
    let text = ' '+basic(value)+' ';
    for (const alias of aliases) text = text.replace(new RegExp('\\b'+alias.term.replace(/ /g,'\\s+')+'\\b','g'), alias.canonical);
    return text.trim();
  };
  let entries;
  function searchableEntries() {
    if (!entries) entries=data.entries.map(entry => {const text=[entry.question,entry.topic,entry.answer,...entry.keywords].join(' ');return {...entry,haystack:basic(text)+' '+normalise(text)};});
    return entries;
  }
  function render(updateUrl=true) {
    const value = query.value.slice(0,160).trim(), terms = normalise(value).split(' ').filter(Boolean);
    clear.hidden = !value; cards.hidden = !!value; results.hidden = !value;const common=document.getElementById('faq-common');if(common)common.hidden=!!value;
    list.replaceChildren();
    if (updateUrl) { const url=new URL(location.href);if(value)url.searchParams.set('q',value);else url.searchParams.delete('q');history.replaceState(null,'',url); }
    if (!value) { status.textContent='';empty.hidden=true;return; }
    // Every word must match; punctuation-only queries produce an honest empty state.
    const matches = terms.length ? searchableEntries().filter(entry => terms.every(term => entry.haystack.includes(term))) : [];
    status.textContent = matches.length+' '+(matches.length===1?'answer':'answers')+' found';
    empty.hidden = matches.length>0;
    for (const entry of matches) {
      const item=document.createElement('li');item.className='faq-result';
      const link=document.createElement('a');link.href=entry.url;
      const topic=document.createElement('small');topic.textContent=entry.topic;
      const title=document.createElement('h3');title.textContent=entry.question;
      const text=document.createElement('p');text.textContent=entry.answer;
      link.append(topic,title);const source=document.createElement('a');source.href=entry.source;source.textContent='Read the full guidance';item.append(link,text,source);list.append(item);
    }
  }
  form.hidden=false;
  query.value=(new URL(location.href).searchParams.get('q')||'').slice(0,160);
  render(false);
  query.addEventListener('input',()=>render());
  form.addEventListener('submit',event=>{event.preventDefault();render();});
  clear.addEventListener('click',()=>{query.value='';render();query.focus();});
  addEventListener('popstate',()=>{query.value=(new URL(location.href).searchParams.get('q')||'').slice(0,160);render(false);});
  addEventListener('pageshow',()=>{query.value=(new URL(location.href).searchParams.get('q')||'').slice(0,160);render(false);});
})();
