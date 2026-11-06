/* Retained appointment/measurement forms: no real messages; current release chrome. */
const {chromium}=require('playwright'),assert=require('node:assert/strict');
const base=process.env.REVIEW_BASE_URL||'http://127.0.0.1:8000/';
(async()=>{const browser=await chromium.launch({executablePath:'/usr/bin/chromium',args:['--no-sandbox']});try{const context=await browser.newContext({viewport:{width:390,height:900}});const errors=[],missing=[];context.on('response',r=>{if(new URL(r.url()).origin===new URL(base).origin&&r.status()>=400)missing.push(r.url())});await context.route('**/*',r=>new URL(r.request().url()).origin===new URL(base).origin?r.continue():r.abort());
    const forms = await context.newPage();
    forms.on('pageerror', error => errors.push(error.message));
    async function prepare(file) {
      await forms.goto(base + file);
      await forms.locator('#fullName').fill('Phase 1 QA — mock only');
      await forms.locator('#phone').fill('+250780000000');
      for (const input of await forms.locator('input[required]:not([type="checkbox"])').all()) {
        const type = await input.getAttribute('type');
        if (type === 'date') await input.fill(await input.getAttribute('min'));
        else if (!(await input.inputValue())) await input.fill(type === 'email' ? 'qa@example.invalid' : 'Mock validation');
      }
      for (const select of await forms.locator('select[required]').all()) {
        const value = await select.locator('option').evaluateAll(options => options.find(option => option.value && !option.disabled)?.value);
        if (value) await select.selectOption(value);
      }
      if (file === 'measurement-submission.html') await forms.locator('#standardSize').selectOption({index:1});
      await forms.locator('#agreeTerms, #formTermsAgree').check();
    }
    for (const file of ['booking.html','booking-adjustment.html','booking-housecall.html','booking-workplace.html','measurement-submission.html']) {
      for (const scenario of ['success','rejection','missing-success','http-error','malformed','network']) {
        let count=0;
        await forms.route('https://api.web3forms.com/submit',async route => {
          count++;
          const data=route.request().postDataJSON();assert(data.access_key);assert(!data.apikey);
          if (scenario==='network') return route.abort();
          await route.fulfill({status:scenario==='http-error'?500:200,contentType:'application/json',body:scenario==='malformed'?'not JSON':JSON.stringify(scenario==='missing-success'?{}:{success:scenario!=='rejection'})});
        });
        await prepare(file);
        const submit=forms.locator('button[type="submit"]');await submit.click();
        if(scenario==='success') await forms.locator('#successBox').waitFor({state:'visible'});
        else { await forms.getByRole('status').filter({hasText:'We could not confirm'}).waitFor();assert(await submit.isEnabled());assert.equal(await forms.locator('#fullName').inputValue(),'Phase 1 QA — mock only'); }
        assert.equal(count,1);await forms.unroute('https://api.web3forms.com/submit');
      }
      let count=0,release;
      const held=new Promise(resolve=>release=resolve);
      await forms.route('https://api.web3forms.com/submit',async route=>{count++;await held;await route.fulfill({contentType:'application/json',body:'{"success":true}'});});
      await prepare(file);await forms.locator('button[type="submit"]').click();
      await forms.waitForFunction(()=>document.querySelector('form').getAttribute('aria-busy')==='true');
      await forms.locator('#agreeTerms, #formTermsAgree').uncheck();await forms.locator('#agreeTerms, #formTermsAgree').check();
      assert(await forms.locator('button[type="submit"]').isDisabled());
      await forms.locator('form').evaluate(form=>form.dispatchEvent(new Event('submit',{bubbles:true,cancelable:true})));
      release();await forms.locator('#successBox').waitFor({state:'visible'});assert.equal(count,1);await forms.unroute('https://api.web3forms.com/submit');
    }
    console.log('PASS: 30 mocked submission outcomes and duplicate-request/consent protection on all five forms.');
    await prepare('measurement-submission.html');await forms.locator('#standardSize').selectOption({index:0});
    await forms.locator('button[type="submit"]').click();await forms.getByRole('status').filter({hasText:'Please provide a standard size'}).waitFor();
    assert(await forms.locator('#standardSize').evaluate(el=>document.activeElement===el));
    await prepare('booking.html');await forms.locator('#phone').fill('letters');
    assert.equal(await forms.locator('#phone').evaluate(el=>el.validity.valid),false);
    await forms.clock.install();
    await forms.locator('#phone').fill('+250780000000');
    await forms.evaluate(()=>{window.fetch=(url,options)=>new Promise((resolve,reject)=>options.signal.addEventListener('abort',()=>reject(new DOMException('Aborted','AbortError'))));});
    await forms.locator('button[type="submit"]').click();await forms.clock.fastForward(21000);
    await forms.getByRole('status').filter({hasText:'timed out'}).waitFor();
    assert(await forms.locator('button[type="submit"]').isEnabled());
    console.log('PASS: measurement minimum, invalid phone rejection and timeout recovery.');
    assert.deepEqual(errors,[]);assert.deepEqual(missing,[]);
    console.log('PASS: no JavaScript page errors or local missing-resource responses. External services were blocked/mocked.');

}finally{await browser.close()}})().catch(e=>{console.error(e);process.exit(1)});
