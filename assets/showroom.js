/* R51: filter only the publication-approved, server-rendered media index.
   Selection, consent, fabric and quotation state belong to the existing journey. */
(()=>{'use strict';
 function init(){
  const form=document.getElementById('showroomFilters'),grid=document.getElementById('showroomGrid');if(!form||!grid)return;
  const search=document.getElementById('showroomSearch'),count=document.getElementById('showroomCount'),empty=document.getElementById('showroomEmpty'),clear=document.getElementById('showroomClear');
  const fields=[['audience','showroomAudience'],['garment','showroomGarment'],['style','showroomStyle'],['kind','showroomClass']].map(([key,id])=>({key,control:document.getElementById(id)})).filter(field=>field.control);
  const designLinks=[...grid.querySelectorAll('a.showroom-design-link[href]')].map(link=>({link,originalHref:link.getAttribute('href')}));
  function syncDesignLinks(){const api=window.MrDesignSelections;if(typeof api?.selectionURL!=='function')return;for(const{link,originalHref}of designLinks){try{link.setAttribute('href',api.selectionURL(originalHref));}catch{/* Retain a working original detail link if browser storage is unavailable. */}}}
  document.addEventListener('mrsewing:selectionchange',syncDesignLinks);document.addEventListener('mrsewing:selectionlifetime',syncDesignLinks);syncDesignLinks();
  const cards=[...grid.querySelectorAll('.showroom-card[data-media-id]')];let items=[];
  try{const parsed=JSON.parse(document.getElementById('showroomData')?.textContent||'{}');items=Array.isArray(parsed.items)?parsed.items:[];}catch{/* Server-rendered cards remain usable if optional JSON is unavailable. */}
  const byId=new Map(items.filter(item=>item&&typeof item.mediaId==='string').map(item=>[item.mediaId,item]));
  const fold=value=>String(value||'').normalize('NFC').toLocaleLowerCase().replace(/\s+/g,' ').trim();
  const records=cards.map(card=>{
   const item=byId.get(card.dataset.mediaId)||{};
   return{card,audience:item.audience||card.dataset.audience||'',garment:item.garmentType||card.dataset.garmentType||'',style:Array.isArray(item.styleTags)?item.styleTags:(card.dataset.styleTags||'').split(/\s+/).filter(Boolean),kind:item.classification||card.dataset.classification||'',text:fold([item.originalFilename,item.title,card.textContent,Array.isArray(item.styleTags)?item.styleTags.join(' '):''].filter(Boolean).join(' '))};
  });
  function allowed(control,value){return [...control.options].some(option=>option.value===value)?value:'';}
  function readURL(){
   const params=new URLSearchParams(location.search);for(const{key,control}of fields)control.value=allowed(control,params.get(key)||'');
   if(search)search.value=(params.get('q')||'').slice(0,160);
  }
  function writeURL(method){
   const url=new URL(location.href);for(const{key,control}of fields){if(control.value)url.searchParams.set(key,control.value);else url.searchParams.delete(key);}
   const query=search?.value.trim().slice(0,160)||'';if(query)url.searchParams.set('q',query);else url.searchParams.delete('q');
   const next=url.pathname+url.search+url.hash;if(next!==location.pathname+location.search+location.hash)history[method==='push'?'pushState':'replaceState'](history.state,'',next);
  }
  function apply(method){
   const values=Object.fromEntries(fields.map(({key,control})=>[key,control.value])),words=fold(search?.value).split(' ').filter(Boolean);let visible=0;
   for(const record of records){const matches=(!values.audience||record.audience===values.audience)&&(!values.garment||record.garment===values.garment)&&(!values.style||record.style.includes(values.style))&&(!values.kind||record.kind===values.kind)&&words.every(word=>record.text.includes(word));record.card.hidden=!matches;if(matches)visible++;}
   if(count)count.textContent=visible+' of '+records.length+' '+(records.length===1?'item':'items');
   if(empty)empty.hidden=visible!==0;
   if(method)writeURL(method);
  }
  form.addEventListener('submit',event=>{event.preventDefault();apply('push');});
  for(const{control}of fields)control.addEventListener('change',()=>apply('push'));
  search?.addEventListener('input',()=>apply('replace'));
  clear?.addEventListener('click',event=>{event.preventDefault();for(const{control}of fields)control.value='';if(search)search.value='';apply('push');search?.focus();});
  form.addEventListener('reset',()=>queueMicrotask(()=>apply('push')));
  window.addEventListener('popstate',()=>{readURL();apply();});
  readURL();apply();form.dataset.showroomReady='true';
 }
 if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init,{once:true});else init();
})();
