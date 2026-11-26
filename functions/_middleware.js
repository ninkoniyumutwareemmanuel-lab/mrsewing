/* Website source boundary. It is deliberately independent of indexing/host rules.
 * The public release exporter also omits these paths for static hosts where
 * Pages Functions do not execute. Public Git history is not made private here. */
const INTERNAL=new Set(['_data','_templates','_media','scripts','tests','docs','functions','.github','.git','.agents','.codex','.aws']);
export async function onRequest(context){
 const url=new URL(context.request.url);
 let path=url.pathname;
 try{for(let i=0;i<3;i++){const decoded=decodeURIComponent(path);if(decoded===path)break;path=decoded;}}
 catch{return context.next();}
 // Normalize decoded dot segments as well as encoded separators before testing
 // the first path component; an asset-prefix traversal is not a public asset.
 const segments=[];
 for(const segment of path.replaceAll('\\','/').split('/')){
  if(!segment||segment==='.')continue;
  if(segment==='..'){segments.pop();continue;}
  segments.push(segment);
 }
 const first=segments[0];
 if(!INTERNAL.has(first))return context.next();
 return new Response(context.request.method==='HEAD'?null:'Not found',{status:404,headers:{'Content-Type':'text/plain; charset=utf-8','Cache-Control':'no-store','X-Robots-Tag':'noindex, nofollow, noarchive'}});
}
