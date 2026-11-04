/* Homepage-only progressive enhancements; never change the standalone forms. */
(()=>{'use strict';
const dropdown=document.querySelector('.services-dropdown details');
document.addEventListener('keydown',e=>{if(e.key==='Escape'&&dropdown?.open){e.preventDefault();e.stopImmediatePropagation();dropdown.open=false;dropdown.querySelector('summary').focus();}},true);
document.addEventListener('click',e=>{if(dropdown?.open&&!dropdown.contains(e.target))dropdown.open=false;});
dropdown?.addEventListener('click',e=>{if(e.target.closest('a'))dropdown.open=false;});
// Keep the hero quotation journey distinct from the customer-support form.
const dialog=document.getElementById('quotation');
if(dialog&&typeof dialog.showModal==='function'){
 let returnFocus=null;dialog.close();dialog.dataset.modalReady='true';dialog.dataset.ready='true';const close=dialog.querySelector('.quotation-close');close.hidden=false;
 function openQuote(trigger){returnFocus=trigger||document.querySelector('.hero-actions a[href="#quotation"]');if(!dialog.open)dialog.showModal();document.getElementById('quotation-dialog-title').focus();}
 document.querySelectorAll('a[href="#quotation"]').forEach(a=>a.addEventListener('click',e=>{e.preventDefault();openQuote(a);}));
 close.addEventListener('click',()=>dialog.close());dialog.addEventListener('click',e=>{if(e.target===dialog){const r=dialog.getBoundingClientRect();if(e.clientX<r.left||e.clientX>r.right||e.clientY<r.top||e.clientY>r.bottom)dialog.close();}});
 dialog.addEventListener('close',()=>{if(returnFocus?.isConnected)returnFocus.focus({preventScroll:true});});
 if(location.hash==='#quotation')openQuote();
}
// Both enquiries reuse the existing approved provider, with independent pending and success state.
function setupEnquiry(prefix,formId){
 const form=document.getElementById(formId);if(!form)return;
 const button=form.querySelector('[type=submit]'),phone=document.getElementById(prefix+'Phone'),message=document.getElementById(prefix+'Message'),status=document.getElementById(prefix+'Status'),success=document.getElementById(prefix+'Success');let pending=false;const label=button.innerHTML;
 function validate(){const value=phone.value.trim(),digits=value.replace(/\D/g,'').length;phone.setCustomValidity(/^[0-9+\-\s().]+$/.test(value)&&digits>=7&&digits<=15?'':'Enter a valid phone number including your country code.');message.setCustomValidity(message.value.trim()?'':'Please tell us how we can help.');}
 phone.addEventListener('input',validate);message.addEventListener('input',validate);
 form.addEventListener('submit',async e=>{e.preventDefault();validate();if(pending||!form.reportValidity())return;if(form.elements.botcheck.value){status.textContent='We could not confirm your request. Please contact us directly.';return;}
 const data=Object.fromEntries(new FormData(form));delete data.botcheck;const email=data['Email Address'].trim();data['Email Address']=email||'Not provided';if(email)data.replyto=email;data['Terms Consent']='Agreed';data['Customer Message']=message.value.trim();pending=true;button.disabled=true;button.textContent='Sending…';form.setAttribute('aria-busy','true');status.textContent='Sending your request. Please wait.';const controller=new AbortController(),timer=setTimeout(()=>controller.abort(),20000);
 try{const response=await fetch(form.action,{method:'POST',headers:{'Content-Type':'application/json',Accept:'application/json'},body:JSON.stringify(data),signal:controller.signal});const result=await response.json();if(!response.ok||result.success!==true)throw new Error('Not confirmed');form.hidden=true;success.hidden=false;success.focus();}
 catch(error){status.textContent=error.name==='AbortError'?'We could not confirm delivery before the connection timed out. Your request may have arrived. Please contact us on WhatsApp before trying again.':'We could not confirm your request. Your entries are preserved. Please try again or contact us directly on WhatsApp.';}
 finally{clearTimeout(timer);pending=false;button.disabled=false;button.innerHTML=label;form.removeAttribute('aria-busy');}
 });
}
setupEnquiry('quote','quotationForm');setupEnquiry('support','supportForm');
})();
