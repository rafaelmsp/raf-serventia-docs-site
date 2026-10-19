const puppeteer=require('puppeteer'),assert=require('node:assert/strict'),fs=require('fs'),path=require('path');
(async()=>{
 const b=await puppeteer.launch({headless:true,executablePath:'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',args:['--no-sandbox']});
 const results=[];
 try{
  for(const width of [390,1366]){
   const p=await b.newPage();await p.setViewport({width,height:820});
   const errors=[];p.on('pageerror',e=>errors.push(e.message));
   const base='https://rafaelmsp.github.io/raf-serventia-docs-site/';
   for(const code of ['O-03','BF-01']){
    const res=await p.goto(base+'itens/'+code+'.html',{waitUntil:'domcontentloaded',timeout:20000});
    assert.equal(res.status(),200);
    await p.waitForFunction(()=>!document.getElementById('lesson-app').hidden,{timeout:13000});
    await p.evaluate(c=>localStorage.removeItem('raf-learn-v2-'+c),code);
    await p.reload({waitUntil:'domcontentloaded'});
    await p.waitForFunction(()=>!document.getElementById('lesson-app').hidden,{timeout:10000});
    assert((await p.$eval('.lesson-hero h1',e=>e.textContent)).length>10);
    await p.$eval('.control-primary',x=>x.click());
    await p.$eval('.control-primary',x=>x.click());
    await p.waitForFunction(()=>document.querySelector('.visual-figure img')?.complete&&document.querySelector('.visual-figure img')?.naturalWidth>0,{timeout:12000});
    await p.$eval('.hotspot-btn:nth-child(2)',x=>x.click());
    assert(await p.$eval('.hotspot-explain p',x=>x.textContent.length>20));
    const span=await p.evaluate(()=>document.documentElement.scrollWidth-innerWidth);
    assert(span<=2);
    results.push({width,code,http:res.status(),hotspots:true,svgLoaded:true,overflow:false});
   }
   assert.equal(errors.length,0,'JS '+errors.join(';'));
   await p.close();
  }
 }finally{await b.close()}
 console.log(JSON.stringify({success:results.length,items:results},null,2));
 fs.writeFileSync(path.join(__dirname,'v2-live.json'),JSON.stringify(results,null,2),'utf8');
})().catch(e=>{console.error(e.stack);process.exitCode=1});
