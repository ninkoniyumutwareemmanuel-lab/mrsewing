/* Exact Ads destinations: local real HTTP/render, never external conversions. */
'use strict';
const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
function library(){for(const name of['playwright','playwright-core','/workspace/tools/phase1/node_modules/playwright-core']){try{return require(name)}catch(e){if(e.code!=='MODULE_NOT_FOUND')throw e}}throw Error('Playwright is required');}
const{chromium}=library(),BASE=process.env.REVIEW_BASE_URL||'http://127.0.0.1:8020',OUT=process.env.REVIEW_ARTIFACTS||'/tmp/mrsewing-release-sitelinks';
const routes=['/services/custom-tailoring/','/mensuits/','/womensuits/','/services/alterations/','/services/garment-care/','/contact/'];
const query='?utm_source=google&utm_medium=cpc&utm_campaign=synthetic-release-check&gclid=synthetic-not-an-ad-click';
const report={scope:'Current local generated release; actual production HTTP/Google Ads receipt not established',routes:[],views:[],errors:[],missing:[],realSubmissions:false,externalConversions:false};
(async()=>{fs.mkdirSync(OUT,{recursive:true});const b=await chromium.launch({executablePath:process.env.CHROMIUM_BINARY||(fs.existsSync('/usr/bin/chromium')?'/usr/bin/chromium':undefined),args:['--no-sandbox']});try{
 const ctx=await b.newContext({reducedMotion:'reduce'});await ctx.route('**/*',r=>new URL(r.request().url()).origin===BASE&&r.request().method()==='GET'?r.continue():r.abort());
 const page=await ctx.newPage();page.on('pageerror',e=>report.errors.push(e.message));page.on('response',r=>{if(r.url().startsWith(BASE)&&r.status()>=400)report.missing.push({url:r.url(),status:r.status()})});
 const sitemap=fs.readFileSync(path.resolve(__dirname,'../sitemap.xml'),'utf8');
 for(const route of routes){
  const canonical='https://mrsewingfashion.com'+route;
  const response=await ctx.request.get(BASE+route,{maxRedirects:0});assert.equal(response.status(),200);assert(sitemap.includes('<loc>'+canonical+'</loc>'));
  const staged=await ctx.request.get(BASE+route,{headers:{Host:'mrsewing-staging.pages.dev'}});assert.match(staged.headers()['x-robots-tag'],/noindex/);
  for(const width of[320,390,768,1440]){
   await page.setViewportSize({width,height:900});await page.goto(BASE+route+query,{waitUntil:'load'});
   assert.equal(new URL(page.url()).pathname,route);assert.equal(new URL(page.url()).search,query);
   assert.equal(await page.locator('link[rel=canonical]').getAttribute('href'),canonical);
   assert.match(await page.locator('meta[name=robots]').getAttribute('content'),/^index, follow$/,'intended production source remains indexable');
   assert.equal(await page.locator('main h1').count(),1);assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1));
   assert.equal(await page.locator('header a[href="/shop/"],footer a[href="/shop/"]').count(),0);
   if(width===390)await page.screenshot({path:path.join(OUT,route.split('/').filter(Boolean).join('-')+'-390.png')});
   report.views.push({route,width,queryPreserved:true,canonical,status:'PASS'});
  }
  report.routes.push({url:canonical,localHTTP:200,redirects:0,sitemap:true,productionMeta:'index, follow',stagingHeader:'noindex',campaignLandingQueryPreserved:true,status:'PASS'});
 }
 const legacy=await ctx.request.get(BASE+'/mensuits.html'+query,{maxRedirects:0});assert.equal(legacy.status(),301);assert.equal(legacy.headers().location,'/mensuits/'+query);report.legacyRedirect={from:'/mensuits.html',to:'/mensuits/',status:301,queryPreserved:true};
 assert.deepEqual(report.errors,[]);assert.deepEqual(report.missing,[]);report.status='PASS';
}catch(e){report.status='FAIL';report.failure={message:e.message,stack:e.stack};process.exitCode=1;}finally{await b.close();fs.writeFileSync(path.join(OUT,'results.json'),JSON.stringify(report,null,2));console.log(JSON.stringify({status:report.status,routes:report.routes,views:report.views.length,failure:report.failure}));}})();
