/* One accessible shell for the existing same-origin selection and request pages.
 * The iframe retains the actual forms, state, validators and receiving contract.
 * No personal information is added to the parent URL or local storage. */
(()=>{'use strict';
 if(window.parent!==window||!window.HTMLDialogElement)return;
 const reviewPath='/services/custom-tailoring/selected-designs/';
 const permitted=p=>[reviewPath,'/services/custom-tailoring/fabric/','/request/'].includes(p)||p.startsWith('/guides/fabrics/');
 const browsing=p=>p==='/services/custom-tailoring/'||p==='/collections/'||/^\/(men|women)suits\//.test(p)||/^\/collections\/designs\//.test(p);
 if(!browsing(location.pathname))return;
 let dialog,frame,title,progress,opener,lastURL='',quoteStep=0,frameHistory=[],resumeButton;
 const resumeKey='mrsewing-tailoring-dialog-v1',resumeTTL=30*60*1000;
 function remember(path){try{const u=new URL(path,location.origin);if(u.origin!==location.origin||!permitted(u.pathname))return;const allowed=new Set(['selection','selectionFlow','selectionEdit','selectionSession','sharedFabric','multiple','fabricSelect','fabricFor','design','photo','project','service','order','fabricChoice','fabricRef']);for(const key of [...u.searchParams.keys()])if(!allowed.has(key))u.searchParams.delete(key);sessionStorage.setItem(resumeKey,JSON.stringify({url:u.pathname+u.search,updated:Date.now()}));}catch{}}
 function resumePath(){try{const saved=JSON.parse(sessionStorage.getItem(resumeKey)||'null');if(!saved||Date.now()-saved.updated>=resumeTTL||saved.updated>Date.now()){sessionStorage.removeItem(resumeKey);return null;}const u=new URL(saved.url,location.origin),meta=JSON.parse(sessionStorage.getItem('mrsewing-design-session-v1')||'null');if(u.origin!==location.origin||!permitted(u.pathname)||(!u.searchParams.has('selectionFlow')&&meta?.status!=='active'))return null;return saved.url;}catch{return null;}}
 function offerResume(){if(!resumePath())return;if(!resumeButton){resumeButton=document.createElement('button');resumeButton.type='button';resumeButton.className='home-button tailoring-resume-request';resumeButton.textContent='Resume Request';resumeButton.addEventListener('click',()=>open(resumePath(),resumeButton));const main=document.querySelector('main');(main?.querySelector('.home-shell')||main)?.prepend(resumeButton);}if(resumeButton)resumeButton.hidden=false;}
 const labels=['Selected designs','Fabric preference','Fabric details','Your information','Review request'];
 function announce(index,text){title.textContent=text||labels[index];progress.textContent='Step '+(index+1)+' of '+labels.length+' · '+labels[index];}
 function close(){if(!dialog?.open)return;dialog.close();document.documentElement.classList.remove('tailoring-dialog-open');window.MrDesignSelections?.read();if(history.state?.tailoringRequest)history.replaceState(null,'',location.href);offerResume();opener?.focus();}
 function create(){
  dialog=document.createElement('dialog');dialog.className='tailoring-request-dialog';dialog.setAttribute('aria-labelledby','tailoring-dialog-title');
  const head=document.createElement('header');head.className='tailoring-dialog-header';
  const names=document.createElement('div');progress=document.createElement('p');progress.className='tailoring-dialog-progress';progress.setAttribute('role','status');progress.setAttribute('aria-live','polite');
  title=document.createElement('h2');title.id='tailoring-dialog-title';names.append(progress,title);
  const exit=document.createElement('button');exit.type='button';exit.className='tailoring-dialog-close';exit.textContent='Close';exit.setAttribute('aria-label','Close quotation request and keep selections');exit.addEventListener('click',close);head.append(names,exit);
  frame=document.createElement('iframe');frame.title='Tailoring request steps';frame.className='tailoring-dialog-frame';
  frame.addEventListener('load',prepare);dialog.append(head,frame);document.body.append(dialog);
  dialog.addEventListener('cancel',event=>{event.preventDefault();close();});dialog.addEventListener('click',event=>{if(event.target===dialog)close();});
 }
 function open(path,trigger,fresh=false){
  if(!path)return false;
  const u=new URL(path,location.origin);if(u.origin!==location.origin||!permitted(u.pathname))return false;
  if(!dialog)create();opener=trigger||document.activeElement;
  if(!dialog.open){dialog.showModal();document.documentElement.classList.add('tailoring-dialog-open');history.pushState({tailoringRequest:true},'',location.href);}
  // Reopening on this page keeps the live, unfinished form rather than reloading it.
  if(!lastURL||fresh){lastURL=u.href;frameHistory=[];frame.src=u.href;announce(0,'Your Selected Designs');}
  if(resumeButton)resumeButton.hidden=true;
  dialog.querySelector('.tailoring-dialog-close').focus();return true;
 }
 function prepare(){
  let doc,win,u;try{doc=frame.contentDocument;win=frame.contentWindow;u=new URL(win.location.href);}catch{title.textContent='Open your request separately';return;}
  if(!doc||!permitted(u.pathname))return;
  lastURL=u.href;remember(u.href);if(!dialog.open)window.MrDesignSelections?.read();if(frameHistory.at(-1)!==u.href)frameHistory.push(u.href);
  doc.documentElement.classList.add('request-dialog-embedded');const sheet=doc.createElement('link');sheet.rel='stylesheet';sheet.href='/assets/tailoring-request-dialog.css?v=experience-20261126';doc.head.append(sheet);
  const stage=u.pathname===reviewPath?0:u.pathname==='/services/custom-tailoring/fabric/'?1:u.pathname.startsWith('/guides/fabrics/')?2:3;
  announce(stage,stage===0?'Your Selected Designs':undefined);
  doc.addEventListener('keydown',event=>{const nested=[...doc.querySelectorAll('dialog[open],[role=dialog]')].some(node=>node.open||node.getClientRects().length&&win.getComputedStyle(node).visibility!=='hidden');if(event.key==='Escape'&&!nested){event.preventDefault();close();}});
  doc.addEventListener('click',event=>{
   const link=event.target.closest('a[href]');if(!link||event.defaultPrevented||event.ctrlKey||event.metaKey||event.shiftKey||event.altKey)return;
   const target=new URL(link.href,u.href);if(target.origin!==location.origin)return;
   if(browsing(target.pathname)){event.preventDefault();close();location.assign(target.href);}
   else if(!permitted(target.pathname)&&!target.pathname.startsWith('/assets/')&&!/\.(?:jpe?g|png|webp|pdf)$/i.test(target.pathname)){link.target='_blank';link.rel='noopener';}
  });
  const main=doc.querySelector('main');if(main)main.setAttribute('tabindex','-1');
  if(stage===3)quoteSteps(doc,win);
  const back=doc.createElement('button');back.type='button';back.className='home-button request-dialog-back';back.textContent='Back';
  back.addEventListener('click',()=>{if(stage===3&&quoteStep>0){quoteStep--;showQuote(doc);return;}if(frameHistory.length>1){frameHistory.pop();const path=frameHistory.pop();frame.src=path;}else close();});
  (main?.querySelector('.release-main')||main||doc.body).prepend(back);
  main?.focus({preventScroll:true});
 }
 function quoteSteps(doc,win){
  const form=doc.getElementById('customerRequestForm'),parts=[...doc.querySelectorAll('[data-quotation-section]')];if(!form||!parts.length)return;
  quoteStep=0;const nav=doc.createElement('nav');nav.className='request-dialog-step-actions';nav.setAttribute('aria-label','Quotation steps');
  const next=doc.createElement('button');next.type='button';next.className='home-button home-button-gold';next.textContent='Continue';next.dataset.dialogContinue='';nav.append(next);form.append(nav);
  next.addEventListener('click',()=>{
   const section=parts[quoteStep];
   const invalid=[...section.querySelectorAll('input,select,textarea')].find(input=>!input.disabled&&!input.checkValidity());if(invalid){invalid.reportValidity();return;}
   if(section.dataset.quotationSection==='deadline'){const assessment=win.MrCustomQuotation?.deadlineAssessment();if(assessment&&!assessment.valid){doc.getElementById('requestCompletionTime').setCustomValidity('Choose a valid completion deadline in the future.');doc.getElementById('requestCompletionTime').reportValidity();return;}}
   quoteStep=Math.min(parts.length-1,quoteStep+1);showQuote(doc);
  });
  // The original validator still checks the complete form. Reveal the section
  // containing an invalid field so errors are never trapped in a hidden step.
  form.addEventListener('invalid',event=>{const index=parts.findIndex(part=>part.contains(event.target));if(index>=0){quoteStep=index;showQuote(doc,false);}},true);
  const refresh=()=>{
   const success=doc.getElementById('requestSuccess'),review=doc.getElementById('requestReview');
   if(success&&!success.hidden){announce(4,'Request Submitted for Review');try{sessionStorage.removeItem(resumeKey);}catch{}if(resumeButton)resumeButton.hidden=true;}
   else if(review&&!review.hidden)announce(4,'Review Your Request');
   else showQuote(doc,false);
  };
  for(const id of['requestReview','requestSuccess']){const node=doc.getElementById(id);if(node)new MutationObserver(refresh).observe(node,{attributes:true,attributeFilter:['hidden']});}
  doc.getElementById('editRequest')?.addEventListener('click',()=>{quoteStep=parts.length-1;showQuote(doc);});
  doc.getElementById('sendRequest')?.replaceChildren(doc.createTextNode('Submit Request'));
  showQuote(doc);
 }
 function showQuote(doc,focus=true){
  const parts=[...doc.querySelectorAll('[data-quotation-section]')];parts.forEach((part,index)=>part.hidden=index!==quoteStep);
  const next=doc.querySelector('[data-dialog-continue]');if(next)next.hidden=quoteStep===parts.length-1;
  const caption=parts[quoteStep]?.querySelector('legend')?.textContent||'Your Request';announce(3,caption+' · '+(quoteStep+1)+' of '+parts.length);
  if(focus){const first=parts[quoteStep]?.querySelector('input:not([type=hidden]),select,textarea,button');first?.focus({preventScroll:true});frame.contentWindow.scrollTo(0,0);}
 }
 document.addEventListener('click',event=>{const link=event.target.closest('a.selected-design-bar');if(link&&!event.ctrlKey&&!event.metaKey&&!event.shiftKey&&!event.altKey&&open(link.href,link))event.preventDefault();});
 document.addEventListener('mrsewing:designselected',event=>{const path=document.querySelector('.selected-design-bar')?.href||window.MrDesignSelections?.selectionURL(reviewPath)||reviewPath;open(path,event.detail?.trigger,true);});
 window.addEventListener('popstate',()=>{if(dialog?.open&&!history.state?.tailoringRequest)close();});
 window.MrTailoringRequest={open,close,isOpen:()=>!!dialog?.open};
 if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',offerResume,{once:true});else offerResume();
})();
