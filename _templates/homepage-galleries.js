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
