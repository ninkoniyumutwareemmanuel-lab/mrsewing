/* Non-interactive sequence. Only the operating-system reduced-motion preference changes movement. */
(()=>{for(const bar of document.querySelectorAll('.announcement-bar')){const motion=matchMedia('(prefers-reduced-motion: reduce)');const paint=()=>bar.toggleAttribute('data-motion-ready',!motion.matches);motion.addEventListener('change',paint);paint();}})();
