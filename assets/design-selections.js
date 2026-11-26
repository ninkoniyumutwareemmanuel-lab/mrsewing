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
 function leave(){if(mode!=='browse')return;/* A closed same-origin dialog is background UI, not departure from its browsing parent. */if(window.parent!==window){try{if(window.parent.MrTailoringRequest&&!window.parent.MrTailoringRequest.isOpen())return;}catch{}}sync();if(meta?.status==='active'&&!Number.isFinite(meta.expiresAt)){const leftAt=Date.now();meta={...meta,leftAt,expiresAt:leftAt+limit};put(metaKey,meta);}schedule();}
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
  flow=identifier();setFlow(flow,{sessionId:meta?.id||null,items:rows,fabricPreference:preference,draftFrom:meta?.draftFrom||null});
  if(meta?.status==='active'){meta={...meta,status:'closed',leftAt:null,expiresAt:null,quoteId:flow};put(metaKey,meta);remove(browseKey);}
  mode='quote';setItems(rows);clearTimeout(timer);if(review)history.replaceState(null,'',url(location.pathname+location.search+location.hash));return flow;
 }
 function url(path,rows=read(),edit=false){const u=new URL(path,location.origin);u.searchParams.set('selection',pack(rows));for(const key of ['selectionFlow','selectionEdit','selectionSession'])u.searchParams.delete(key);if(mode==='quote'&&flow)u.searchParams.set(edit?'selectionEdit':'selectionFlow',flow);else if(meta?.id)u.searchParams.set('selectionSession',meta.id);const pref=packPreference(preference);if(pref)u.searchParams.set('sharedFabric',pref);else u.searchParams.delete('sharedFabric');return u.pathname+u.search+u.hash;}
 function fabricPreference(value){if(arguments.length){preference=cleanPreference(value);persist();}else sync();return cleanPreference(preference);}
 function restoreSnapshot(snapshot){const rows=clean(snapshot?.items);if(!rows.length)return false;flow=identifier();mode='quote';preference=cleanPreference(snapshot.fabricPreference);setItems(rows);setFlow(flow,{sessionId:null,items:rows,fabricPreference:preference});clearTimeout(timer);return true;}
 function complete(){if(mode==='quote'&&flow){const old=storedFlow(flow);setFlow(flow,{sessionId:old?.sessionId||null,items:[],completed:true});setItems([]);preference=null;}}
 meta=metadata();expire();
 const incomingPreference=unpackPreference(params.get('sharedFabric'));
 const incoming=unpack(params.get('selection')),session=params.get('selectionSession'),edit=params.get('selectionEdit');
 const quotePage=location.pathname==='/services/custom-tailoring/fabric/'&&params.get('multiple')==='1'||location.pathname.startsWith('/guides/fabrics/')&&(params.has('fabricFor')||params.get('fabricSelect')==='1')||location.pathname==='/request/'&&params.get('multiple')==='1';
 if(params.has('expressRecovery')&&!browsing()){mode='quote';setItems([]);preference=null;}
 else if(browsing()&&edit){const saved=storedFlow(edit);fresh(saved?(saved.completed?[]:saved.items):incoming,saved?(saved.completed?null:saved.fabricPreference):incomingPreference);if(saved&&!saved.completed){meta.draftFrom=edit;put(metaKey,meta);}const u=new URL(location.href);u.searchParams.delete('selectionEdit');u.searchParams.delete('selectionFlow');u.searchParams.set('selectionSession',meta.id);history.replaceState(null,'',u.pathname+u.search+u.hash);}
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
 return{read,persist,startAdd,close,url,complete,sync,fabricPreference,restoreSnapshot,isQuote:()=>mode==='quote',storageOK:()=>storageOK};
};

