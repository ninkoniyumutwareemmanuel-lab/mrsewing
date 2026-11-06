/* Continuous source-driven motion. Normal phone scrolling never stops a gallery. */
(()=>{'use strict';document.documentElement.setAttribute('data-galleries-ready','');document.addEventListener('keydown',e=>{if(e.key==='Escape')document.documentElement.setAttribute('data-galleries-paused','');});})();
