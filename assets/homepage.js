(function setupHomepageMenu() {
  const button = document.querySelector('.home-menu-toggle');
  const menu = document.getElementById('home-navigation');
  if (!button || !menu) return;
  function setOpen(open, restoreFocus = false) {
    button.setAttribute('aria-expanded', String(open));
    button.setAttribute('aria-label', open ? 'Close navigation' : 'Open navigation');
    menu.dataset.open = String(open);
    if (restoreFocus) button.focus();
  }
  button.addEventListener('click', () => setOpen(button.getAttribute('aria-expanded') !== 'true'));
  menu.addEventListener('click', event => {
    const link = event.target.closest('a');
    if (!link) return;
    setOpen(false);
    // In-page navigation must not leave focus inside the now-hidden dropdown.
    const url = new URL(link.href, location.href);
    if (url.pathname === location.pathname && url.hash) {
      const section = document.getElementById(decodeURIComponent(url.hash.slice(1)));
      const target = section && (section.querySelector('h1,h2') || section);
      if (target) {
        target.tabIndex = -1;
        // Let the native fragment navigation finish before placing focus.
        requestAnimationFrame(() => target.focus({ preventScroll:true }));
      }
    }
  });
  document.addEventListener('click', event => {
    if (!menu.contains(event.target) && !button.contains(event.target)) setOpen(false);
  });
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && button.getAttribute('aria-expanded') === 'true') setOpen(false, true);
  });
  // Reset on the layout breakpoint only, not while mobile browser chrome resizes.
  matchMedia('(max-width: 1099px)').addEventListener('change', () => setOpen(false));
})();
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
/* Three original text slides; four-second rotation with passive touch hold and transient focus/hover pause. */
(()=>{'use strict';
const root=document.querySelector('[data-order-carousel]');if(!root)return;
const track=root.querySelector('.order-slides'),slides=[...track.querySelectorAll('[data-order-slide]')],dots=[...root.querySelectorAll('[data-order-select]')],motion=matchMedia('(prefers-reduced-motion: reduce)');if(slides.length!==3)return;
const interval=4000,duration=550,held=new Set();let current=0,hovered=false,focused=false,inputMode='keyboard',timer=null,finishTimer=null,finishAnimation=null;
function stop(){if(timer!==null){clearTimeout(timer);timer=null;}}
function suspended(){return hovered||focused||held.size>0||document.hidden||motion.matches;}
function controls(){root.dataset.active=String(current);root.dataset.rotation=motion.matches?'reduced-motion':suspended()?'suspended':'playing';dots.forEach((d,i)=>d.setAttribute('aria-pressed',String(i===current)));slides.forEach((s,i)=>{s.setAttribute('aria-hidden',String(i!==current));s.inert=i!==current;});}
function schedule(){if(timer!==null||suspended())return;timer=setTimeout(()=>{timer=null;show((current+1)%slides.length);},interval);}
function reset(){stop();controls();schedule();}
function reorder(){track.style.transition='none';track.style.transform='translateX(0)';track.replaceChildren(...slides.slice(current),...slides.slice(0,current));}
function finish(){if(finishTimer!==null){clearTimeout(finishTimer);finishTimer=null;}if(finishAnimation){const f=finishAnimation;finishAnimation=null;f();}}
function show(index){stop();finish();if(index===current){reset();return;}const previous=current;track.style.transition='none';track.style.transform='translateX(0)';track.replaceChildren(slides[previous],slides[index],...slides.filter((_,i)=>i!==previous&&i!==index));void track.offsetWidth;current=index;controls();if(motion.matches)reorder();else{track.style.transition=`transform ${duration}ms cubic-bezier(.22,.61,.36,1)`;track.style.transform='translateX(-100%)';finishAnimation=reorder;finishTimer=setTimeout(finish,duration);}schedule();}
document.addEventListener('keydown',()=>{inputMode='keyboard';},true);
root.addEventListener('pointerenter',e=>{if(e.pointerType==='mouse'||e.pointerType==='pen'){hovered=true;reset();}},{passive:true});
root.addEventListener('pointerleave',e=>{if(e.pointerType==='mouse'||e.pointerType==='pen'){hovered=false;reset();}},{passive:true});
root.addEventListener('pointerdown',e=>{inputMode='pointer';focused=false;if(e.pointerType==='touch')held.add(e.pointerId);reset();},{passive:true});
function release(e){if(held.delete(e.pointerId)){focused=false;reset();}}
window.addEventListener('pointerup',release,{passive:true});window.addEventListener('pointercancel',release,{passive:true});
root.addEventListener('focusin',()=>{focused=inputMode==='keyboard';reset();});
root.addEventListener('focusout',()=>{queueMicrotask(()=>{focused=inputMode==='keyboard'&&root.contains(document.activeElement);reset();});});
dots.forEach((d,i)=>d.addEventListener('click',()=>show(i)));
root.addEventListener('keydown',e=>{if(!['ArrowLeft','ArrowRight','Home','End'].includes(e.key))return;e.preventDefault();focused=true;show(e.key==='Home'?0:e.key==='End'?slides.length-1:(current+(e.key==='ArrowRight'?1:-1)+slides.length)%slides.length);dots[current].focus();});
document.addEventListener('visibilitychange',reset);motion.addEventListener('change',()=>{stop();finish();reset();});
window.addEventListener('pagehide',stop);window.addEventListener('pageshow',reset);
reorder();root.dataset.enhanced='true';root.querySelector('.carousel-controls').hidden=false;reset();
})();
/* R64: whole-gallery tap/keyboard motion toggle; no visible pause button. */
(()=>{'use strict';
 const rows=[...document.querySelectorAll('[data-moving-gallery]')];
 if(!rows.length)return;
 document.documentElement.setAttribute('data-galleries-ready','');
 const state=(row,paused)=>{
   row.setAttribute('data-gallery-paused',String(paused));
   row.setAttribute('aria-pressed',String(paused));
   row.setAttribute('aria-label',(row.dataset.galleryTitle||'Suit gallery')+'; tap or press Enter to '+(paused?'resume':'pause')+' moving photographs');
 };
 rows.forEach(row=>{
   state(row,false);
   const toggle=()=>state(row,row.getAttribute('data-gallery-paused')!=='true');
   row.addEventListener('click',toggle);
   row.addEventListener('keydown',e=>{
     if(e.key==='Enter'||e.key===' '){e.preventDefault();toggle();}
   });
 });
 document.addEventListener('keydown',e=>{
   if(e.key==='Escape')rows.forEach(row=>state(row,true));
 });
})();
