/* Optional sharing of validated, non-personal design references. No files or messages are sent. */
(()=>{'use strict';
 const byId=id=>document.getElementById(id);
 function init(){
  const options=byId('selection-share-options');
  if(!options)return;
  const whatsapp=byId('selection-share-whatsapp'),native=byId('selection-share-native'),copy=byId('selection-share-copy'),status=byId('selection-share-status'),manual=byId('selection-share-text'),parts=byId('selection-share-parts');
  const MAX_PART=1800;
  const fits=text=>text.length<=MAX_PART&&encodeURIComponent(text).length<=MAX_PART;
  const say=text=>{status.textContent=text;};
  function data(){
   const rows=window.MrDesignSelections?.sharingSnapshot?.()||[];
   return rows.map(row=>{
    // Only the vetted photograph's source path is projected onto the current preview host.
    const photograph=new URL(row.src,location.origin),design=new URL(row.route,location.origin);
    if(photograph.origin!==location.origin||design.origin!==location.origin||!['http:','https:'].includes(photograph.protocol))throw Error('Invalid design reference');
    return {name:String(row.name).replace(/\s*[—·-]\s*MS-\d+\b/g,'').trim(),quantity:row.quantity,design:design.href,photograph:photograph.href};
   });
  }
  function prepared(){
   const rows=data();
   if(!rows.length)throw Error('No designs selected');
   const preview=!['mrsewingfashion.com','www.mrsewingfashion.com'].includes(location.hostname);
   const intro='Hello Mr Sewing Fashion. I have selected '+rows.length+' suit '+(rows.length===1?'design':'designs')+' from your website and would like to share '+(rows.length===1?'it':'them')+' with you.';
   const total='Total garments: '+rows.reduce((sum,row)=>sum+row.quantity,0)+'.';
   const note=preview?'Staging preview links: these open the current preview website, not the live production website.':'';
   const entries=rows.map((row,i)=>(i+1)+'. '+row.name+'\nQuantity: '+row.quantity+'\nPhotograph: '+row.photograph);
   const links=rows.map((row,i)=>(i+1)+'. '+row.name+'\nQuantity: '+row.quantity+'\nDesign: '+row.design+'\nPhotograph: '+row.photograph);
   const close='Please review these designs with me.';
   return {rows,intro: intro+'\n'+total,note,entries,close,text:[intro,total,note,...links,close].filter(Boolean).join('\n\n'),whatsappText:[intro,total,note,...entries,close].filter(Boolean).join('\n\n')};
  }
  function fallback(message,text){
   manual.value=text;manual.hidden=false;manual.focus();manual.select();say(message);
  }
  function get(){try{return prepared();}catch{say('Your selected designs are unavailable. Return to the suit galleries and review your selections.');return null;}}
  function reset(){parts?.replaceChildren();manual.value='';manual.hidden=true;say('');}
  function handoff(text,trigger){
   if(!window.MrSewingWhatsApp?.open){fallback('WhatsApp is unavailable here. Copy the complete design list below and use the official contact link.',get()?.text||text);return;}
   // Existing Terms controller has a 6000-character cap; never pass an oversized message.
   if(!fits(text)){fallback('This design list is too long for a safe WhatsApp link. Copy the complete text below into WhatsApp.',get()?.text||text);return;}
   say('Review the Terms before continuing. WhatsApp opens a draft; review it and press Send there. No message has been sent by the website.');
   window.MrSewingWhatsApp.open(text,trigger);
  }
  whatsapp.addEventListener('click',()=>{
   const bundle=get();if(!bundle)return;reset();
   if(fits(bundle.whatsappText)){handoff(bundle.whatsappText,whatsapp);return;}
   // Split only between whole design entries. The original order and every link are retained.
   const chunks=[];let group=[];
   const compose=(entries,part,total)=>[bundle.intro,bundle.note,'Part '+part+' of '+total,...entries,bundle.close].filter(Boolean).join('\n\n');
   for(const entry of bundle.entries){
    if(!fits(compose([entry],9999,9999))){fallback('This design list is too long for a safe WhatsApp link. Copy the complete text below; no designs have been omitted.',bundle.text);return;}
    if(group.length&&!fits(compose([...group,entry],9999,9999))){chunks.push(group);group=[];}
    group.push(entry);
   }
   if(group.length)chunks.push(group);
   manual.value=bundle.text;manual.hidden=false;
   say('Your complete list is prepared in '+chunks.length+' WhatsApp parts. Open each numbered part, accept the Terms, then review and send it in WhatsApp. No designs have been omitted and nothing has been sent automatically.');
   for(const[part,entries]of chunks.entries()){
    const button=document.createElement('button');button.type='button';button.className='home-button home-button-gold';button.textContent='Open WhatsApp Part '+(part+1)+' of '+chunks.length;button.dataset.whatsappPart=String(part+1);button.dataset.partIndex=String(part);
    const text=compose(entries,part+1,chunks.length);
    button.addEventListener('click',()=>{
     const current=get();if(!current)return;
     if(current.text!==bundle.text){reset();say('Your selections changed. Choose Send to Mr Sewing on WhatsApp again to prepare the updated list.');return;}
     handoff(text,button);
    });parts.append(button);
   }
   parts.querySelector('button')?.focus();
  });
  native.addEventListener('click',async()=>{
   const bundle=get();if(!bundle)return;reset();
   if(typeof navigator.share!=='function'){fallback('Sharing with other apps is unavailable in this browser. Copy the complete design list below or choose Copy Design Links.',bundle.text);return;}
   try{
    await navigator.share({title:'Mr Sewing Fashion — Selected Designs',text:bundle.text});
    say('The device sharing action completed. Message delivery is not confirmed.');
   }catch(error){
    if(error?.name==='AbortError'){say('Sharing cancelled. Your selected designs are unchanged.');return;}
    fallback('Sharing with other apps could not be completed. Copy the complete design list below or choose Copy Design Links.',bundle.text);
   }
  });
  copy.addEventListener('click',async()=>{
   const bundle=get();if(!bundle)return;reset();
   try{
    if(typeof navigator.clipboard?.writeText!=='function')throw Error('Clipboard unavailable');
    await navigator.clipboard.writeText(bundle.text);say('Design links copied.');
   }catch{
    fallback('Copy could not be completed. Select and copy the complete design list below.',bundle.text);
   }
  });
  // Removal and quantity changes invalidate any previously prepared multipart links.
  document.addEventListener('mrsewing:selectionchange',reset);
 }
 if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init);else init();
})();
