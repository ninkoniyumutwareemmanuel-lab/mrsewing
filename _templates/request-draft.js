/* Per-tab quotation draft only. Never an order database, attachment store or staff dashboard. */
(()=>{'use strict';const form=document.getElementById('customerRequestForm');if(!form||form.dataset.kind!=='quotation')return;
const context=new URLSearchParams(location.search);const key='mrsewing-quotation-draft-v1';const scope=location.pathname+'|'+(form.dataset.service||'custom-tailoring')+'|'+(form.dataset.special==='true'?'special':context.get('general')==='1'?'general':context.get('design')||'');
const ids=['requestName','requestPhone','requestEmail','requestLocation','requestQuantity','requestDate','requestFabric','requestMeasurements','requestGarment','requestCondition','requestCollection','requestAssistance','requestTime','requestParticipants','requestEvent','requestMessage'];const ttl=30*60*1000;
try{const d=JSON.parse(sessionStorage.getItem(key)||'null');if(d&&Date.now()-d.updated>=ttl)sessionStorage.removeItem(key);else if(d?.scope===scope&&d.updated<=Date.now()){for(const id of ids){const el=document.getElementById(id);if(el&&typeof d.values?.[id]==='string')el.value=d.values[id];}}}catch(_){}
function save(){const values={};for(const id of ids){const el=document.getElementById(id);if(el)values[id]=el.value.slice(0,4000);}try{sessionStorage.setItem(key,JSON.stringify({scope,updated:Date.now(),values}));}catch(_){}}
form.addEventListener('input',save);form.addEventListener('change',save);
const success=document.getElementById('requestSuccess');if(success)new MutationObserver(()=>{if(!success.hidden)try{sessionStorage.removeItem(key);}catch(_){}}).observe(success,{attributes:true,attributeFilter:['hidden']});
})();
