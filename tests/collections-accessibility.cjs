/* Install @axe-core/playwright outside the checkout; expose it via NODE_PATH. */
const {chromium}=require('playwright'),{default:AxeBuilder}=require('@axe-core/playwright'),fs=require('fs'),assert=require('node:assert/strict');
const base=process.env.REVIEW_BASE_URL||'http://127.0.0.1:8000/';
(async()=>{const browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',args:['--no-sandbox']});const reports=[];try{const c=await browser.newContext();await c.route('**/*',r=>new URL(r.request().url()).origin===new URL(base).origin?r.continue():r.abort());const p=await c.newPage();
for(const width of [390,1440])for(const route of ['collections/','mensuits/','womensuits/','collections/designs/ms-009/']){
 await p.setViewportSize({width,height:900});await p.goto(base+route);await p.locator('h1').waitFor();
 let result=await new AxeBuilder({page:p}).withTags(['wcag2a','wcag2aa','wcag21aa','best-practice']).analyze();reports.push({width,route,view:'page',violations:result.violations});
 if(route.includes('designs/')){await p.locator('#open-photo').click();result=await new AxeBuilder({page:p}).withTags(['wcag2a','wcag2aa','wcag21aa','best-practice']).analyze();reports.push({width,route,view:'viewer',violations:result.violations});}
}
const out=process.env.REVIEW_ARTIFACTS||'/workspace/artifacts/collections-v3';fs.mkdirSync(out,{recursive:true});fs.writeFileSync(out+'/accessibility.json',JSON.stringify(reports,null,2));
const failures=reports.filter(r=>r.violations.length);for(const r of failures)console.log(JSON.stringify(r));assert.equal(failures.length,0,'Automated accessibility violations');console.log('PASS: axe WCAG 2 A/AA, WCAG 2.1 AA and best-practice scans on four routes at mobile/desktop, including full-screen viewing.');
}finally{await browser.close()}})().catch(e=>{console.error(e);process.exit(1)});
