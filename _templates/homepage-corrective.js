/* Homepage-only progressive enhancements; never change the standalone forms. */
(()=>{'use strict';
const dropdown=document.querySelector('.services-dropdown details');
document.addEventListener('keydown',e=>{if(e.key==='Escape'&&dropdown?.open){e.preventDefault();e.stopImmediatePropagation();dropdown.open=false;dropdown.querySelector('summary').focus();}},true);
document.addEventListener('click',e=>{if(dropdown?.open&&!dropdown.contains(e.target))dropdown.open=false;});
dropdown?.addEventListener('click',e=>{if(e.target.closest('a'))dropdown.open=false;});
const options=[...document.querySelectorAll('[data-option]')],panels=[...document.querySelectorAll('[data-option-panel]')];let current=0;
function show(index){current=(index+panels.length)%panels.length;options.forEach((e,i)=>e.setAttribute('aria-pressed',String(i===current)));panels.forEach((e,i)=>e.hidden=i!==current);const pos=document.querySelector('.option-position');if(pos)pos.textContent=`${current+1} / ${panels.length}`;}
options.forEach((button,i)=>{button.addEventListener('click',()=>show(i));button.addEventListener('keydown',e=>{if(['ArrowLeft','ArrowRight','Home','End'].includes(e.key)){e.preventDefault();show(e.key==='Home'?0:e.key==='End'?panels.length-1:current+(e.key==='ArrowRight'?1:-1));options[current].focus();}});});
document.querySelectorAll('[data-option-direction]').forEach(e=>e.addEventListener('click',()=>show(current+Number(e.dataset.optionDirection))));if(panels.length)show(0);
const form=document.getElementById('quotationForm');if(!form)return;const button=form.querySelector('[type=submit]'),phone=document.getElementById('quotePhone'),message=document.getElementById('quoteMessage'),status=document.getElementById('quoteStatus'),success=document.getElementById('quoteSuccess');let pending=false;const label=button.innerHTML;
function validate(){const value=phone.value.trim(),digits=value.replace(/\D/g,'').length;phone.setCustomValidity(/^[0-9+\-\s().]+$/.test(value)&&digits>=7&&digits<=15?'':'Enter a valid phone number including your country code.');message.setCustomValidity(message.value.trim()?'':'Please tell us what you need.');}
phone.addEventListener('input',validate);message.addEventListener('input',validate);
form.addEventListener('submit',async e=>{e.preventDefault();validate();if(pending||!form.reportValidity())return;if(form.elements.botcheck.value){status.textContent='We could not confirm your request. Please contact us directly.';return;}
const data=Object.fromEntries(new FormData(form));delete data.botcheck;const email=data['Email Address'].trim();data['Email Address']=email||'Not provided';if(email)data.replyto=email;data['Terms Consent']='Agreed';data['Customer Message']=message.value.trim();pending=true;button.disabled=true;button.textContent='Sending…';form.setAttribute('aria-busy','true');status.textContent='Sending your request. Please wait.';const controller=new AbortController(),timer=setTimeout(()=>controller.abort(),20000);
try{const response=await fetch(form.action,{method:'POST',headers:{'Content-Type':'application/json',Accept:'application/json'},body:JSON.stringify(data),signal:controller.signal});const result=await response.json();if(!response.ok||result.success!==true)throw new Error('Not confirmed');form.hidden=true;success.hidden=false;success.focus();}
catch(error){status.textContent=error.name==='AbortError'?'We could not confirm delivery before the connection timed out. Your request may have arrived. Please contact us on WhatsApp before trying again.':'We could not confirm your request. Your entries are preserved. Please try again or contact us directly on WhatsApp.';}
finally{clearTimeout(timer);pending=false;button.disabled=false;button.innerHTML=label;form.removeAttribute('aria-busy');}});
})();
