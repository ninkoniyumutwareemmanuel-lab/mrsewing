/* Existing section URLs remain useful without guessing PDF page numbers. */
(()=>{'use strict';
 const panel=document.querySelector('[data-policy-document-current]');if(!panel)return;
 const anchors=new Set([...document.querySelectorAll('[data-policy-document-anchor]')].map(node=>node.id));
 function focusDocument(){let key;try{key=decodeURIComponent(location.hash.slice(1));}catch{return;}if(!key||!anchors.has(key))return;const heading=document.getElementById('policy-document-heading');panel.scrollIntoView({block:'start',behavior:'auto'});heading?.focus({preventScroll:true});}
 addEventListener('hashchange',focusDocument);const initialFocus=()=>requestAnimationFrame(focusDocument);if(document.readyState==='complete')initialFocus();else document.addEventListener('DOMContentLoaded',initialFocus,{once:true});
})();
