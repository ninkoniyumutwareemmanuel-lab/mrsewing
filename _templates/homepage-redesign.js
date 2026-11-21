/* R56 paired galleries: explicit pause/resume, keyboard and reduced-motion. */
(()=>{'use strict';
 const rows=[...document.querySelectorAll('.r56-gallery-panel')];
 if(!rows.length)return;
 rows.forEach(panel=>{
  const strip=panel.querySelector('.r56-gallery'),button=panel.querySelector('[data-r56-pause]');
  if(!strip||!button)return;
  let paused=false;
  function refresh(){strip.setAttribute('data-paused',String(paused));button.setAttribute('aria-pressed',String(paused));button.textContent=paused?'Resume motion':'Pause motion';}
  button.addEventListener('click',()=>{paused=!paused;refresh();});
  refresh();
 });
 document.addEventListener('keydown',e=>{
  if(e.key!=='Escape')return;
  for(const panel of rows){
   const strip=panel.querySelector('.r56-gallery'),button=panel.querySelector('[data-r56-pause]');
   if(strip&&button){strip.setAttribute('data-paused','true');button.setAttribute('aria-pressed','true');button.textContent='Resume motion';}
  }
 });
})();
