/* Email-only selected-design validation. No files, private records, payments or reservations. */
import {validateFields} from '../../scripts/edge/customer-requests.mjs';
import {fabrics} from '../../scripts/edge/request-data.mjs';
const TIME_ZONE='Africa/Kigali (UTC+02:00)';
const friendly=name=>String(name).replace(/\s*[—·-]\s*MS-\d+\b/g,'').trim();
const reply=(status,body)=>new Response(JSON.stringify(body),{status,headers:{'Content-Type':'application/json','Cache-Control':'no-store','X-Robots-Tag':'noindex, nofollow','X-Content-Type-Options':'nosniff'}});
function checkFabric(fields){
 if(fields['Fabric Choice']==='Customer fabric choice'){const f=Object.hasOwn(fabrics,fields['Fabric Reference']||'')?fabrics[fields['Fabric Reference']]:null;if(!f||fields['Suit Audience']&&f.category!==fields['Suit Audience'])throw Error('Choose an approved fabric for this suit category or request advice.');fields['Selected Fabric']=f.name;fields['Fabric Category']=f.category==='women'?'Women’s Suits':'Men’s Suits';fields['Fabric Tier']='Tier '+f.tier;fields['Fabric Availability']='Availability and final quotation require confirmation';}
 else if(fields['Fabric Choice']==='Help Me Choose Fabric'){for(const k of ['Fabric Reference','Selected Fabric','Fabric Category','Fabric Tier'])delete fields[k];fields['Fabric Assistance']='Requested';}else if(fields['Fabric Choice']==='Customer-Supplied Fabric'){for(const k of ['Fabric Reference','Selected Fabric','Fabric Category','Fabric Tier','Fabric Assistance'])delete fields[k];fields['Fabric Preference']='Customer-Supplied Fabric';fields['Fabric Availability']='Customer-supplied fabric suitability requires assessment';}else throw Error('Complete fabric selection or request fabric advice.');
 return fields;
}
function customerRequirements(raw){
 if(!raw||Array.isArray(raw)||typeof raw!=='object')throw Error('Invalid request fields.');
 const required=(key,max)=>{const value=raw[key];if(typeof value!=='string'||!value.trim()||value.length>max||/[\u0000-\u0008\u000b\u000c\u000e-\u001f\u007f]/.test(value))throw Error('Complete '+key.toLowerCase()+'.');return value.trim();};
 const country=required('Country',160),delivery=required('Delivery Location / Address',500),date=required('Requested Completion Date',10),time=required('Requested Completion Time',5);
 const match=/^(\d{4})-(\d{2})-(\d{2})$/.exec(date);
 if(!match)throw Error('Enter a valid requested completion date.');
 const year=Number(match[1]),month=Number(match[2]),day=Number(match[3]),leap=year%4===0&&(year%100!==0||year%400===0),days=[31,leap?29:28,31,30,31,30,31,31,30,31,30,31];
 if(year<1||month<1||month>12||day<1||day>days[month-1])throw Error('Enter a valid requested completion date.');
 if(!/^(?:[01]\d|2[0-3]):[0-5]\d$/.test(time))throw Error('Enter a valid requested completion time in Kigali time.');
 if(raw['Requested Completion Time Zone']!==undefined&&raw['Requested Completion Time Zone']!==TIME_ZONE)throw Error('Use Kigali time (Africa/Kigali, UTC+02:00) for the requested deadline.');
 // The legacy Location key remains for existing provider/contact handling; no delivery promise is made.
 return {...raw,Country:country,'Delivery Location / Address':delivery,Location:delivery,'Requested Completion Date':date,'Requested Completion Time':time,'Requested Completion Time Zone':TIME_ZONE};
}
function selectedFields(raw){
 const fields=validateFields(raw,{selectedSuit:true});
 for(const key of ['Order Priority','After-hours Request','Garment Type','Other Garment','Fabric Preferences','Preferred Date','Preferred Time'])delete fields[key];
 return checkFabric(fields);
}
export async function handleSelected(request,key,fetcher=fetch){
 const url=new URL(request.url),host=url.hostname;if(!['mrsewingfashion.com','mrsewing-staging.pages.dev','localhost','127.0.0.1'].includes(host)&&!host.endsWith('.mrsewing-staging.pages.dev'))return reply(403,{success:false,error:'Unrecognised website.'});
 if(request.method!=='POST')return reply(405,{success:false,error:'POST required.'});if(request.headers.get('Origin')&&request.headers.get('Origin')!==url.origin)return reply(403,{success:false,error:'Submit from this website.'});
 if(request.headers.get('Content-Type')?.split(';')[0]!=='application/json')return reply(415,{success:false,error:'Only a text-based JSON request is supported. No photograph files are accepted.'});
 let fields;try{const reader=request.body?.getReader();if(!reader)throw Error('Request required.');let total=0;const parts=[];while(true){const chunk=await reader.read();if(chunk.done)break;total+=chunk.value.length;if(total>30000){await reader.cancel();return reply(413,{success:false,error:'Request too large.'});}parts.push(chunk.value);}const bytes=new Uint8Array(total);let offset=0;for(const part of parts){bytes.set(part,offset);offset+=part.length;}const body=JSON.parse(new TextDecoder().decode(bytes));if(!body||typeof body!=='object'||Array.isArray(body))throw Error('Invalid request.');if(body.termsAccepted!==true||body.botcheck)throw Error('Terms acceptance and valid request required.');
 if(body.fields?.Service!=='Custom Tailoring & Suits'||body.fields?.['Design Order Type']!=='Standard Order'||!body.fields?.['Design Reference']||!body.fields?.['Selected Photograph URL'])throw Error('Choose a website design photograph and fabric preference.');
 const raw=customerRequirements(body.fields);
 fields=selectedFields(raw);
 if(body.selections!==undefined){
  if(!Array.isArray(body.selections)||!body.selections.length||body.selections.length>50)throw Error('Select between one and fifty approved design references.');
  const seen=new Set(),rows=[];let quantity=0;
  for(const item of body.selections){
   if(!item||typeof item!=='object'||Array.isArray(item)||!Number.isInteger(item.quantity)||item.quantity<1||item.quantity>9999||!['now','advice','own'].includes(item.fabricChoice))throw Error('Review the design quantities and fabric preferences.');
   const choice=item.fabricChoice==='now'?'Customer fabric choice':item.fabricChoice==='own'?'Customer-Supplied Fabric':'Help Me Choose Fabric';
   const row=selectedFields({...raw,'Design Reference':item.design,'Selected Photograph URL':item.photo,'Design Image':item.photo,'Portfolio Reference':item.project||'',Quantity:String(item.quantity),'Fabric Choice':choice,'Fabric Reference':item.fabricRef||''});
   if(seen.has(row['Selected Photograph URL']))throw Error('Remove duplicate photographs and adjust the garment quantity instead.');seen.add(row['Selected Photograph URL']);quantity+=item.quantity;rows.push(row);
  }
  if(quantity>9999)throw Error('Contact Customer Support to discuss this garment quantity.');
  fields.Quantity=String(quantity);fields['Total Garments']=String(quantity);fields['Selected Design Count']=String(rows.length);
  fields['Selected Design IDs']=rows.map((r,i)=>(i+1)+'. '+r['Design Reference']).join('\n');
  fields['Selected Photograph URLs']=rows.map(r=>r['Selected Photograph URL']).join('\n');
  fields['Selected Designs']=rows.map((r,i)=>(i+1)+'. '+friendly(r['Design Name'])+' | Quantity: '+r.Quantity+' | Photograph: '+r['Selected Photograph URL']+' | Page: '+r['Design Link']+' | Fabric: '+(r['Selected Fabric']||r['Fabric Preference']||r['Fabric Choice'])).join('\n');
 }else{
  fields['Total Garments']=fields.Quantity;fields['Selected Design Count']='1';fields['Selected Design IDs']='1. '+fields['Design Reference'];fields['Selected Photograph URLs']=fields['Selected Photograph URL'];fields['Selected Designs']='1. '+friendly(fields['Design Name'])+' | Quantity: '+fields.Quantity+' | Photograph: '+fields['Selected Photograph URL']+' | Page: '+fields['Design Link']+' | Fabric: '+(fields['Selected Fabric']||fields['Fabric Preference']||fields['Fabric Choice']);
 }
 fields['Design Name']=friendly(fields['Design Name']);fields['Requested Completion Deadline']=fields['Requested Completion Date']+' '+fields['Requested Completion Time']+' '+TIME_ZONE;fields['Deadline Status']='Requested only; feasibility and completion date/time require business confirmation.';
 fields.Consent='Terms accepted; request for human review only';
 }catch(error){return reply(400,{success:false,error:error instanceof SyntaxError?'Invalid request.':error.message});}
 if(!key)return reply(503,{success:false,error:'Submission is not configured. No request was confirmed.'});
 const controller=new AbortController(),timer=setTimeout(()=>controller.abort(),15000);try{const r=await fetcher('https://api.web3forms.com/submit',{method:'POST',headers:{'Content-Type':'application/json',Accept:'application/json'},body:JSON.stringify({access_key:key,subject:'Selected Design Quotation Request - Mr Sewing',from_name:'Mr Sewing Website',...fields,...(fields['Email Address']?{replyto:fields['Email Address']}:{}),botcheck:''}),signal:controller.signal});const result=await r.json();if(!r.ok||result.success!==true)return reply(502,{success:false,error:'The submission service did not confirm acceptance.'});return reply(200,{success:true});}catch{return reply(502,{success:false,error:'We could not confirm submission. It may have arrived; contact Customer Support before retrying.'});}finally{clearTimeout(timer);}
}
