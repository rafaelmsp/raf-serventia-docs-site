const fs=require('fs'),path=require('path'),http=require('http'),assert=require('node:assert/strict'),puppeteer=require('puppeteer');
const ROOT=path.resolve(__dirname,'..');
const types={'.html':'text/html; charset=utf-8','.json':'application/json','.js':'application/javascript','.css':'text/css','.svg':'image/svg+xml','.jpg':'image/jpeg','.pdf':'application/pdf'};
const server=http.createServer((req,res)=>{
 const file=path.resolve(ROOT,'.'+decodeURIComponent(new URL(req.url,'http://localhost').pathname));
 if(!file.startsWith(ROOT+path.sep)){res.writeHead(403).end();return}
 fs.readFile(file,(e,data)=>{if(e){res.writeHead(404).end();return}
 res.writeHead(200,{'Content-Type':types[path.extname(file)]||'application/octet-stream'});res.end(data)});
});
(async()=>{
 await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));
 const base='http://127.0.0.1:'+server.address().port;
 const browser=await puppeteer.launch({headless:true,executablePath:'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',args:['--no-sandbox']});
 const failures=[],screenshots=path.join(ROOT,'tests','v2-screenshots');fs.mkdirSync(screenshots,{recursive:true});
 let cases=0;
 try{
  const idx=JSON.parse(fs.readFileSync(path.join(ROOT,'dados/procedimentos.json'),'utf8'));
  const pilots=['O-03','BF-01','O-08','P-01','R-01','BV-01'];
  for(const width of [360,390,430,768,1024,1366]){
   const page=await browser.newPage();await page.setViewport({width,height:830});
   const errors=[];page.on('pageerror',e=>errors.push(e.message));
   for(const code of pilots){
    try{
     const response=await page.goto(base+'/itens/'+code+'.html',{waitUntil:'networkidle0',timeout:15000});
     assert.equal(response.status(),200,'response');
     await page.evaluate((key)=>localStorage.removeItem('raf-learn-v2-'+key),code);
     await page.reload({waitUntil:'domcontentloaded'});
     await page.waitForFunction(()=>!document.getElementById('lesson-app').hidden,{timeout:8000});
     const initial=await page.evaluate(()=>({
      code:document.body.dataset.code,percent:document.querySelector('.meter-fill').style.width,
      width:document.documentElement.scrollWidth-innerWidth,
      name:document.querySelector('.lesson-hero h1').textContent}));
     assert.equal(initial.code,code);
     assert(initial.width<=2,'overflow '+width+' '+code+' '+initial.width);
     await page.$eval('.control-primary',x=>x.click());
     assert((await page.$eval('.meter-head',e=>e.textContent)).includes('2 de 7'));
     await page.$eval('.control-primary',x=>x.click());
     await page.waitForFunction(()=>document.querySelector('.visual-figure img')?.complete&&document.querySelector('.visual-figure img')?.naturalWidth>0);
     await page.$eval('.hotspot-btn:nth-child(2)',x=>x.click());
     assert(await page.$eval('.hotspot-explain p',e=>e.textContent.length>=20));
     await page.$eval('.control-primary',x=>x.click());
     await page.$eval('.control-primary',x=>x.click());
     assert(await page.$eval('.coach-item',x=>x.textContent.length>35));
     await page.$eval('.control-primary',x=>x.click());
     await page.$eval('.quiz-option:nth-child(2)',x=>x.click());
     assert(await page.$eval('.quiz-feedback',x=>x.innerText.length>10));
     await page.$eval('.control-primary',x=>x.click());
     await page.$eval('.quiz-option:nth-child(2)',x=>x.click());
     assert(await page.$eval('.quiz-feedback',x=>x.innerText.length>10));
     assert(await page.$eval('.source-row a',x=>x.href.includes('manual-fonte.pdf#page=')));
     if(width===390){
      await page.goto(base+'/itens/'+code+'.html',{waitUntil:'networkidle0'});
      await page.screenshot({path:path.join(screenshots,'v2-'+code+'-390.png'),fullPage:false});
     }
     cases++;
    }catch(err){failures.push({width,code,error:err.message.slice(0,280)})}
   }
   if(errors.length)failures.push({width,errors});
   await page.close();
  }
  const page=await browser.newPage();await page.setViewport({width:390,height:830});
  for(const row of idx){
   try{
    const res=await page.goto(base+'/itens/'+row.codigo+'.html',{waitUntil:'domcontentloaded',timeout:10000});
    assert.equal(res.status(),200);
    await page.waitForFunction(()=>!document.getElementById('lesson-app').hidden,{timeout:5000});
    const overflow=await page.evaluate(()=>document.documentElement.scrollWidth-innerWidth);
    assert(overflow<=2,'overflow '+overflow);
   }catch(err){failures.push({code:row.codigo,error:err.message.slice(0,200)})}
  }
  for(const route of ['index.html','aprender.html','andamento-pedagogico.html']){
    const r=await page.goto(base+'/'+route,{waitUntil:'domcontentloaded'});
    if(r.status()!==200)failures.push({route,http:r.status()});
  }
  await page.close();
 }finally{await browser.close();server.close()}
 const result={timestamp:new Date().toISOString(),pilot_cases:cases,expected_pilot_cases:36,all_lesson_routes:96,
  html_entry_points:3,failures};
 fs.writeFileSync(path.join(ROOT,'tests','v2-qa.json'),JSON.stringify(result,null,2),'utf8');
 console.log(JSON.stringify(result,null,2));
 if(failures.length)process.exitCode=1;
})().catch(e=>{console.error(e.stack);server.close();process.exitCode=1});