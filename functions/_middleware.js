/* Staging source boundary. Public repository history is not made private by this. */
const STAGING='mrsewing-staging.pages.dev';
const INTERNAL=new Set(['_data','_templates','_media','scripts','tests','docs','functions','.github','.git','.agents','.codex','.aws']);
export async function onRequest(context){
 const url=new URL(context.request.url);
 if(url.hostname!==STAGING&&!url.hostname.endsWith('.'+STAGING))return context.next();
 let path=url.pathname;
 try{for(let i=0;i<3;i++){const decoded=decodeURIComponent(path);if(decoded===path)break;path=decoded;}}
 catch{return context.next();}
 const first=path.replaceAll('\\','/').split('/').filter(Boolean)[0];
 if(!INTERNAL.has(first))return context.next();
 return new Response(context.request.method==='HEAD'?null:'Not found',{status:404,headers:{'Content-Type':'text/plain; charset=utf-8','Cache-Control':'no-store','X-Robots-Tag':'noindex, nofollow, noarchive'}});
}
