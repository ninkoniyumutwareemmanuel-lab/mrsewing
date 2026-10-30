/* Collections V3: local filtering and static links; no storage or customer data. */
(() => {
  'use strict';
  const payload=JSON.parse(document.getElementById('showroom-data').textContent), designs=payload.designs;
  const $=id=>document.getElementById(id);let params=new URL(location.href).searchParams;
  const legacy=params.get('design') || (/^#design-(MS-\d+)$/.exec(location.hash)||[])[1];
  if(legacy){const d=designs.find(d=>d.id===legacy);if(d){location.replace(new URL(d.url,location.origin).href);return;}}
  const normalize=s=>String(s).normalize('NFKD').replace(/[\u0300-\u036f]/g,'').toLowerCase();
  const compact=s=>normalize(s).replace(/[^a-z0-9]/g,'');
  let gender=['all','men','women'].includes(params.get('gender'))?params.get('gender'):payload.defaultGender;
  let state={q:(params.get('q')||'').slice(0,160),style:params.get('style')||'',occasion:params.get('occasion')||''},shown=12,matches=[];
  const el=(tag,text,attrs={})=>{const e=document.createElement(tag);if(text!==null)e.textContent=text;for(const [k,v]of Object.entries(attrs))e.setAttribute(k,v);return e;};
  function card(d){
    const a=el('a',null,{class:'design-preview view-details-btn',href:d.url}),i=d.images[0],p=el('picture',null);
    const sizes='(min-width: 1100px) 280px, (min-width: 600px) 30vw, calc((100vw - 52px) / 2)';
    if(i.avif)p.append(el('source',null,{type:'image/avif',srcset:i.avif,sizes}));
    const img=el('img',null,{src:i.thumb,srcset:i.srcset,sizes,alt:i.alt,width:i.width,height:i.height,loading:'lazy',decoding:'async'});img.style.objectPosition=i.position;p.append(img);
    a.append(p,el('span',d.name,{class:'show-card-copy'}));const article=el('article',null,{class:'show-card','data-id':d.id});article.append(a);return article;
  }
  function render(append=false,reuse=false){
    if(!append){shown=12;const q=compact(state.q),tokens=normalize(state.q).split(/[^a-z0-9]+/).filter(Boolean);matches=designs.filter(d=>(gender==='all'||d.gender===gender)&&(!state.style||d.styles.includes(state.style))&&(!state.occasion||d.occasions.includes(state.occasion))&&(!q||compact(d.id)===q||tokens.every(t=>normalize([d.id,d.name,d.gender==='unclassified'?'':d.gender,d.description,d.garmentType,...d.styles,...d.occasions,...d.colors].join(' ')).split(/[^a-z0-9]+/).some(word=>word.startsWith(t)))));if(!reuse)$('design-grid').replaceChildren();}
    const start=append?shown-12:0,frag=document.createDocumentFragment();if(!reuse)matches.slice(start,shown).forEach(d=>frag.append(card(d)));$('design-grid').append(frag);
    $('gallery-status').textContent=`${matches.length} designs · Showing ${Math.min(shown,matches.length)}`;
    if(legacy&&!designs.some(d=>d.id===legacy))$('gallery-status').textContent='This design is unavailable. Explore the collection below.';
    $('gallery-empty').hidden=matches.length>0;$('load-more').hidden=shown>=matches.length;
    if(!matches.length){const occasion=state.occasion.replace(/-/g,' ');$('gallery-empty').querySelector('p').textContent=occasion?'No verified '+occasion+' designs match this selection yet. Discuss your occasion with Mr Sewing or reset the filters.':'Try another search or explore the collection.';$('empty-enquiry').href='https://wa.me/250787411501?text='+encodeURIComponent('Hello Mr Sewing! I would like to discuss '+(occasion||'a tailoring design')+'.\n'+location.href);}
  }
  function apply(){const u=new URL(location.href);if(gender===payload.defaultGender)u.searchParams.delete('gender');for(const [k,v]of Object.entries(state)){if(v)u.searchParams.set(k,v);else u.searchParams.delete(k);}if(u.href!==location.href)history.pushState(null,'',u);render();}
  for(const [key,id]of [['style','style-filter'],['occasion','occasion-filter']]){if(![...$(id).options].some(o=>o.value===state[key]))state[key]='';$(id).value=state[key];$(id).addEventListener('change',()=>{state[key]=$(id).value;apply();});}
  $('design-search').value=state.q;let timer;$('design-search').addEventListener('input',()=>{clearTimeout(timer);timer=setTimeout(()=>{state.q=$('design-search').value;apply();},120);});
  function reset(){clearTimeout(timer);gender=payload.defaultGender;state={q:'',style:'',occasion:''};for(const id of ['design-search','style-filter','occasion-filter'])$(id).value='';apply();}
  $('clear-filters').addEventListener('click',reset);$('empty-clear').addEventListener('click',()=>{reset();$('design-search').focus();});
  $('load-more').addEventListener('click',()=>{const count=$('design-grid').children.length;shown+=12;render(true);$('design-grid').children[count]?.querySelector('a').focus({preventScroll:true});});
  addEventListener('popstate',()=>{clearTimeout(timer);params=new URL(location.href).searchParams;gender=['all','men','women'].includes(params.get('gender'))?params.get('gender'):payload.defaultGender;state={q:(params.get('q')||'').slice(0,160),style:params.get('style')||'',occasion:params.get('occasion')||''};$('design-search').value=state.q;for(const [key,id]of [['style','style-filter'],['occasion','occasion-filter']]){if(![...$(id).options].some(o=>o.value===state[key]))state[key]='';$(id).value=state[key];}render();});
  document.querySelector('.show-controls').hidden=false;render(false,!state.q&&!state.style&&!state.occasion&&gender===payload.defaultGender);
})();
