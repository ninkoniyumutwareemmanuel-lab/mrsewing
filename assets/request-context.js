/* Non-homepage selection context only. Never store customer contact fields/messages. */
(()=>{'use strict';if(window.mrRequestContext)return;
const services={'custom-tailoring':'/services/custom-tailoring/','alterations':'/services/alterations/','garment-care':'/services/garment-care/','mobile-fitting':'/services/mobile-fitting/'};
const enums={service:Object.keys(services),experience:['standard','vip'],order:['standard','special'],priority:['standard','express'],afterHours:['yes','no']},key='mrsewing-request-context-v1';
function clean(x){const out={};for(const k of Object.keys(enums))if(enums[k].includes(x?.[k]))out[k]=x[k];if(/^MS-\d{3,}$/.test(x?.design||''))out.design=x.design;return out;}
let saved={};try{saved=clean(JSON.parse(sessionStorage.getItem(key)||'{}'));}catch{}
let state={...saved,...clean(Object.fromEntries(new URLSearchParams(location.search)))};
for(const [s,path]of Object.entries(services))if(location.pathname===path)state.service=s;
if(location.pathname.includes('/custom-tailoring/')&&(!location.pathname.endsWith('/special-order/')||!enums.service.includes(new URLSearchParams(location.search).get('service'))))state.service='custom-tailoring';
if(location.pathname.endsWith('/special-order/')&&!new URLSearchParams(location.search).has('order'))state.order='special';
function write(){try{sessionStorage.setItem(key,JSON.stringify(clean(state)));}catch{}}
write();window.mrRequestContext={read:()=>({...state}),update:x=>{state=clean({...state,...x});write();},clear:()=>{state={};try{sessionStorage.removeItem(key);}catch{}}};
document.addEventListener('click',event=>{const a=event.target.closest('a[href]');if(!a)return;const u=new URL(a.href,location.href);if(u.origin!==location.origin||!/^\/(?:request\/|mensuits\/|womensuits\/|collections\/|services\/custom-tailoring\/(?:design-choice|standard-order|special-order)\/)/.test(u.pathname))return;
const ctx={...state,...clean(Object.fromEntries(u.searchParams))};if(a.hasAttribute('data-experience-choice')){ctx.priority='standard';ctx.afterHours='no';delete ctx.design;delete ctx.order;}
if(!a.hasAttribute('data-experience-choice')&&state.experience)ctx.experience=state.experience;
if(state.priority&&!a.hasAttribute('data-experience-choice'))ctx.priority=state.priority;
for(const [k,v]of Object.entries(clean(ctx)))u.searchParams.set(k,v);a.href=u.pathname+u.search+u.hash;state=clean(ctx);write();},true);
if(/^\/(?:mensuits|womensuits|collections)\//.test(location.pathname)&&!document.querySelector('[data-publication-hold]')){
const main=document.querySelector('main');if(main){const d=document.getElementById('design-data');if(d){try{const ref=JSON.parse(d.textContent).design.id;if(/^MS-\d{3,}$/.test(ref)){state.design=ref;write();}}catch{}}
const note=document.createElement('p');note.className='request-context-note';note.textContent=`${state.experience==='vip'?'VIP Service':'Standard Service'} · Standard Order · ${state.priority==='express'?'Express Priority':'Standard Priority'}${state.design?' · Reference '+state.design:''}`;main.prepend(note);}}
const dropdown=document.querySelector('.services-dropdown details');document.addEventListener('keydown',e=>{if(e.key==='Escape'&&dropdown?.open){e.preventDefault();e.stopImmediatePropagation();dropdown.open=false;dropdown.querySelector('summary').focus();}},true);document.addEventListener('click',e=>{if(dropdown?.open&&!dropdown.contains(e.target))dropdown.open=false;});
})();
