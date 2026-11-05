/* Whitelisted request choices only; never persist customer contact details or free text. */
(()=>{'use strict';if(window.mrRequestContext)return;
const paths={'custom-tailoring':'/services/custom-tailoring/','alterations':'/services/alterations/','garment-care':'/services/garment-care/','mobile-fitting':'/services/mobile-fitting/','vip':'/services/vip/'};
const enums={service:Object.keys(paths),experience:['standard','vip'],order:['standard','special'],priority:['standard','express'],afterHours:['yes','no'],category:['men','women'],fabricChoice:['now','advice'],fabricRef:/* fabric-reference-ids */[]},key='mrsewing-request-context-v1';
function clean(x){const y={};for(const k of Object.keys(enums))if(enums[k].includes(x?.[k]))y[k]=x[k];if(/^MS-\d{3,}$/.test(x?.design||''))y.design=x.design;if(y.fabricChoice==='advice'||y.fabricRef&&y.category&&!y.fabricRef.startsWith(y.category+'-'))delete y.fabricRef;return y;}
let saved={};try{saved=clean(JSON.parse(sessionStorage.getItem(key)||'{}'));}catch{}
let state={...saved,...clean(Object.fromEntries(new URLSearchParams(location.search)))};
for(const [service,path]of Object.entries(paths))if(location.pathname===path){state.service=service;state.experience=service==='vip'?'vip':'standard';}
if(location.pathname.startsWith('/services/custom-tailoring/')){state.service='custom-tailoring';state.experience='standard';}
if(location.pathname==='/mensuits/'||location.pathname==='/womensuits/'){state.service='custom-tailoring';state.experience='standard';state.order='standard';state.category=location.pathname==='/mensuits/'?'men':'women';delete state.design;}
if(location.pathname.endsWith('/special-order/')){state.order='special';delete state.design;}
function write(){try{sessionStorage.setItem(key,JSON.stringify(clean(state)));}catch{}}
write();window.mrRequestContext={read:()=>({...state}),update:x=>{state=clean({...state,...x});write();},clear:()=>{state={};try{sessionStorage.removeItem(key);}catch{}}};
document.addEventListener('click',event=>{const a=event.target.closest('a[href]');if(!a)return;const u=new URL(a.href,location.href);if(u.origin!==location.origin||!/^\/(?:request\/|mensuits\/|womensuits\/|collections\/|services\/custom-tailoring\/)/.test(u.pathname))return;
const next={...state,...clean(Object.fromEntries(u.searchParams))};if(u.pathname.endsWith('/special-order/')){next.order='special';delete next.design;u.searchParams.delete('design');}if(u.pathname==='/mensuits/'||u.pathname==='/womensuits/'){next.category=u.pathname==='/mensuits/'?'men':'women';next.order='standard';delete next.design;u.searchParams.delete('design');}next.service='custom-tailoring';next.experience='standard';for(const [k,v]of Object.entries(clean(next)))u.searchParams.set(k,v);a.href=u.pathname+u.search+u.hash;state=clean(next);write();},true);
if(location.pathname.startsWith('/collections/designs/')){try{const d=JSON.parse(document.getElementById('design-data').textContent).design;state.design=d.id;state.order='standard';state.service='custom-tailoring';state.experience='standard';if(['men','women'].includes(d.gender))state.category=d.gender;write();}catch{}}
const dropdown=document.querySelector('.services-dropdown details');document.addEventListener('keydown',e=>{if(e.key==='Escape'&&dropdown?.open){e.preventDefault();e.stopImmediatePropagation();dropdown.open=false;dropdown.querySelector('summary').focus();}},true);document.addEventListener('click',e=>{if(dropdown?.open&&!dropdown.contains(e.target))dropdown.open=false;});
})();
