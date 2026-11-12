/* Non-interactive sequence. Only the operating-system reduced-motion preference changes movement. */
(()=>{for(const bar of document.querySelectorAll('.announcement-bar')){const motion=matchMedia('(prefers-reduced-motion: reduce)');const paint=()=>bar.toggleAttribute('data-motion-ready',!motion.matches);motion.addEventListener('change',paint);paint();}})();

/* Track the real combined height so responsive and reduced-motion states keep anchors visible. */
(()=>{const header=document.getElementById('site-header');if(!header?.querySelector('.announcement-bar'))return;const root=document.documentElement;root.classList.add('has-sticky-offer');const measure=()=>root.style.setProperty('--offer-header-height',Math.ceil(header.getBoundingClientRect().height)+'px');measure();if(window.ResizeObserver)new ResizeObserver(measure).observe(header);window.addEventListener('resize',measure);window.addEventListener('pageshow',measure);})();
