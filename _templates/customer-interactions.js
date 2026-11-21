/* WhatsApp chat opens directly; Terms are accessible in the site footer. */
(()=>{'use strict';let photo,opener;
function dialog(id,title){const d=document.createElement('dialog');d.id=id;d.className='customer-dialog';d.setAttribute('aria-labelledby',id+'-title');d.innerHTML='<button type="button" class="dialog-close" aria-label="Close dialog">Close</button><h2 id="'+id+'-title">'+title+'</h2>';d.querySelector('button').addEventListener('click',()=>d.close());d.addEventListener('close',()=>{opener?.focus({preventScroll:true});});document.body.append(d);return d;}
function openWhatsApp(text){const u=new URL('https://wa.me/250787411501');if(text)u.searchParams.set('text',String(text).slice(0,6000));window.open(u.href,'_blank','noopener');}
window.MrSewingWhatsApp={open:openWhatsApp};
function addTermsFooterLink(){
 const footer=document.querySelector('#site-footer footer, footer.homepage-footer, footer');
 if(!footer||footer.querySelector('.footer-terms-quicklink'))return;
 const parent=footer.querySelector('.footer-bottom-copy')||footer.querySelector('.footer-bottom')||footer;
 const a=document.createElement('a');a.href='/terms-and-conditions/current/';a.className='footer-terms-quicklink';a.textContent='Terms & Conditions';parent.appendChild(a);
}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',addTermsFooterLink,{once:true});else addTermsFooterLink();
document.addEventListener('click',e=>{
 const link=e.target.closest?.('[data-enlarge]');if(!link)return;const u=new URL(link.href,location.href);
 if(u.origin!==location.origin||!/^https?:$/.test(u.protocol))return;
 e.preventDefault();if(!photo){photo=dialog('measurementPhotoDialog','Measurement illustration');photo.append(document.createElement('img'));}
 opener=link;const img=photo.querySelector('img');img.src=u.href;img.alt=link.querySelector('img').alt;
 photo.querySelector('h2').textContent=link.getAttribute('aria-label').replace(/^Enlarge /,'');photo.showModal();photo.querySelector('button').focus();
},true);
})();

/* Optional Meta Pixel integration. Owner authorised placement on main.
   The owner-approved production flag and visitor consent system remain unchanged. */
(function () {
  "use strict";
  var config = /*meta-pixel-config*/null;
  if (!config || !config.productionEnabled || config.status !== "owner-approved-production") return;
  if (window.__mrSewingMetaPixelLoader) return;
  window.__mrSewingMetaPixelLoader = true;
  var tag = document.createElement("script");
  tag.src = "/assets/meta-pixel.js?v=compact-20261121";
  tag.async = true;
  tag.setAttribute("data-mr-meta-pixel", "");
  tag.dataset.pixelId = String(config.pixelId);
  tag.dataset.productionEnabled = "true";
  document.head.appendChild(tag);
})();
