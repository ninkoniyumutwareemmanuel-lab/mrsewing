/* R48: selected-suit quotation presentation. Existing flow snapshots and submission remain authoritative. */
(()=>{'use strict';
 const get=id=>document.getElementById(id);
 const active=()=>!!window.MrDesignSelections?.isSelectedQuote?.();
 const rows=()=>window.MrDesignSelections?.quoteSnapshot?.()||[];
 const friendly=name=>String(name||'').replace(/\s*[—·-]\s*MS-\d+\b/g,'').trim();
 function selectionURL(path){return window.MrDesignSelections?.selectionURL?.(path)||path;}
 function preferenceDetails(){
  const shared=window.MrDesignSelections?.fabricPreferenceDetails?.();if(shared)return shared;
  // Preserve supported older request URLs without pretending different legacy choices are one fabric.
  const selected=rows(),first=selected[0];if(!first)return{choice:'advice',label:'Help Me Choose Fabric'};
  const choices=new Set(selected.map(row=>[row.fabricChoice,row.fabricRef||''].join('|')));
  if(choices.size>1)return{choice:'legacy',label:'Existing fabric preferences',legacy:true};
  return{choice:first.fabricChoice,label:first.fabricChoice==='own'?'I Have My Own Fabric':first.fabricChoice==='advice'?'Help Me Choose Fabric':'Selected fabric',fabricName:first.fabricChoice==='now'?first.fabricName:'',colourName:''};
 }
 function summary(parent,{review=false}={}){
  const selected=rows(),total=selected.reduce((n,row)=>n+Number(row.quantity||row.qty||1),0);
  const section=document.createElement('section');section.className='selected-quote-block';
  const heading=document.createElement(review?'h3':'h2');heading.textContent='Your Selected Designs';section.append(heading);
  const details=document.createElement('details');details.className='selected-quote-summary';
  const trigger=document.createElement('summary'),count=document.createElement('span'),view=document.createElement('span');
  count.className='selected-quote-count';count.textContent=selected.length+' '+(selected.length===1?'design':'designs')+' selected · '+total+' '+(total===1?'garment':'garments');view.className='selected-quote-view';view.textContent='View Selected Designs';trigger.append(count,view);details.append(trigger);
  const grid=document.createElement('section');grid.className='batch-design-summary';grid.setAttribute('aria-label','Selected suit photographs and quantities');
  for(const row of selected){
   const item=document.createElement('article');item.dataset.designId=row.design;
   const photograph=document.createElement('a'),image=document.createElement('img'),copy=document.createElement('div'),name=document.createElement('h3'),quantity=document.createElement('p');
   photograph.href=new URL(row.src,location.origin).href;photograph.target='_blank';photograph.rel='noopener';photograph.className='selected-quote-photo';photograph.setAttribute('aria-label','View selected photograph of '+friendly(row.name));
   image.src=row.src;image.alt=friendly(row.alt||row.name);if(row.width)image.width=row.width;if(row.height)image.height=row.height;image.loading='lazy';image.decoding='async';photograph.append(image);
   name.textContent=friendly(row.name);quantity.textContent='Quantity: '+Number(row.quantity||row.qty||1);copy.append(name,quantity);item.append(photograph,copy);grid.append(item);
  }
  if(!selected.length){const empty=document.createElement('p');empty.textContent='No designs selected. Add a design before continuing.';grid.append(empty);}
  details.append(grid);section.append(details);parent.append(section);return section;
 }
 function preferenceSummary(parent,{review=false,edit=null}={}){
  const details=preferenceDetails(),section=document.createElement('section'),heading=document.createElement(review?'h3':'h2'),values=document.createElement('dl');
  section.className='selected-quote-block selected-quote-preference';heading.textContent='Your Fabric and Colour Preference';section.append(heading);
  function value(label,text){const term=document.createElement('dt'),definition=document.createElement('dd');term.textContent=label;definition.textContent=text;values.append(term,definition);}
  if(details.choice==='now'){
   value('Selected Fabric',details.fabricName||details.label||'Selected fabric');
   value('Preferred Colour',details.colourName?(details.colourName+(details.colourDescription?' — '+details.colourDescription:'')):'Not specified');
  }else value('Fabric Preference',details.label||(details.choice==='own'?'I Have My Own Fabric':'Help Me Choose Fabric'));
  section.append(values);
  const note=document.createElement('p');note.className='selected-preference-note';note.textContent=details.legacy?'Your existing fabric choices are retained. You can edit one shared preference for this enquiry.':'Applies to this enquiry, subject to fabric suitability, colour and availability confirmation for each garment.';section.append(note);
  if(edit){edit.href=selectionURL('/services/custom-tailoring/fabric/?multiple=1');edit.textContent='Edit Fabric Preference';edit.dataset.selectedFabricEdit='';const nav=document.createElement('nav');nav.className='selected-quote-edit';nav.setAttribute('aria-label','Edit fabric and colour preference');nav.append(edit);section.append(nav);}
  parent.append(section);return section;
 }
 function hide(node){if(!node)return;node.classList.add('selected-quote-hidden');node.hidden=true;for(const field of node.matches('input,select,textarea')?[node]:node.querySelectorAll('input,select,textarea')){field.disabled=true;field.required=false;field.setCustomValidity('');}}
 function hideField(id){const field=get(id);if(!field)return;const row=field.closest('.request-fields>div');if(row){hide(row);return;}for(const label of document.querySelectorAll('label[for="'+id+'"]'))hide(label);hide(field);if(field.parentElement?.matches('label'))hide(field.parentElement);}
 function labelFor(id,text){const label=document.querySelector('label[for="'+id+'"]');if(label)label.textContent=text;}
 function inputRow(id,label,name,type='text'){
  const row=document.createElement('div'),caption=document.createElement('label'),input=document.createElement('input');caption.htmlFor=id;caption.textContent=label+' (required)';input.id=id;input.name=name;input.type=type;input.required=true;input.addEventListener('input',()=>input.setCustomValidity(''));row.append(caption,input);return row;
 }
 function refresh(){
  if(!active())return;const form=get('customerRequestForm');if(!form)return;
  let holder=form.querySelector('[data-selected-quote-holder]');if(!holder){holder=document.createElement('div');holder.dataset.selectedQuoteHolder='';const anchor=form.querySelector('fieldset');if(anchor)anchor.before(holder);else form.prepend(holder);}
  const existingEdit=form.querySelector('[data-edit-designs]'),existingFabric=form.querySelector('[data-selected-fabric-edit]');
  const wasOpen=holder.querySelector('.selected-quote-summary')?.open||false;holder.replaceChildren();const block=summary(holder);block.querySelector('.selected-quote-summary').open=wasOpen;
  const nav=document.createElement('nav');nav.className='selected-quote-edit';nav.setAttribute('aria-label','Edit selected designs');
  let edit=existingEdit;if(!edit){edit=document.createElement('a');edit.dataset.editDesigns='';edit.textContent='Add or Change Designs';}edit.href=selectionURL('/services/custom-tailoring/');nav.append(edit);block.append(nav);
  const fabric=existingFabric||document.createElement('a');preferenceSummary(holder,{edit:fabric});
  const quantity=get('requestQuantity');if(quantity){quantity.value=rows().reduce((n,row)=>n+Number(row.quantity||row.qty||1),0);quantity.readOnly=true;hide(quantity.closest('.request-fields>div')||quantity);}
 }
 function apply(){
  if(!active())return;const form=get('customerRequestForm');if(!form)return;
  const first=form.dataset.selectedSuitReady!=='true';form.classList.add('selected-suit-quote');document.body.classList.add('selected-suit-quotation-page');
  const intro=document.querySelector('main .release-intro');if(intro){const heading=intro.querySelector('h1'),copy=intro.querySelector('p:last-child');if(heading)heading.textContent='Your Quotation Request';if(copy&&copy!==intro.querySelector('.home-eyebrow'))copy.textContent='Review your selections and tell us when you need your garments.';}
  const progress=document.querySelector('.request-progress');if(progress&&first){progress.replaceChildren(...['Your selections','Contact details & deadline','Review & submit'].map(text=>{const li=document.createElement('li');li.textContent=text;return li;}));}
  // Keep the existing source-of-truth inputs and listeners; remove their duplicated presentation only.
  const originalEdit=form.querySelector('[data-edit-designs]');if(originalEdit&&originalEdit.closest('[data-standard-design]'))form.append(originalEdit);
  for(const id of['requestPriority','requestAfterHours','requestGarment','requestOtherGarment','requestFabric','requestFabricChoice','requestFabricSelection','requestMeasurements'])hideField(id);
  hide(get('priority-guidance'));hide(get('requestFabricReferenceField'));hide(get('selectedDesignPreview'));hide(get('portfolioRequestContext'));hide(get('request-title'));hide(get('request-guidance'));
  const context=get('requestContextSummary');if(context)hide(context);
  const system=form.querySelector('fieldset:not(.selected-quote-deadline)');if(system&&!system.querySelector('#requestName')){system.classList.add('selected-quote-system');const legend=system.querySelector('legend');if(legend)hide(legend);}
  for(const node of form.querySelectorAll('[data-standard-design]'))hide(node);
  for(const id of['requestFabricChoice','requestFabric']){const block=get(id)?.closest('[data-custom-only]');if(block)hide(block);}
  const fields=form.querySelector('.request-fields');if(fields&&!get('selected-contact-heading')){const heading=document.createElement('h2');heading.id='selected-contact-heading';heading.className='selected-form-heading';heading.textContent='Contact and Delivery Details';fields.prepend(heading);}
  const location=get('requestLocation');if(location){location.name='Delivery Location / Address';location.maxLength=500;location.required=true;location.autocomplete='street-address';labelFor('requestLocation','Delivery location / address (required)');}
  labelFor('requestName','Full name (required)');labelFor('requestPhone','Phone / WhatsApp number (required)');labelFor('requestEmail','Email address (optional)');
  if(!get('requestCountry')){const row=inputRow('requestCountry','Country','Country'),input=row.querySelector('input');input.maxLength=160;input.autocomplete='country-name';const address=location?.closest('.request-fields>div');if(address)address.before(row);else fields?.append(row);}
  const date=get('requestDate');if(date){date.name='Requested Completion Date';date.required=true;date.disabled=false;date.setAttribute('aria-describedby','selected-deadline-guidance selected-deadline-zone');labelFor('requestDate','Completion date (required)');}
  if(!get('selected-quote-deadline')){
   const group=document.createElement('fieldset');group.id='selected-quote-deadline';group.className='selected-quote-deadline';const legend=document.createElement('legend');legend.textContent='When Do You Need Your Garments?';group.append(legend);
   const controls=document.createElement('div');controls.className='selected-deadline-controls';const dateRow=date?.closest('.request-fields>div');if(dateRow){dateRow.before(group);controls.append(dateRow);}else fields?.append(group);
   const timeRow=inputRow('requestCompletionTime','Completion time (Kigali)','Requested Completion Time','time'),time=timeRow.querySelector('input');time.step='60';time.setAttribute('aria-describedby','selected-deadline-guidance selected-deadline-zone');controls.append(timeRow);group.append(controls);
   const zone=document.createElement('p');zone.id='selected-deadline-zone';zone.className='request-note';zone.textContent='Kigali time — Africa/Kigali (UTC+02:00).';
   const note=document.createElement('p');note.id='selected-deadline-guidance';note.className='request-note';note.textContent='This is your requested completion deadline. Mr Sewing Fashion will confirm feasibility before accepting the order.';
   const timezone=document.createElement('input');timezone.type='hidden';timezone.name='Requested Completion Time Zone';timezone.value='Africa/Kigali (UTC+02:00)';group.append(zone,note,timezone);
  }
  const message=get('requestMessage');if(message){message.required=false;message.rows=3;message.setCustomValidity('');labelFor('requestMessage','Additional garment requirements (optional)');if(!get('selected-additional-heading')){const container=message.parentElement,heading=document.createElement('h2');heading.id='selected-additional-heading';heading.className='selected-form-heading';heading.textContent='Additional Requirements';container.classList.add('selected-quote-additional');container.prepend(heading);}}
  const reviewButton=get('reviewRequest');if(reviewButton)reviewButton.textContent='Review Quotation Request';
  refresh();form.dataset.selectedSuitReady='true';
  if(first)window.MrQuotationDraft?.restore?.();
 }
 function valid(){
  if(!active())return true;
  if(window.MrDesignSelections?.fabricPreferenceValid?.()===false){const status=get('requestStatus');if(status)status.textContent='Review your fabric and preferred colour, or choose fabric advice before continuing.';get('customerRequestForm')?.querySelector('[data-selected-fabric-edit]')?.focus();return false;}
  for(const id of['requestCountry','requestLocation']){const field=get(id);if(field)field.setCustomValidity(field.value.trim()?'':'Please complete this field.');}
  const date=get('requestDate'),time=get('requestCompletionTime');
  if(date){let good=/^\d{4}-\d{2}-\d{2}$/.test(date.value);if(good){const[dYear,dMonth,dDay]=date.value.split('-').map(Number),parsed=new Date(date.value+'T00:00:00Z');good=dYear>=1&&parsed.getUTCFullYear()===dYear&&parsed.getUTCMonth()===dMonth-1&&parsed.getUTCDate()===dDay;}date.setCustomValidity(good?'':'Enter a valid requested completion date.');}
  if(time)time.setCustomValidity(/^([01]\d|2[0-3]):[0-5]\d$/.test(time.value)?'':'Enter the requested completion time in Kigali time.');
  const okay=[get('requestCountry'),get('requestLocation'),date,time].filter(Boolean).every(field=>field.checkValidity());if(!okay)get('customerRequestForm')?.reportValidity();return okay;
 }
 function review(dl){if(!active())return;const term=document.createElement('dt'),definition=document.createElement('dd');term.textContent='Your Selected Designs';summary(definition,{review:true});dl.append(term,definition);const fabricTerm=document.createElement('dt'),fabricDefinition=document.createElement('dd');fabricTerm.textContent='Your Fabric and Colour Preference';preferenceSummary(fabricDefinition,{review:true});dl.append(fabricTerm,fabricDefinition);}
 window.MrSelectedSuitQuote={apply,refresh,valid,review,renderDesignSummary:summary};
 if(document.readyState==='complete')apply();else document.addEventListener('DOMContentLoaded',apply,{once:true});
})();