/* Shared enquiry preferences; palette labels are requests, never inventory claims. */
window.MrFabricPreferences=function(source){
 const labels={now:'Choose a Fabric',advice:'Help Me Choose',own:'Use My Own Fabric'};
 function clean(value){
  if(!value||typeof value!=='object'||!Object.hasOwn(labels,value.choice))return null;
  const out={choice:value.choice,fabricRef:'',colour:'',colourDescription:'',pattern:''};
  if(out.choice==='now'){
   out.fabricRef=Object.hasOwn(source.fabrics,value.fabricRef||'')?value.fabricRef:'';
   out.colour=Object.hasOwn(source.colours||{},value.colour||'')?value.colour:'';
   out.pattern=Object.hasOwn(source.patterns||{},value.pattern||'')?value.pattern:'';
   if(out.colour==='other'&&typeof value.colourDescription==='string'&&value.colourDescription.length<=80&&/^[\p{L}\p{N} .,'’()/+#-]*$/u.test(value.colourDescription))out.colourDescription=value.colourDescription.trim();
  }
  return out;
 }
 function valid(value){const p=clean(value);return !!p&&(p.choice!=='now'||!!p.fabricRef&&!!p.colour);}
 function details(value){const p=clean(value);return p?{...p,label:labels[p.choice],fabricName:source.fabrics[p.fabricRef]?.name||'',collectionName:source.fabrics[p.fabricRef]?.collection||'',patternName:source.patterns?.[p.pattern]?.name||'',colourName:source.colours?.[p.colour]?.name||''}:null;}
 function pack(value){const p=clean(value);return p?JSON.stringify([p.choice,p.fabricRef,p.colour,p.colourDescription,p.pattern]):'';}
 function unpack(value){try{if(typeof value!=='string'||value.length>600)return null;const a=JSON.parse(value);return Array.isArray(a)&&[4,5].includes(a.length)?clean({choice:a[0],fabricRef:a[1],colour:a[2],colourDescription:a[3],pattern:a[4]||''}):null;}catch{return null;}}
 return{clean,valid,details,pack,unpack};
};

/* Non-personal quotation selections only. Exact photos/fabrics are validated again on the server. */
(()=>{'use strict';const source=JSON.parse(document.getElementById('designSelectionData')?.textContent||'null');if(!source)return;const params=new URLSearchParams(location.search);let items=[],storageOK=true,bar,announcement,redrawSelectionList;
function resolve(x){const d=source.designs[x?.design];if(!d)return null;const project=x.project?source.projects[x.project]:null;if(x.project&&(!project||project.designRef!==x.design))return null;const photos=project?.images||d.images;const image=photos.find(i=>i.url===x.photo);if(!image)return null;return {...x,name:project?.name||d.name,route:project?.route||d.route,category:project?.category||d.audience,src:image.src,alt:image.alt,width:image.width,height:image.height};}
function clean(rows){if(!Array.isArray(rows))return[];const seen=new Set();return rows.map(x=>{const d=resolve(x);if(!d||seen.has(d.photo))return null;seen.add(d.photo);return{design:d.design,photo:d.photo,project:d.project||null,quantity:/^[1-9]\d{0,3}$/.test(String(d.quantity))?Number(d.quantity):1,fabricChoice:['now','advice','own'].includes(d.fabricChoice)?d.fabricChoice:'advice',fabricRef:typeof d.fabricRef==='string'?d.fabricRef:''};}).filter(Boolean);}
function unpack(value){try{return clean(JSON.parse(value).map(a=>{const d=source.designs[a[0]],p=a[2]?source.projects[a[2]]:null,image=(p?.images||d?.images||[])[a[1]];return{design:a[0],photo:image?.url,project:a[2],quantity:a[3],fabricChoice:a[4],fabricRef:a[5]};}));}catch{return[];}}
function browsing(path=location.pathname){return path==='/services/custom-tailoring/'||path==='/collections/'||path==='/showroom/'||path.startsWith('/mensuits/')||path.startsWith('/womensuits/')||path.startsWith('/collections/designs/')&&Object.values(source.designs).some(d=>d.route===path);}
function pack(rows){return JSON.stringify(clean(rows).map(x=>{const d=source.designs[x.design],p=x.project?source.projects[x.project]:null;return[x.design,(p?.images||d.images).findIndex(i=>i.url===x.photo),x.project,x.quantity,x.fabricChoice,x.fabricRef];}));}
const preferences=window.MrFabricPreferences(source);
const lifetime=window.MrSelectionSession({clean,unpack,pack,getItems:()=>items,setItems:rows=>{items=rows;},browsing,cleanPreference:preferences.clean,packPreference:preferences.pack,unpackPreference:preferences.unpack});
function read(){return lifetime.read();}
function packed(){return pack(read());}
function url(path){return lifetime.url(path);}
function save(){lifetime.persist();storageOK=lifetime.storageOK();if(document.querySelector('[data-selection-list]')||params.get('multiple')==='1'&&document.getElementById('fabricChoiceForm'))history.replaceState(null,'',url(location.pathname+location.search+location.hash));refresh();document.dispatchEvent(new Event('mrsewing:selectionchange'));}
function add(x){const d=resolve(x);if(!d)return false;lifetime.startAdd();if(!items.some(y=>y.photo===d.photo))items.push({design:x.design,photo:x.photo,project:x.project,quantity:1,fabricChoice:'advice',fabricRef:''});save();return true;}
function batch(){return params.get('multiple')==='1'&&!!document.getElementById('customerRequestForm')&&document.getElementById('customerRequestForm').dataset.special!=='true';}
function isSelectedQuote(){const f=document.getElementById('customerRequestForm');return !!f&&f.dataset.kind==='quotation'&&f.dataset.special!=='true'&&params.get('general')!=='1'&&document.getElementById('requestService')?.value==='custom-tailoring'&&document.getElementById('requestOrder')?.value==='standard'&&(batch()||!!window.MrSelectedDesign?.resolve(window.mrRequestContext?.read()||{}));}
function quoteRows(){if(lifetime.isQuote()||batch())return read();const state=window.mrRequestContext?.read()||{},r=window.MrSelectedDesign?.resolve(state);return r?clean([{design:state.design,photo:r.photoURL,project:state.project,quantity:Number(document.getElementById('requestQuantity')?.value)||1,fabricChoice:state.fabricChoice,fabricRef:state.fabricRef||''}]):[];}
function quoteSnapshot(){return quoteRows().map(x=>{const r=resolve(x);return{...r,name:friendly(r.name),fabricName:x.fabricChoice==='own'?'I Have My Own Fabric':x.fabricChoice==='advice'?'Help Me Choose Fabric':source.fabrics[x.fabricRef]?.name||'Choose Fabric'};});}
function quoteURL(path){const rows=quoteRows();lifetime.close(rows);return lifetime.url(path,rows,browsing(new URL(path,location.origin).pathname));}
function fabricPreference(){return lifetime.fabricPreference();}
function fabricPreferenceDetails(){return preferences.details(fabricPreference());}
function setFabricPreference(value){const p=preferences.clean(value);if(!p)return false;items=read();for(const row of items){row.fabricChoice=p.choice;row.fabricRef=p.fabricRef;}lifetime.fabricPreference(p);save();return true;}
function ensureQuote(){if(!read().length&&!lifetime.isQuote()&&!params.has('selection')&&!params.has('selectionFlow')&&params.get('multiple')!=='1'&&params.has('design')){const c=window.mrRequestContext?.read()||{},r=window.MrSelectedDesign?.resolve(c);if(r)items=clean([{design:c.design,photo:r.photoURL,project:c.project,quantity:1,fabricChoice:c.fabricChoice,fabricRef:c.fabricRef}]);}lifetime.close(read());return read();}
function quotationURL(){const rows=ensureQuote(),first=rows[0];if(!first)return url('/request/?multiple=1');const c={service:'custom-tailoring',order:'standard',design:first.design,photo:first.photo,project:first.project||undefined,fabricChoice:first.fabricChoice,fabricRef:first.fabricRef||undefined};window.mrRequestContext?.update(c);const u=new URL(url('/request/?multiple=1'),location.origin);for(const [k,v]of Object.entries(c))if(v)u.searchParams.set(k,v);return u.pathname+u.search;}
function decorate(d){if(!isSelectedQuote()||d.Service!=='Custom Tailoring & Suits')return d;const rows=quoteRows(),first=rows[0];d['Selected Design Count']=String(rows.length);d.Quantity=String(rows.reduce((n,x)=>n+x.quantity,0));d['Total Garments']=d.Quantity;d['Selected Designs']=rows.map((x,i)=>{const r=resolve(x);return(i+1)+'. '+friendly(r.name)+' | Quantity: '+x.quantity+' | '+x.photo+' | Fabric: '+(x.fabricChoice==='own'?'I have my own fabric':x.fabricChoice==='advice'?'Help me choose fabric':(source.fabrics[x.fabricRef]?.name||'Choose fabric'));}).join('\n');for(const k of ['Order Priority','After-hours Request','Garment Type','Other Garment','Fabric Preferences','Preferred Date','Preferred Time','Fabric Reference','Selected Fabric','Fabric Category','Fabric Tier','Fabric Preference','Fabric Assistance'])delete d[k];if(first){const r=resolve(first);d['Design Reference']=first.design;d['Selected Photograph URL']=first.photo;d['Design Image']=first.photo;d['Design Name']=friendly(r.name);d['Design Link']=new URL(r.route,'https://mrsewingfashion.com').href;d['Fabric Choice']=first.fabricChoice==='now'?'Customer fabric choice':first.fabricChoice==='own'?'Customer-Supplied Fabric':'Help Me Choose Fabric';if(first.fabricChoice==='now')d['Fabric Reference']=first.fabricRef;if(first.project)d['Portfolio Reference']=first.project;}const pref=fabricPreferenceDetails();if(pref){d['Shared Fabric Preference']=pref.label;d['Fabric Preference Scope']='Whole selected-design enquiry; suitability assessed for each garment';d['Fabric Choice']=pref.choice==='now'?'Customer fabric choice':pref.choice==='own'?'Customer-Supplied Fabric':'Help Me Choose Fabric';for(const key of ['Selected Fabric','Fabric Reference','Fabric Preference','Fabric Assistance','Fabric Category','Fabric Tier'])delete d[key];if(pref.choice==='now'){d['Selected Fabric']=pref.fabricName;d['Fabric Reference']=pref.fabricRef;if(pref.collectionName)d['Fabric Collection']=pref.collectionName;if(pref.patternName)d['Pattern & Texture']=pref.patternName;d['Preferred Colour']=pref.colourName+(pref.colourDescription?' — '+pref.colourDescription:'');d['Preferred Colour Reference']=pref.colour;if(pref.colourDescription)d['Colour Description']=pref.colourDescription;}else if(pref.choice==='own')d['Fabric Preference']='Customer-Supplied Fabric';else d['Fabric Assistance']='Requested';d['Selected Designs']=rows.map((x,i)=>(i+1)+'. '+friendly(resolve(x).name)+' | Quantity: '+x.quantity+' | '+x.photo).join('\n');}d['Requested Completion Time Zone']='Africa/Kigali (UTC+02:00)';return d;}
function submission(){return isSelectedQuote()?quoteRows():undefined;}
function review(dl){if(isSelectedQuote())window.MrSelectedSuitQuote?.review(dl);}
function friendly(name){return String(name).replace(/\s*[—·-]\s*MS-\d+\b/g,'').trim();}
function sharingSnapshot(){return read().map(x=>{const r=resolve(x);return{...r,name:friendly(r.name)};});}
window.MrDesignSelections={recoverySnapshot:()=>({items:read(),fabricPreference:fabricPreference()}),restoreQuotationSnapshot:s=>lifetime.restoreSnapshot(s),read,add,fabricPreference,fabricPreferenceDetails,setFabricPreference,fabricPreferenceValid:()=>!fabricPreference()||preferences.valid(fabricPreference()),quotationURL,editSelectionsURL:()=>quoteURL('/services/custom-tailoring/'),decorate,submission,review,sharingSnapshot,quoteRows,quoteSnapshot,isSelectedQuote,selectionURL:path=>isSelectedQuote()?quoteURL(path):url(path),isBatch:batch,fabricMode:!!document.getElementById('fabricChoiceForm')};
function refresh(){const allowed=browsing();const count=read().length;document.documentElement.classList.toggle('has-selected-designs',!!count&&allowed);if(bar){bar.hidden=!count||!allowed;bar.href=url('/services/custom-tailoring/selected-designs/');bar.querySelector('[data-selected-count]').textContent=count+' '+(count===1?'Design':'Designs')+' Selected';}for(const b of document.querySelectorAll('[data-select-design]')){const d=source.designs[b.dataset.selectDesign],u=new URL(b.href||location.href,location.origin);const photo=u.searchParams.get('photo')||d?.images[0]?.url;const selected=items.some(x=>x.design===b.dataset.selectDesign&&x.photo===photo);b.setAttribute('aria-pressed',String(selected));b.textContent=selected?'Design Selected ✓':'Select This Design';}}
document.addEventListener('mrsewing:selectionlifetime',()=>{refresh();redrawSelectionList?.();if(isSelectedQuote())window.MrSelectedSuitQuote?.refresh();});
document.addEventListener('DOMContentLoaded',()=>{if(isSelectedQuote())lifetime.close(quoteRows());const current=document.getElementById('design-data');if(current){const d=JSON.parse(current.textContent).design;const button=document.querySelector('.design-enquiry');if(button){button.dataset.selectDesign=d.id;button.setAttribute('role','button');button.addEventListener('keydown',e=>{if(e.key===' '){e.preventDefault();button.click();}});}}
bar=document.createElement('a');bar.className='selected-design-bar';bar.hidden=true;bar.href='/services/custom-tailoring/selected-designs/';bar.innerHTML='<span data-selected-count></span><span>Review Your Designs <span aria-hidden="true">→</span></span>';announcement=document.createElement('p');announcement.className='visually-hidden';announcement.dataset.selectionAnnouncement='';announcement.setAttribute('role','status');announcement.setAttribute('aria-live','polite');announcement.setAttribute('aria-atomic','true');document.body.append(bar,announcement);refresh();
for(const b of document.querySelectorAll('[data-select-design]'))b.addEventListener('click',e=>{e.preventDefault();const d=source.designs[b.dataset.selectDesign],u=new URL(b.href||location.href,location.origin),ctx=window.mrRequestContext?.read()||{};const project=u.searchParams.get('project')||(ctx.design===d.id?ctx.project:null);const photo=u.searchParams.get('photo')||(ctx.design===d.id?ctx.photo:null)||d.images[0].url;if(add({design:d.id,photo,project})){announcement.textContent='Added. Keep browsing or review your selections.';document.dispatchEvent(new CustomEvent('mrsewing:designselected',{detail:{trigger:b}}));if(!storageOK)announcement.textContent='Use Selected Designs to continue with these selections; browser storage is unavailable.';}});
const list=document.querySelector('[data-selection-list]');if(list){function draw(){list.replaceChildren();let total=document.querySelector('[data-selection-total]');if(!total){total=document.createElement('p');total.dataset.selectionTotal='';total.setAttribute('role','status');list.before(total);}const updateTotal=()=>{const rows=read();total.textContent=rows.length+' '+(rows.length===1?'design':'designs')+' · '+rows.reduce((n,x)=>n+x.quantity,0)+' '+(rows.reduce((n,x)=>n+x.quantity,0)===1?'garment':'garments');};updateTotal();if(!read().length){list.textContent='No designs selected yet. Return to the suit galleries to select your designs.';}for(const x of read()){const r=resolve(x),article=document.createElement('article'),h=document.createElement('h2'),a=document.createElement('a'),image=document.createElement('img'),label=document.createElement('label'),q=document.createElement('input'),remove=document.createElement('button');h.textContent=friendly(r.name);a.href=new URL(r.src,location.origin).href;a.target='_blank';a.rel='noopener';a.className='selection-photo';a.setAttribute('aria-label','View selected photograph of '+friendly(r.name));image.src=r.src;image.alt=r.alt;image.width=r.width;image.height=r.height;image.loading='lazy';image.decoding='async';a.append(image);label.textContent='Garment quantity';q.type='number';q.min='1';q.max='9999';q.value=x.quantity;q.required=true;label.append(q);q.addEventListener('change',()=>{if(q.reportValidity()){items.find(y=>y.photo===x.photo).quantity=Number(q.value);save();announcement.textContent='Quantity updated for '+friendly(r.name)+'.';updateTotal();}});remove.type='button';remove.className='home-button';remove.textContent='Remove Design';remove.addEventListener('click',()=>{const index=read().findIndex(y=>y.photo===x.photo);items=items.filter(y=>y.photo!==x.photo);save();draw();announcement.textContent=friendly(r.name)+' removed. '+read().length+' designs selected.';const controls=list.querySelectorAll('button');if(controls.length)controls[Math.min(index,controls.length-1)].focus();else{list.tabIndex=-1;list.focus();}});const details=document.createElement('div');details.className='selection-design-details';const controls=document.createElement('div');controls.className='selection-quantity';const minus=document.createElement('button'),plus=document.createElement('button');minus.type=plus.type='button';minus.textContent='−';plus.textContent='+';minus.setAttribute('aria-label','Decrease quantity for '+friendly(r.name));plus.setAttribute('aria-label','Increase quantity for '+friendly(r.name));for(const [button,change] of [[minus,-1],[plus,1]])button.addEventListener('click',()=>{q.value=Math.min(9999,Math.max(1,(Number(q.value)||1)+change));q.dispatchEvent(new Event('change'));});q.setAttribute('aria-label','Quantity for '+friendly(r.name));controls.append(minus,label,plus);details.append(h,controls,remove);article.append(a,details);list.append(article);}const next=document.querySelector('[data-selected-continue]');next.hidden=!items.length;next.href=url('/services/custom-tailoring/fabric/?multiple=1');const actions=document.querySelector('[data-selection-actions]');if(actions)actions.hidden=!items.length;const browse=document.querySelector('[data-selection-list] + p a');if(browse&&lifetime.isQuote())browse.href=lifetime.url('/services/custom-tailoring/',read(),true);}redrawSelectionList=draw;draw();const next=document.querySelector('[data-selected-continue]');next.addEventListener('click',e=>{const rows=read();if(!rows.length){e.preventDefault();draw();announcement.textContent='Your unfinished selections have expired. Please select your designs again.';return;}lifetime.close(rows);next.href=url('/services/custom-tailoring/fabric/?multiple=1');refresh();});}
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
  function sync(){const choice=selected();button.textContent='Continue';if(choice){const old=api.fabricPreference();api.setFabricPreference({choice,fabricRef:choice==='now'?old?.fabricRef||'':'',colour:choice==='now'?old?.colour||'':'',colourDescription:choice==='now'?old?.colourDescription||'':'',pattern:choice==='now'?old?.pattern||'':''});}status.textContent='';}
  form.addEventListener('change',sync);sync();
  form.addEventListener('submit',event=>{event.preventDefault();if(!form.reportValidity())return;sync();location.href=selected()==='now'?url('/guides/fabrics/?fabricSelect=1&multiple=1'):api.quotationURL();});
  return;
 }
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
   if(details.collectionName)value('Collection',details.collectionName);
   if(details.patternName)value('Pattern & Texture',details.patternName);
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
  if(!active())return;const form=get('customerRequestForm');if(!form)return;if(form.dataset.customQuotationReady==='true'){window.MrCustomQuotation?.refreshOrder?.();return;}
  let holder=form.querySelector('[data-selected-quote-holder]');if(!holder){holder=document.createElement('div');holder.dataset.selectedQuoteHolder='';const anchor=form.querySelector('fieldset');if(anchor)anchor.before(holder);else form.prepend(holder);}
  const existingEdit=form.querySelector('[data-edit-designs]'),existingFabric=form.querySelector('[data-selected-fabric-edit]');
  const wasOpen=holder.querySelector('.selected-quote-summary')?.open||false;holder.replaceChildren();const block=summary(holder);block.querySelector('.selected-quote-summary').open=wasOpen;
  const nav=document.createElement('nav');nav.className='selected-quote-edit';nav.setAttribute('aria-label','Edit selected designs');
  let edit=existingEdit;if(!edit){edit=document.createElement('a');edit.dataset.editDesigns='';edit.textContent='Add or Change Designs';}edit.href=selectionURL('/services/custom-tailoring/');nav.append(edit);block.append(nav);
  const fabric=existingFabric||document.createElement('a');preferenceSummary(holder,{edit:fabric});
  const quantity=get('requestQuantity');if(quantity){quantity.value=rows().reduce((n,row)=>n+Number(row.quantity||row.qty||1),0);quantity.readOnly=true;hide(quantity.closest('.request-fields>div')||quantity);}
 }
 function apply(){
  if(!active())return;const form=get('customerRequestForm');if(!form)return;if(form.dataset.customQuotationReady==='true'){window.MrCustomQuotation?.apply();return;}
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
  if(first)window.MrQuotationDraft?.restore?.();window.MrCustomQuotation?.apply();
 }
 function valid(){
  if(!active())return true;if(window.MrCustomQuotation?.active())return window.MrCustomQuotation.valid();
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

/* R49: one reusable Custom Tailoring form framework. No order, appointment or payment is confirmed here. */
(()=>{'use strict';
 const get=id=>document.getElementById(id),value=id=>get(id)?.value?.trim()||'';
 const locations={workshop:'Main Workshop — KN 441 St, Norvège, Kigali',downtown:'Downtown Consultation Location — MIC Building, by appointment'};
 const garmentLabels={shirt:'Shirt',trousers:'Trousers',dress:'Dress',skirt:'Skirt',jacket:'Jacket',coat:'Coat',other:'Other custom clothing'};
 const links={production:'/faq/production-delivery/#production-start',measurement:'/faq/measurements-fittings/#measurement-appointments',independent:'/faq/measurements-fittings/#independent-consultation-cost',orderVisit:'/faq/measurements-fittings/#order-measurement-visit',online:'/faq/measurements-fittings/#online-measurements',locations:'/faq/booking-visiting/#locations',delivery:'/faq/production-delivery/#outside-kigali',international:'/faq/production-delivery/#international-shipping',collection:'/faq/production-delivery/#customer-collection',response:'/faq/production-delivery/#quotation-response-times'};
 function mode(){const f=get('customerRequestForm');if(!f||f.dataset.kind!=='quotation'||get('requestService')?.value!=='custom-tailoring')return null;if(f.dataset.special==='true')return 'special';return window.MrDesignSelections?.isSelectedQuote?.()?'suit':null;}
 const active=()=>!!mode();
 function el(tag,cls,text){const n=document.createElement(tag);if(cls)n.className=cls;if(text!==undefined)n.textContent=text;return n;}
 function link(path,text){const a=el('a','custom-quotation-link',text);a.href=path;return a;}
 function note(text,path,label='More information'){const p=el('p','request-note',text+' ');if(path)p.append(link(path,label));return p;}
 function row(id,label,name,type='text',required=false){const box=el('div','custom-quotation-field'),caption=el('label','',label+(required?' (required)':' (optional)')),input=document.createElement(type==='textarea'?'textarea':'input');caption.htmlFor=id;input.id=id;input.name=name;if(type!=='textarea')input.type=type;else input.rows=3;input.required=required;if(type==='text'||type==='textarea')input.maxLength=type==='textarea'?4000:160;input.addEventListener('input',()=>input.setCustomValidity(''));box.append(caption,input);return box;}
 function selectRow(id,label,name,options,required=true){const box=el('div','custom-quotation-field'),caption=el('label','',label+(required?' (required)':' (optional)')),select=document.createElement('select');caption.htmlFor=id;select.id=id;select.name=name;select.required=required;select.add(new Option('Choose an option',''));for(const[k,t]of Object.entries(options))select.add(new Option(t,k));box.append(caption,select);return box;}
 function group(name,title){const field=el('fieldset','custom-quotation-section'),legend=el('legend','',title);field.dataset.quotationSection=name;field.append(legend);return field;}
 function disable(node,hidden=true){if(!node)return;node.hidden=hidden;for(const input of node.querySelectorAll('input,select,textarea')){input.disabled=hidden;if(hidden)input.setCustomValidity('');}}
 function nativeRow(id){const control=get(id);if(!control)return null;const own=control.closest('.custom-quotation-field');if(own)return own;const old=control.closest('.request-fields>div')||control.parentElement;return old;}
 function setLabel(id,text){const label=document.querySelector('label[for="'+id+'"]');if(label)label.textContent=text;}
 function ensureContact(section,id,label,name,type,required=true){let box=nativeRow(id);if(!box)box=row(id,label,name,type,required);const input=box.querySelector('#'+id);input.disabled=false;input.required=required;input.name=name;input.classList.remove('selected-quote-hidden');input.hidden=false;box.hidden=false;box.classList.remove('selected-quote-hidden');box.classList.add('custom-quotation-field');setLabel(id,label+(required?' (required)':' (optional)'));section.append(box);return input;}
 function calendar(date){if(!/^\d{4}-\d{2}-\d{2}$/.test(date))return false;const[y,m,d]=date.split('-').map(Number),p=new Date(Date.UTC(y,m-1,d));return y>=1&&p.getUTCFullYear()===y&&p.getUTCMonth()===m-1&&p.getUTCDate()===d;}
 function clock(time){return /^(?:[01]\d|2[0-3]):[0-5]\d$/.test(time);}
 function deadlineAssessment(){const date=value('requestDate'),time=value('requestCompletionTime'),good=calendar(date)&&clock(time),stamp=good?Date.parse(date+'T'+time+':00+02:00'):NaN,valid=good&&stamp>Date.now(),planningMs=valid?stamp-Date.now()-86400000:null;return{status:valid?(mode()==='special'?'Human assessment required':planningMs>=7*86400000?'Standard':'Express'):'',deadline:good?date+' '+time+' Africa/Kigali (UTC+02:00)':'',deadlineMs:Number.isFinite(stamp)?stamp:null,planningMs,valid};}
 function isRwanda(){return ['rwanda','rw','rwa','republic of rwanda'].includes(value('requestCountry').toLowerCase().replace(/\s+/g,' '));}
 function isKigali(){return ['kigali','kigali city','city of kigali'].includes(value('requestCity').toLowerCase().replace(/\s+/g,' '));}
 function quantity(){return mode()==='suit'?(window.MrDesignSelections?.quoteRows?.()||[]).reduce((n,r)=>n+Number(r.quantity||1),0):Number(value('requestQuantity'))||0;}
 function details(){const method=value('requestMeasurementMethod'),receiving=value('requestDeliveryMethod');return{version:2,mode:mode(),city:value('requestCity'),measurement:{method,purpose:method==='visit'?value('requestVisitPurpose'):'',location:method==='workshop'?value('requestMeasurementLocation'):'',date:['workshop','visit'].includes(method)?value('requestMeasurementDate'):'',time:['workshop','visit'].includes(method)?value('requestMeasurementTime'):'',address:method==='visit'?value('requestVisitAddress'):'',details:method==='visit'?value('requestVisitDetails'):''},delivery:{method:receiving,location:receiving==='collection'?value('requestCollectionLocation'):'',address:receiving==='delivery'?value('requestDeliveryAddress'):''}};}
 function updateConditional(){if(!active()||!get('customQuotationLayout'))return;const method=value('requestMeasurementMethod');disable(get('customMeasurementWorkshop'),method!=='workshop');disable(get('customMeasurementVisit'),method!=='visit');disable(get('customMeasurementAppointment'),!['workshop','visit'].includes(method));get('customMeasurementOnline').hidden=method!=='online';for(const id of['requestMeasurementLocation','requestMeasurementDate','requestMeasurementTime','requestVisitPurpose','requestVisitAddress']){const x=get(id);if(x)x.required=!x.disabled;}
  const receiving=value('requestDeliveryMethod');disable(get('customDeliveryAddress'),receiving!=='delivery');disable(get('customCollectionLocation'),receiving!=='collection');const address=get('requestDeliveryAddress');address.required=receiving==='delivery'&&!(isRwanda()&&isKigali());setLabel('requestDeliveryAddress','Delivery address '+(address.required?'(required)':'(optional at enquiry stage)'));const fee=get('customDeliveryNote');fee.replaceChildren();
  if(receiving==='collection')fee.append(note('Choose a preferred collection location. The team will confirm arrangements.',links.collection,'Collection information'));
  else if(receiving==='delivery'&&value('requestCountry')&&value('requestCity')){
   if(isRwanda()&&isKigali())fee.append(note(mode()==='suit'?'Initial eligible custom-suit delivery within Kigali is included. Your address is optional now and must be confirmed before dispatch.':'Kigali delivery arrangements for Special Tailoring are assessed in your quotation. The address may be provided now and must be confirmed before dispatch.',links.delivery,'Delivery information'));
   else if(isRwanda())fee.append(note('Calculated delivery: '+(quantity()*5000).toLocaleString('en-US')+' RWF ('+quantity()+' garments × 5,000 RWF). This is a calculated amount, subject to the accepted quotation.',links.delivery,'Delivery rates'));
   else fee.append(note('International shipping is assessed and quoted for your order. A complete delivery address is required; no fixed shipping price or transit time is promised.',links.international,'International shipping'));
  }
  if(mode()==='special'){const other=value('requestGarment')==='other';disable(get('customSpecialOther'),!other);get('requestOtherGarment').required=other;const now=value('requestFabricChoice')==='now';disable(get('requestFabricReferenceField'),!now);get('requestFabricSelection').required=now;}
  const today=new Date(Date.now()+7200000).toISOString().slice(0,10);get('requestDate').min=today;
 }
 function orderSummary(section){window.MrSelectedSuitQuote?.renderDesignSummary(section);const designNav=el('nav','selected-quote-edit');designNav.setAttribute('aria-label','Edit selected designs');const edit=link(window.MrDesignSelections?.selectionURL?.('/services/custom-tailoring/')||'/services/custom-tailoring/','Add or Change Designs');edit.dataset.editDesigns='';designNav.append(edit);section.append(designNav);
  const preference=window.MrDesignSelections?.fabricPreferenceDetails?.(),box=el('div','custom-fabric-summary');if(preference?.choice==='now'){box.append(el('p','','Selected Fabric: '+preference.fabricName),...(preference.collectionName?[el('p','','Collection: '+preference.collectionName)]:[]),...(preference.patternName?[el('p','','Pattern & Texture: '+preference.patternName)]:[]),el('p','','Preferred Colour: '+(preference.colourName||'Not specified')+(preference.colourDescription?' — '+preference.colourDescription:'')));}else box.append(el('p','',preference?.label||'Existing fabric preferences retained'));
  const fabric=link(window.MrDesignSelections?.selectionURL?.('/services/custom-tailoring/fabric/?multiple=1')||'/services/custom-tailoring/fabric/','Edit Fabric Preference');fabric.dataset.selectedFabricEdit='';box.append(fabric);box.append(note('Fabric suitability, colour and availability require confirmation for each garment.'));section.append(box);
 }
 function specialOrder(section){
  const previous=value('requestGarment'),old=get('requestGarment'),oldRow=nativeRow('requestGarment');if(oldRow)oldRow.remove();const garments=selectRow('requestGarment','What garment do you want made?','Garment Type',garmentLabels);section.append(garments);if(Object.hasOwn(garmentLabels,previous))get('requestGarment').value=previous;else if(previous){get('requestGarment').value='other';}
  let other=get('requestOtherGarment')?nativeRow('requestOtherGarment'):row('requestOtherGarment','Describe the garment','Other Garment','text',true);other.id='customSpecialOther';get('requestOtherGarment')?.removeAttribute('disabled');section.append(other);if(previous&&!Object.hasOwn(garmentLabels,previous))get('requestOtherGarment').value=previous;
  const q=ensureContact(section,'requestQuantity','Garment quantity','Quantity','number');q.min='1';q.max='9999';q.step='1';
  section.append(row('requestDesignDescription','Describe your design','Design Description','textarea',true));
  const fabric=get('requestFabricChoice'),block=fabric?.closest('[data-custom-only]');if(block){block.hidden=false;block.classList.remove('selected-quote-hidden');for(const input of block.querySelectorAll('input,select')){input.disabled=false;input.hidden=false;input.classList.remove('selected-quote-hidden');}setLabel('requestFabricChoice','Fabric preference (required)');fabric.required=true;for(const option of fabric.options)option.textContent={advice:'Help Me Choose a Fabric',now:'I Want to Choose a Fabric',own:'I Have My Own Fabric'}[option.value]||option.textContent;section.append(block);}
  const pictures=el('button','home-button','Share Reference Pictures on WhatsApp');pictures.type='button';pictures.dataset.specialPictures='';pictures.addEventListener('click',()=>window.MrSewingWhatsApp?.open('Hello Mr Sewing Fashion. I would like to share reference pictures for a Special Tailoring request. Garment: '+(garmentLabels[value('requestGarment')]||'Custom garment')+'. Quantity: '+value('requestQuantity')+'. Design: '+value('requestDesignDescription')+'. I will attach my pictures and press Send in WhatsApp.',pictures));section.append(pictures,note('Attach reference pictures manually in WhatsApp and press Send. No photograph upload is required.'));
 }
 function apply(){if(!active())return;const form=get('customerRequestForm');if(form.dataset.customQuotationReady==='true'){updateConditional();return;}const special=mode()==='special';
  document.body.classList.add('custom-quotation-page','selected-suit-quotation-page');form.classList.add('custom-quotation-form','selected-suit-quote');
  const intro=document.querySelector('main .release-intro');if(intro){intro.querySelector('h1').textContent=special?'Special Tailoring Request':'Your Quotation Request';const copy=intro.querySelector('p:last-child');if(copy)copy.textContent=special?'Tell us what you would like made and review your request before submitting.':'Review your selections and tell us when you need your garments.';}
  if(special){const breadcrumb=document.querySelector('main nav[aria-label="Breadcrumb"] ol');if(breadcrumb){breadcrumb.replaceChildren();for(const[text,path]of[['Home','/'],['Custom Tailoring & Suits','/services/custom-tailoring/'],['Special Tailoring',null]]){const li=document.createElement('li');if(path)li.append(link(path,text));else{const current=el('span','',text);current.setAttribute('aria-current','page');li.append(current);}breadcrumb.append(li);}}}
  for(const id of['request-title','request-guidance','priority-guidance','requestContextSummary','portfolioRequestContext'])if(get(id))get(id).hidden=true;const progress=document.querySelector('.request-progress');if(progress)progress.hidden=true;
  const layout=el('div','custom-quotation-layout');layout.id='customQuotationLayout';const order=group('order','Your Order'),information=group('information','Your Information'),deadline=group('deadline','When Do You Need It?'),measurements=group('measurements','Measurements & Fitting'),delivery=group('delivery','Delivery or Collection'),review=group('review','Review Your Request');layout.append(order,information,deadline,measurements,delivery,review);
  // Move existing controls and their listeners into the common framework.
  const contacts={};for(const[id,label,name,type,required]of[['requestName','Full name','Full Name','text',true],['requestPhone','Phone / WhatsApp number','Phone Number','tel',true],['requestEmail','Email address','Email Address','email',false],['requestCountry','Country','Country','text',true],['requestCity','City','City','text',true]])contacts[id]=ensureContact(information,id,label,name,type,required);
  contacts.requestCountry.autocomplete='country-name';contacts.requestCity.autocomplete='address-level2';contacts.requestCity.placeholder='For example, Kigali';
  const date=ensureContact(deadline,'requestDate','Requested completion date','Requested Completion Date','date'),time=ensureContact(deadline,'requestCompletionTime','Requested completion time (Kigali)','Requested Completion Time','time');time.step='60';date.setAttribute('aria-describedby','customDeadlineNote');time.setAttribute('aria-describedby','customDeadlineNote');const zone=el('input');zone.type='hidden';zone.name='Requested Completion Time Zone';zone.value='Africa/Kigali (UTC+02:00)';deadline.append(zone);const deadlineNote=note('Kigali time — Africa/Kigali (UTC+02:00). The team will confirm feasibility before accepting the order.',links.production,'When production begins');deadlineNote.id='customDeadlineNote';deadline.append(deadlineNote);const express=el('div','custom-express-assessment');express.dataset.expressAssessment='';deadline.append(express);
  measurements.append(selectRow('requestMeasurementMethod','How would you like your measurements taken?','Measurement Method',{workshop:'I Will Visit Mr Sewing',visit:'I Would Like Mr Sewing to Visit Me',online:'I Will Provide Measurements Online'}));const workshop=el('div','custom-conditional');workshop.id='customMeasurementWorkshop';workshop.append(selectRow('requestMeasurementLocation','Preferred location','Measurement Location',locations));measurements.append(workshop);
  const visit=el('div','custom-conditional');visit.id='customMeasurementVisit';visit.append(selectRow('requestVisitPurpose','Which visit service would you like?','Measurement Visit Purpose',{'order-related':'Order-related measurement visit','independent':'Independent Consultation & Fitting'}));const visitAddress=row('requestVisitAddress','Visit address','Measurement Visit Address','textarea',true);visitAddress.querySelector('textarea').maxLength=500;visit.append(visitAddress,row('requestVisitDetails','Relevant location details','Measurement Location Details','textarea'));visit.querySelector('#requestVisitDetails').maxLength=500;visit.append(note('An order-related eligible Kigali measurement visit is 10,000 RWF after quotation acceptance and the required garment advance.',links.orderVisit,'Order-related visit conditions'),note('Independent Consultation & Fitting is 35,000 RWF. The same approved measurement service is not charged both fees; selecting a preference does not require payment.',links.independent,'Consultation fee'));measurements.append(visit);
  const appointment=el('div','custom-appointment-grid');appointment.id='customMeasurementAppointment';appointment.append(row('requestMeasurementDate','Preferred appointment date','Preferred Measurement Date','date',true),row('requestMeasurementTime','Preferred appointment time (Kigali)','Preferred Measurement Time','time',true),note('Your preferred appointment requires team confirmation. Downtown MIC Building is by appointment.',links.measurement,'Appointment information'));measurements.append(appointment);
  const online=el('div','custom-conditional');online.id='customMeasurementOnline';online.append(note('You may request a quotation before supplying measurements. Keep your request open while consulting the guide.',links.online,'Online measurement information'));const guide=link('/measurements/','Open Measurements Guide');guide.target='_blank';guide.rel='noopener';online.append(guide);measurements.append(online);
  delivery.append(selectRow('requestDeliveryMethod','How would you like to receive your garments?','Delivery or Collection',{delivery:'Deliver to Me',collection:'I Will Collect'}));const address=el('div','custom-conditional');address.id='customDeliveryAddress';const addressRow=row('requestDeliveryAddress','Delivery address','Delivery Address','textarea');addressRow.querySelector('textarea').maxLength=500;address.append(addressRow);delivery.append(address);const collection=el('div','custom-conditional');collection.id='customCollectionLocation';collection.append(selectRow('requestCollectionLocation','Preferred collection location','Collection Location',locations));delivery.append(collection);const fee=el('div');fee.id='customDeliveryNote';fee.setAttribute('aria-live','polite');delivery.append(fee);
  const additional=ensureContact(order,'requestMessage','Additional Information','Additional Information','textarea',false);additional.rows=3;additional.maxLength=4000;order.querySelector('#selected-additional-heading')?.remove();
  const consent=get('requestConsent')?.closest('label'),reviewButton=get('reviewRequest');if(consent){consent.hidden=false;consent.classList.remove('selected-quote-hidden');get('requestConsent').disabled=false;get('requestConsent').required=true;review.append(consent);}if(reviewButton){reviewButton.textContent='Review Quotation Request';reviewButton.disabled=false;review.append(reviewButton);}review.append(note('Submission requests a quotation and confirms neither an order nor an appointment.',links.response,'Quotation response targets'));
  form.querySelector('[data-selected-quote-holder]')?.remove();get('selected-quote-deadline')?.remove();
  // Retain hidden system records; disable obsolete visible form controls.
  const legacy=el('div','custom-quotation-hidden');legacy.hidden=true;for(const child of [...form.children])legacy.append(child);for(const control of legacy.querySelectorAll('input,select,textarea'))if(control.type!=='hidden'&&control.name!=='botcheck'){control.disabled=true;control.required=false;control.setCustomValidity('');}form.append(legacy,layout);
  if(special)specialOrder(order);else orderSummary(order);order.append(nativeRow('requestMessage'));
  form.dataset.customQuotationReady='true';updateConditional();form.addEventListener('input',()=>{updateConditional();document.dispatchEvent(new Event('mrsewing:quotationchange'));});form.addEventListener('change',()=>{updateConditional();document.dispatchEvent(new Event('mrsewing:quotationchange'));});window.MrQuotationDraft?.restore?.();updateConditional();document.dispatchEvent(new Event('mrsewing:quotationchange'));
 }
 function valid(){if(!active())return true;const form=get('customerRequestForm');updateConditional();if(mode()==='suit'&&window.MrDesignSelections?.fabricPreferenceValid?.()===false){get('requestStatus').textContent='Review your fabric and preferred colour before continuing.';form.querySelector('[data-selected-fabric-edit]')?.focus();return false;}
  for(const id of['requestName','requestPhone','requestCountry','requestCity']){const field=get(id);field.setCustomValidity(value(id)?'':'Please complete this field.');}
  const assessment=deadlineAssessment();get('requestDate').setCustomValidity(calendar(value('requestDate'))?'':'Enter a valid completion date.');get('requestCompletionTime').setCustomValidity(clock(value('requestCompletionTime'))?'':'Enter a valid completion time in Kigali time.');if(calendar(value('requestDate'))&&clock(value('requestCompletionTime'))&&!assessment.valid)get('requestCompletionTime').setCustomValidity('Choose a requested completion deadline in the future.');
  for(const id of['requestMeasurementDate']){const field=get(id);field.setCustomValidity(field.disabled||calendar(value(id))?'':'Enter a valid preferred appointment date.');}for(const id of['requestMeasurementTime']){const field=get(id);field.setCustomValidity(field.disabled||clock(value(id))?'':'Enter a valid preferred appointment time.');}
  for(const id of['requestVisitAddress','requestDeliveryAddress','requestDesignDescription','requestOtherGarment']){const field=get(id);if(field)field.setCustomValidity(field.disabled||!field.required||value(id)?'':'Please complete this field.');}
  return form.reportValidity();
 }
 function decorate(fields){if(!active())return fields;const result={...fields},info=details(),special=mode()==='special';for(const key of['Order Priority','After-hours Request','Garment Type','Other Garment','Measurements','Delivery Location / Address','Customer Message','Fabric Preferences'])delete result[key];result.City=info.city;result.Location=[info.city,value('requestCountry')].filter(Boolean).join(', ');result.Country=value('requestCountry');result['Additional Information']=value('requestMessage');result['Requested Completion Date']=value('requestDate');result['Requested Completion Time']=value('requestCompletionTime');result['Requested Completion Time Zone']='Africa/Kigali (UTC+02:00)';result['Provisional Deadline Assessment']=deadlineAssessment().status;
  if(special){result['Garment Type']=value('requestGarment');if(value('requestGarment')==='other')result['Other Garment']=value('requestOtherGarment');result.Quantity=String(quantity());result['Design Description']=value('requestDesignDescription');result['Fabric Choice']=value('requestFabricChoice')==='now'?'Customer fabric choice':value('requestFabricChoice')==='own'?'Customer-Supplied Fabric':'Help Me Choose Fabric';if(value('requestFabricChoice')==='now')result['Fabric Reference']=value('requestFabricSelection');else{delete result['Fabric Reference'];delete result['Selected Fabric'];}}
  return result;
 }
 function renderReview(dl){if(!active())return;function item(label,text){if(!text)return;const dt=el('dt','',label),dd=el('dd','',text);dl.append(dt,dd);}const special=mode()==='special',info=details(),assessment=deadlineAssessment();
  if(!special){const dt=el('dt','','Your Order'),dd=el('dd');window.MrSelectedSuitQuote?.renderDesignSummary(dd,{review:true});dl.append(dt,dd);const pref=window.MrDesignSelections?.fabricPreferenceDetails?.();if(pref?.choice==='now'){item('Selected Fabric',pref.fabricName);if(pref.collectionName)item('Collection',pref.collectionName);if(pref.patternName)item('Pattern & Texture',pref.patternName);item('Preferred Colour',pref.colourName+(pref.colourDescription?' — '+pref.colourDescription:''));}else item('Fabric Preference',pref?.label||'Existing fabric preferences retained');}else{item('Garment',value('requestGarment')==='other'?value('requestOtherGarment'):garmentLabels[value('requestGarment')]);item('Quantity',String(quantity()));item('Design Description',value('requestDesignDescription'));item('Fabric Preference',get('requestFabricChoice')?.selectedOptions?.[0]?.textContent);if(value('requestFabricChoice')==='now')item('Selected Fabric',get('requestFabricSelection')?.selectedOptions?.[0]?.textContent);}
  item('Additional Information',value('requestMessage'));item('Full name',value('requestName'));item('Phone / WhatsApp',value('requestPhone'));item('Email',value('requestEmail'));item('Country',value('requestCountry'));item('City',info.city);item('Requested completion',assessment.deadline);item('Provisional assessment',assessment.status);
  item('Measurements',{workshop:'I Will Visit Mr Sewing',visit:'I Would Like Mr Sewing to Visit Me',online:'I Will Provide Measurements Online'}[info.measurement.method]);if(info.measurement.location)item('Measurement location',locations[info.measurement.location]);if(info.measurement.date)item('Preferred appointment',info.measurement.date+' '+info.measurement.time+' Kigali time');item('Visit address',info.measurement.address);item('Location details',info.measurement.details);if(info.measurement.method==='visit'){item('Measurement Visit Purpose',info.measurement.purpose==='independent'?'Independent Consultation & Fitting':'Order-related measurement visit');item('Measurement fee guidance',info.measurement.purpose==='independent'?'Independent Consultation & Fitting: 35,000 RWF. Scope and appointment require confirmation; selecting a preference does not require payment.':'Eligible order-related Kigali measurement visit: 10,000 RWF after quotation acceptance and the required garment advance. Eligibility and appointment require confirmation; selecting a preference does not require payment.');}
  item('Receiving your garments',info.delivery.method==='collection'?'I Will Collect':'Deliver to Me');if(info.delivery.method==='collection')item('Collection location',locations[info.delivery.location]);else{item('Delivery address',info.delivery.address||'To be confirmed before dispatch');if(isRwanda()&&!isKigali())item('Calculated delivery',quantity()+' garments × 5,000 RWF = '+(quantity()*5000).toLocaleString('en-US')+' RWF; subject to the accepted quotation');else if(isRwanda()&&isKigali()&&!special)item('Initial delivery','Included for eligible custom suits within Kigali');else item('Delivery charge','Individually assessed and quoted');}
 }
 function refreshOrder(){if(mode()!=='suit'||get('customerRequestForm')?.dataset.customQuotationReady!=='true')return;const section=document.querySelector('[data-quotation-section=order]');if(!section)return;const message=nativeRow('requestMessage');if(message)message.remove();for(const child of [...section.children])if(child.tagName!=='LEGEND')child.remove();orderSummary(section);if(message)section.append(message);}
 function nonSensitiveSnapshot(){const info=details();return{measurement:{method:info.measurement.method,purpose:info.measurement.purpose,location:info.measurement.location,date:info.measurement.date,time:info.measurement.time},delivery:{method:info.delivery.method,location:info.delivery.location},mode:mode(),country:value('requestCountry'),city:value('requestCity'),date:value('requestDate'),time:value('requestCompletionTime'),special:mode()==='special'?{garment:value('requestGarment'),quantity:quantity(),fabricChoice:value('requestFabricChoice'),fabricRef:value('requestFabricSelection')}:null};}
 function restoreOrder(snapshot){if(!active()||!snapshot||snapshot.mode!==mode())return;for(const[id,key]of[['requestMeasurementMethod','method'],['requestVisitPurpose','purpose'],['requestMeasurementLocation','location'],['requestMeasurementDate','date'],['requestMeasurementTime','time']])if(get(id)&&typeof snapshot.measurement?.[key]==='string')get(id).value=snapshot.measurement[key];for(const[id,key]of[['requestDeliveryMethod','method'],['requestCollectionLocation','location']])if(get(id)&&typeof snapshot.delivery?.[key]==='string')get(id).value=snapshot.delivery[key];for(const[id,key]of[['requestCountry','country'],['requestCity','city'],['requestDate','date'],['requestCompletionTime','time']])if(typeof snapshot[key]==='string'&&get(id))get(id).value=snapshot[key];if(mode()==='special'&&snapshot.special){for(const[id,key]of[['requestGarment','garment'],['requestQuantity','quantity'],['requestFabricChoice','fabricChoice'],['requestFabricSelection','fabricRef']])if(get(id)&&['string','number'].includes(typeof snapshot.special[key]))get(id).value=String(snapshot.special[key]);}updateConditional();document.dispatchEvent(new Event('mrsewing:quotationchange'));}
 window.MrCustomQuotation={active,mode,apply,details,valid,decorate,renderReview,refreshOrder,deadlineAssessment,nonSensitiveSnapshot,restoreOrder};
 if(document.readyState==='complete')apply();else document.addEventListener('DOMContentLoaded',apply,{once:true});
})();

/* R49: explicit, non-contact 24-hour enquiry recovery. Never a browsing-session restore. */
(()=>{'use strict';
 const KEY='mrsewing-express-recoveries-v1',DAY=86400000,byId=id=>document.getElementById(id),params=new URLSearchParams(location.search);
 let storageOK=true,recovered=null,recoveryApplied=false,continuedFor='',statusNode;
 const uuid=()=>globalThis.crypto?.randomUUID?.()||Date.now().toString(36)+'-'+Math.random().toString(36).slice(2);
 function read(){try{const d=JSON.parse(localStorage.getItem(KEY)||'{"entries":{}}');if(!d?.entries||typeof d.entries!=='object'||Array.isArray(d.entries))return{entries:{}};return d;}catch{storageOK=false;return{entries:{}};}}
 function write(d){try{localStorage.setItem(KEY,JSON.stringify(d));return true;}catch{storageOK=false;return false;}}
 function entries(){const d=read();let changed=false;for(const[id,e]of Object.entries(d.entries)){if(!e||!Number.isFinite(e.createdAt)||!Number.isFinite(e.expiresAt)||e.createdAt>Date.now()||e.expiresAt-e.createdAt!==DAY||Date.now()>=e.expiresAt||!['suit','special'].includes(e.snapshot?.mode)){delete d.entries[id];changed=true;}}if(changed)write(d);return d.entries;}
 function orderSnapshot(){const api=window.MrCustomQuotation,mode=api?.mode?.();if(!['suit','special'].includes(mode))return null;const raw=api.nonSensitiveSnapshot?.()||{},selection=window.MrDesignSelections?.recoverySnapshot?.();
  const snapshot={mode,date:byId('requestDate')?.value||'',time:byId('requestCompletionTime')?.value||'',country:byId('requestCountry')?.value.trim().slice(0,160)||'',city:byId('requestCity')?.value.trim().slice(0,160)||''};
  snapshot.measurement=raw.measurement;snapshot.delivery=raw.delivery;
  if(mode==='suit'){snapshot.items=selection?.items||[];snapshot.fabricPreference=selection?.fabricPreference||null;if(!snapshot.items.length)return null;}
  else{snapshot.special={garment:byId('requestGarment')?.value||raw.special?.garment||'',quantity:Number(byId('requestQuantity')?.value)||1,fabricChoice:byId('requestFabricChoice')?.value||'advice',fabricRef:byId('requestFabricSelection')?.value||''};}
  return snapshot;
 }
 function currentId(){const p=new URLSearchParams(location.search);return p.get('selectionFlow')||p.get('quotationSession')||uuid();}
 function entryId(){const current=currentId();return recovered?.id||Object.entries(entries()).find(([,e])=>e.linkedFlows?.includes(current))?.[0]||current;}
 function save(){const snapshot=orderSnapshot(),assessment=window.MrCustomQuotation?.deadlineAssessment?.();if(!snapshot||!assessment?.valid||!Number.isFinite(assessment.deadlineMs)||assessment.deadlineMs<=Date.now()||snapshot.mode==='suit'&&assessment.status!=='Express')return null;const id=entryId(),now=Date.now(),d={entries:entries()},old=d.entries[id];d.entries[id]={createdAt:now,expiresAt:now+DAY,snapshot,linkedFlows:[...new Set([...(old?.linkedFlows||[]),currentId()])]};if(!write(d))return null;return id;}
 function remove(id){if(!id)return;const d={entries:entries()};delete d.entries[id];write(d);}
 function recoveryURL(id,e){const path=e.snapshot.mode==='special'?'/services/custom-tailoring/special-order/':'/request/?multiple=1';const u=new URL(path,location.origin);u.searchParams.set('expressRecovery',id);return u.pathname+u.search;}
 function recover(id){const e=entries()[id];if(!e)return false;location.href=recoveryURL(id,e);return true;}
 // Hydrate before DOMContentLoaded so the existing form/context listeners see the recovered order.
 const recoverId=params.get('expressRecovery');if(recoverId){const entry=entries()[recoverId];if(entry&&((entry.snapshot.mode==='suit'&&location.pathname==='/request/')||(entry.snapshot.mode==='special'&&location.pathname==='/services/custom-tailoring/special-order/'))){recovered={id:recoverId,snapshot:entry.snapshot};if(entry.snapshot.mode==='suit'){
   if(window.MrDesignSelections?.restoreQuotationSnapshot?.(entry.snapshot)){const target=window.MrDesignSelections.quotationURL();history.replaceState(null,'',target);entry.linkedFlows=[...new Set([...(entry.linkedFlows||[]),currentId()])];const d=read();d.entries[recoverId]=entry;write(d);}else recovered=null;
  }else{const u=new URL(location.href);u.searchParams.delete('expressRecovery');u.searchParams.set('quotationSession',uuid());history.replaceState(null,'',u.pathname+u.search+u.hash);entry.linkedFlows=[...new Set([...(entry.linkedFlows||[]),currentId()])];const d=read();d.entries[recoverId]=entry;write(d);}
 }}
 const enquiryForm=byId('customerRequestForm'),legacyDesign=new URLSearchParams(location.search).get('design');const customEnquiry=enquiryForm?.dataset.special==='true'||window.MrDesignSelections?.isSelectedQuote?.()||(enquiryForm?.dataset.kind==='quotation'&&byId('requestService')?.value==='custom-tailoring'&&!!legacyDesign);if(customEnquiry&&!new URLSearchParams(location.search).has('selectionFlow')&&!new URLSearchParams(location.search).has('quotationSession')){const u=new URL(location.href);u.searchParams.set('quotationSession',uuid());history.replaceState(null,'',u.pathname+u.search+u.hash);}
 function prepared(){const api=window.MrCustomQuotation,assessment=api?.deadlineAssessment?.(),mode=api?.mode?.(),rows=window.MrDesignSelections?.quoteSnapshot?.()||[],fabric=window.MrDesignSelections?.fabricPreferenceDetails?.();
  const blocks=['Hello Mr Sewing Fashion. '+(mode==='special'?'I need assistance assessing a Special Tailoring deadline.':'Express enquiry for custom-tailored suits.')];
  if(mode==='suit'){
   blocks.push(rows.length+' designs / '+rows.reduce((n,r)=>n+r.quantity,0)+' garments.');for(const[rIndex,row]of rows.entries())blocks.push((rIndex+1)+'. '+String(row.name).replace(/\s*[—·-]\s*MS-\d+\b/g,'')+'\nQuantity: '+row.quantity+'\nPhotograph: '+new URL(row.src,location.origin).href);
   if(fabric)blocks.push('Fabric preference: '+fabric.label+(fabric.fabricName?'\nSelected fabric: '+fabric.fabricName:'')+(fabric.collectionName?'\nCollection: '+fabric.collectionName:'')+(fabric.patternName?'\nPattern & texture: '+fabric.patternName:'')+(fabric.colourName?'\nPreferred colour: '+fabric.colourName+(fabric.colourDescription?' — '+fabric.colourDescription:''):''));
  }else{const garment=byId('requestGarment');blocks.push('Garment: '+(garment?.selectedOptions?.[0]?.textContent||garment?.value||'Special Tailoring')+'\nQuantity: '+(byId('requestQuantity')?.value||'1'));if(byId('requestDesignDescription')?.value.trim())blocks.push('Design description: '+byId('requestDesignDescription').value.trim());const f=byId('requestFabricChoice');if(f)blocks.push('Fabric preference: '+(f.selectedOptions?.[0]?.textContent||f.value));}
  blocks.push('Requested completion: '+(byId('requestDate')?.value||'Not specified')+' '+(byId('requestCompletionTime')?.value||'')+' Africa/Kigali (UTC+02:00).\nAssessment: '+(assessment?.status||'Human assessment required')+'.\nPlease review feasibility and the quotation with me.');
  if(!['mrsewingfashion.com','www.mrsewingfashion.com'].includes(location.hostname))blocks.push('Staging preview links; these are not verified production destinations.');
  const fits=t=>t.length<=1600&&encodeURIComponent(t).length<=1600,parts=[];let chunk='';for(const block of blocks){if(!fits(block))return{message:blocks.join('\n\n'),parts:[],manual:true};const joined=chunk?chunk+'\n\n'+block:block;if(!fits(joined)){parts.push(chunk);chunk=block;}else chunk=joined;}if(chunk)parts.push(chunk);
  return{message:blocks.join('\n\n'),parts:parts.map((text,i)=>parts.length>1?'Tailoring enquiry — Part '+(i+1)+' of '+parts.length+'\n'+text:text),manual:false};
 }
 function notify(text){if(statusNode)statusNode.textContent=text;}
 function contactSaved(){const id=save();notify(id?'Your order selections are saved in this browser for up to 24 hours. WhatsApp messages and calls still require your action.':'Your browser could not save recovery data. Keep this page open to retain your enquiry.');return id;}
 function handoff(trigger){contactSaved();const bundle=prepared(),panel=byId('express-message-parts');panel.replaceChildren();if(bundle.parts.length===1){window.MrSewingWhatsApp?.open(bundle.parts[0],trigger);return;}const note=document.createElement('p');note.textContent=bundle.parts.length?'Your complete enquiry needs '+bundle.parts.length+' WhatsApp messages. Open, review and send each part yourself.':'This enquiry is too long for a safe WhatsApp link. Copy the complete text below and review it in the official conversation.';panel.append(note);
  bundle.parts.forEach((text,i)=>{const b=document.createElement('button');b.type='button';b.className='home-button';b.dataset.expressPart=i+1;b.textContent='WhatsApp — Part '+(i+1)+' of '+bundle.parts.length;b.addEventListener('click',()=>window.MrSewingWhatsApp?.open(text,b));panel.append(b);});
  const label=document.createElement('label'),text=document.createElement('textarea');label.textContent='Complete enquiry text';text.dataset.expressComplete='';text.value=bundle.message;text.readOnly=true;text.rows=8;label.append(text);panel.append(label);
 }
 function refresh(){const api=window.MrCustomQuotation,panel=document.querySelector('[data-express-assessment]');if(!api?.active?.()||!panel)return;const assessment=api.deadlineAssessment?.(),isSpecial=api.mode()==='special',deadline=(byId('requestDate')?.value||'')+' '+(byId('requestCompletionTime')?.value||'');if(!assessment?.valid||assessment.status==='Standard'||assessment.status==='Invalid'||!assessment.deadline){panel.hidden=true;return;}if(continuedFor===deadline){panel.hidden=true;return;}
  panel.hidden=false;if(panel.dataset.ready==='true'){panel.querySelector('[data-express-heading]').textContent=isSpecial?'Special deadline assessment':'Express';panel.querySelector('[data-express-message]').textContent=isSpecial?'Special garments need human deadline assessment. Contact us directly if your request is urgent.':'Your requested deadline requires Express service. Contact us directly for assistance.';return;}
  panel.dataset.ready='true';const h=document.createElement('h3'),message=document.createElement('p'),actions=document.createElement('div'),wa=document.createElement('button'),call=document.createElement('a'),keep=document.createElement('button');h.dataset.expressHeading='';message.dataset.expressMessage='';actions.className='request-actions';wa.type=keep.type='button';wa.className=call.className=keep.className='home-button';wa.dataset.expressWhatsapp='';wa.textContent='WhatsApp';wa.addEventListener('click',()=>handoff(wa));call.dataset.expressCall='';call.href='tel:+250787411501';call.textContent='Call Us';call.addEventListener('click',()=>contactSaved());keep.dataset.expressContinue='';keep.textContent='Continue Quotation Request';keep.addEventListener('click',()=>{continuedFor=(byId('requestDate')?.value||'')+' '+(byId('requestCompletionTime')?.value||'');panel.hidden=true;byId('requestMeasurementMethod')?.focus();});actions.append(wa,call,keep);statusNode=document.createElement('p');statusNode.setAttribute('role','status');statusNode.setAttribute('aria-live','polite');const parts=document.createElement('div');parts.id='express-message-parts';panel.append(h,message,actions,statusNode,parts);refresh();
 }
 function init(){if(recoverId&&!recovered){const form=byId('customerRequestForm');if(form)form.hidden=true;const main=document.querySelector('main .release-main');if(main){const note=document.createElement('p'),link=document.createElement('a');note.setAttribute('role','status');note.textContent='This saved enquiry has expired or is unavailable in this browser. Select your designs to start a fresh request.';link.href='/services/custom-tailoring/';link.className='home-button';link.textContent='Explore Custom Tailoring';main.append(note,link);}return;}if(recovered){const restore=()=>{if(recoveryApplied||byId('customerRequestForm')?.dataset.customQuotationReady!=='true'||!window.MrCustomQuotation?.active?.())return;recoveryApplied=true;window.MrCustomQuotation.restoreOrder(recovered.snapshot);};document.addEventListener('mrsewing:quotationchange',restore);restore();}
  const api=window.MrCustomQuotation;if(customEnquiry||api?.active?.()){refresh();document.addEventListener('mrsewing:quotationchange',refresh);byId('customerRequestForm')?.addEventListener('input',refresh);byId('customerRequestForm')?.addEventListener('change',refresh);const success=byId('requestSuccess');if(success)new MutationObserver(()=>{if(!success.hidden)remove(entryId());}).observe(success,{attributes:true,attributeFilter:['hidden']});}
  if(location.pathname==='/services/custom-tailoring/'){const saved=Object.entries(entries());if(saved.length){const section=document.createElement('section'),h=document.createElement('h2');section.className='release-section express-recovery-list';h.textContent='Continue a Saved Tailoring Enquiry';section.append(h);for(const[id,e]of saved){const a=document.createElement('a');a.className='home-button';a.dataset.expressRecover=id;a.href=recoveryURL(id,e);a.textContent=(e.snapshot.mode==='suit'?'Suit':'Special Tailoring')+' enquiry — '+e.snapshot.date+' '+e.snapshot.time;section.append(a);}document.querySelector('main .home-shell')?.prepend(section);}}
 }
 window.MrExpressEnquiry={save,recover,entries,expire:entries,message:()=>prepared().message,messageParts:()=>prepared().parts,storageKey:KEY};if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init);else init();
})();

/* One accessible shell for the existing same-origin selection and request pages.
 * The iframe retains the actual forms, state, validators and receiving contract.
 * No personal information is added to the parent URL or local storage. */
(()=>{'use strict';
 if(window.parent!==window||!window.HTMLDialogElement)return;
 const reviewPath='/services/custom-tailoring/selected-designs/';
 const permitted=p=>[reviewPath,'/services/custom-tailoring/fabric/','/request/'].includes(p)||p.startsWith('/guides/fabrics/');
 const browsing=p=>p==='/services/custom-tailoring/'||p==='/collections/'||/^\/(men|women)suits\//.test(p)||/^\/collections\/designs\//.test(p);
 if(!browsing(location.pathname))return;
 let dialog,frame,title,progress,opener,lastURL='',quoteStep=0,frameHistory=[],resumeButton;
 const resumeKey='mrsewing-tailoring-dialog-v1',resumeTTL=30*60*1000;
 function remember(path){try{const u=new URL(path,location.origin);if(u.origin!==location.origin||!permitted(u.pathname))return;const allowed=new Set(['selection','selectionFlow','selectionEdit','selectionSession','sharedFabric','multiple','fabricSelect','fabricFor','design','photo','project','service','order','fabricChoice','fabricRef']);for(const key of [...u.searchParams.keys()])if(!allowed.has(key))u.searchParams.delete(key);sessionStorage.setItem(resumeKey,JSON.stringify({url:u.pathname+u.search,updated:Date.now()}));}catch{}}
 function resumePath(){try{const saved=JSON.parse(sessionStorage.getItem(resumeKey)||'null');if(!saved||Date.now()-saved.updated>=resumeTTL||saved.updated>Date.now()){sessionStorage.removeItem(resumeKey);return null;}const u=new URL(saved.url,location.origin),meta=JSON.parse(sessionStorage.getItem('mrsewing-design-session-v1')||'null');if(u.origin!==location.origin||!permitted(u.pathname)||(!u.searchParams.has('selectionFlow')&&meta?.status!=='active'))return null;return saved.url;}catch{return null;}}
 function offerResume(){if(!resumePath())return;if(!resumeButton){resumeButton=document.createElement('button');resumeButton.type='button';resumeButton.className='home-button tailoring-resume-request';resumeButton.textContent='Resume Request';resumeButton.addEventListener('click',()=>open(resumePath(),resumeButton));const main=document.querySelector('main');(main?.querySelector('.home-shell')||main)?.prepend(resumeButton);}if(resumeButton)resumeButton.hidden=false;}
 const labels=['Selected designs','Fabric preference','Fabric details','Your information','Review request'];
 function announce(index,text){title.textContent=text||labels[index];progress.textContent='Step '+(index+1)+' of '+labels.length+' · '+labels[index];}
 function close(){if(!dialog?.open)return;dialog.close();document.documentElement.classList.remove('tailoring-dialog-open');window.MrDesignSelections?.read();if(history.state?.tailoringRequest)history.replaceState(null,'',location.href);offerResume();opener?.focus();}
 function create(){
  dialog=document.createElement('dialog');dialog.className='tailoring-request-dialog';dialog.setAttribute('aria-labelledby','tailoring-dialog-title');
  const head=document.createElement('header');head.className='tailoring-dialog-header';
  const names=document.createElement('div');progress=document.createElement('p');progress.className='tailoring-dialog-progress';progress.setAttribute('role','status');progress.setAttribute('aria-live','polite');
  title=document.createElement('h2');title.id='tailoring-dialog-title';names.append(progress,title);
  const exit=document.createElement('button');exit.type='button';exit.className='tailoring-dialog-close';exit.textContent='Close';exit.setAttribute('aria-label','Close quotation request and keep selections');exit.addEventListener('click',close);head.append(names,exit);
  frame=document.createElement('iframe');frame.title='Tailoring request steps';frame.className='tailoring-dialog-frame';
  frame.addEventListener('load',prepare);dialog.append(head,frame);document.body.append(dialog);
  dialog.addEventListener('cancel',event=>{event.preventDefault();close();});dialog.addEventListener('click',event=>{if(event.target===dialog)close();});
 }
 function open(path,trigger,fresh=false){
  if(!path)return false;
  const u=new URL(path,location.origin);if(u.origin!==location.origin||!permitted(u.pathname))return false;
  if(!dialog)create();opener=trigger||document.activeElement;
  if(!dialog.open){dialog.showModal();document.documentElement.classList.add('tailoring-dialog-open');history.pushState({tailoringRequest:true},'',location.href);}
  // Reopening on this page keeps the live, unfinished form rather than reloading it.
  if(!lastURL||fresh){lastURL=u.href;frameHistory=[];frame.src=u.href;announce(0,'Your Selected Designs');}
  if(resumeButton)resumeButton.hidden=true;
  dialog.querySelector('.tailoring-dialog-close').focus();return true;
 }
 function prepare(){
  let doc,win,u;try{doc=frame.contentDocument;win=frame.contentWindow;u=new URL(win.location.href);}catch{title.textContent='Open your request separately';return;}
  if(!doc||!permitted(u.pathname))return;
  lastURL=u.href;remember(u.href);if(!dialog.open)window.MrDesignSelections?.read();if(frameHistory.at(-1)!==u.href)frameHistory.push(u.href);
  doc.documentElement.classList.add('request-dialog-embedded');const sheet=doc.createElement('link');sheet.rel='stylesheet';sheet.href='/assets/tailoring-request-dialog.css?v=experience-20261126';doc.head.append(sheet);
  const stage=u.pathname===reviewPath?0:u.pathname==='/services/custom-tailoring/fabric/'?1:u.pathname.startsWith('/guides/fabrics/')?2:3;
  announce(stage,stage===0?'Your Selected Designs':undefined);
  doc.addEventListener('keydown',event=>{const nested=[...doc.querySelectorAll('dialog[open],[role=dialog]')].some(node=>node.open||node.getClientRects().length&&win.getComputedStyle(node).visibility!=='hidden');if(event.key==='Escape'&&!nested){event.preventDefault();close();}});
  doc.addEventListener('click',event=>{
   const link=event.target.closest('a[href]');if(!link||event.defaultPrevented||event.ctrlKey||event.metaKey||event.shiftKey||event.altKey)return;
   const target=new URL(link.href,u.href);if(target.origin!==location.origin)return;
   if(browsing(target.pathname)){event.preventDefault();close();location.assign(target.href);}
   else if(!permitted(target.pathname)&&!target.pathname.startsWith('/assets/')&&!/\.(?:jpe?g|png|webp|pdf)$/i.test(target.pathname)){link.target='_blank';link.rel='noopener';}
  });
  const main=doc.querySelector('main');if(main)main.setAttribute('tabindex','-1');
  if(stage===3)quoteSteps(doc,win);
  const back=doc.createElement('button');back.type='button';back.className='home-button request-dialog-back';back.textContent='Back';
  back.addEventListener('click',()=>{if(stage===3&&quoteStep>0){quoteStep--;showQuote(doc);return;}if(frameHistory.length>1){frameHistory.pop();const path=frameHistory.pop();frame.src=path;}else close();});
  (main?.querySelector('.release-main')||main||doc.body).prepend(back);
  main?.focus({preventScroll:true});
 }
 function quoteSteps(doc,win){
  const form=doc.getElementById('customerRequestForm'),parts=[...doc.querySelectorAll('[data-quotation-section]')];if(!form||!parts.length)return;
  quoteStep=0;const nav=doc.createElement('nav');nav.className='request-dialog-step-actions';nav.setAttribute('aria-label','Quotation steps');
  const next=doc.createElement('button');next.type='button';next.className='home-button home-button-gold';next.textContent='Continue';next.dataset.dialogContinue='';nav.append(next);form.append(nav);
  next.addEventListener('click',()=>{
   const section=parts[quoteStep];
   const invalid=[...section.querySelectorAll('input,select,textarea')].find(input=>!input.disabled&&!input.checkValidity());if(invalid){invalid.reportValidity();return;}
   if(section.dataset.quotationSection==='deadline'){const assessment=win.MrCustomQuotation?.deadlineAssessment();if(assessment&&!assessment.valid){doc.getElementById('requestCompletionTime').setCustomValidity('Choose a valid completion deadline in the future.');doc.getElementById('requestCompletionTime').reportValidity();return;}}
   quoteStep=Math.min(parts.length-1,quoteStep+1);showQuote(doc);
  });
  // The original validator still checks the complete form. Reveal the section
  // containing an invalid field so errors are never trapped in a hidden step.
  form.addEventListener('invalid',event=>{const index=parts.findIndex(part=>part.contains(event.target));if(index>=0){quoteStep=index;showQuote(doc,false);}},true);
  const refresh=()=>{
   const success=doc.getElementById('requestSuccess'),review=doc.getElementById('requestReview');
   if(success&&!success.hidden){announce(4,'Request Submitted for Review');try{sessionStorage.removeItem(resumeKey);}catch{}if(resumeButton)resumeButton.hidden=true;}
   else if(review&&!review.hidden)announce(4,'Review Your Request');
   else showQuote(doc,false);
  };
  for(const id of['requestReview','requestSuccess']){const node=doc.getElementById(id);if(node)new MutationObserver(refresh).observe(node,{attributes:true,attributeFilter:['hidden']});}
  doc.getElementById('editRequest')?.addEventListener('click',()=>{quoteStep=parts.length-1;showQuote(doc);});
  doc.getElementById('sendRequest')?.replaceChildren(doc.createTextNode('Submit Request'));
  showQuote(doc);
 }
 function showQuote(doc,focus=true){
  const parts=[...doc.querySelectorAll('[data-quotation-section]')];parts.forEach((part,index)=>part.hidden=index!==quoteStep);
  const next=doc.querySelector('[data-dialog-continue]');if(next)next.hidden=quoteStep===parts.length-1;
  const caption=parts[quoteStep]?.querySelector('legend')?.textContent||'Your Request';announce(3,caption+' · '+(quoteStep+1)+' of '+parts.length);
  if(focus){const first=parts[quoteStep]?.querySelector('input:not([type=hidden]),select,textarea,button');first?.focus({preventScroll:true});frame.contentWindow.scrollTo(0,0);}
 }
 document.addEventListener('click',event=>{const link=event.target.closest('a.selected-design-bar');if(link&&!event.ctrlKey&&!event.metaKey&&!event.shiftKey&&!event.altKey&&open(link.href,link))event.preventDefault();});
 document.addEventListener('mrsewing:designselected',event=>{const path=document.querySelector('.selected-design-bar')?.href||window.MrDesignSelections?.selectionURL(reviewPath)||reviewPath;open(path,event.detail?.trigger,true);});
 window.addEventListener('popstate',()=>{if(dialog?.open&&!history.state?.tailoringRequest)close();});
 window.MrTailoringRequest={open,close,isOpen:()=>!!dialog?.open};
 if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',offerResume,{once:true});else offerResume();
})();
