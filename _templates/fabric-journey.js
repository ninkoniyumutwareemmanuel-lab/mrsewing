/* Existing ordinary-suit journey: one shared preference, fabric and illustrative colour. */
window.MrFabricJourney=function({api,source,resolve,friendly,url,ensureQuote,preferences}){
 const form=document.getElementById('fabricChoiceForm'),params=new URLSearchParams(location.search);
 const picking=location.pathname==='/guides/fabrics/'&&(params.get('fabricSelect')==='1'||params.has('fabricFor'));
 if(!form&&!picking){if(location.pathname==='/guides/fabrics/')document.body.classList.add('fabric-guide-page');return;}
 const rows=ensureQuote();
 function designs(parent){
  window.MrSelectedSuitQuote?.renderDesignSummary(parent);
  const edit=document.createElement('a');edit.className='home-text-link';edit.textContent='Add or Change Designs';edit.href=api.editSelectionsURL();parent.append(edit);
 }
 function empty(parent){const note=document.createElement('p');note.className='guide-notice';note.textContent='No designs selected. Choose a suit design to continue with fabric preferences.';const link=document.createElement('a');link.href='/services/custom-tailoring/';link.className='home-button home-button-gold';link.textContent='Explore Suit Designs';parent.append(note,link);}
 if(form){
  document.body.classList.add('fabric-preference-page');const summary=document.querySelector('[data-shared-design-summary]');
  if(!rows.length){form.hidden=true;empty(summary);return;}designs(summary);
  const button=form.querySelector('[type=submit]'),status=document.getElementById('fabric-choice-status'),current=api.fabricPreference();
  for(const radio of form.querySelectorAll('[name=sharedFabricChoice]'))radio.checked=current?.choice===radio.value;
  function selected(){return form.querySelector('[name=sharedFabricChoice]:checked')?.value;}
  function sync(){const choice=selected();button.textContent=choice==='now'?'Continue to Fabric Selection':choice?'Continue to Quotation':'Continue';if(choice){const old=api.fabricPreference();api.setFabricPreference({choice,fabricRef:choice==='now'?old?.fabricRef||'':'',colour:choice==='now'?old?.colour||'':'',colourDescription:choice==='now'?old?.colourDescription||'':'',pattern:choice==='now'?old?.pattern||'':''});}status.textContent='';}
  form.addEventListener('change',sync);sync();
  form.addEventListener('submit',event=>{event.preventDefault();if(!form.reportValidity())return;sync();location.href=selected()==='now'?url('/guides/fabrics/?fabricSelect=1&multiple=1'):api.quotationURL();});
  return;
 }
};
