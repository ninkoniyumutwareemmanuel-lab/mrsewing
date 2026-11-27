/* R64: whole-gallery tap/keyboard motion toggle; no visible pause button. */
(()=>{'use strict';
 const rows=[...document.querySelectorAll('[data-moving-gallery]')];
 if(!rows.length)return;
 document.documentElement.setAttribute('data-galleries-ready','');
 const state=(row,paused)=>{
   row.setAttribute('data-gallery-paused',String(paused));
   const control=row.querySelector('[data-gallery-motion-control]');if(control){control.setAttribute('aria-pressed',String(paused));control.textContent=(paused?'Resume':'Pause')+' moving photographs';}
   row.setAttribute('aria-description','Tap this gallery, or use its motion control, to pause or resume moving photographs. Escape pauses both galleries.');
 };
 rows.forEach(row=>{
   state(row,false);
   const toggle=()=>state(row,row.getAttribute('data-gallery-paused')!=='true');
   row.addEventListener('click',event=>{if(!event.target.closest('[data-gallery-motion-control]'))toggle();});row.querySelector('[data-gallery-motion-control]')?.addEventListener('click',toggle);
   row.addEventListener('keydown',e=>{
     if(e.target===row&&(e.key==='Enter'||e.key===' ')){e.preventDefault();toggle();}
   });
 });
 document.addEventListener('keydown',e=>{
   if(e.key==='Escape')rows.forEach(row=>state(row,true));
 });
})();
