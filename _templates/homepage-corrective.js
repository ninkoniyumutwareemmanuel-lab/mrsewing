/* Homepage-only progressive enhancements; never change the standalone forms. */
(()=>{'use strict';
const dropdown=document.querySelector('.services-dropdown details');
document.addEventListener('keydown',e=>{if(e.key==='Escape'&&dropdown?.open){e.preventDefault();e.stopImmediatePropagation();dropdown.open=false;dropdown.querySelector('summary').focus();}},true);
document.addEventListener('click',e=>{if(dropdown?.open&&!dropdown.contains(e.target))dropdown.open=false;});
dropdown?.addEventListener('click',e=>{if(e.target.closest('a'))dropdown.open=false;});
// Legacy homepage quotation anchors continue to the same booking journey.
document.querySelectorAll('a[href="#quotation"]').forEach(a=>a.addEventListener('click',e=>{e.preventDefault();location.assign('/booking/')}));
if(location.hash==='#quotation')location.replace('/booking/');
// Both enquiries reuse the existing approved provider, with independent pending and success state.
function setupEnquiry(prefix,formId){
 const form=document.getElementById(formId);if(!form)return;
 const button=form.querySelector('[type=submit]'),phone=document.getElementById(prefix+'Phone'),message=document.getElementById(prefix+'Message'),status=document.getElementById(prefix+'Status'),success=document.getElementById(prefix+'Success');let pending=false;const label=button.innerHTML;
 function validate(){const name=form.elements['Full Name'];name.setCustomValidity(name.value.trim()?'':'Please enter your name.');const value=phone.value.trim(),digits=value.replace(/\D/g,'').length;phone.setCustomValidity(/^[0-9+\-\s().]+$/.test(value)&&digits>=7&&digits<=15?'':'Enter a valid phone number including your country code.');message.setCustomValidity(message.value.trim()?'':'Please tell us how we can help.');}
 form.elements['Full Name'].addEventListener('input',validate);phone.addEventListener('input',validate);message.addEventListener('input',validate);
 form.addEventListener('submit',async e=>{e.preventDefault();validate();if(pending||!form.reportValidity())return;if(form.elements.botcheck.value){status.textContent='We could not confirm your request. Please contact us directly.';return;}
 const data=Object.fromEntries(new FormData(form));delete data.botcheck;const email=data['Email Address'].trim();data['Email Address']=email||'Not provided';if(email)data.replyto=email;data['Terms Consent']='Agreed';data['Customer Message']=message.value.trim();pending=true;button.disabled=true;button.textContent='Sending…';form.setAttribute('aria-busy','true');status.textContent='Sending your request. Please wait.';const controller=new AbortController(),timer=setTimeout(()=>controller.abort(),20000);
 try{const response=await fetch(form.action,{method:'POST',headers:{'Content-Type':'application/json',Accept:'application/json'},body:JSON.stringify(data),signal:controller.signal});const result=await response.json();if(!response.ok||result.success!==true)throw new Error('Not confirmed');status.textContent='';form.hidden=true;success.hidden=false;success.focus();}
 catch(error){status.textContent=error.name==='AbortError'?'We could not confirm delivery before the connection timed out. Your request may have arrived. Please contact us on WhatsApp before trying again.':'We could not confirm your request. Your entries are preserved. Please try again or contact us directly on WhatsApp.';}
 finally{clearTimeout(timer);pending=false;button.disabled=false;button.innerHTML=label;form.removeAttribute('aria-busy');}
 });
}
setupEnquiry('support','supportForm');
})();

/* R63: viewport-aware silent suit-video loops, with independent pause and reduced-motion respect. */
(()=>{'use strict';
 const figures=[...document.querySelectorAll('.tailoring-video-card')];
 if(!figures.length)return;
 const reduce=window.matchMedia('(prefers-reduced-motion: reduce)');
 const userPaused=new WeakSet(),visible=new WeakMap(),items=[];
 function reflect(v,b){
   const playing=!v.paused;
   b.setAttribute('aria-pressed',String(playing));
   b.setAttribute('aria-label',(playing?'Pause ':'Play ')+(v.dataset.videoTitle||'suit')+' video');
   b.querySelector('span').textContent=playing?'Ⅱ':'▶';
 }
 function pause(v,b){v.pause();reflect(v,b);}
 function start(v,b,manual=false){
   if(document.hidden||!visible.get(v))return;
   if(!manual&&(reduce.matches||userPaused.has(v)))return;
   v.muted=true;
   try{const task=v.play();if(task&&typeof task.catch==='function')task.catch(()=>reflect(v,b));}
   catch(_){/* Autoplay restriction leaves a manual Play button. */}
   reflect(v,b);
 }
 figures.forEach(fig=>{
   const v=fig.querySelector('video[data-tailoring-loop]'),b=fig.querySelector('[data-video-toggle]');
   if(!v||!b)return;
   v.muted=true;v.loop=true;v.playsInline=true;
   v.controls=false;b.hidden=false;
   visible.set(v,false);items.push([v,b,fig]);
   v.addEventListener('play',()=>reflect(v,b));
   v.addEventListener('pause',()=>reflect(v,b));
   b.addEventListener('click',()=>{
     if(v.paused){userPaused.delete(v);start(v,b,true);}
     else{userPaused.add(v);pause(v,b);}
   });
   reflect(v,b);
 });
 if(!items.length)return;
 const observer=('IntersectionObserver' in window)?new IntersectionObserver(entries=>{
   entries.forEach(entry=>{
     const pair=items.find(([, ,fig])=>fig===entry.target);
     if(!pair)return;
     const [v,b]=pair;
     const canPlay=entry.isIntersecting&&entry.intersectionRatio>=.35;
     visible.set(v,canPlay);
     if(canPlay)start(v,b);else pause(v,b);
   });
 },{threshold:[0,.35,.65]}):null;
 if(observer)items.forEach(([, ,fig])=>observer.observe(fig));
 else items.forEach(([v,b])=>{visible.set(v,true);start(v,b);});
 function reconcile(){items.forEach(([v,b])=>{if(document.hidden||reduce.matches)pause(v,b);else start(v,b);});}
 document.addEventListener('visibilitychange',reconcile);
 reduce.addEventListener('change',reconcile);
 window.addEventListener('pagehide',()=>items.forEach(([v,b])=>pause(v,b)));
})();
