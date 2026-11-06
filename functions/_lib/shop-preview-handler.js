/* Server-side isolation: production always falls through to normal static Shop. */
export async function handlePreview(context,pages){
 const u=new URL(context.request.url),host=u.hostname;
 const staging=host==='mrsewing-staging.pages.dev'||/^[a-z0-9-]+\.mrsewing-staging\.pages\.dev$/.test(host);
 if(!staging||u.protocol!=='https:'||!['GET','HEAD'].includes(context.request.method))return context.next();
 const path=u.pathname.endsWith('/')?u.pathname:u.pathname+'/';
 let html=pages[path];
 if(typeof html!=='string')return context.next();
 // Review links must open this accessible staging deployment, not absent production drafts.
 html=html.replaceAll('https%3A%2F%2Fmrsewingfashion.com%2Fshop%2F',encodeURIComponent(u.origin+'/shop/')).replaceAll('data-product-url="https://mrsewingfashion.com/shop/','data-product-url="'+u.origin+'/shop/').replaceAll('data-share-product="https://mrsewingfashion.com/shop/','data-share-product="'+u.origin+'/shop/');
 return new Response(context.request.method==='HEAD'?null:html,{status:200,headers:{'Content-Type':'text/html; charset=utf-8','X-Robots-Tag':'noindex, nofollow, noarchive','Cache-Control':'no-store','X-Content-Type-Options':'nosniff','Referrer-Policy':'strict-origin-when-cross-origin','X-Mr-Sewing-Shop-Preview':'draft-review'}});
}
