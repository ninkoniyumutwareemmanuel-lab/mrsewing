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
  function sync(){const choice=selected();button.textContent=choice==='now'?'Continue to Fabric Selection':choice?'Continue to Quotation':'Continue';if(choice){const old=api.fabricPreference();api.setFabricPreference({choice,fabricRef:choice==='now'?old?.fabricRef||'':'',colour:choice==='now'?old?.colour||'':'',colourDescription:choice==='now'?old?.colourDescription||'':''});}status.textContent='';}
  form.addEventListener('change',sync);sync();
  form.addEventListener('submit',event=>{event.preventDefault();if(!form.reportValidity())return;sync();location.href=selected()==='now'?url('/guides/fabrics/?fabricSelect=1&multiple=1'):api.quotationURL();});
  return;
 }
 document.body.classList.add('fabric-guide-page');const collection=document.querySelector('.guide-collection');if(!collection)return;
 const panel=document.createElement('section');panel.className='fabric-selection-context';panel.setAttribute('aria-label','Fabric and colour selection');collection.before(panel);
 if(!rows.length){empty(panel);return;}
 const heading=document.createElement('h2'),instruction=document.createElement('p'),summary=document.createElement('div');heading.textContent='Choose a Fabric and Colour';instruction.textContent='Select one preferred fabric and colour for your enquiry. We assess suitability for each garment.';panel.append(heading,instruction);summary.className='fabric-selection-designs';designs(summary);panel.append(summary);
 const selected=document.createElement('div');selected.className='fabric-choice-confirmation';selected.setAttribute('aria-live','polite');panel.append(selected);
 const colourForm=document.createElement('form');colourForm.id='sharedFabricColourForm';colourForm.setAttribute('aria-label','Preferred fabric colour');
 const fieldset=document.createElement('fieldset'),legend=document.createElement('legend');legend.textContent='Preferred Colour — Subject to Availability Confirmation';fieldset.append(legend);
 const note=document.createElement('p');note.className='request-note';note.id='fabric-colour-note';note.textContent='Swatches are illustrative and may differ from the actual fabric shade. These are colour preferences, not confirmed stock.';fieldset.append(note);
 const groupNames={neutral:'Neutral colours',blue:'Blue shades','red-purple':'Red and purple','earth-green':'Earth and green',other:'Another colour'};
 for(const [group,title]of Object.entries(groupNames)){
  const section=document.createElement('section'),h=document.createElement('h3'),grid=document.createElement('div');h.textContent=title;grid.className='fabric-colour-grid';
  for(const [id,colour]of Object.entries(source.colours).filter(([,c])=>c.group===group)){
   const label=document.createElement('label'),input=document.createElement('input'),swatch=document.createElement('span'),name=document.createElement('span');label.className='fabric-colour-option';input.type='radio';input.name='preferredColour';input.value=id;input.required=true;input.setAttribute('aria-describedby','fabric-colour-note');swatch.className='fabric-colour-swatch';swatch.setAttribute('aria-hidden','true');if(colour.hex)swatch.style.backgroundColor=colour.hex;else{swatch.classList.add('fabric-colour-other');swatch.textContent='?';}name.className='fabric-colour-name';name.textContent=colour.name;label.append(input,swatch,name);grid.append(label);
  }section.append(h,grid);fieldset.append(section);
 }
 const other=document.createElement('div'),otherLabel=document.createElement('label'),description=document.createElement('input');other.className='fabric-colour-description';otherLabel.htmlFor='colourDescription';otherLabel.textContent='Describe your preferred colour (up to 80 characters)';description.id='colourDescription';description.name='colourDescription';description.maxLength=80;description.autocomplete='off';other.append(otherLabel,description);fieldset.append(other);colourForm.append(fieldset);
 const status=document.createElement('p');status.id='fabric-colour-status';status.setAttribute('role','status');status.setAttribute('aria-live','polite');const button=document.createElement('button');button.type='submit';button.className='home-button home-button-gold';button.dataset.fabricContinue='';button.textContent='Continue to Quotation';const edit=document.createElement('a');edit.className='home-text-link';edit.href=url('/services/custom-tailoring/fabric/?multiple=1');edit.textContent='Edit Fabric Preference';const actions=document.createElement('div');actions.className='request-actions';actions.append(button,edit);colourForm.append(status,actions);
 // Keep fabric cards first, then the colour selector in the same existing guide.
 collection.after(colourForm);
 function descriptionValid(){const text=description.value.trim(),valid=!!text&&text.length<=80&&/^[\p{L}\p{N} .,'’()/+#-]{1,80}$/u.test(text);description.setCustomValidity(valid?'':'Describe the colour using up to 80 letters, numbers and basic colour punctuation.');return valid;}
 function paint(){
  const pref=api.fabricPreference(),details=api.fabricPreferenceDetails();selected.replaceChildren();
  for(const [label,value]of [['Selected Fabric',details?.choice==='now'&&details.fabricName?details.fabricName:'Choose a fabric below'],['Preferred Colour',details?.colourName?(details.colourName+(details.colourDescription?' — '+details.colourDescription:'')):'Choose a colour below']]){const p=document.createElement('p'),strong=document.createElement('strong');strong.textContent=label+': ';p.append(strong,document.createTextNode(value));selected.append(p);}
  fieldset.disabled=!pref?.fabricRef||pref.choice!=='now';other.hidden=pref?.colour!=='other';description.required=!other.hidden;description.disabled=other.hidden;description.setCustomValidity('');
  for(const radio of colourForm.querySelectorAll('[name=preferredColour]'))radio.checked=pref?.colour===radio.value;
  for(const b of collection.querySelectorAll('[data-pick-fabric]')){const active=pref?.fabricRef===b.dataset.pickFabric;b.setAttribute('aria-pressed',String(active));b.textContent=active?'Fabric Selected ✓':'Select This Fabric';}
 }
 description.value=api.fabricPreference()?.colourDescription||'';
 for(const card of collection.querySelectorAll('[data-fabric-id]')){
  const id=card.dataset.fabricId;if(!Object.hasOwn(source.fabrics,id))continue;const choose=document.createElement('button');choose.type='button';choose.className='home-button home-button-gold';choose.dataset.pickFabric=id;choose.textContent='Select This Fabric';choose.addEventListener('click',()=>{const previous=api.fabricPreference();api.setFabricPreference({choice:'now',fabricRef:id,colour:previous?.choice==='now'?previous.colour:'',colourDescription:previous?.choice==='now'?previous.colourDescription:''});status.textContent='';paint();colourForm.scrollIntoView({block:'start',behavior:'instant'});legend.tabIndex=-1;legend.focus({preventScroll:true});});card.querySelector('.fabric-card-copy').append(choose);
 }
 colourForm.addEventListener('change',event=>{if(event.target.name!=='preferredColour')return;const pref=api.fabricPreference();if(!pref?.fabricRef)return;api.setFabricPreference({...pref,colour:event.target.value,colourDescription:event.target.value==='other'?description.value:''});status.textContent='';paint();if(event.target.value==='other')description.focus();});
 description.addEventListener('input',()=>{const pref=api.fabricPreference();if(pref?.colour==='other'){descriptionValid();api.setFabricPreference({...pref,colourDescription:description.value});}});
 colourForm.addEventListener('submit',event=>{event.preventDefault();const pref=api.fabricPreference();if(!pref?.fabricRef){status.textContent='Select a fabric before choosing your preferred colour.';collection.querySelector('[data-pick-fabric]')?.focus();return;}if(pref.colour==='other'&&!descriptionValid()){description.reportValidity();return;}if(!colourForm.reportValidity()||!preferences.valid(pref)){status.textContent='Choose one preferred colour to continue.';return;}location.href=api.quotationURL();});paint();
};
