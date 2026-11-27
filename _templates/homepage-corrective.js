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

/* R64: silent automatic suit videos with clean visuals; tap video or use Enter/Space to pause. */
(()=>{'use strict';
 const videos=[...document.querySelectorAll('.tailoring-video-card video[data-tailoring-loop]')];
 if(!videos.length)return;
 const reduce=window.matchMedia('(prefers-reduced-motion: reduce)');
 const manualPause=new WeakSet(),visible=new WeakMap();
 function reflect(v){
   const playing=!v.paused;
   v.setAttribute('aria-pressed',String(playing));
   v.setAttribute('aria-label',(playing?'Pause ':'Play ')+(v.dataset.videoTitle||'suit reference')+' video; tap or press Enter');
 }
 function stop(v){v.pause();reflect(v);}
 function play(v,manual=false){
   if(document.hidden||!visible.get(v))return;
   if(!manual&&(reduce.matches||manualPause.has(v)))return;
   v.muted=true;
   try{
     const task=v.play();
     if(task&&typeof task.catch==='function')task.catch(()=>reflect(v));
   }catch(_){/* Browser policy may block autoplay; the poster remains. */}
   reflect(v);
 }
 function toggle(v){
   if(v.paused){manualPause.delete(v);play(v,true);}
   else{manualPause.add(v);stop(v);}
 }
 videos.forEach(v=>{
   v.controls=false;v.muted=true;v.loop=true;v.playsInline=true;
   v.setAttribute('role','button');v.tabIndex=0;
   visible.set(v,false);
   v.addEventListener('play',()=>reflect(v));
   v.addEventListener('pause',()=>reflect(v));
   v.addEventListener('click',()=>toggle(v));
   v.addEventListener('keydown',e=>{
     if(e.key==='Enter'||e.key===' '){e.preventDefault();toggle(v);}
   });
   reflect(v);
 });
 const observer=('IntersectionObserver' in window)?new IntersectionObserver(entries=>{
   entries.forEach(entry=>{
     const v=entry.target;
     const canPlay=entry.isIntersecting&&entry.intersectionRatio>=.35;
     visible.set(v,canPlay);
     if(canPlay)play(v);else stop(v);
   });
 },{threshold:[0,.35,.65]}):null;
 if(observer)videos.forEach(v=>observer.observe(v));
 else videos.forEach(v=>{visible.set(v,true);play(v);});
 function reconcile(){videos.forEach(v=>{
   if(document.hidden||reduce.matches)stop(v);else play(v);
 });}
 document.addEventListener('visibilitychange',reconcile);
 reduce.addEventListener('change',reconcile);
 window.addEventListener('pagehide',()=>videos.forEach(stop));
})();
