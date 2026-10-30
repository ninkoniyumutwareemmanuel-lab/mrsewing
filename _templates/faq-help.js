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
  function excerpt(answer, text) {
    const words = basic(text).split(' ').filter(Boolean);
    for (const group of data.synonyms) if (group.some(term => words.includes(basic(term)))) words.push(...group.map(basic));
    const lower = answer.toLowerCase();
    const positions = words.map(word => lower.indexOf(word)).filter(pos => pos>=0);
    let start = positions.length ? Math.max(0,Math.min(...positions)-45) : 0;
    if (start) { const nextSpace=answer.indexOf(' ',start); if(nextSpace>=0)start=nextSpace+1; }
    let end = Math.min(answer.length,start+200);
    if (end<answer.length) { const space=answer.lastIndexOf(' ',end);if(space>start)end=space; }
    return (start?'… ':'')+answer.slice(start,end)+(end<answer.length?' …':'');
  }
  function render(updateUrl=true) {
    const value = query.value.slice(0,160).trim(), terms = normalise(value).split(' ').filter(Boolean);
    clear.hidden = !value; cards.hidden = !!value; results.hidden = !value;
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
      const text=document.createElement('p');text.textContent=excerpt(entry.answer,value);
      link.append(topic,title,text);item.append(link);list.append(item);
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
