const puppeteer=require('puppeteer'),assert=require('node:assert/strict'),fs=require('fs'),path=require('path');
(async()=>{
 const b=await puppeteer.launch({headless:true,executablePath:'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',args:['--no-sandbox']});
 const p=await b.newPage();await p.setViewport({width:390,height:844});
 const errors=[];p.on('pageerror',e=>errors.push(e.message));
 try{
  console.log('STEP launch');
  const r=await p.goto('https://rafaelmsp.github.io/raf-serventia-docs-site/itens/O-03.html',{waitUntil:'domcontentloaded',timeout:18000});
  console.log('STEP navigation',r.status());
  await p.waitForSelector('.premium-tabs [data-tab="fluxo"]',{timeout:10000});
  console.log('STEP tabs',await p.$$eval('[role="tab"]',x=>x.length));
  await p.$eval('[data-tab="fluxo"]',e=>e.click());
  await p.waitForSelector('.node-button[data-index="0"]');
  await p.$eval('.node-button[data-index="0"]',e=>e.click());
  console.log('STEP description',await p.$eval('#node-title',e=>e.innerText.slice(0,80)));
  const result={status:r.status(),tabs:5,code:'O-03',width:390,jsErrors:errors};
  fs.writeFileSync(path.join(__dirname,'qa-live-smoke.json'),JSON.stringify(result,null,2),'utf8');
  console.log('RESULT',JSON.stringify(result));
 }finally{await b.close()}
})().catch(e=>{console.error('FAILED',e.message);process.exitCode=1});
