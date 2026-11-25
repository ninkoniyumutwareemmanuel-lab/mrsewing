/* One text-first collection journey, including existing selected-suit requests. */
(()=>{'use strict';
 const root=document.querySelector('.fg-showroom');if(!root)return;
 const params=new URLSearchParams(location.search),api=window.MrDesignSelections;
 const picking=params.get('fabricSelect')==='1'||params.has('fabricFor');
 const detail=root.matches('.fg-detail'),dataNode=document.getElementById('fg-data');
 const data=dataNode?JSON.parse(dataNode.textContent):null;
 const status=document.createElement('p');status.setAttribute('role','status');status.className='fg-note';
 let rows=[];
 if(picking){
  rows=api?.quoteRows?.()||api?.read?.()||[];
  const panel=document.createElement('section');panel.className='fabric-selection-context';
  const heading=document.createElement('h2');heading.textContent='Your Selected Designs';panel.append(heading);
  if(rows.length){window.MrSelectedSuitQuote?.renderDesignSummary(panel);const edit=document.createElement('a');edit.href=api.editSelectionsURL();edit.textContent='Add or Change Designs';edit.className='home-text-link';panel.append(edit);}
  else{const message=document.createElement('p'),link=document.createElement('a');message.textContent='No active designs selected. Browse fabric collections independently, or select designs to start a quotation.';link.href='/services/custom-tailoring/';link.textContent='Explore Clothing Designs';panel.append(message,link);}
  root.prepend(panel);
  for(const link of root.querySelectorAll('a[href]')){const u=new URL(link.href,location.href);if(u.origin===location.origin&&u.pathname.startsWith('/guides/fabrics/')){u.searchParams.set('fabricSelect','1');u.searchParams.set('multiple','1');link.href=api?.selectionURL(u.pathname+u.search+u.hash)||u.pathname+u.search+u.hash;}}
 }
 if(!detail||!data)return;
 const summary=document.getElementById('fg-selection'),request=document.getElementById('fg-request'),other=document.getElementById('fg-other'),otherLabel=document.getElementById('fg-other-label'),details=document.getElementById('fg-selected-details');
 request.after(status);
 const previous=api?.fabricPreference?.();
 if(previous?.choice==='now'){
  const index=data.styles.findIndex(style=>style.id===previous.fabricRef);
  if(index>=0){const radio=root.querySelector('[name="fg-type"][value="'+index+'"]');if(radio)radio.checked=true;}
  for(const radio of root.querySelectorAll('[name="fg-pattern"]'))if(radio.value===previous.pattern)radio.checked=true;
  for(const radio of root.querySelectorAll('[name="fg-colour"]'))if(radio.value===previous.colour)radio.checked=true;
  other.value=previous.colourDescription||'';
 }
 function choice(){
  const index=Number(root.querySelector('[name="fg-type"]:checked')?.value||0),style=data.styles[index];
  const pattern=root.querySelector('[name="fg-pattern"]:checked')?.value||'plain';
  const colour=data.colors.find(c=>c.id===root.querySelector('[name="fg-colour"]:checked')?.value)||data.colors[0];
  return{choice:'now',fabricRef:style.id,pattern,colour:colour.id,colourDescription:colour.id==='other'?other.value.trim():''};
 }
 function update(){
  const selected=choice(),index=data.styles.findIndex(style=>style.id===selected.fabricRef),pattern=data.patterns.find(p=>p[0]===selected.pattern),colour=data.colors.find(c=>c.id===selected.colour);
  otherLabel.hidden=selected.colour!=='other';other.disabled=otherLabel.hidden;
  const custom=selected.colourDescription;other.setCustomValidity(!custom||/^[\p{L}\p{N} .,'’()/+#-]{1,80}$/u.test(custom)?'':'Use up to 80 letters, numbers and basic colour punctuation.');
  summary.textContent=data.collection+' Collection — '+data.types[index]+' — '+pattern[1]+' — '+(custom||colour.name);
  root.querySelectorAll('.fg-spec').forEach((element,i)=>element.classList.toggle('fg-active',i===index));
  const spec=document.getElementById('fg-type-'+index);if(spec&&details)details.replaceChildren(...Array.from(spec.children).map(element=>element.cloneNode(true)));
  if(picking&&rows.length){request.textContent='Continue to Quotation';request.href='#fg-request';}
  else request.href='/request/?general=1&fabricPreference='+encodeURIComponent(summary.textContent.slice(0,200));
  status.textContent='';
 }
 root.addEventListener('change',update);other.addEventListener('input',update);
 request.addEventListener('click',event=>{
  if(!picking||!rows.length)return;
  event.preventDefault();if(!other.reportValidity())return;
  if(!api.setFabricPreference(choice())||!api.fabricPreferenceValid()){status.textContent='Review your fabric, pattern and colour preferences.';return;}
  location.href=api.quotationURL();
 });
 update();
})();
