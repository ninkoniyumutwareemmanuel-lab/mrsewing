/* R56 paired galleries: explicit pause/resume plus keyboard, with no-JS static fallback. */
(()=>{'use strict';
 const rows=[...document.querySelectorAll('.r56-gallery-panel')];
 if(!rows.length)return;
 const set=(panel,paused)=>{
  const strip=panel.querySelector('.r56-gallery'),button=panel.querySelector('[data-r56-pause]');
  if(!strip||!button)return;
  strip.setAttribute('data-paused',String(paused));
  button.setAttribute('aria-pressed',String(paused));
  button.textContent=paused?'Resume motion':'Pause motion';
 };
 rows.forEach(panel=>{
  const button=panel.querySelector('[data-r56-pause]');
  if(!button)return;
  button.hidden=false;
  set(panel,false);
  button.addEventListener('click',()=>set(panel,panel.querySelector('.r56-gallery').getAttribute('data-paused')!=='true'));
 });
 document.addEventListener('keydown',e=>{
  if(e.key==='Escape')rows.forEach(panel=>set(panel,true));
 });
})();
