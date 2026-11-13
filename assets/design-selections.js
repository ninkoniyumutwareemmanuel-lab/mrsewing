/* R46: per-tab, non-personal browsing lifetime; quotation snapshots have independent identities. */
window.MrSelectionSession=function({clean,unpack,pack,getItems,setItems,browsing,cleanPreference,packPreference,unpackPreference}){
 const browseKey='mrsewing-design-selections-v1',metaKey='mrsewing-design-session-v1',quoteKey='mrsewing-quotation-selections-v1',limit=120000;
 const params=new URLSearchParams(location.search),review=location.pathname==='/services/custom-tailoring/selected-designs/';
 let storageOK=true,meta=null,flow=null,mode='browse',timer,departing=false,preference=null;
 const memory=new Map();
 function load(key,fallback){if(!storageOK&&memory.has(key))return memory.get(key)??fallback;try{const raw=sessionStorage.getItem(key);return raw===null?fallback:JSON.parse(raw);}catch{storageOK=false;return memory.get(key)??fallback;}}
 function put(key,value){memory.set(key,value);try{sessionStorage.setItem(key,JSON.stringify(value));}catch{storageOK=false;}}
 function remove(key){memory.set(key,undefined);try{sessionStorage.removeItem(key);}catch{storageOK=false;}}
 function identifier(){return globalThis.crypto?.randomUUID?.()||Date.now().toString(36)+'-'+Math.random().toString(36).slice(2);}
 function metadata(){const value=load(metaKey,null);return value&&typeof value.id==='string'&&['active','closed','expired'].includes(value.status)?value:null;}
 function quotes(){const value=load(quoteKey,{flows:{}});return value&&value.flows&&typeof value.flows==='object'&&!Array.isArray(value.flows)?value:{flows:{}};}
 function storedFlow(id){if(!id||!Object.hasOwn(quotes().flows,id))return null;return quotes().flows[id];}
 function setFlow(id,value){const all=quotes();all.flows[id]=value;put(quoteKey,all);}
 function fresh(rows=[],pref=null){preference=cleanPreference(pref);meta={id:identifier(),status:'active',leftAt:null,expiresAt:null,fabricPreference:preference};mode='browse';flow=null;setItems(clean(rows));put(metaKey,meta);put(browseKey,clean(rows));}
 function expire(){if(meta?.status==='active'&&Number.isFinite(meta.expiresAt)&&Date.now()>=meta.expiresAt){meta={...meta,status:'expired'};put(metaKey,meta);remove(browseKey);if(mode==='browse'){setItems([]);preference=null;}return true;}return false;}
 function schedule(){clearTimeout(timer);if(mode==='browse'&&!browsing()&&meta?.status==='active'&&Number.isFinite(meta.expiresAt))timer=setTimeout(()=>{sync();document.dispatchEvent(new Event('mrsewing:selectionlifetime'));},Math.max(1,meta.expiresAt-Date.now()));}
 function leave(){if(mode!=='browse')return;sync();if(meta?.status==='active'&&!Number.isFinite(meta.expiresAt)){const leftAt=Date.now();meta={...meta,leftAt,expiresAt:leftAt+limit};put(metaKey,meta);}schedule();}
 function sync(force=false){const latest=metadata();if(mode==='browse'){
  const changed=latest?.id!==meta?.id||latest?.status!==meta?.status;meta=latest;
  if(!meta||meta.status!=='active'){setItems([]);preference=null;return;}
  if(expire())return;
  if(force||changed){setItems(clean(load(browseKey,[])));preference=cleanPreference(meta.fabricPreference);}
  if(browsing()&&!departing&&Number.isFinite(meta.expiresAt)){meta={...meta,leftAt:null,expiresAt:null};put(metaKey,meta);}
 }else if(force&&flow){const saved=storedFlow(flow);setItems(saved&&!saved.completed?clean(saved.items):[]);preference=saved&&!saved.completed?cleanPreference(saved.fabricPreference):null;}schedule();}
 function read(){sync();return clean(getItems());}
 function persist(){sync();const rows=clean(getItems());setItems(rows);if(mode==='quote'&&flow){const old=storedFlow(flow);if(old?.completed){setItems([]);return;}setFlow(flow,{...old,sessionId:old?.sessionId||meta?.id||null,items:rows,fabricPreference:preference});}else if(meta?.status==='active'){meta={...meta,fabricPreference:preference};put(metaKey,meta);put(browseKey,rows);}}
 function startAdd(){sync();if(mode!=='browse'||meta?.status!=='active')fresh();}
 function close(rows=read()){
  if(mode==='quote'&&flow)return flow;
  rows=clean(rows);if(!rows.length)return null;
  flow=identifier();setFlow(flow,{sessionId:meta?.id||null,items:rows,fabricPreference:preference});
  if(meta?.status==='active'){meta={...meta,status:'closed',leftAt:null,expiresAt:null,quoteId:flow};put(metaKey,meta);remove(browseKey);}
  mode='quote';setItems(rows);clearTimeout(timer);if(review)history.replaceState(null,'',url(location.pathname+location.search+location.hash));return flow;
 }
 function url(path,rows=read(),edit=false){const u=new URL(path,location.origin);u.searchParams.set('selection',pack(rows));for(const key of ['selectionFlow','selectionEdit','selectionSession'])u.searchParams.delete(key);if(mode==='quote'&&flow)u.searchParams.set(edit?'selectionEdit':'selectionFlow',flow);else if(meta?.id)u.searchParams.set('selectionSession',meta.id);const pref=packPreference(preference);if(pref)u.searchParams.set('sharedFabric',pref);else u.searchParams.delete('sharedFabric');return u.pathname+u.search+u.hash;}
 function fabricPreference(value){if(arguments.length){preference=cleanPreference(value);persist();}else sync();return cleanPreference(preference);}
 function complete(){if(mode==='quote'&&flow){const old=storedFlow(flow);setFlow(flow,{sessionId:old?.sessionId||null,items:[],completed:true});setItems([]);preference=null;}}
 meta=metadata();expire();
 const incomingPreference=unpackPreference(params.get('sharedFabric'));
 const incoming=unpack(params.get('selection')),session=params.get('selectionSession'),edit=params.get('selectionEdit');
 const quotePage=location.pathname==='/services/custom-tailoring/fabric/'&&params.get('multiple')==='1'||location.pathname==='/guides/fabrics/'&&(params.has('fabricFor')||params.get('fabricSelect')==='1')||location.pathname==='/request/'&&params.get('multiple')==='1';
 if(browsing()&&edit){const saved=storedFlow(edit);fresh(saved?(saved.completed?[]:saved.items):incoming,saved?(saved.completed?null:saved.fabricPreference):incomingPreference);const u=new URL(location.href);u.searchParams.delete('selectionEdit');u.searchParams.delete('selectionFlow');u.searchParams.set('selectionSession',meta.id);history.replaceState(null,'',u.pathname+u.search+u.hash);}
 else{
  const requestedFlow=!browsing()&&(params.get('selectionFlow')||(review&&meta?.status==='closed'&&session===meta.id?meta.quoteId:null));
  if(requestedFlow){mode='quote';flow=requestedFlow;let saved=storedFlow(flow);if(!saved&&incoming.length){saved={sessionId:session||null,items:incoming,fabricPreference:incomingPreference};setFlow(flow,saved);}setItems(saved&&!saved.completed?clean(saved.items):[]);preference=saved&&!saved.completed?cleanPreference(saved.fabricPreference):null;}
  else{
   let rows=meta?.status==='active'?clean(load(browseKey,[])):[];
   // Old packed URLs may import only in a genuinely new tab, never over a tombstone/newer session.
   if(!meta){rows=incoming.length?incoming:clean(load(browseKey,[]));if(rows.length)fresh(rows,incomingPreference);else setItems([]);}
   else{setItems(rows);preference=cleanPreference(meta.fabricPreference);if(session===meta.id&&meta.status==='active'&&!rows.length&&incoming.length){setItems(incoming);put(browseKey,incoming);}}
   if(quotePage)close(read());
  }
 }
 if(mode==='browse'){if(browsing())sync();else leave();}
 window.addEventListener('pagehide',()=>{if(browsing()){departing=true;leave();}});
 document.addEventListener('click',e=>{const a=e.target.closest?.('a[href]');if(!a||e.defaultPrevented||a.target==='_blank'||a.hasAttribute('download')||e.ctrlKey||e.metaKey||e.shiftKey||e.altKey)return;const u=new URL(a.href,location.href);if(u.origin!==location.origin||!browsing(u.pathname)){departing=true;leave();}});
 window.addEventListener('pageshow',e=>{departing=false;sync(true);if(e.persisted&&mode==='quote'&&quotePage&&location.pathname!=='/request/'){location.reload();return;}document.dispatchEvent(new Event('mrsewing:selectionlifetime'));});
 document.addEventListener('visibilitychange',()=>{if(!document.hidden){sync();document.dispatchEvent(new Event('mrsewing:selectionlifetime'));}});
 return{read,persist,startAdd,close,url,complete,sync,fabricPreference,isQuote:()=>mode==='quote',storageOK:()=>storageOK};
};

