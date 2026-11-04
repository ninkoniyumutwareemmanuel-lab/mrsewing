/* Three original text slides; no clones, auto-advance at five visible seconds. */
(()=>{'use strict';
const root=document.querySelector('[data-order-carousel]');if(!root)return;
const track=root.querySelector('.order-slides'),slides=[...track.querySelectorAll('[data-order-slide]')],dots=[...root.querySelectorAll('[data-order-select]')],toggle=root.querySelector('[data-carousel-toggle]'),position=root.querySelector('.carousel-position'),motion=matchMedia('(prefers-reduced-motion: reduce)');
if(slides.length!==3)return;
const interval=5000,duration=550;let current=0,userPaused=false,hovered=false,timer=null,started=0,remaining=interval,finishTimer=null,finishAnimation=null;
function stop(){if(timer!==null){clearTimeout(timer);timer=null;remaining=Math.max(0,remaining-(performance.now()-started));}}
function schedule(){if(timer!==null||userPaused||hovered||motion.matches||document.hidden)return;started=performance.now();timer=setTimeout(()=>{timer=null;show((current+1)%slides.length);},remaining);}
function controls(){root.dataset.active=String(current);root.dataset.rotation=motion.matches?'reduced-motion':userPaused?'paused':hovered||document.hidden?'suspended':'playing';dots.forEach((d,i)=>d.setAttribute('aria-pressed',String(i===current)));slides.forEach((s,i)=>{s.setAttribute('aria-hidden',String(i!==current));s.inert=i!==current;});position.textContent=`${current+1} / ${slides.length}`;toggle.hidden=motion.matches;toggle.textContent=userPaused?'Play':'Pause';toggle.setAttribute('aria-label',userPaused?'Start automatic order carousel':'Pause automatic order carousel');}
function reorder(){track.style.transition='none';track.style.transform='translateX(0)';track.replaceChildren(...slides.slice(current),...slides.slice(0,current));}
function finish(){if(finishTimer!==null){clearTimeout(finishTimer);finishTimer=null;}if(finishAnimation){const f=finishAnimation;finishAnimation=null;f();}}
function show(index){stop();finish();if(index===current){remaining=interval;controls();schedule();return;}const previous=current;track.style.transition='none';track.style.transform='translateX(0)';track.replaceChildren(slides[previous],slides[index],...slides.filter((_,i)=>i!==previous&&i!==index));void track.offsetWidth;current=index;remaining=interval;controls();if(motion.matches){reorder();}else{track.style.transition=`transform ${duration}ms cubic-bezier(.22,.61,.36,1)`;track.style.transform='translateX(-100%)';finishAnimation=reorder;finishTimer=setTimeout(finish,duration);}schedule();}
function pauseInteraction(){stop();userPaused=true;controls();}
dots.forEach((d,i)=>d.addEventListener('click',()=>{pauseInteraction();show(i);}));
toggle.addEventListener('click',()=>{stop();userPaused=!userPaused;if(!userPaused)hovered=false;controls();schedule();});
root.addEventListener('pointerenter',e=>{if(e.pointerType!=='touch'){stop();hovered=true;controls();}});
root.addEventListener('pointerleave',()=>{hovered=false;controls();schedule();});
root.addEventListener('pointerdown',e=>{if(!e.target.closest('[data-carousel-toggle]'))pauseInteraction();});
root.addEventListener('focusin',e=>{if(!e.target.closest('[data-carousel-toggle]'))pauseInteraction();});
root.addEventListener('keydown',e=>{if(!['ArrowLeft','ArrowRight','Home','End'].includes(e.key))return;e.preventDefault();pauseInteraction();show(e.key==='Home'?0:e.key==='End'?slides.length-1:(current+(e.key==='ArrowRight'?1:-1)+slides.length)%slides.length);dots[current].focus();});
document.addEventListener('visibilitychange',()=>{if(document.hidden)stop();controls();schedule();});
motion.addEventListener('change',()=>{stop();finish();controls();schedule();});
reorder();root.dataset.enhanced='true';root.querySelector('.carousel-controls').hidden=false;controls();schedule();
})();
