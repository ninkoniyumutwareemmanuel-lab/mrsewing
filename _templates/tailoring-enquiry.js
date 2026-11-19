/* R52: improve an existing Terms-gated link; never send a message or upload a file. */
(()=>{'use strict';
 const config={{tailoring_positioning_config}};
 function data(){try{return JSON.parse(document.getElementById('design-data')?.textContent||'null')?.design||null;}catch{return null;}}
 function local(raw){try{const url=new URL(raw,location.origin);return url.origin===location.origin&&/^https?:$/.test(url.protocol)?url:null;}catch{return null;}}
 function approvedPath(raw,images){
  if(!raw)return null;
  try{
   const requested=new URL(raw,location.origin);
   // Existing request context uses production-canonical photograph URLs.
   if(![location.origin,'https://mrsewingfashion.com'].includes(requested.origin)||requested.search||requested.hash)return null;
   const image=images.find(image=>{const source=local(image.src);return source&&decodeURI(source.pathname)===decodeURI(requested.pathname);});
   return image?local(image.src):null;
  }catch{return null;}
 }
 function enhance(link){
  if(!link.dataset.tailoringDesign)return false;
  const design=data();
  if(!design||design.id!==link.dataset.tailoringDesign||!Array.isArray(design.images))return false;
  const detail=local(link.dataset.tailoringDetail),actual=local(design.url);
  if(!detail||!actual||detail.pathname!==actual.pathname||detail.search||detail.hash)return false;
  let selected=null;
  try{
   const action=document.querySelector('.design-enquiry');
   const selection=action?new URL(action.href,location.origin):null;
   if(selection?.searchParams.get('design')===design.id)selected=approvedPath(selection.searchParams.get('photo'),design.images);
  }catch{}
  if(!selected){const query=new URLSearchParams(location.search);if(!query.get('design')||query.get('design')===design.id)selected=approvedPath(query.get('photo'),design.images);}
  selected=selected||approvedPath(link.dataset.tailoringPhoto,design.images)||approvedPath(design.images[0]?.src,design.images);
  const name=String(link.dataset.tailoringDesignName||design.name||'').replace(/\s*[—·-]\s*MS-\d+\b/g,'').trim();
  if(!selected||!name||name.length>200||/[\r\n\x00-\x1f]/.test(name))return false;
  const preview=!['mrsewingfashion.com','www.mrsewingfashion.com'].includes(location.hostname);
  const text=[config.whatsapp.designIntroduction,'Design: '+name,'Photograph: '+selected.href,'Design details: '+detail.href,preview?config.whatsapp.previewNotice:'',config.whatsapp.manualPhotoNote].filter(Boolean).join('\n\n');
  // This is one design; do not truncate or bypass the full-list sharing module.
  if(text.length>1800||encodeURIComponent(text).length>5000)return false;
  link.href='/whatsapp/?'+new URLSearchParams({text});
  return true;
 }
 function initialize(){document.querySelectorAll('[data-tailoring-whatsapp]').forEach(enhance);}
 // Window capture runs before the existing document-capture Terms controller.
 // Refresh after a thumbnail change without replacing its selection behaviour.
 window.addEventListener('click',event=>{
  const link=event.target.closest?.('a[data-tailoring-whatsapp]');if(!link)return;
  enhance(link);
  document.dispatchEvent(new CustomEvent(config.measurement.eventName,{detail:{action:'whatsapp-design-click',context:link.dataset.tailoringWhatsapp,hasDesign:!!link.dataset.tailoringDesign}}));
 },true);
 if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',initialize);else initialize();
})();
