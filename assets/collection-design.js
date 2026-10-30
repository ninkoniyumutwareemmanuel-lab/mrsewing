/* Static garment page: enquiry, accessible original-photo viewing and sharing. */
(() => {
  'use strict';
  const d=JSON.parse(document.getElementById('design-data').textContent).design;
  const $=id=>document.getElementById(id),dialog=$('photo-viewer'),img=dialog.querySelector('img');
  const url=new URL(d.url,location.origin).href;
  document.querySelector('.design-enquiry').href='https://wa.me/250787411501?text='+encodeURIComponent(`Hello Mr Sewing! I would like to discuss this design.\nDesign: ${d.name}\nReference: ${d.id}\nLink: ${url}`);
  let index=0,previousOverflow='',opener=null,sharing=false;
  function photo(){const i=d.images[index];img.src=i.src;img.alt=i.alt;img.width=i.width;img.height=i.height;$('photo-count').textContent=`${index+1} / ${d.images.length}`;$('photo-previous').disabled=$('photo-next').disabled=d.images.length<2;}
  function open(i=0,source=$('open-photo')){index=i;opener=source;previousOverflow=document.body.style.overflow;photo();dialog.showModal();document.body.style.overflow='hidden';$('close-photo').focus();}
  function next(delta){index=(index+delta+d.images.length)%d.images.length;photo();}
  $('open-photo').addEventListener('click',e=>{e.preventDefault();open();});
  document.querySelectorAll('[data-photo]').forEach(b=>b.addEventListener('click',()=>open(Number(b.dataset.photo),b)));
  $('close-photo').addEventListener('click',()=>dialog.close());dialog.addEventListener('close',()=>{document.body.style.overflow=previousOverflow;opener?.focus({preventScroll:true});});
  $('photo-previous').addEventListener('click',()=>next(-1));$('photo-next').addEventListener('click',()=>next(1));
  dialog.addEventListener('keydown',e=>{if(e.key==='ArrowLeft'||e.key==='ArrowRight'){e.preventDefault();next(e.key==='ArrowRight'?1:-1);}if(e.key==='Tab'){const buttons=[...dialog.querySelectorAll('button')].filter(b=>!b.disabled);if(e.shiftKey&&document.activeElement===buttons[0]){e.preventDefault();buttons.at(-1).focus();}else if(!e.shiftKey&&document.activeElement===buttons.at(-1)){e.preventDefault();buttons[0].focus();}}});
  let touch;img.addEventListener('touchstart',e=>{touch=e.changedTouches[0];},{passive:true});img.addEventListener('touchend',e=>{if(!touch)return;const end=e.changedTouches[0],dx=end.clientX-touch.clientX,dy=end.clientY-touch.clientY;touch=null;if(Math.abs(dx)>60&&Math.abs(dx)>Math.abs(dy)*1.3)next(dx<0?1:-1);},{passive:true});
  img.addEventListener('error',()=>{$('photo-count').textContent='Photograph unavailable. Close to return to the design.';});
  async function copy(){
    try{if(!navigator.clipboard?.writeText)throw Error('Unavailable');await navigator.clipboard.writeText(url);$('share-status').textContent='Design link copied.';}
    catch{let input=$('manual-share-link');if(!input){input=document.createElement('input');input.id='manual-share-link';input.className='manual-share-link';input.readOnly=true;input.setAttribute('aria-label','Design link to copy');$('share-status').after(input);}input.value=url;input.focus();input.select();$('share-status').textContent='Select and copy this design link.';}
  }
  $('share-design').hidden=false;$('share-design').addEventListener('click',async()=>{
    if(sharing)return;sharing=true;$('share-design').disabled=true;$('manual-share-link')?.remove();
    try{if(navigator.share){try{await navigator.share({title:d.name,text:'Explore this design with Mr Sewing.',url});$('share-status').textContent='Design sharing completed.';}catch(e){if(e.name==='AbortError')$('share-status').textContent='Sharing cancelled.';else await copy();}}else await copy();}
    finally{sharing=false;$('share-design').disabled=false;}
  });
})();
