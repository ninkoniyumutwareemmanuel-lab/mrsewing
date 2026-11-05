/* Private intake API. No binding defaults, public object URLs or production enablement. */
import referenceData from '../../_data/request-reference-allowlist.json' with {type:'json'};
const services=['Custom Tailoring & Suits','Clothing Alterations & Repairs','Garment Care & Cleaning','Mobile Tailoring, Styling & Event Assistance','VIP Services'];
export const limits={maxFiles:3,maxFileBytes:3*1024*1024,maxPixels:20000000};
const allowed=['Full Name','Phone Number','Email Address','Location','Quantity','Preferred Date','Fabric Preferences','Measurements','Garment Type','Garment Condition','Handover Preference','Assistance Type','Preferred Time','Participants','Event Details','Customer Message','Service','Service Experience','Design Order Type','Design Reference','Design Name','Suit Category','Suit Category Reference','Suit Audience','Fabric Choice','Selected Fabric','Fabric Reference','Fabric Category','Fabric Tier','Fabric Availability','Fabric Assistance','Order Priority','After-hours Request'];
const headers={'Content-Type':'application/json','Cache-Control':'no-store','X-Content-Type-Options':'nosniff','X-Robots-Tag':'noindex, nofollow','Cross-Origin-Resource-Policy':'same-origin'};
const reply=(data,status=200)=>new Response(JSON.stringify(data),{status,headers});
const digest=async bytes=>[...new Uint8Array(await crypto.subtle.digest('SHA-256',bytes))].map(v=>v.toString(16).padStart(2,'0')).join('');
export function ready(env){return env.REQUESTS_ENABLED==='true'&&['REQUESTS_DB','PRIVATE_REQUEST_FILES','TURNSTILE_SECRET','TURNSTILE_SITE_KEY','REQUEST_EMAIL_ACCESS_KEY','REQUEST_RATE_SECRET','STAFF_ACCESS_TEAM','STAFF_ACCESS_AUD','STAFF_ALLOWED_EMAILS'].every(k=>!!env[k])&&String(env.REQUEST_RATE_SECRET).length>=32&&/^[a-z0-9-]+\.cloudflareaccess\.com$/.test(env.STAFF_ACCESS_TEAM)&&String(env.STAFF_ALLOWED_EMAILS).split(',').every(e=>/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(e.trim()));}
function permittedHost(request,env){const h=new URL(request.url).hostname;return h==='mrsewing-staging.pages.dev'||h.endsWith('.mrsewing-staging.pages.dev')||(env.LOCAL_TESTING==='true'&&['127.0.0.1','localhost'].includes(h));}
function fail(status,message){throw Object.assign(Error(message),{status});}
export function validateFields(raw){
 if(!raw||Array.isArray(raw)||typeof raw!=='object')fail(400,'Invalid request fields.');
 const data={};for(const k of allowed)if(raw[k]!==undefined){if(typeof raw[k]!=='string'||raw[k].length>4000||/\u0000/.test(raw[k]))fail(400,'Invalid field length or value.');data[k]=raw[k].trim();}
 if(!data['Full Name']||data['Full Name'].length>160||!data['Customer Message']||!data.Location||data.Location.length>160)fail(400,'Complete name, location and message.');
 if(!/^[+\d\s().-]{7,40}$/.test(data['Phone Number']||'')||!/^\d{7,15}$/.test((data['Phone Number']||'').replace(/\D/g,'')))fail(400,'Enter a valid phone number.');
 if(data['Email Address']&&(!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(data['Email Address'])||data['Email Address'].length>254))fail(400,'Enter a valid email address.');
 if(!services.includes(data.Service)||!['Standard Priority','Express Priority'].includes(data['Order Priority']))fail(400,'Choose a valid service and priority.');
 if(!/^\d{1,4}$/.test(data.Quantity||'')||+data.Quantity<1)fail(400,'Enter a valid garment quantity.');
 if(data['Design Reference']){const design=referenceData[data['Design Reference']];if(!design)fail(400,'Choose a published design reference.');data['Design Name']=design.name;if(design.category){data['Suit Category']=design.category;data['Suit Audience']=design.audience;}}
 return data;
}
const crcTable=Uint32Array.from({length:256},(_,n)=>{for(let k=0;k<8;k++)n=n&1?0xedb88320^(n>>>1):n>>>1;return n>>>0;});
function crc32(bytes){let c=0xffffffff;for(const b of bytes)c=crcTable[(c^b)&255]^(c>>>8);return(c^0xffffffff)>>>0;}
export function inspectImage(bytes,mime){
 const b=new Uint8Array(bytes),v=new DataView(b.buffer,b.byteOffset,b.byteLength);let width,height,type;
 if(b.length<24)fail(400,'Invalid image.');
 if(b.slice(0,8).join(',')==='137,80,78,71,13,10,26,10'){
  type='image/png';let p=8,first=true,data=false,end=false;
  while(p+12<=b.length){const n=v.getUint32(p),tag=String.fromCharCode(...b.slice(p+4,p+8));if(n>limits.maxFileBytes||p+12+n>b.length||crc32(b.slice(p+4,p+8+n))!==v.getUint32(p+8+n))fail(400,'Invalid PNG structure.');
   if(first){if(tag!=='IHDR'||n!==13)fail(400,'Invalid PNG header.');width=v.getUint32(p+8);height=v.getUint32(p+12);first=false;}
   if(tag==='acTL')fail(400,'Use a still image, not an animation.');if(tag==='IDAT')data=true;p+=12+n;if(tag==='IEND'){if(n!==0||p!==b.length)fail(400,'Invalid PNG ending.');end=true;break;}}
  if(!data||!end)fail(400,'Incomplete PNG.');
 }else if(b[0]===255&&b[1]===216&&b.at(-2)===255&&b.at(-1)===217){
  type='image/jpeg';let p=2,scan=false;
  while(p+4<b.length){if(b[p++]!==255)fail(400,'Invalid JPEG structure.');while(b[p]===255)p++;const marker=b[p++];if(marker===0xda){scan=true;break;}if(marker===0xd9)break;const n=v.getUint16(p);if(n<2||p+n>b.length)fail(400,'Invalid JPEG segment.');if([0xc0,0xc1,0xc2].includes(marker)){if(n<8)fail(400,'Invalid JPEG dimensions.');height=v.getUint16(p+3);width=v.getUint16(p+5);}p+=n;}
  if(!scan||!width)fail(400,'Incomplete JPEG.');
 }else if(String.fromCharCode(...b.slice(0,4))==='RIFF'&&String.fromCharCode(...b.slice(8,12))==='WEBP'&&v.getUint32(4,true)+8===b.length){
  type='image/webp';let p=12,found=false;
  while(p+8<=b.length){const tag=String.fromCharCode(...b.slice(p,p+4)),n=v.getUint32(p+4,true),s=p+8;if(s+n>b.length)fail(400,'Invalid WebP structure.');if(['ANIM','ANMF'].includes(tag))fail(400,'Use a still image.');
   if(tag==='VP8 '&&n>=10&&b[s+3]===157&&b[s+4]===1&&b[s+5]===42){width=v.getUint16(s+6,true)&16383;height=v.getUint16(s+8,true)&16383;found=true;}
   if(tag==='VP8L'&&n>=5&&b[s]===47){const bits=v.getUint32(s+1,true);width=(bits&16383)+1;height=((bits>>>14)&16383)+1;found=true;}p=s+n+(n%2);}
  if(!found||p!==b.length)fail(400,'Unsupported WebP image.');
 }else fail(400,'Use a valid JPEG, PNG or WebP image.');
 if(type!==mime||!width||!height||width*height>limits.maxPixels||width>12000||height>12000)fail(400,'Image type or dimensions are not supported.');return{type,width,height};
}
const jwksCache=new Map();
export async function authorised(request,env,fetcher=fetch){
 const token=request.headers.get('Cf-Access-Jwt-Assertion');if(!token||token.length>16000)return false;
 try{const parts=token.split('.');if(parts.length!==3)return false;const decode=s=>Uint8Array.from(atob(s.replace(/-/g,'+').replace(/_/g,'/')),x=>x.charCodeAt(0));const head=JSON.parse(new TextDecoder().decode(decode(parts[0]))),claims=JSON.parse(new TextDecoder().decode(decode(parts[1])));const team=env.STAFF_ACCESS_TEAM;if(!/^[a-z0-9-]+\.cloudflareaccess\.com$/.test(team)||head.alg!=='RS256'||!head.kid)return false;
  const now=Date.now()/1000,aud=Array.isArray(claims.aud)?claims.aud:[claims.aud];if(claims.iss!=='https://'+team||!Number.isFinite(claims.exp)||claims.exp<=now||!aud.includes(env.STAFF_ACCESS_AUD)||!Number.isFinite(claims.iat)||claims.iat>now+30||(claims.nbf!==undefined&&(!Number.isFinite(claims.nbf)||claims.nbf>now+30)))return false;
  if(typeof claims.email!=='string'||!claims.email.includes('@'))return false;
  if(!String(env.STAFF_ALLOWED_EMAILS).toLowerCase().split(',').map(s=>s.trim()).includes(String(claims.email).toLowerCase()))return false;
  let cached=jwksCache.get(team);if(!cached||cached.expires<Date.now()){const r=await fetcher('https://'+team+'/cdn-cgi/access/certs');if(!r.ok)return false;cached={keys:(await r.json()).keys,expires:Date.now()+300000};jwksCache.set(team,cached);}const jwk=cached.keys.find(k=>k.kid===head.kid&&k.kty==='RSA');if(!jwk)return false;
  const key=await crypto.subtle.importKey('jwk',jwk,{name:'RSASSA-PKCS1-v1_5',hash:'SHA-256'},false,['verify']);return await crypto.subtle.verify('RSASSA-PKCS1-v1_5',key,decode(parts[2]),new TextEncoder().encode(parts[0]+'.'+parts[1]));
 }catch(_){return false;}
}
async function sendEmail(record,env,fetcher){
 let state='failed';try{const body={...JSON.parse(record.fields_json),access_key:env.REQUEST_EMAIL_ACCESS_KEY,subject:'Mr Sewing request '+record.id,from_name:'Mr Sewing Website','Request Reference':record.id,'Private Attachments':'View through the authenticated Customer Requests area.','Staff Requests':'https://mrsewing-staging.pages.dev/staff/customer-requests/'};if(body['Email Address'])body.replyto=body['Email Address'];const r=await fetcher('https://api.web3forms.com/submit',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body),signal:AbortSignal.timeout(15000)});if(r.ok&&(await r.json()).success===true)state='accepted';}catch(_){}
 await env.REQUESTS_DB.prepare('UPDATE customer_requests SET email_status=? WHERE id=?').bind(state,record.id).run();return state;
}
export async function handle(request,env,fetcher=fetch){
 try{
  if(!permittedHost(request,env))return reply({error:'This API is enabled for the staging project only.'},403);
  const path=new URL(request.url).pathname;
  if(path==='/api/customer-requests/config'&&request.method==='GET')return reply({enabled:ready(env),...(ready(env)?{siteKey:env.TURNSTILE_SITE_KEY,...limits}:{})});
  if(!ready(env))return reply({error:'Private requests are not configured. No request or file has been saved.'},503);
  if(path.startsWith('/api/staff/')){
   if(!await authorised(request,env,fetcher))return reply({error:'Authorised staff access is required.'},401);
   if(path==='/api/staff/customer-requests'&&request.method==='GET'){
    const {results}=await env.REQUESTS_DB.prepare('SELECT id,created_at,fields_json,attachments_json,status,email_status FROM customer_requests ORDER BY created_at DESC LIMIT 100').all();return reply({requests:results.map(r=>({...r,fields:JSON.parse(r.fields_json),attachments:JSON.parse(r.attachments_json),fields_json:undefined,attachments_json:undefined}))});}
   const match=path.match(/^\/api\/staff\/customer-requests\/(MSQ-[A-Z0-9-]+)\/attachments\/([a-f0-9-]{36})$/);
   if(match&&request.method==='GET'){const row=await env.REQUESTS_DB.prepare('SELECT attachments_json FROM customer_requests WHERE id=?').bind(match[1]).first();const attachment=row&&JSON.parse(row.attachments_json).find(a=>a.id===match[2]);if(!attachment)return reply({error:'Attachment not found.'},404);const obj=await env.PRIVATE_REQUEST_FILES.get(attachment.key);if(!obj)return reply({error:'Attachment not found.'},404);return new Response(obj.body,{headers:{'Content-Type':attachment.type,'Content-Disposition':'attachment; filename="reference.'+({'image/jpeg':'jpg','image/png':'png','image/webp':'webp'}[attachment.type])+'"','Cache-Control':'private, no-store','X-Content-Type-Options':'nosniff','Content-Security-Policy':"default-src 'none'; sandbox",'X-Robots-Tag':'noindex, nofollow','Cross-Origin-Resource-Policy':'same-origin'}});}
   return reply({error:'Not found.'},404);
  }
  if(path!=='/api/customer-requests'||request.method!=='POST')return reply({error:'Not found.'},404);
  if(request.headers.get('Origin')!==new URL(request.url).origin)return reply({error:'Invalid request origin.'},403);
  if(!request.headers.get('content-type')?.startsWith('multipart/form-data'))return reply({error:'Use the request form.'},415);
  if(+(request.headers.get('content-length')||0)>10*1024*1024)return reply({error:'Request too large.'},413);
  const idem=request.headers.get('Idempotency-Key');if(!/^[a-f0-9-]{36}$/.test(idem||''))return reply({error:'Invalid request token.'},400);
  // Bound the entire body, including chunked requests, before multipart parsing.
  if(!request.body)return reply({error:'Request body is required.'},400);
  const reader=request.body.getReader();let total=0,parts=[];while(true){const {value,done}=await reader.read();if(done)break;total+=value.byteLength;if(total>10*1024*1024){await reader.cancel();return reply({error:'Request too large.'},413);}parts.push(value);}
  const bytes=new Uint8Array(total);let at=0;for(const part of parts){bytes.set(part,at);at+=part.byteLength;}const form=await new Response(bytes,{headers:{'Content-Type':request.headers.get('content-type')}}).formData();if(form.get('botcheck'))return reply({error:'Request not accepted.'},400);
  let raw;try{raw=JSON.parse(String(form.get('fields')));}catch(_){return reply({error:'Invalid request details.'},400);}const fields=validateFields(raw);if(form.get('termsAccepted')!=='true')return reply({error:'Terms acceptance is required.'},400);
  const files=form.getAll('files');if(files.length>limits.maxFiles)return reply({error:'Too many images.'},400);const prepared=[];
  for(const f of files){if(typeof f==='string'||f.size===0||f.size>limits.maxFileBytes)return reply({error:'Each image must be no larger than 3 MB.'},400);const bytes=await f.arrayBuffer(),info=inspectImage(bytes,f.type);prepared.push({bytes,info,name:f.name.replace(/[\u0000-\u001f\u007f]/g,'').slice(0,120),hash:await digest(bytes)});}
  fields['Terms Acceptance']='Customer asserted acceptance at submission';fields['Terms Version']='general-2026-11-05-r6';
  const hash=await digest(new TextEncoder().encode(JSON.stringify(fields)+JSON.stringify(prepared.map(f=>f.hash))));const existing=await env.REQUESTS_DB.prepare('SELECT id,payload_hash,email_status FROM customer_requests WHERE idempotency_key=?').bind(idem).first();if(existing){if(existing.payload_hash!==hash)return reply({error:'Request changed. Use a new request token.'},409);return reply({saved:true,reference:existing.id,emailStatus:existing.email_status,duplicate:true});}
  const captcha=await fetcher('https://challenges.cloudflare.com/turnstile/v0/siteverify',{method:'POST',body:new URLSearchParams({secret:env.TURNSTILE_SECRET,response:String(form.get('captcha')||'').slice(0,2048),remoteip:request.headers.get('CF-Connecting-IP')||''})});const check=await captcha.json();if(!captcha.ok||check.success!==true||check.hostname!==new URL(request.url).hostname||check.action!=='customer_request')return reply({error:'Please complete the security check again.'},400);
  const hour=Math.floor(Date.now()/3600000),key=await crypto.subtle.importKey('raw',new TextEncoder().encode(env.REQUEST_RATE_SECRET),{name:'HMAC',hash:'SHA-256'},false,['sign']);const rate=[...new Uint8Array(await crypto.subtle.sign('HMAC',key,new TextEncoder().encode((request.headers.get('CF-Connecting-IP')||'unknown')+'|'+hour)))].map(v=>v.toString(16).padStart(2,'0')).join('');
  await env.REQUESTS_DB.prepare('DELETE FROM request_rate_limits WHERE expires<?').bind(Date.now()).run();
  const hit=await env.REQUESTS_DB.prepare('INSERT INTO request_rate_limits(key,count,expires) VALUES(?,1,?) ON CONFLICT(key) DO UPDATE SET count=count+1 WHERE count<30').bind(rate,(hour+1)*3600000).run();if(!hit.meta.changes)return reply({error:'Too many requests. Please try later.'},429);
  const id='MSQ-'+new Date().toISOString().slice(0,10).replaceAll('-','')+'-'+crypto.randomUUID().toUpperCase();const attachments=[];
  try{for(const f of prepared){const attachmentId=crypto.randomUUID(),key=id+'/'+attachmentId;attachments.push({id:attachmentId,key,name:f.name,size:f.bytes.byteLength,...f.info});await env.PRIVATE_REQUEST_FILES.put(key,f.bytes,{httpMetadata:{contentType:f.info.type}});}
   const record={id,created_at:new Date().toISOString(),fields_json:JSON.stringify(fields),attachments_json:JSON.stringify(attachments)};
   await env.REQUESTS_DB.prepare('INSERT INTO customer_requests(id,created_at,idempotency_key,payload_hash,fields_json,attachments_json,status,email_status) VALUES(?,?,?,?,?,?,?,?)').bind(id,record.created_at,idem,hash,record.fields_json,record.attachments_json,'New','pending').run();
   const emailStatus=await sendEmail(record,env,fetcher);return reply({saved:true,reference:id,emailStatus},201);
  }catch(error){const saved=await env.REQUESTS_DB.prepare('SELECT id,email_status FROM customer_requests WHERE idempotency_key=?').bind(idem).first();if(saved){if(saved.id!==id)await Promise.allSettled(attachments.map(a=>env.PRIVATE_REQUEST_FILES.delete(a.key)));return reply({saved:true,reference:saved.id,emailStatus:saved.email_status},202);}await Promise.allSettled(attachments.map(a=>env.PRIVATE_REQUEST_FILES.delete(a.key)));throw error;}
 }catch(error){return reply({error:error.status?error.message:'We could not confirm the request. Please contact Customer Support before retrying.'},error.status||503);}
}
