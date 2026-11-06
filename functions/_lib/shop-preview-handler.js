/* Server-side isolation: production always falls through to normal static Shop. */
export async function handlePreview(context,pages){
 const u=new URL(context.request.url),host=u.hostname;
 const staging=host==='mrsewing-staging.pages.dev'||/^[a-z0-9-]+\.mrsewing-staging\.pages\.dev$/.test(host);
 if(!staging||u.protocol!=='https:'||!['GET','HEAD'].includes(context.request.method))return context.next();
 const path=u.pathname.endsWith('/')?u.pathname:u.pathname+'/';
 const html=pages[path];
 if(typeof html!=='string')return context.next();
 return new Response(context.request.method==='HEAD'?null:html,{status:200,headers:{'Content-Type':'text/html; charset=utf-8','X-Robots-Tag':'noindex, nofollow, noarchive','Cache-Control':'no-store','X-Content-Type-Options':'nosniff','Referrer-Policy':'strict-origin-when-cross-origin','X-Mr-Sewing-Shop-Preview':'draft-review'}});
}
