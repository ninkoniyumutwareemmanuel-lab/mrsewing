import {config} from './public-api-config.js';
const jsonError=message=>new Response(JSON.stringify({success:false,error:message}),{status:403,headers:{'Content-Type':'application/json','Cache-Control':'no-store'}});
/* Only public email intake, only exact live origins, only the main branch runtime. */
export async function publicIntake(context,handle){
 const request=context.request,u=new URL(request.url),origin=request.headers.get('Origin');
 if(!origin||origin===u.origin)return handle(request);
 if(u.origin!==config.backendOrigin||!config.productionOrigins.includes(origin)||!config.paths.includes(u.pathname))return jsonError('Submit from the approved website.');
 const cors=response=>{const headers=new Headers(response.headers);headers.set('Access-Control-Allow-Origin',origin);headers.set('Vary','Origin');headers.set('Cache-Control','no-store');return new Response(response.body,{status:response.status,headers});};
 if(request.method==='OPTIONS'){
  const method=request.headers.get('Access-Control-Request-Method');const names=(request.headers.get('Access-Control-Request-Headers')||'').toLowerCase().split(',').map(x=>x.trim()).filter(Boolean);
  if(method!=='POST'||names.some(n=>!['content-type','accept'].includes(n)))return cors(jsonError('Unsupported request.'));
  return cors(new Response(null,{status:204,headers:{'Access-Control-Allow-Methods':'POST, OPTIONS','Access-Control-Allow-Headers':'Content-Type, Accept'}}));
 }
 if(request.method!=='POST')return cors(new Response(JSON.stringify({success:false,error:'POST required.'}),{status:405,headers:{'Content-Type':'application/json'}}));
 const headers=new Headers(request.headers);headers.delete('Origin');
 // Origin was verified above; all existing host/body/design/stock/consent validation follows.
 return cors(await handle(new Request(request,{headers})));
}
