/* Existing gallery motion and Escape pause preserved; add per-gallery pause controls. */
(()=>{'use strict';
 document.documentElement.setAttribute('data-galleries-ready','');
 for(const region of document.querySelectorAll('[data-moving-gallery]')){
  const button=region.previousElementSibling;
  if(!button||!button.matches('[data-gallery-toggle]'))continue;
  button.hidden=false;
  button.addEventListener('click',()=>{
   const paused=region.dataset.galleryPaused!=='true';
   region.dataset.galleryPaused=String(paused);
   button.setAttribute('aria-pressed',String(paused));
   button.textContent=paused?'Resume photos':'Pause photos';
  });
 }
 document.addEventListener('keydown',event=>{
  if(event.key!=='Escape')return;
  document.documentElement.setAttribute('data-galleries-paused','');
  for(const region of document.querySelectorAll('[data-moving-gallery]')){
   region.dataset.galleryPaused='true';
   const button=region.previousElementSibling;
   if(button&&button.matches('[data-gallery-toggle]')){
    button.setAttribute('aria-pressed','true');
    button.textContent='Resume photos';
   }
  }
 });
})();
