/* Centralized, local-only custom-tailoring showroom. No trackers or dependencies. */
(() => {
  'use strict';
  if (location.hash === '#orderModal') return; // shared legacy redirect owns this navigation
  const payload = JSON.parse(document.getElementById('showroom-data').textContent);
  const designs = payload.designs, byId = new Map(designs.map(d => [d.id, d]));
  const $ = id => document.getElementById(id), dialog = $('design-viewer');
  const key = 'mr-sewing:favourites:v1', batch = 12;
  let favourites = new Set(), state, matches = [], shown = batch, current = null, photoIndex = 0;
  let opener = null, returnId = '', pushed = false, previousOverflow = '', sharing = false, shortlistPage = 0;
  const labels = {'double-breasted':'Double-breasted', classic:'Classic', modern:'Modern', kaunda:'Kaunda', graduation:'Graduation', men:'Men', women:'Women'};
  const label = s => labels[s] || s;
  const normalize = s => String(s).normalize('NFKD').replace(/[\u0300-\u036f]/g, '').toLowerCase();
  const compact = s => normalize(s).replace(/[^a-z0-9]/g, '');
  const searchIndex=new Map(designs.map(d=>{const fields=[d.id,d.name,d.gender==='unclassified'?'':d.gender,d.garmentType,d.description,...d.styles,...d.occasions,...d.colors];return [d.id,[...normalize(fields.join(' ')).split(/[^a-z0-9]+/).filter(Boolean),...fields.map(compact)]]}));
  function element(tag, text, attrs={}) { const e = document.createElement(tag); if (text !== null) e.textContent = text; for (const [k,v] of Object.entries(attrs)) e.setAttribute(k,v); return e; }
  function stored() {
    try { const data = JSON.parse(localStorage.getItem(key) || '[]'); if (!Array.isArray(data)) throw new Error('Invalid saved list'); return new Set(data.filter(id => typeof id === 'string' && byId.has(id))); }
    catch { $('storage-status').textContent = 'Favourites can be saved on this page only. Browser storage is unavailable or was reset.'; return new Set(); }
  }
  favourites = stored();
  function persist() { try { localStorage.setItem(key, JSON.stringify([...favourites])); } catch { $('storage-status').textContent = 'Saved on this page only. Your browser could not store this shortlist.'; } }
  function designURL(id) { const url = new URL('/collections/', location.origin); url.searchParams.set('design',id); url.hash = 'design-'+id; return url.href; }
  function whatsapp(text) { return 'https://wa.me/250787411501?text='+encodeURIComponent(text); }
  function readState() {
    const p = new URL(location.href).searchParams;
    return {q:(p.get('q') || '').slice(0,160),gender:['all','men','women'].includes(p.get('gender'))?p.get('gender'):payload.defaultGender,style:p.get('style') || '',occasion:p.get('occasion') || '',saved:p.get('saved')==='1'};
  }
  function writeState() {
    const url = new URL(location.href);
    for (const [k,v] of Object.entries({q:state.q,gender:state.gender===payload.defaultGender?'':state.gender,style:state.style,occasion:state.occasion,saved:state.saved?'1':''})) { if (v) url.searchParams.set(k,v); else url.searchParams.delete(k); }
    history.replaceState(null,'',url);
  }
  function controls() {
    $('design-search').value = state.q; $('style-filter').value = state.style; $('occasion-filter').value = state.occasion;
    document.querySelectorAll('[data-gender]').forEach(b => b.setAttribute('aria-pressed',String(b.dataset.gender===state.gender)));
    $('show-saved').setAttribute('aria-pressed',String(state.saved)); $('shortlist-tools').hidden = !state.saved;
  }
  function filtered() {
    const tokens = normalize(state.q).split(/[^a-z0-9]+/).filter(Boolean);
    return designs.filter(d => (state.gender==='all' || d.gender===state.gender) && (!state.style || d.styles.includes(state.style)) && (!state.occasion || d.occasions.includes(state.occasion)) && (!state.saved || favourites.has(d.id)) && tokens.every(t => searchIndex.get(d.id).some(word=>word.startsWith(t))));
  }
  function picture(image) {
    const p = element('picture',null);
    if (image.avif) p.append(element('source',null,{type:'image/avif',srcset:image.avif,sizes:'(min-width: 1100px) 280px, (min-width: 600px) 30vw, calc((100vw - 52px) / 2)'}));
    const img = element('img',null,{src:image.thumb,srcset:image.srcset,sizes:'(min-width: 1100px) 280px, (min-width: 600px) 30vw, calc((100vw - 52px) / 2)',alt:image.alt,width:image.width,height:image.height,loading:'lazy',decoding:'async'});img.style.objectPosition=image.position;p.append(img);return p;
  }
  function heart() { const svg = document.createElementNS('http://www.w3.org/2000/svg','svg');svg.setAttribute('viewBox','0 0 24 24');svg.setAttribute('aria-hidden','true');svg.innerHTML='<path d="M20.8 4.6a5.5 5.5 0 0 0-7.8 0L12 5.7l-1.1-1.1a5.5 5.5 0 0 0-7.8 7.8L12 21l8.8-8.6a5.5 5.5 0 0 0 0-7.8Z"/>';return svg; }
  function card(d) {
    const article = element('article',null,{class:'show-card','data-id':d.id});
    const a = element('a',null,{class:'design-preview view-details-btn',href:designURL(d.id),'data-open':d.id});a.append(picture(d.images[0]));
    const copy = element('span',null,{class:'show-card-copy'});copy.append(element('span',d.name),element('small',d.id));a.append(copy);
    const save = element('button',null,{type:'button',class:'save-design','data-save':d.id,'aria-pressed':String(favourites.has(d.id)),'aria-label':(favourites.has(d.id)?'Remove ':'Save ')+d.id+' '+(favourites.has(d.id)?'from':'to')+' favourites'});save.append(heart());article.append(a,save);return article;
  }
  function shortlist() {
    const list = designs.filter(d => favourites.has(d.id)); const size=8;
    if (shortlistPage*size>=list.length) shortlistPage=0;
    const portion = list.slice(shortlistPage*size,(shortlistPage+1)*size);
    $('share-shortlist').hidden = !list.length; $('next-shortlist').hidden = list.length<=size;
    $('share-shortlist').textContent = list.length>size?`Share designs ${shortlistPage*size+1}–${shortlistPage*size+portion.length} of ${list.length} on WhatsApp`:'Share shortlist on WhatsApp';
    $('share-shortlist').href=whatsapp("Hello Mr Sewing! I've explored your collections and selected these designs:\n\n"+portion.map((d,i)=>`${shortlistPage*size+i+1}. ${d.id} — ${d.name}\n   ${designURL(d.id)}`).join('\n\n')+"\n\nI'd like to discuss customization options and receive a quotation.");
  }
  function savedUI() {
    $('saved-count').textContent=favourites.size;
    document.querySelectorAll('[data-save]').forEach(b=>{const yes=favourites.has(b.dataset.save);b.setAttribute('aria-pressed',String(yes));b.setAttribute('aria-label',`${yes?'Remove':'Save'} ${b.dataset.save} ${yes?'from':'to'} favourites`);});
    if (current) {const yes=favourites.has(current.id);$('save-viewer').setAttribute('aria-pressed',String(yes));$('save-viewer').textContent=yes?'Remove from Favourites':'Save to Favourites';}
    shortlist();
  }
  function render(append=false,reuse=false) {
    if (!append) { matches=filtered();shown=batch;if(!reuse)$('design-grid').replaceChildren(); }
    const start=append?shown-batch:0;
    if(!reuse){const fragment=document.createDocumentFragment();for(const d of matches.slice(start,shown)) fragment.append(card(d));$('design-grid').append(fragment);}else document.querySelectorAll('.save-design').forEach(b=>b.replaceChildren(heart()));
    $('gallery-empty').hidden=matches.length>0;$('load-more').hidden=shown>=matches.length;
    $('gallery-status').textContent=`${matches.length} ${state.saved?'saved ':''}design${matches.length===1?'':'s'}${matches.length?` · Showing ${Math.min(shown,matches.length)}`:''}.`;
    if (!matches.length && state.saved) $('gallery-empty').querySelector('p').textContent='Your shortlist is empty. Save a design using its heart button. Saved designs stay on this browser only.';
    else $('gallery-empty').querySelector('p').textContent='Try another style or reference, or clear your filters.';
    controls();savedUI();
  }
  function apply() { writeState();render(); }
  function reset() {state={q:'',gender:payload.defaultGender,style:'',occasion:'',saved:false};apply();}
  function setFavourite(id) {if(favourites.has(id))favourites.delete(id);else favourites.add(id);persist();if(state.saved){render();if(!dialog.open)$('show-saved').focus({preventScroll:true});}else savedUI();}
  function showPhoto() {
    const image=current.images[photoIndex],img=dialog.querySelector('.design-photo');
    img.src=image.src;img.alt=image.alt;img.width=image.width;img.height=image.height;img.style.objectPosition='center';
    $('photo-count').textContent=`${photoIndex+1} / ${current.images.length}`; $('photo-previous').disabled=$('photo-next').disabled=current.images.length<2;
  }
  function openDesign(id,historyMode=false,source=null) {
    const d=byId.get(id);
    if (!d) { $('gallery-status').textContent='This design is unavailable or has been retired. Please explore the available designs.'; if(dialog.open)dialog.close();return; }
    if(!dialog.open){opener=source || document.activeElement;returnId=source?.dataset.open || '';previousOverflow=document.body.style.overflow;document.body.style.overflow='hidden';dialog.showModal();$('close-design').focus();pushed=historyMode;}
    current=d;photoIndex=0;showPhoto();$('design-title').textContent=d.name;$('design-reference').textContent=d.id;
    $('share-status').textContent='';document.getElementById('manual-share-link')?.remove();$('design-details').open=false;
    $('design-description').textContent=d.description;
    $('provenance-label').hidden=d.provenance==='unverified';$('provenance-label').textContent=d.provenance==='made_by_mr_sewing'?'Made by Mr Sewing':d.provenance==='design_inspiration'?'Design Inspiration':'';
    const meta=$('design-metadata');meta.replaceChildren();for(const [name,val] of [['Style',d.styles.map(label).join(', ')],['Occasion',d.occasions.map(label).join(', ')],['Garment',d.garmentType],['Colour',d.colors.join(', ')]]){if(!val)continue;const row=element('div',null);row.append(element('dt',name),element('dd',val));meta.append(row);}
    dialog.querySelector('.design-enquiry').href=whatsapp(`Hello Mr Sewing! I'm interested in this design:\n\nDesign: ${d.name}\nReference: ${d.id}\nLink: ${designURL(d.id)}\n\nI'd like to discuss customization options and receive a quotation.`);
    dialog.querySelector('.design-booking').href='/booking/?design='+encodeURIComponent(d.name+' · '+d.id)+'&photo='+encodeURIComponent(d.images[0].src);
    if(historyMode){const url=new URL(location.href);url.searchParams.set('design',id);url.hash='design-'+id;history.pushState(null,'',url);}
    savedUI();
  }
  function closeRequest() {if(pushed){pushed=false;history.back();}else{const u=new URL(location.href);u.searchParams.delete('design');if(u.hash.startsWith('#design-'))u.hash='';history.replaceState(null,'',u);dialog.close();finishClose();}}
  function navigate(delta) {const list=matches.some(d=>d.id===current.id)?matches:designs;const index=list.findIndex(d=>d.id===current.id);const d=list[(index+delta+list.length)%list.length];if(!d)return;openDesign(d.id);const u=new URL(location.href);u.searchParams.set('design',d.id);u.hash='design-'+d.id;history.replaceState(null,'',u);}
  async function copyLink(url) {
    try {if(!navigator.clipboard?.writeText)throw new Error('Clipboard unavailable');await navigator.clipboard.writeText(url);$('share-status').textContent='Design link copied.';}
    catch {let input=$('manual-share-link');if(!input){input=element('input',null,{id:'manual-share-link',class:'manual-share-link',readonly:'','aria-label':'Design link to copy'});$('share-status').after(input);}input.value=url;input.focus();input.select();$('share-status').textContent='Select and copy this design link.';}
  }
  async function share() {
    if(sharing||!current)return;sharing=true;$('share-design').disabled=true;const d=current,url=designURL(d.id);
    try {if(navigator.share){try{await navigator.share({title:d.name+' · '+d.id,text:'Explore this tailoring design with Mr Sewing.',url});$('share-status').textContent='Design sharing completed.';}catch(error){if(error.name==='AbortError')$('share-status').textContent='Sharing cancelled.';else await copyLink(url);}}else await copyLink(url);}
    finally {sharing=false;$('share-design').disabled=false;}
  }
  document.querySelector('.show-controls').hidden=false;state=readState();render(false,!state.q&&state.gender===payload.defaultGender&&!state.style&&!state.occasion&&!state.saved);
  $('design-grid').addEventListener('click',e=>{const save=e.target.closest('[data-save]');if(save){setFavourite(save.dataset.save);return;}const a=e.target.closest('[data-open]');if(a){e.preventDefault();openDesign(a.dataset.open,true,a);}});
  let searchTimer;$('design-search').addEventListener('input',()=>{clearTimeout(searchTimer);searchTimer=setTimeout(()=>{state.q=$('design-search').value;apply();},120);});
  for(const [id,key] of [['style-filter','style'],['occasion-filter','occasion']])$(id).addEventListener('change',()=>{state[key]=$(id).value;apply();});
  document.querySelectorAll('[data-gender]').forEach(b=>b.addEventListener('click',()=>{state.gender=b.dataset.gender;apply();}));
  document.querySelectorAll('[data-occasion]').forEach(b=>b.addEventListener('click',()=>{state.occasion=b.dataset.occasion;state.gender='all';apply();$('gallery-heading').scrollIntoView();$('gallery-heading').tabIndex=-1;$('gallery-heading').focus({preventScroll:true});}));
  $('clear-filters').addEventListener('click',reset);$('empty-clear').addEventListener('click',()=>{reset();$('design-search').focus();});
  $('show-saved').addEventListener('click',()=>{state={q:'',style:'',occasion:'',gender:'all',saved:!state.saved};shortlistPage=0;apply();});
  $('next-shortlist').addEventListener('click',()=>{shortlistPage++;shortlist();});
  $('load-more').addEventListener('click',()=>{const count=$('design-grid').children.length;shown+=batch;render(true);const next=$('design-grid').children[count]?.querySelector('a');next?.focus({preventScroll:true});});
  $('close-design').addEventListener('click',closeRequest);dialog.addEventListener('cancel',e=>{e.preventDefault();closeRequest();});
  function finishClose() {if(dialog.open)return;document.body.style.overflow=previousOverflow;current=null;const target=opener?.isConnected?opener:document.querySelector(`[data-open="${returnId}"]`);if(target)target.focus({preventScroll:true});else{$('gallery-heading').tabIndex=-1;$('gallery-heading').focus({preventScroll:true});}}
  dialog.addEventListener('close',finishClose);
  $('design-previous').addEventListener('click',()=>navigate(-1));$('design-next').addEventListener('click',()=>navigate(1));
  for(const [id,delta] of [['photo-previous',-1],['photo-next',1]])$(id).addEventListener('click',()=>{photoIndex=(photoIndex+delta+current.images.length)%current.images.length;showPhoto();});
  $('save-viewer').addEventListener('click',()=>setFavourite(current.id));$('share-design').addEventListener('click',share);
  dialog.addEventListener('keydown',e=>{if(e.key==='ArrowLeft'){e.preventDefault();navigate(-1);}if(e.key==='ArrowRight'){e.preventDefault();navigate(1);}if(e.key==='Tab'){const focusable=[...dialog.querySelectorAll('a[href],button,input,summary')].filter(e=>!e.disabled&&e.getClientRects().length);const first=focusable[0],last=focusable.at(-1);if(e.shiftKey&&document.activeElement===first){e.preventDefault();last.focus();}else if(!e.shiftKey&&document.activeElement===last){e.preventDefault();first.focus();}}});
  let touch;const photo=dialog.querySelector('.design-photo');photo.addEventListener('error',()=>{$('share-status').textContent='The photograph could not be loaded. You can still enquire using its reference.';});photo.addEventListener('touchstart',e=>{touch=e.changedTouches[0];},{passive:true});photo.addEventListener('touchend',e=>{if(!touch)return;const end=e.changedTouches[0],dx=end.clientX-touch.clientX,dy=end.clientY-touch.clientY;touch=null;if(Math.abs(dx)>60&&Math.abs(dx)>Math.abs(dy)*1.3){const delta=dx<0?1:-1;if(current.images.length>1){photoIndex=(photoIndex+delta+current.images.length)%current.images.length;showPhoto();}else navigate(delta);}},{passive:true});
  window.addEventListener('popstate',()=>{const nextState=readState();if(JSON.stringify(nextState)!==JSON.stringify(state)){state=nextState;render();}const id=new URL(location.href).searchParams.get('design');if(id)openDesign(id);else if(dialog.open){dialog.close();finishClose();}});
  window.addEventListener('storage',e=>{if(e.key===key){favourites=stored();if(state.saved)render();else savedUI();}});
  const direct=new URL(location.href).searchParams.get('design');if(direct)openDesign(direct);
})();