/* Shared enquiry preferences; palette labels are requests, never inventory claims. */
window.MrFabricPreferences=function(source){
 const labels={now:'I Want to Choose a Fabric',advice:'Help Me Choose a Fabric',own:'I Have My Own Fabric'};
 function clean(value){
  if(!value||typeof value!=='object'||!Object.hasOwn(labels,value.choice))return null;
  const out={choice:value.choice,fabricRef:'',colour:'',colourDescription:''};
  if(out.choice==='now'){
   out.fabricRef=Object.hasOwn(source.fabrics,value.fabricRef||'')?value.fabricRef:'';
   out.colour=Object.hasOwn(source.colours||{},value.colour||'')?value.colour:'';
   if(out.colour==='other'&&typeof value.colourDescription==='string'&&value.colourDescription.length<=80&&/^[\p{L}\p{N} .,'’()/+#-]*$/u.test(value.colourDescription))out.colourDescription=value.colourDescription.trim();
  }
  return out;
 }
 function valid(value){const p=clean(value);return !!p&&(p.choice!=='now'||!!p.fabricRef&&!!p.colour&&(p.colour!=='other'||!!p.colourDescription));}
 function details(value){const p=clean(value);return p?{...p,label:labels[p.choice],fabricName:source.fabrics[p.fabricRef]?.name||'',colourName:source.colours?.[p.colour]?.name||''}:null;}
 function pack(value){const p=clean(value);return p?JSON.stringify([p.choice,p.fabricRef,p.colour,p.colourDescription]):'';}
 function unpack(value){try{if(typeof value!=='string'||value.length>600)return null;const a=JSON.parse(value);return Array.isArray(a)&&a.length===4?clean({choice:a[0],fabricRef:a[1],colour:a[2],colourDescription:a[3]}):null;}catch{return null;}}
 return{clean,valid,details,pack,unpack};
};

/* Non-personal quotation selections only. Exact photos/fabrics are validated again on the server. */
(()=>{'use strict';const source=JSON.parse(document.getElementById('designSelectionData')?.textContent||'null');if(!source)return;const params=new URLSearchParams(location.search);let items=[],storageOK=true,bar,announcement,redrawSelectionList;
function resolve(x){const d=source.designs[x?.design];if(!d)return null;const project=x.project?source.projects[x.project]:null;if(x.project&&(!project||project.designRef!==x.design))return null;const photos=project?.images||d.images;const image=photos.find(i=>i.url===x.photo);if(!image)return null;return {...x,name:project?.name||d.name,route:project?.route||d.route,category:project?.category||d.audience,src:image.src,alt:image.alt,width:image.width,height:image.height};}
function clean(rows){if(!Array.isArray(rows))return[];const seen=new Set();return rows.map(x=>{const d=resolve(x);if(!d||seen.has(d.photo))return null;seen.add(d.photo);return{design:d.design,photo:d.photo,project:d.project||null,quantity:/^[1-9]\d{0,3}$/.test(String(d.quantity))?Number(d.quantity):1,fabricChoice:['now','advice','own'].includes(d.fabricChoice)?d.fabricChoice:'advice',fabricRef:typeof d.fabricRef==='string'?d.fabricRef:''};}).filter(Boolean);}
function unpack(value){try{return clean(JSON.parse(value).map(a=>{const d=source.designs[a[0]],p=a[2]?source.projects[a[2]]:null,image=(p?.images||d?.images||[])[a[1]];return{design:a[0],photo:image?.url,project:a[2],quantity:a[3],fabricChoice:a[4],fabricRef:a[5]};}));}catch{return[];}}
function browsing(path=location.pathname){return path==='/services/custom-tailoring/'||path.startsWith('/mensuits/')||path.startsWith('/womensuits/')||path.startsWith('/collections/designs/')&&Object.values(source.designs).some(d=>d.route===path);}
function pack(rows){return JSON.stringify(clean(rows).map(x=>{const d=source.designs[x.design],p=x.project?source.projects[x.project]:null;return[x.design,(p?.images||d.images).findIndex(i=>i.url===x.photo),x.project,x.quantity,x.fabricChoice,x.fabricRef];}));}
const preferences=window.MrFabricPreferences(source);
const lifetime=window.MrSelectionSession({clean,unpack,pack,getItems:()=>items,setItems:rows=>{items=rows;},browsing,cleanPreference:preferences.clean,packPreference:preferences.pack,unpackPreference:preferences.unpack});
function read(){return lifetime.read();}
function packed(){return pack(read());}
function url(path){return lifetime.url(path);}
function save(){lifetime.persist();storageOK=lifetime.storageOK();if(document.querySelector('[data-selection-list]')||params.get('multiple')==='1'&&document.getElementById('fabricChoiceForm'))history.replaceState(null,'',url(location.pathname+location.search+location.hash));refresh();document.dispatchEvent(new Event('mrsewing:selectionchange'));}
function add(x){const d=resolve(x);if(!d)return false;lifetime.startAdd();if(!items.some(y=>y.photo===d.photo))items.push({design:x.design,photo:x.photo,project:x.project,quantity:1,fabricChoice:'advice',fabricRef:''});save();return true;}
function batch(){return params.get('multiple')==='1'&&!!document.getElementById('customerRequestForm');}
function isSelectedQuote(){const f=document.getElementById('customerRequestForm');return !!f&&f.dataset.kind==='quotation'&&f.dataset.special!=='true'&&params.get('general')!=='1'&&document.getElementById('requestService')?.value==='custom-tailoring'&&document.getElementById('requestOrder')?.value==='standard'&&(batch()||!!window.MrSelectedDesign?.resolve(window.mrRequestContext?.read()||{}));}
function quoteRows(){if(lifetime.isQuote()||batch())return read();const state=window.mrRequestContext?.read()||{},r=window.MrSelectedDesign?.resolve(state);return r?clean([{design:state.design,photo:r.photoURL,project:state.project,quantity:Number(document.getElementById('requestQuantity')?.value)||1,fabricChoice:state.fabricChoice,fabricRef:state.fabricRef||''}]):[];}
function quoteSnapshot(){return quoteRows().map(x=>{const r=resolve(x);return{...r,name:friendly(r.name),fabricName:x.fabricChoice==='own'?'I Have My Own Fabric':x.fabricChoice==='advice'?'Help Me Choose Fabric':source.fabrics[x.fabricRef]?.name||'Choose Fabric'};});}
function quoteURL(path){const rows=quoteRows();lifetime.close(rows);return lifetime.url(path,rows,browsing(new URL(path,location.origin).pathname));}
function fabricPreference(){return lifetime.fabricPreference();}
function fabricPreferenceDetails(){return preferences.details(fabricPreference());}
function setFabricPreference(value){const p=preferences.clean(value);if(!p)return false;items=read();for(const row of items){row.fabricChoice=p.choice;row.fabricRef=p.fabricRef;}lifetime.fabricPreference(p);save();return true;}
function ensureQuote(){if(!read().length&&!lifetime.isQuote()&&!params.has('selection')&&!params.has('selectionFlow')&&params.get('multiple')!=='1'&&params.has('design')){const c=window.mrRequestContext?.read()||{},r=window.MrSelectedDesign?.resolve(c);if(r)items=clean([{design:c.design,photo:r.photoURL,project:c.project,quantity:1,fabricChoice:c.fabricChoice,fabricRef:c.fabricRef}]);}lifetime.close(read());return read();}
function quotationURL(){const rows=ensureQuote(),first=rows[0];if(!first)return url('/request/?multiple=1');const c={service:'custom-tailoring',order:'standard',design:first.design,photo:first.photo,project:first.project||undefined,fabricChoice:first.fabricChoice,fabricRef:first.fabricRef||undefined};window.mrRequestContext?.update(c);const u=new URL(url('/request/?multiple=1'),location.origin);for(const [k,v]of Object.entries(c))if(v)u.searchParams.set(k,v);return u.pathname+u.search;}
function decorate(d){if(!isSelectedQuote()||d.Service!=='Custom Tailoring & Suits')return d;const rows=quoteRows(),first=rows[0];d['Selected Design Count']=String(rows.length);d.Quantity=String(rows.reduce((n,x)=>n+x.quantity,0));d['Total Garments']=d.Quantity;d['Selected Designs']=rows.map((x,i)=>{const r=resolve(x);return(i+1)+'. '+friendly(r.name)+' | Quantity: '+x.quantity+' | '+x.photo+' | Fabric: '+(x.fabricChoice==='own'?'I have my own fabric':x.fabricChoice==='advice'?'Help me choose fabric':(source.fabrics[x.fabricRef]?.name||'Choose fabric'));}).join('\n');for(const k of ['Order Priority','After-hours Request','Garment Type','Other Garment','Fabric Preferences','Preferred Date','Preferred Time','Fabric Reference','Selected Fabric','Fabric Category','Fabric Tier','Fabric Preference','Fabric Assistance'])delete d[k];if(first){const r=resolve(first);d['Design Reference']=first.design;d['Selected Photograph URL']=first.photo;d['Design Image']=first.photo;d['Design Name']=friendly(r.name);d['Design Link']=new URL(r.route,'https://mrsewingfashion.com').href;d['Fabric Choice']=first.fabricChoice==='now'?'Customer fabric choice':first.fabricChoice==='own'?'Customer-Supplied Fabric':'Help Me Choose Fabric';if(first.fabricChoice==='now')d['Fabric Reference']=first.fabricRef;if(first.project)d['Portfolio Reference']=first.project;}const pref=fabricPreferenceDetails();if(pref){d['Shared Fabric Preference']=pref.label;d['Fabric Preference Scope']='Whole selected-design enquiry; suitability assessed for each garment';d['Fabric Choice']=pref.choice==='now'?'Customer fabric choice':pref.choice==='own'?'Customer-Supplied Fabric':'Help Me Choose Fabric';for(const key of ['Selected Fabric','Fabric Reference','Fabric Preference','Fabric Assistance','Fabric Category','Fabric Tier'])delete d[key];if(pref.choice==='now'){d['Selected Fabric']=pref.fabricName;d['Fabric Reference']=pref.fabricRef;d['Preferred Colour']=pref.colourName+(pref.colourDescription?' — '+pref.colourDescription:'');d['Preferred Colour Reference']=pref.colour;if(pref.colourDescription)d['Colour Description']=pref.colourDescription;}else if(pref.choice==='own')d['Fabric Preference']='Customer-Supplied Fabric';else d['Fabric Assistance']='Requested';d['Selected Designs']=rows.map((x,i)=>(i+1)+'. '+friendly(resolve(x).name)+' | Quantity: '+x.quantity+' | '+x.photo).join('\n');}d['Requested Completion Time Zone']='Africa/Kigali (UTC+02:00)';return d;}
function submission(){return isSelectedQuote()?quoteRows():undefined;}
function review(dl){if(isSelectedQuote())window.MrSelectedSuitQuote?.review(dl);}
function friendly(name){return String(name).replace(/\s*[—·-]\s*MS-\d+\b/g,'').trim();}
function sharingSnapshot(){return read().map(x=>{const r=resolve(x);return{...r,name:friendly(r.name)};});}
window.MrDesignSelections={read,add,fabricPreference,fabricPreferenceDetails,setFabricPreference,fabricPreferenceValid:()=>!fabricPreference()||preferences.valid(fabricPreference()),quotationURL,editSelectionsURL:()=>quoteURL('/services/custom-tailoring/'),decorate,submission,review,sharingSnapshot,quoteRows,quoteSnapshot,isSelectedQuote,selectionURL:path=>isSelectedQuote()?quoteURL(path):url(path),isBatch:batch,fabricMode:!!document.getElementById('fabricChoiceForm')};
function refresh(){const allowed=browsing();const count=read().length;document.documentElement.classList.toggle('has-selected-designs',!!count&&allowed);if(bar){bar.hidden=!count||!allowed;bar.href=url('/services/custom-tailoring/selected-designs/');bar.querySelector('[data-selected-count]').textContent=count+' '+(count===1?'Design':'Designs')+' Selected';}for(const b of document.querySelectorAll('[data-select-design]')){const d=source.designs[b.dataset.selectDesign],u=new URL(b.href||location.href,location.origin);const photo=u.searchParams.get('photo')||d?.images[0]?.url;const selected=items.some(x=>x.design===b.dataset.selectDesign&&x.photo===photo);b.setAttribute('aria-pressed',String(selected));b.textContent=selected?'Design Selected ✓':'Select This Design';}}
document.addEventListener('mrsewing:selectionlifetime',()=>{refresh();redrawSelectionList?.();if(isSelectedQuote())window.MrSelectedSuitQuote?.refresh();});
document.addEventListener('DOMContentLoaded',()=>{if(isSelectedQuote())lifetime.close(quoteRows());const current=document.getElementById('design-data');if(current){const d=JSON.parse(current.textContent).design;const button=document.querySelector('.design-enquiry');if(button){button.dataset.selectDesign=d.id;button.setAttribute('role','button');button.addEventListener('keydown',e=>{if(e.key===' '){e.preventDefault();button.click();}});}}
bar=document.createElement('a');bar.className='selected-design-bar';bar.hidden=true;bar.href='/services/custom-tailoring/selected-designs/';bar.innerHTML='<span data-selected-count></span><span>Review Your Designs <span aria-hidden="true">→</span></span>';announcement=document.createElement('p');announcement.className='visually-hidden';announcement.dataset.selectionAnnouncement='';announcement.setAttribute('role','status');announcement.setAttribute('aria-live','polite');announcement.setAttribute('aria-atomic','true');document.body.append(bar,announcement);refresh();
for(const b of document.querySelectorAll('[data-select-design]'))b.addEventListener('click',e=>{e.preventDefault();const d=source.designs[b.dataset.selectDesign],u=new URL(b.href||location.href,location.origin),ctx=window.mrRequestContext?.read()||{};const project=u.searchParams.get('project')||(ctx.design===d.id?ctx.project:null);const photo=u.searchParams.get('photo')||(ctx.design===d.id?ctx.photo:null)||d.images[0].url;if(add({design:d.id,photo,project})){announcement.textContent='Added. Keep browsing or review your selections.';if(!storageOK)announcement.textContent='Use Selected Designs to continue with these selections; browser storage is unavailable.';}});
const list=document.querySelector('[data-selection-list]');if(list){function draw(){list.replaceChildren();if(!read().length){list.textContent='No designs selected yet. Return to the suit galleries to select your designs.';}for(const x of read()){const r=resolve(x),article=document.createElement('article'),h=document.createElement('h2'),a=document.createElement('a'),image=document.createElement('img'),label=document.createElement('label'),q=document.createElement('input'),remove=document.createElement('button');h.textContent=friendly(r.name);a.href=new URL(r.src,location.origin).href;a.target='_blank';a.rel='noopener';a.className='selection-photo';a.setAttribute('aria-label','View selected photograph of '+friendly(r.name));image.src=r.src;image.alt=r.alt;image.width=r.width;image.height=r.height;image.loading='lazy';image.decoding='async';a.append(image);label.textContent='Garment quantity';q.type='number';q.min='1';q.max='9999';q.value=x.quantity;q.required=true;label.append(q);q.addEventListener('change',()=>{if(q.reportValidity()){items.find(y=>y.photo===x.photo).quantity=Number(q.value);save();announcement.textContent='Quantity updated for '+friendly(r.name)+'.';}});remove.type='button';remove.className='home-button';remove.textContent='Remove Design';remove.addEventListener('click',()=>{const index=read().findIndex(y=>y.photo===x.photo);items=items.filter(y=>y.photo!==x.photo);save();draw();announcement.textContent=friendly(r.name)+' removed. '+read().length+' designs selected.';const controls=list.querySelectorAll('button');if(controls.length)controls[Math.min(index,controls.length-1)].focus();else{list.tabIndex=-1;list.focus();}});article.append(a,h,label,remove);list.append(article);}const next=document.querySelector('[data-selected-continue]');next.hidden=!items.length;next.href=url('/services/custom-tailoring/fabric/?multiple=1');const actions=document.querySelector('[data-selection-actions]');if(actions)actions.hidden=!items.length;const browse=document.querySelector('[data-selection-list] + p a');if(browse&&lifetime.isQuote())browse.href=lifetime.url('/services/custom-tailoring/',read(),true);}redrawSelectionList=draw;draw();const next=document.querySelector('[data-selected-continue]');next.addEventListener('click',e=>{const rows=read();if(!rows.length){e.preventDefault();draw();announcement.textContent='Your unfinished selections have expired. Please select your designs again.';return;}lifetime.close(rows);next.href=url('/services/custom-tailoring/fabric/?multiple=1');refresh();});}
if(document.getElementById('fabricChoiceForm')||location.pathname==='/guides/fabrics/'&&(params.has('fabricFor')||params.get('fabricSelect')==='1'))ensureQuote();
window.MrFabricJourney?.({api:window.MrDesignSelections,source,resolve,friendly,url,ensureQuote,preferences});
for(const a of document.querySelectorAll('[data-edit-designs]')){a.href=isSelectedQuote()?quoteURL('/services/custom-tailoring/'):storageOK?'/services/custom-tailoring/':url('/services/custom-tailoring/');a.addEventListener('click',()=>{if(isSelectedQuote()){a.href=quoteURL('/services/custom-tailoring/');return;}if(!batch()&&!items.length){const s=window.mrRequestContext?.read()||{},d=window.MrSelectedDesign?.resolve(s);if(d)add({design:s.design,photo:d.photoURL,project:s.project});}a.href=storageOK?'/services/custom-tailoring/':url('/services/custom-tailoring/');});}
if(isSelectedQuote()){const success=document.getElementById('requestSuccess');if(success)new MutationObserver(()=>{if(!success.hidden){lifetime.complete();refresh();const u=new URL(location.href);u.searchParams.delete('selection');u.searchParams.delete('multiple');history.replaceState(null,'',u.pathname+u.search+u.hash);}}).observe(success,{attributes:true,attributeFilter:['hidden']});}
});
})();

/* Existing ordinary-suit journey: one shared preference, fabric and illustrative colour. */
window.MrFabricJourney=function({api,source,resolve,friendly,url,ensureQuote,preferences}){
 const form=document.getElementById('fabricChoiceForm'),params=new URLSearchParams(location.search);
 const picking=location.pathname==='/guides/fabrics/'&&(params.get('fabricSelect')==='1'||params.has('fabricFor'));
 if(!form&&!picking){if(location.pathname==='/guides/fabrics/')document.body.classList.add('fabric-guide-page');return;}
 const rows=ensureQuote();
 function designs(parent){
  window.MrSelectedSuitQuote?.renderDesignSummary(parent);
  const edit=document.createElement('a');edit.className='home-text-link';edit.textContent='Add or Change Designs';edit.href=api.editSelectionsURL();parent.append(edit);
 }
 function empty(parent){const note=document.createElement('p');note.className='guide-notice';note.textContent='No designs selected. Choose a suit design to continue with fabric preferences.';const link=document.createElement('a');link.href='/services/custom-tailoring/';link.className='home-button home-button-gold';link.textContent='Explore Suit Designs';parent.append(note,link);}
 if(form){
  document.body.classList.add('fabric-preference-page');const summary=document.querySelector('[data-shared-design-summary]');
  if(!rows.length){form.hidden=true;empty(summary);return;}designs(summary);
  const button=form.querySelector('[type=submit]'),status=document.getElementById('fabric-choice-status'),current=api.fabricPreference();
  for(const radio of form.querySelectorAll('[name=sharedFabricChoice]'))radio.checked=current?.choice===radio.value;
  function selected(){return form.querySelector('[name=sharedFabricChoice]:checked')?.value;}
  function sync(){const choice=selected();button.textContent=choice==='now'?'Continue to Fabric Selection':choice?'Continue to Quotation':'Continue';if(choice){const old=api.fabricPreference();api.setFabricPreference({choice,fabricRef:choice==='now'?old?.fabricRef||'':'',colour:choice==='now'?old?.colour||'':'',colourDescription:choice==='now'?old?.colourDescription||'':''});}status.textContent='';}
  form.addEventListener('change',sync);sync();
  form.addEventListener('submit',event=>{event.preventDefault();if(!form.reportValidity())return;sync();location.href=selected()==='now'?url('/guides/fabrics/?fabricSelect=1&multiple=1'):api.quotationURL();});
  return;
 }
 document.body.classList.add('fabric-guide-page');const collection=document.querySelector('.guide-collection');if(!collection)return;
 const panel=document.createElement('section');panel.className='fabric-selection-context';panel.setAttribute('aria-label','Fabric and colour selection');collection.before(panel);
 if(!rows.length){empty(panel);return;}
 const heading=document.createElement('h2'),instruction=document.createElement('p'),summary=document.createElement('div');heading.textContent='Choose a Fabric and Colour';instruction.textContent='Select one preferred fabric and colour for your enquiry. We assess suitability for each garment.';panel.append(heading,instruction);summary.className='fabric-selection-designs';designs(summary);panel.append(summary);
 const selected=document.createElement('div');selected.className='fabric-choice-confirmation';selected.setAttribute('aria-live','polite');panel.append(selected);
 const colourForm=document.createElement('form');colourForm.id='sharedFabricColourForm';colourForm.setAttribute('aria-label','Preferred fabric colour');
 const fieldset=document.createElement('fieldset'),legend=document.createElement('legend');legend.textContent='Preferred Colour — Subject to Availability Confirmation';fieldset.append(legend);
 const note=document.createElement('p');note.className='request-note';note.id='fabric-colour-note';note.textContent='Swatches are illustrative and may differ from the actual fabric shade. These are colour preferences, not confirmed stock.';fieldset.append(note);
 const groupNames={neutral:'Neutral colours',blue:'Blue shades','red-purple':'Red and purple','earth-green':'Earth and green',other:'Another colour'};
 for(const [group,title]of Object.entries(groupNames)){
  const section=document.createElement('section'),h=document.createElement('h3'),grid=document.createElement('div');h.textContent=title;grid.className='fabric-colour-grid';
  for(const [id,colour]of Object.entries(source.colours).filter(([,c])=>c.group===group)){
   const label=document.createElement('label'),input=document.createElement('input'),swatch=document.createElement('span'),name=document.createElement('span');label.className='fabric-colour-option';input.type='radio';input.name='preferredColour';input.value=id;input.required=true;input.setAttribute('aria-describedby','fabric-colour-note');swatch.className='fabric-colour-swatch';swatch.setAttribute('aria-hidden','true');if(colour.hex)swatch.style.backgroundColor=colour.hex;else{swatch.classList.add('fabric-colour-other');swatch.textContent='?';}name.className='fabric-colour-name';name.textContent=colour.name;label.append(input,swatch,name);grid.append(label);
  }section.append(h,grid);fieldset.append(section);
 }
 const other=document.createElement('div'),otherLabel=document.createElement('label'),description=document.createElement('input');other.className='fabric-colour-description';otherLabel.htmlFor='colourDescription';otherLabel.textContent='Describe your preferred colour (up to 80 characters)';description.id='colourDescription';description.name='colourDescription';description.maxLength=80;description.autocomplete='off';other.append(otherLabel,description);fieldset.append(other);colourForm.append(fieldset);
 const status=document.createElement('p');status.id='fabric-colour-status';status.setAttribute('role','status');status.setAttribute('aria-live','polite');const button=document.createElement('button');button.type='submit';button.className='home-button home-button-gold';button.dataset.fabricContinue='';button.textContent='Continue to Quotation';const edit=document.createElement('a');edit.className='home-text-link';edit.href=url('/services/custom-tailoring/fabric/?multiple=1');edit.textContent='Edit Fabric Preference';const actions=document.createElement('div');actions.className='request-actions';actions.append(button,edit);colourForm.append(status,actions);
 // Keep fabric cards first, then the colour selector in the same existing guide.
 collection.after(colourForm);
 function descriptionValid(){const text=description.value.trim(),valid=!!text&&text.length<=80&&/^[\p{L}\p{N} .,'’()/+#-]{1,80}$/u.test(text);description.setCustomValidity(valid?'':'Describe the colour using up to 80 letters, numbers and basic colour punctuation.');return valid;}
 function paint(){
  const pref=api.fabricPreference(),details=api.fabricPreferenceDetails();selected.replaceChildren();
  for(const [label,value]of [['Selected Fabric',details?.choice==='now'&&details.fabricName?details.fabricName:'Choose a fabric below'],['Preferred Colour',details?.colourName?(details.colourName+(details.colourDescription?' — '+details.colourDescription:'')):'Choose a colour below']]){const p=document.createElement('p'),strong=document.createElement('strong');strong.textContent=label+': ';p.append(strong,document.createTextNode(value));selected.append(p);}
  fieldset.disabled=!pref?.fabricRef||pref.choice!=='now';other.hidden=pref?.colour!=='other';description.required=!other.hidden;description.disabled=other.hidden;description.setCustomValidity('');
  for(const radio of colourForm.querySelectorAll('[name=preferredColour]'))radio.checked=pref?.colour===radio.value;
  for(const b of collection.querySelectorAll('[data-pick-fabric]')){const active=pref?.fabricRef===b.dataset.pickFabric;b.setAttribute('aria-pressed',String(active));b.textContent=active?'Fabric Selected ✓':'Select This Fabric';}
 }
 description.value=api.fabricPreference()?.colourDescription||'';
 for(const card of collection.querySelectorAll('[data-fabric-id]')){
  const id=card.dataset.fabricId;if(!Object.hasOwn(source.fabrics,id))continue;const choose=document.createElement('button');choose.type='button';choose.className='home-button home-button-gold';choose.dataset.pickFabric=id;choose.textContent='Select This Fabric';choose.addEventListener('click',()=>{const previous=api.fabricPreference();api.setFabricPreference({choice:'now',fabricRef:id,colour:previous?.choice==='now'?previous.colour:'',colourDescription:previous?.choice==='now'?previous.colourDescription:''});status.textContent='';paint();colourForm.scrollIntoView({block:'start',behavior:'instant'});legend.tabIndex=-1;legend.focus({preventScroll:true});});card.querySelector('.fabric-card-copy').append(choose);
 }
 colourForm.addEventListener('change',event=>{if(event.target.name!=='preferredColour')return;const pref=api.fabricPreference();if(!pref?.fabricRef)return;api.setFabricPreference({...pref,colour:event.target.value,colourDescription:event.target.value==='other'?description.value:''});status.textContent='';paint();if(event.target.value==='other')description.focus();});
 description.addEventListener('input',()=>{const pref=api.fabricPreference();if(pref?.colour==='other'){descriptionValid();api.setFabricPreference({...pref,colourDescription:description.value});}});
 colourForm.addEventListener('submit',event=>{event.preventDefault();const pref=api.fabricPreference();if(!pref?.fabricRef){status.textContent='Select a fabric before choosing your preferred colour.';collection.querySelector('[data-pick-fabric]')?.focus();return;}if(pref.colour==='other'&&!descriptionValid()){description.reportValidity();return;}if(!colourForm.reportValidity()||!preferences.valid(pref)){status.textContent='Choose one preferred colour to continue.';return;}location.href=api.quotationURL();});paint();
};

/* R48: selected-suit quotation presentation. Existing flow snapshots and submission remain authoritative. */
(()=>{'use strict';
 const get=id=>document.getElementById(id);
 const active=()=>!!window.MrDesignSelections?.isSelectedQuote?.();
 const rows=()=>window.MrDesignSelections?.quoteSnapshot?.()||[];
 const friendly=name=>String(name||'').replace(/\s*[—·-]\s*MS-\d+\b/g,'').trim();
 function selectionURL(path){return window.MrDesignSelections?.selectionURL?.(path)||path;}
 function preferenceDetails(){
  const shared=window.MrDesignSelections?.fabricPreferenceDetails?.();if(shared)return shared;
  // Preserve supported older request URLs without pretending different legacy choices are one fabric.
  const selected=rows(),first=selected[0];if(!first)return{choice:'advice',label:'Help Me Choose Fabric'};
  const choices=new Set(selected.map(row=>[row.fabricChoice,row.fabricRef||''].join('|')));
  if(choices.size>1)return{choice:'legacy',label:'Existing fabric preferences',legacy:true};
  return{choice:first.fabricChoice,label:first.fabricChoice==='own'?'I Have My Own Fabric':first.fabricChoice==='advice'?'Help Me Choose Fabric':'Selected fabric',fabricName:first.fabricChoice==='now'?first.fabricName:'',colourName:''};
 }
 function summary(parent,{review=false}={}){
  const selected=rows(),total=selected.reduce((n,row)=>n+Number(row.quantity||row.qty||1),0);
  const section=document.createElement('section');section.className='selected-quote-block';
  const heading=document.createElement(review?'h3':'h2');heading.textContent='Your Selected Designs';section.append(heading);
  const details=document.createElement('details');details.className='selected-quote-summary';
  const trigger=document.createElement('summary'),count=document.createElement('span'),view=document.createElement('span');
  count.className='selected-quote-count';count.textContent=selected.length+' '+(selected.length===1?'design':'designs')+' selected · '+total+' '+(total===1?'garment':'garments');view.className='selected-quote-view';view.textContent='View Selected Designs';trigger.append(count,view);details.append(trigger);
  const grid=document.createElement('section');grid.className='batch-design-summary';grid.setAttribute('aria-label','Selected suit photographs and quantities');
  for(const row of selected){
   const item=document.createElement('article');item.dataset.designId=row.design;
   const photograph=document.createElement('a'),image=document.createElement('img'),copy=document.createElement('div'),name=document.createElement('h3'),quantity=document.createElement('p');
   photograph.href=new URL(row.src,location.origin).href;photograph.target='_blank';photograph.rel='noopener';photograph.className='selected-quote-photo';photograph.setAttribute('aria-label','View selected photograph of '+friendly(row.name));
   image.src=row.src;image.alt=friendly(row.alt||row.name);if(row.width)image.width=row.width;if(row.height)image.height=row.height;image.loading='lazy';image.decoding='async';photograph.append(image);
   name.textContent=friendly(row.name);quantity.textContent='Quantity: '+Number(row.quantity||row.qty||1);copy.append(name,quantity);item.append(photograph,copy);grid.append(item);
  }
  if(!selected.length){const empty=document.createElement('p');empty.textContent='No designs selected. Add a design before continuing.';grid.append(empty);}
  details.append(grid);section.append(details);parent.append(section);return section;
 }
 function preferenceSummary(parent,{review=false,edit=null}={}){
  const details=preferenceDetails(),section=document.createElement('section'),heading=document.createElement(review?'h3':'h2'),values=document.createElement('dl');
  section.className='selected-quote-block selected-quote-preference';heading.textContent='Your Fabric and Colour Preference';section.append(heading);
  function value(label,text){const term=document.createElement('dt'),definition=document.createElement('dd');term.textContent=label;definition.textContent=text;values.append(term,definition);}
  if(details.choice==='now'){
   value('Selected Fabric',details.fabricName||details.label||'Selected fabric');
   value('Preferred Colour',details.colourName?(details.colourName+(details.colourDescription?' — '+details.colourDescription:'')):'Not specified');
  }else value('Fabric Preference',details.label||(details.choice==='own'?'I Have My Own Fabric':'Help Me Choose Fabric'));
  section.append(values);
  const note=document.createElement('p');note.className='selected-preference-note';note.textContent=details.legacy?'Your existing fabric choices are retained. You can edit one shared preference for this enquiry.':'Applies to this enquiry, subject to fabric suitability, colour and availability confirmation for each garment.';section.append(note);
  if(edit){edit.href=selectionURL('/services/custom-tailoring/fabric/?multiple=1');edit.textContent='Edit Fabric Preference';edit.dataset.selectedFabricEdit='';const nav=document.createElement('nav');nav.className='selected-quote-edit';nav.setAttribute('aria-label','Edit fabric and colour preference');nav.append(edit);section.append(nav);}
  parent.append(section);return section;
 }
 function hide(node){if(!node)return;node.classList.add('selected-quote-hidden');node.hidden=true;for(const field of node.matches('input,select,textarea')?[node]:node.querySelectorAll('input,select,textarea')){field.disabled=true;field.required=false;field.setCustomValidity('');}}
 function hideField(id){const field=get(id);if(!field)return;const row=field.closest('.request-fields>div');if(row){hide(row);return;}for(const label of document.querySelectorAll('label[for="'+id+'"]'))hide(label);hide(field);if(field.parentElement?.matches('label'))hide(field.parentElement);}
 function labelFor(id,text){const label=document.querySelector('label[for="'+id+'"]');if(label)label.textContent=text;}
 function inputRow(id,label,name,type='text'){
  const row=document.createElement('div'),caption=document.createElement('label'),input=document.createElement('input');caption.htmlFor=id;caption.textContent=label+' (required)';input.id=id;input.name=name;input.type=type;input.required=true;input.addEventListener('input',()=>input.setCustomValidity(''));row.append(caption,input);return row;
 }
 function refresh(){
  if(!active())return;const form=get('customerRequestForm');if(!form)return;
  let holder=form.querySelector('[data-selected-quote-holder]');if(!holder){holder=document.createElement('div');holder.dataset.selectedQuoteHolder='';const anchor=form.querySelector('fieldset');if(anchor)anchor.before(holder);else form.prepend(holder);}
  const existingEdit=form.querySelector('[data-edit-designs]'),existingFabric=form.querySelector('[data-selected-fabric-edit]');
  const wasOpen=holder.querySelector('.selected-quote-summary')?.open||false;holder.replaceChildren();const block=summary(holder);block.querySelector('.selected-quote-summary').open=wasOpen;
  const nav=document.createElement('nav');nav.className='selected-quote-edit';nav.setAttribute('aria-label','Edit selected designs');
  let edit=existingEdit;if(!edit){edit=document.createElement('a');edit.dataset.editDesigns='';edit.textContent='Add or Change Designs';}edit.href=selectionURL('/services/custom-tailoring/');nav.append(edit);block.append(nav);
  const fabric=existingFabric||document.createElement('a');preferenceSummary(holder,{edit:fabric});
  const quantity=get('requestQuantity');if(quantity){quantity.value=rows().reduce((n,row)=>n+Number(row.quantity||row.qty||1),0);quantity.readOnly=true;hide(quantity.closest('.request-fields>div')||quantity);}
 }
 function apply(){
  if(!active())return;const form=get('customerRequestForm');if(!form)return;
  const first=form.dataset.selectedSuitReady!=='true';form.classList.add('selected-suit-quote');document.body.classList.add('selected-suit-quotation-page');
  const intro=document.querySelector('main .release-intro');if(intro){const heading=intro.querySelector('h1'),copy=intro.querySelector('p:last-child');if(heading)heading.textContent='Your Quotation Request';if(copy&&copy!==intro.querySelector('.home-eyebrow'))copy.textContent='Review your selections and tell us when you need your garments.';}
  const progress=document.querySelector('.request-progress');if(progress&&first){progress.replaceChildren(...['Your selections','Contact details & deadline','Review & submit'].map(text=>{const li=document.createElement('li');li.textContent=text;return li;}));}
  // Keep the existing source-of-truth inputs and listeners; remove their duplicated presentation only.
  const originalEdit=form.querySelector('[data-edit-designs]');if(originalEdit&&originalEdit.closest('[data-standard-design]'))form.append(originalEdit);
  for(const id of['requestPriority','requestAfterHours','requestGarment','requestOtherGarment','requestFabric','requestFabricChoice','requestFabricSelection','requestMeasurements'])hideField(id);
  hide(get('priority-guidance'));hide(get('requestFabricReferenceField'));hide(get('selectedDesignPreview'));hide(get('portfolioRequestContext'));hide(get('request-title'));hide(get('request-guidance'));
  const context=get('requestContextSummary');if(context)hide(context);
  const system=form.querySelector('fieldset:not(.selected-quote-deadline)');if(system&&!system.querySelector('#requestName')){system.classList.add('selected-quote-system');const legend=system.querySelector('legend');if(legend)hide(legend);}
  for(const node of form.querySelectorAll('[data-standard-design]'))hide(node);
  for(const id of['requestFabricChoice','requestFabric']){const block=get(id)?.closest('[data-custom-only]');if(block)hide(block);}
  const fields=form.querySelector('.request-fields');if(fields&&!get('selected-contact-heading')){const heading=document.createElement('h2');heading.id='selected-contact-heading';heading.className='selected-form-heading';heading.textContent='Contact and Delivery Details';fields.prepend(heading);}
  const location=get('requestLocation');if(location){location.name='Delivery Location / Address';location.maxLength=500;location.required=true;location.autocomplete='street-address';labelFor('requestLocation','Delivery location / address (required)');}
  labelFor('requestName','Full name (required)');labelFor('requestPhone','Phone / WhatsApp number (required)');labelFor('requestEmail','Email address (optional)');
  if(!get('requestCountry')){const row=inputRow('requestCountry','Country','Country'),input=row.querySelector('input');input.maxLength=160;input.autocomplete='country-name';const address=location?.closest('.request-fields>div');if(address)address.before(row);else fields?.append(row);}
  const date=get('requestDate');if(date){date.name='Requested Completion Date';date.required=true;date.disabled=false;date.setAttribute('aria-describedby','selected-deadline-guidance selected-deadline-zone');labelFor('requestDate','Completion date (required)');}
  if(!get('selected-quote-deadline')){
   const group=document.createElement('fieldset');group.id='selected-quote-deadline';group.className='selected-quote-deadline';const legend=document.createElement('legend');legend.textContent='When Do You Need Your Garments?';group.append(legend);
   const controls=document.createElement('div');controls.className='selected-deadline-controls';const dateRow=date?.closest('.request-fields>div');if(dateRow){dateRow.before(group);controls.append(dateRow);}else fields?.append(group);
   const timeRow=inputRow('requestCompletionTime','Completion time (Kigali)','Requested Completion Time','time'),time=timeRow.querySelector('input');time.step='60';time.setAttribute('aria-describedby','selected-deadline-guidance selected-deadline-zone');controls.append(timeRow);group.append(controls);
   const zone=document.createElement('p');zone.id='selected-deadline-zone';zone.className='request-note';zone.textContent='Kigali time — Africa/Kigali (UTC+02:00).';
   const note=document.createElement('p');note.id='selected-deadline-guidance';note.className='request-note';note.textContent='This is your requested completion deadline. Mr Sewing Fashion will confirm feasibility before accepting the order.';
   const timezone=document.createElement('input');timezone.type='hidden';timezone.name='Requested Completion Time Zone';timezone.value='Africa/Kigali (UTC+02:00)';group.append(zone,note,timezone);
  }
  const message=get('requestMessage');if(message){message.required=false;message.rows=3;message.setCustomValidity('');labelFor('requestMessage','Additional garment requirements (optional)');if(!get('selected-additional-heading')){const container=message.parentElement,heading=document.createElement('h2');heading.id='selected-additional-heading';heading.className='selected-form-heading';heading.textContent='Additional Requirements';container.classList.add('selected-quote-additional');container.prepend(heading);}}
  const reviewButton=get('reviewRequest');if(reviewButton)reviewButton.textContent='Review Quotation Request';
  refresh();form.dataset.selectedSuitReady='true';
  if(first)window.MrQuotationDraft?.restore?.();
 }
 function valid(){
  if(!active())return true;
  if(window.MrDesignSelections?.fabricPreferenceValid?.()===false){const status=get('requestStatus');if(status)status.textContent='Review your fabric and preferred colour, or choose fabric advice before continuing.';get('customerRequestForm')?.querySelector('[data-selected-fabric-edit]')?.focus();return false;}
  for(const id of['requestCountry','requestLocation']){const field=get(id);if(field)field.setCustomValidity(field.value.trim()?'':'Please complete this field.');}
  const date=get('requestDate'),time=get('requestCompletionTime');
  if(date){let good=/^\d{4}-\d{2}-\d{2}$/.test(date.value);if(good){const[dYear,dMonth,dDay]=date.value.split('-').map(Number),parsed=new Date(date.value+'T00:00:00Z');good=dYear>=1&&parsed.getUTCFullYear()===dYear&&parsed.getUTCMonth()===dMonth-1&&parsed.getUTCDate()===dDay;}date.setCustomValidity(good?'':'Enter a valid requested completion date.');}
  if(time)time.setCustomValidity(/^([01]\d|2[0-3]):[0-5]\d$/.test(time.value)?'':'Enter the requested completion time in Kigali time.');
  const okay=[get('requestCountry'),get('requestLocation'),date,time].filter(Boolean).every(field=>field.checkValidity());if(!okay)get('customerRequestForm')?.reportValidity();return okay;
 }
 function review(dl){if(!active())return;const term=document.createElement('dt'),definition=document.createElement('dd');term.textContent='Your Selected Designs';summary(definition,{review:true});dl.append(term,definition);const fabricTerm=document.createElement('dt'),fabricDefinition=document.createElement('dd');fabricTerm.textContent='Your Fabric and Colour Preference';preferenceSummary(fabricDefinition,{review:true});dl.append(fabricTerm,fabricDefinition);}
 window.MrSelectedSuitQuote={apply,refresh,valid,review,renderDesignSummary:summary};
 if(document.readyState==='complete')apply();else document.addEventListener('DOMContentLoaded',apply,{once:true});
})();
