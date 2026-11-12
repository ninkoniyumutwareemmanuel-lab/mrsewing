/* R45: selected-suit quote presentation only. Existing selection, fabric and submission systems stay authoritative. */
(()=>{'use strict';
 const get=id=>document.getElementById(id);
 const active=()=>!!window.MrDesignSelections?.isSelectedQuote?.();
 const rows=()=>window.MrDesignSelections?.quoteSnapshot?.()||[];
 const friendly=name=>String(name||'').replace(/\s*[—·-]\s*MS-\d+\b/g,'').trim();
 function selectionURL(path){return window.MrDesignSelections?.selectionURL?.(path)||path;}
 function fabricText(row){return row.fabricChoice==='own'?'I Have My Own Fabric':row.fabricChoice==='advice'?'Help Me Choose Fabric':row.fabricName||'Selected fabric';}
 function summary(parent,{review=false}={}){
  const selected=rows(),total=selected.reduce((n,row)=>n+Number(row.quantity||row.qty||1),0);
  const section=document.createElement('section');section.className='selected-quote-block';
  const heading=document.createElement(review?'h3':'h2');heading.textContent='Your Selected Designs';section.append(heading);
  const details=document.createElement('details');details.className='selected-quote-summary';
  const trigger=document.createElement('summary'),count=document.createElement('span'),view=document.createElement('span');
  count.className='selected-quote-count';count.textContent=selected.length+' '+(selected.length===1?'design':'designs')+' selected · '+total+' '+(total===1?'garment':'garments');view.className='selected-quote-view';view.textContent='View Selected Designs';trigger.append(count,view);details.append(trigger);
  const grid=document.createElement('section');grid.className='batch-design-summary';grid.setAttribute('aria-label','Selected suit photographs and fabric preferences');
  for(const row of selected){
   const item=document.createElement('article');item.dataset.designId=row.design;
   const photograph=document.createElement('a'),image=document.createElement('img'),copy=document.createElement('div'),name=document.createElement('h3'),quantity=document.createElement('p'),fabric=document.createElement('p');
   photograph.href=new URL(row.src,location.origin).href;photograph.target='_blank';photograph.rel='noopener';photograph.className='selected-quote-photo';photograph.setAttribute('aria-label','View selected photograph of '+friendly(row.name));
   image.src=row.src;image.alt=row.alt||friendly(row.name);if(row.width)image.width=row.width;if(row.height)image.height=row.height;image.loading='lazy';image.decoding='async';photograph.append(image);
   name.textContent=friendly(row.name);quantity.textContent='Quantity: '+Number(row.quantity||row.qty||1);fabric.textContent='Fabric: '+fabricText(row);fabric.className='selected-quote-fabric';copy.append(name,quantity,fabric);item.append(photograph,copy);grid.append(item);
  }
  if(!selected.length){const empty=document.createElement('p');empty.textContent='No designs selected. Add a design before continuing.';grid.append(empty);}
  details.append(grid);section.append(details);parent.append(section);return section;
 }
 function hide(node){if(!node)return;node.classList.add('selected-quote-hidden');node.hidden=true;for(const field of node.matches('input,select,textarea')?[node]:node.querySelectorAll('input,select,textarea')){field.disabled=true;field.required=false;field.setCustomValidity('');}}
 function hideField(id){const field=get(id);if(!field)return;const row=field.closest('.request-fields>div');if(row){hide(row);return;}for(const label of document.querySelectorAll('label[for="'+id+'"]'))hide(label);hide(field);if(field.parentElement?.matches('label'))hide(field.parentElement);}
 function labelFor(id,text){const label=document.querySelector('label[for="'+id+'"]');if(label)label.textContent=text;}
 function inputRow(id,label,name,type='text'){
  const row=document.createElement('div'),caption=document.createElement('label'),input=document.createElement('input');caption.htmlFor=id;caption.textContent=label+' (required)';input.id=id;input.name=name;input.type=type;input.required=true;input.addEventListener('input',()=>input.setCustomValidity(''));row.append(caption,input);return row;
 }
 function refresh(){
  if(!active())return;const form=get('customerRequestForm');if(!form)return;
  let holder=form.querySelector('[data-selected-quote-holder]');if(!holder){holder=document.createElement('div');holder.dataset.selectedQuoteHolder='';const anchor=get('requestContextSummary');if(anchor)anchor.after(holder);else form.prepend(holder);}
  const existingEdit=form.querySelector('[data-edit-designs]'),existingFabric=form.querySelector('[data-selected-fabric-edit]');
  holder.replaceChildren();const block=summary(holder);
  const nav=document.createElement('nav');nav.className='selected-quote-edit';nav.setAttribute('aria-label','Edit selected designs or fabric preferences');
  let edit=existingEdit;if(!edit){edit=document.createElement('a');edit.dataset.editDesigns='';edit.textContent='Add or Change Designs';}edit.href=selectionURL('/services/custom-tailoring/');
  let fabric=existingFabric;if(!fabric){fabric=document.createElement('a');fabric.dataset.selectedFabricEdit='';fabric.textContent='Edit Fabric Selection';}fabric.href=selectionURL('/services/custom-tailoring/fabric/?multiple=1');nav.append(edit,fabric);block.append(nav);
  const quantity=get('requestQuantity');if(quantity){quantity.value=rows().reduce((n,row)=>n+Number(row.quantity||row.qty||1),0);quantity.readOnly=true;hide(quantity.closest('.request-fields>div')||quantity);}
 }
 function apply(){
  if(!active())return;const form=get('customerRequestForm');if(!form)return;
  const first=form.dataset.selectedSuitReady!=='true';form.classList.add('selected-suit-quote');
  const progress=document.querySelector('.request-progress');if(progress&&first){progress.replaceChildren(...['Selected designs','Contact details & requested deadline','Review'].map(text=>{const li=document.createElement('li');li.textContent=text;return li;}));}
  // Move the existing design action before hiding its former record-only container.
  const originalEdit=form.querySelector('[data-edit-designs]');if(originalEdit&&originalEdit.closest('[data-standard-design]'))form.append(originalEdit);
  for(const id of['requestPriority','requestAfterHours','requestGarment','requestOtherGarment','requestFabric','requestFabricChoice','requestFabricSelection'])hideField(id);
  hide(get('priority-guidance'));hide(get('requestFabricReferenceField'));hide(get('selectedDesignPreview'));hide(get('portfolioRequestContext'));
  for(const node of form.querySelectorAll('[data-standard-design]'))hide(node);
  for(const id of['requestFabricChoice','requestFabric']){const block=get(id)?.closest('[data-custom-only]');if(block)hide(block);}
  const location=get('requestLocation');if(location){location.name='Delivery Location / Address';location.maxLength=500;location.required=true;location.autocomplete='street-address';labelFor('requestLocation','Delivery location / address (required)');}
  if(!get('requestCountry')){const row=inputRow('requestCountry','Country','Country'),input=row.querySelector('input');input.maxLength=160;input.autocomplete='country-name';const address=location?.closest('.request-fields>div');if(address)address.before(row);else form.querySelector('.request-fields')?.append(row);}
  const date=get('requestDate');if(date){date.name='Requested Completion Date';date.required=true;date.disabled=false;date.setAttribute('aria-describedby','selected-deadline-guidance selected-deadline-zone');labelFor('requestDate','Requested completion date (required)');}
  if(!get('selected-quote-deadline')){
   const group=document.createElement('fieldset');group.id='selected-quote-deadline';group.className='selected-quote-deadline';const legend=document.createElement('legend');legend.textContent='When do you need your garments completed?';group.append(legend);
   const controls=document.createElement('div');controls.className='selected-deadline-controls';const dateRow=date?.closest('.request-fields>div');if(dateRow){dateRow.before(group);controls.append(dateRow);}else form.querySelector('.request-fields')?.append(group);
   const timeRow=inputRow('requestCompletionTime','Requested completion time (Kigali)','Requested Completion Time','time'),time=timeRow.querySelector('input');time.step='60';time.setAttribute('aria-describedby','selected-deadline-guidance selected-deadline-zone');controls.append(timeRow);group.append(controls);
   const zone=document.createElement('p');zone.id='selected-deadline-zone';zone.className='request-note';zone.textContent='Use Kigali time (Africa/Kigali, UTC+02:00), including when you are outside Rwanda.';
   const note=document.createElement('p');note.id='selected-deadline-guidance';note.className='request-note';note.textContent='This is your requested completion deadline. Mr Sewing Fashion will confirm whether the requested date and time are possible before accepting the order.';
   const timezone=document.createElement('input');timezone.type='hidden';timezone.name='Requested Completion Time Zone';timezone.value='Africa/Kigali (UTC+02:00)';group.append(zone,note,timezone);
  }
  const message=get('requestMessage');if(message){message.required=false;message.setCustomValidity('');labelFor('requestMessage','Additional garment requirements (optional)');}
  const context=get('requestContextSummary');if(context)context.textContent='Custom Tailoring & Suits · Your selected designs';
  const guidance=get('request-guidance');if(guidance)guidance.textContent='Review your selected suits and provide your contact details and requested completion deadline. Measurements are not required to begin.';
  refresh();form.dataset.selectedSuitReady='true';
  if(first)window.MrQuotationDraft?.restore?.();
 }
 function valid(){
  if(!active())return true;
  for(const id of['requestCountry','requestLocation']){const field=get(id);if(field)field.setCustomValidity(field.value.trim()?'':'Please complete this field.');}
  const date=get('requestDate'),time=get('requestCompletionTime');
  if(date){let good=/^\d{4}-\d{2}-\d{2}$/.test(date.value);if(good){const[dYear,dMonth,dDay]=date.value.split('-').map(Number),parsed=new Date(date.value+'T00:00:00Z');good=dYear>=1&&parsed.getUTCFullYear()===dYear&&parsed.getUTCMonth()===dMonth-1&&parsed.getUTCDate()===dDay;}date.setCustomValidity(good?'':'Enter a valid requested completion date.');}
  if(time)time.setCustomValidity(/^([01]\d|2[0-3]):[0-5]\d$/.test(time.value)?'':'Enter the requested completion time in Kigali time.');
  const okay=[get('requestCountry'),get('requestLocation'),date,time].filter(Boolean).every(field=>field.checkValidity());if(!okay)get('customerRequestForm')?.reportValidity();return okay;
 }
 function review(dl){if(!active())return;const term=document.createElement('dt'),definition=document.createElement('dd');term.textContent='Your Selected Designs';summary(definition,{review:true});dl.append(term,definition);}
 window.MrSelectedSuitQuote={apply,refresh,valid,review};
 if(document.readyState==='complete')apply();else document.addEventListener('DOMContentLoaded',apply,{once:true});
})();
