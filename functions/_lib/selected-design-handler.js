/* Email-only selected-design validation. No files, private records, payments or reservations. */
import {validateFields} from '../../scripts/edge/customer-requests.mjs';
import {fabrics} from '../../scripts/edge/request-data.mjs';
const reply=(status,body)=>new Response(JSON.stringify(body),{status,headers:{'Content-Type':'application/json','Cache-Control':'no-store','X-Robots-Tag':'noindex, nofollow','X-Content-Type-Options':'nosniff'}});
function checkFabric(fields){
 if(fields['Fabric Choice']==='Customer fabric choice'){const f=Object.hasOwn(fabrics,fields['Fabric Reference']||'')?fabrics[fields['Fabric Reference']]:null;if(!f||fields['Suit Audience']&&f.category!==fields['Suit Audience'])throw Error('Choose an approved fabric for this suit category or request advice.');fields['Selected Fabric']=f.name;fields['Fabric Category']=f.category==='women'?'Women’s Suits':'Men’s Suits';fields['Fabric Tier']='Tier '+f.tier;fields['Fabric Availability']='Availability and final quotation require confirmation';}
 else if(fields['Fabric Choice']==='Help Me Choose Fabric'){for(const k of ['Fabric Reference','Selected Fabric','Fabric Category','Fabric Tier'])delete fields[k];fields['Fabric Assistance']='Requested';}else if(fields['Fabric Choice']==='Customer-Supplied Fabric'){for(const k of ['Fabric Reference','Selected Fabric','Fabric Category','Fabric Tier','Fabric Assistance'])delete fields[k];fields['Fabric Preference']='Customer-Supplied Fabric';fields['Fabric Availability']='Customer-supplied fabric suitability requires assessment';}else throw Error('Complete fabric selection or request fabric advice.');
 return fields;
}
export async function handleSelected(request,key,fetcher=fetch){
 const url=new URL(request.url),host=url.hostname;if(!['mrsewingfashion.com','mrsewing-staging.pages.dev','localhost','127.0.0.1'].includes(host)&&!host.endsWith('.mrsewing-staging.pages.dev'))return reply(403,{success:false,error:'Unrecognised website.'});
 if(request.method!=='POST')return reply(405,{success:false,error:'POST required.'});if(request.headers.get('Origin')&&request.headers.get('Origin')!==url.origin)return reply(403,{success:false,error:'Submit from this website.'});
 if(request.headers.get('Content-Type')?.split(';')[0]!=='application/json')return reply(415,{success:false,error:'Only a text-based JSON request is supported. No photograph files are accepted.'});
 let fields;try{const reader=request.body?.getReader();if(!reader)throw Error('Request required.');let total=0;const parts=[];while(true){const chunk=await reader.read();if(chunk.done)break;total+=chunk.value.length;if(total>30000){await reader.cancel();return reply(413,{success:false,error:'Request too large.'});}parts.push(chunk.value);}const bytes=new Uint8Array(total);let offset=0;for(const part of parts){bytes.set(part,offset);offset+=part.length;}const body=JSON.parse(new TextDecoder().decode(bytes));if(!body||typeof body!=='object'||Array.isArray(body))throw Error('Invalid request.');if(body.termsAccepted!==true||body.botcheck)throw Error('Terms acceptance and valid request required.');
 if(body.fields?.Service!=='Custom Tailoring & Suits'||body.fields?.['Design Order Type']!=='Standard Order'||!body.fields?.['Design Reference']||!body.fields?.['Selected Photograph URL'])throw Error('Choose a website design photograph and fabric preference.');
 fields=validateFields(body.fields);
 fields=checkFabric(fields);
 if(body.selections!==undefined){
  if(!Array.isArray(body.selections)||!body.selections.length||body.selections.length>50)throw Error('Select between one and fifty approved design references.');
  const seen=new Set(),rows=[];let quantity=0;
  for(const item of body.selections){
   if(!item||typeof item!=='object'||Array.isArray(item)||!Number.isInteger(item.quantity)||item.quantity<1||item.quantity>9999||!['now','advice','own'].includes(item.fabricChoice))throw Error('Review the design quantities and fabric preferences.');
   const choice=item.fabricChoice==='now'?'Customer fabric choice':item.fabricChoice==='own'?'Customer-Supplied Fabric':'Help Me Choose Fabric';
   const row=checkFabric(validateFields({...body.fields,'Design Reference':item.design,'Selected Photograph URL':item.photo,'Design Image':item.photo,'Portfolio Reference':item.project||'',Quantity:String(item.quantity),'Fabric Choice':choice,'Fabric Reference':item.fabricRef||''}));
   if(seen.has(row['Selected Photograph URL']))throw Error('Remove duplicate photographs and adjust the garment quantity instead.');seen.add(row['Selected Photograph URL']);quantity+=item.quantity;rows.push(row);
  }
  if(quantity>9999)throw Error('Contact Customer Support to discuss this garment quantity.');
  fields.Quantity=String(quantity);fields['Selected Design Count']=String(rows.length);
  fields['Selected Photograph URLs']=rows.map(r=>r['Selected Photograph URL']).join('\n');
  fields['Selected Designs']=rows.map((r,i)=>(i+1)+'. '+r['Design Name']+' | Quantity: '+r.Quantity+' | Photograph: '+r['Selected Photograph URL']+' | Page: '+r['Design Link']+' | Fabric: '+(r['Selected Fabric']||r['Fabric Preference']||r['Fabric Choice'])).join('\n');
 }
 fields.Consent='Terms accepted; request for human review only';
 }catch(error){return reply(400,{success:false,error:error instanceof SyntaxError?'Invalid request.':error.message});}
 if(!key)return reply(503,{success:false,error:'Submission is not configured. No request was confirmed.'});
 const controller=new AbortController(),timer=setTimeout(()=>controller.abort(),15000);try{const r=await fetcher('https://api.web3forms.com/submit',{method:'POST',headers:{'Content-Type':'application/json',Accept:'application/json'},body:JSON.stringify({access_key:key,subject:'Selected Design Quotation Request - Mr Sewing',from_name:'Mr Sewing Website',...fields,...(fields['Email Address']?{replyto:fields['Email Address']}:{}),botcheck:''}),signal:controller.signal});const result=await r.json();if(!r.ok||result.success!==true)return reply(502,{success:false,error:'The submission service did not confirm acceptance.'});return reply(200,{success:true});}catch{return reply(502,{success:false,error:'We could not confirm submission. It may have arrived; contact Customer Support before retrying.'});}finally{clearTimeout(timer);}
}
