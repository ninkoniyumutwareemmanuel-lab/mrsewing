/* R46: per-tab, non-personal browsing lifetime; quotation snapshots have independent identities. */
window.MrSelectionSession=function({clean,unpack,pack,getItems,setItems,browsing}){
 const browseKey='mrsewing-design-selections-v1',metaKey='mrsewing-design-session-v1',quoteKey='mrsewing-quotation-selections-v1',limit=120000;
 const params=new URLSearchParams(location.search),review=location.pathname==='/services/custom-tailoring/selected-designs/';
 let storageOK=true,meta=null,flow=null,mode='browse',timer,departing=false;
 const memory=new Map();
 function load(key,fallback){if(!storageOK&&memory.has(key))return memory.get(key)??fallback;try{const raw=sessionStorage.getItem(key);return raw===null?fallback:JSON.parse(raw);}catch{storageOK=false;return memory.get(key)??fallback;}}
 function put(key,value){memory.set(key,value);try{sessionStorage.setItem(key,JSON.stringify(value));}catch{storageOK=false;}}
 function remove(key){memory.set(key,undefined);try{sessionStorage.removeItem(key);}catch{storageOK=false;}}
 function identifier(){return globalThis.crypto?.randomUUID?.()||Date.now().toString(36)+'-'+Math.random().toString(36).slice(2);}
 function metadata(){const value=load(metaKey,null);return value&&typeof value.id==='string'&&['active','closed','expired'].includes(value.status)?value:null;}
 function quotes(){const value=load(quoteKey,{flows:{}});return value&&value.flows&&typeof value.flows==='object'&&!Array.isArray(value.flows)?value:{flows:{}};}
 function storedFlow(id){if(!id||!Object.hasOwn(quotes().flows,id))return null;return quotes().flows[id];}
 function setFlow(id,value){const all=quotes();all.flows[id]=value;put(quoteKey,all);}
 function fresh(rows=[]){meta={id:identifier(),status:'active',leftAt:null,expiresAt:null};mode='browse';flow=null;setItems(clean(rows));put(metaKey,meta);put(browseKey,clean(rows));}
 function expire(){if(meta?.status==='active'&&Number.isFinite(meta.expiresAt)&&Date.now()>=meta.expiresAt){meta={...meta,status:'expired'};put(metaKey,meta);remove(browseKey);if(mode==='browse')setItems([]);return true;}return false;}
 function schedule(){clearTimeout(timer);if(mode==='browse'&&!browsing()&&meta?.status==='active'&&Number.isFinite(meta.expiresAt))timer=setTimeout(()=>{sync();document.dispatchEvent(new Event('mrsewing:selectionlifetime'));},Math.max(1,meta.expiresAt-Date.now()));}
 function leave(){if(mode!=='browse')return;sync();if(meta?.status==='active'&&!Number.isFinite(meta.expiresAt)){const leftAt=Date.now();meta={...meta,leftAt,expiresAt:leftAt+limit};put(metaKey,meta);}schedule();}
 function sync(force=false){const latest=metadata();if(mode==='browse'){
  const changed=latest?.id!==meta?.id||latest?.status!==meta?.status;meta=latest;
  if(!meta||meta.status!=='active'){setItems([]);return;}
  if(expire())return;
  if(force||changed)setItems(clean(load(browseKey,[])));
  if(browsing()&&!departing&&Number.isFinite(meta.expiresAt)){meta={...meta,leftAt:null,expiresAt:null};put(metaKey,meta);}
 }else if(force&&flow){const saved=storedFlow(flow);setItems(saved&&!saved.completed?clean(saved.items):[]);}schedule();}
 function read(){sync();return clean(getItems());}
 function persist(){sync();const rows=clean(getItems());setItems(rows);if(mode==='quote'&&flow){const old=storedFlow(flow);if(old?.completed){setItems([]);return;}setFlow(flow,{sessionId:old?.sessionId||meta?.id||null,items:rows});}else if(meta?.status==='active')put(browseKey,rows);}
 function startAdd(){sync();if(mode!=='browse'||meta?.status!=='active')fresh();}
 function close(rows=read()){
  if(mode==='quote'&&flow)return flow;
  rows=clean(rows);if(!rows.length)return null;
  flow=identifier();setFlow(flow,{sessionId:meta?.id||null,items:rows});
  if(meta?.status==='active'){meta={...meta,status:'closed',leftAt:null,expiresAt:null,quoteId:flow};put(metaKey,meta);remove(browseKey);}
  mode='quote';setItems(rows);clearTimeout(timer);if(review)history.replaceState(null,'',url(location.pathname+location.search+location.hash));return flow;
 }
 function url(path,rows=read(),edit=false){const u=new URL(path,location.origin);u.searchParams.set('selection',pack(rows));if(mode==='quote'&&flow)u.searchParams.set(edit?'selectionEdit':'selectionFlow',flow);else if(meta?.id)u.searchParams.set('selectionSession',meta.id);return u.pathname+u.search+u.hash;}
 function complete(){if(mode==='quote'&&flow){const old=storedFlow(flow);setFlow(flow,{sessionId:old?.sessionId||null,items:[],completed:true});setItems([]);}}
 meta=metadata();expire();
 const incoming=unpack(params.get('selection')),session=params.get('selectionSession'),edit=params.get('selectionEdit');
 const quotePage=location.pathname==='/services/custom-tailoring/fabric/'&&params.get('multiple')==='1'||location.pathname==='/guides/fabrics/'&&params.has('fabricFor')||location.pathname==='/request/'&&params.get('multiple')==='1';
 if(browsing()&&edit){const saved=storedFlow(edit);fresh(saved?(saved.completed?[]:saved.items):incoming);const u=new URL(location.href);u.searchParams.delete('selectionEdit');u.searchParams.delete('selectionFlow');u.searchParams.set('selectionSession',meta.id);history.replaceState(null,'',u.pathname+u.search+u.hash);}
 else{
  const requestedFlow=!browsing()&&(params.get('selectionFlow')||(review&&meta?.status==='closed'&&session===meta.id?meta.quoteId:null));
  if(requestedFlow){mode='quote';flow=requestedFlow;let saved=storedFlow(flow);if(!saved&&incoming.length){saved={sessionId:session||null,items:incoming};setFlow(flow,saved);}setItems(saved&&!saved.completed?clean(saved.items):[]);}
  else{
   let rows=meta?.status==='active'?clean(load(browseKey,[])):[];
   // Old packed URLs may import only in a genuinely new tab, never over a tombstone/newer session.
   if(!meta){rows=incoming.length?incoming:clean(load(browseKey,[]));if(rows.length)fresh(rows);else setItems([]);}
   else{setItems(rows);if(session===meta.id&&meta.status==='active'&&!rows.length&&incoming.length){setItems(incoming);put(browseKey,incoming);}}
   if(quotePage)close(read());
  }
 }
 if(mode==='browse'){if(browsing())sync();else leave();}
 window.addEventListener('pagehide',()=>{if(browsing()){departing=true;leave();}});
 document.addEventListener('click',e=>{const a=e.target.closest?.('a[href]');if(!a||e.defaultPrevented||a.target==='_blank'||a.hasAttribute('download')||e.ctrlKey||e.metaKey||e.shiftKey||e.altKey)return;const u=new URL(a.href,location.href);if(u.origin!==location.origin||!browsing(u.pathname)){departing=true;leave();}});
 window.addEventListener('pageshow',e=>{departing=false;sync(true);if(e.persisted&&mode==='quote'&&quotePage&&location.pathname!=='/request/'){location.reload();return;}document.dispatchEvent(new Event('mrsewing:selectionlifetime'));});
 document.addEventListener('visibilitychange',()=>{if(!document.hidden){sync();document.dispatchEvent(new Event('mrsewing:selectionlifetime'));}});
 return{read,persist,startAdd,close,url,complete,sync,isQuote:()=>mode==='quote',storageOK:()=>storageOK};
};
