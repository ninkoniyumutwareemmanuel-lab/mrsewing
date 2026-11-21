/* R55 full-screen reader. Scrolls static pages rendered from the actual
   approved PDF; no embedded-PDF support or external JS dependency required. */
(()=>{'use strict';
const dialog=document.getElementById('termsPdfDialog');
if(!dialog)return;
const scroller=dialog.querySelector('[data-terms-scroll]');
const pages=dialog.querySelector('[data-terms-pages]');
const cards=[...dialog.querySelectorAll('.terms-popup-page')];
const indicator=dialog.querySelector('[data-terms-page-number]');
const zoomIn=dialog.querySelector('[data-terms-zoom-in]');
const zoomOut=dialog.querySelector('[data-terms-zoom-out]');
const closeButton=dialog.querySelector('[data-terms-close]');
const current='/terms-and-conditions/current/';
let pending=false,zoom=1;
function deepLink(){
 if(location.hash){
  let key;try{key=decodeURIComponent(location.hash.slice(1));}catch{return false;}
  if(/^[A-Za-z0-9_-]{1,100}$/.test(key)){
   location.replace(current+location.search+location.hash);return true;
  }
 }
 return false;
}
if(deepLink())return;
function pageIndicator(){
 const container=scroller.getBoundingClientRect();
 const center=container.top+Math.min(container.height*.44,410);
 let chosen=1,best=Infinity;
 cards.forEach((card,index)=>{
  const box=card.getBoundingClientRect();
  const distance=box.top>center?box.top-center:box.bottom<center?center-box.bottom:0;
  if(distance<best){best=distance;chosen=index+1;}
 });
 indicator.textContent=String(chosen);
 pending=false;
}
function requestPageIndicator(){
 if(!pending){pending=true;requestAnimationFrame(pageIndicator);}
}
function setZoom(){
 const available=Math.max(275,scroller.clientWidth-18);
 const baseline=Math.min(available,900);
 pages.style.width=Math.round(baseline*zoom)+'px';
 zoomOut.disabled=zoom<=1;
 zoomIn.disabled=zoom>=2.5;
 scroller.scrollLeft=Math.max(0,(scroller.scrollWidth-scroller.clientWidth)/2);
 requestPageIndicator();
}
zoomIn.addEventListener('click',()=>{zoom=Math.min(2.5,Math.round((zoom+.25)*100)/100);setZoom();});
zoomOut.addEventListener('click',()=>{zoom=Math.max(1,Math.round((zoom-.25)*100)/100);setZoom();});
window.addEventListener('resize',setZoom,{passive:true});
scroller.addEventListener('scroll',requestPageIndicator,{passive:true});
dialog.querySelectorAll('img').forEach(image=>image.addEventListener('load',requestPageIndicator,{once:true}));
function closeReader(){
 if(dialog.open)dialog.close();
 document.body.classList.remove('terms-popup-open');
 let sameOrigin=false;
 try{sameOrigin=!!document.referrer&&new URL(document.referrer).origin===location.origin;}catch{}
 if(sameOrigin&&history.length>1){history.back();}else{location.assign('/');}
}
closeButton.addEventListener('click',closeReader);
dialog.addEventListener('cancel',event=>{event.preventDefault();closeReader();});
if(typeof dialog.showModal==='function'){
 dialog.close();dialog.showModal();
}else{dialog.setAttribute('open','');}
document.body.classList.add('terms-popup-open');
setZoom();
scroller.focus({preventScroll:true});
requestPageIndicator();
})();
