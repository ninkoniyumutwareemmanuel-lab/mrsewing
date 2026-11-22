/* Staging R59: each row has an accessible pause; Escape pauses all. */
(()=>{'use strict';
 const rows=[...document.querySelectorAll('[data-moving-gallery]')];if(!rows.length)return;
 const reduce=window.matchMedia('(prefers-reduced-motion: reduce)');
 document.documentElement.setAttribute('data-galleries-ready','');
 const state=(row,paused)=>{row.setAttribute('data-gallery-paused',String(paused));const button=row.previousElementSibling;if(button?.matches('[data-gallery-pause]')){button.setAttribute('aria-pressed',String(paused));button.textContent=paused?'Resume motion':'Pause motion';}};
 rows.forEach(row=>{const button=row.previousElementSibling;if(!button?.matches('[data-gallery-pause]'))return;button.hidden=reduce.matches;state(row,false);button.addEventListener('click',()=>state(row,row.getAttribute('data-gallery-paused')!=='true'));});
 reduce.addEventListener('change',()=>rows.forEach(row=>{const button=row.previousElementSibling;if(button?.matches('[data-gallery-pause]'))button.hidden=reduce.matches;}));
 document.addEventListener('keydown',e=>{if(e.key==='Escape')rows.forEach(row=>state(row,true));});
})();
