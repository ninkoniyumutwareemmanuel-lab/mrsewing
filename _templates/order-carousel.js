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
