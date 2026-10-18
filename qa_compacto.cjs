const puppeteer=require('puppeteer'),assert=require('assert'),path=require('path'),fs=require('fs'),{pathToFileURL}=require('url');
(async()=>{
 const browser=await puppeteer.launch({headless:true,executablePath:'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',args:['--no-sandbox']});
 const out=path.join(__dirname,'qa','screenshots');fs.mkdirSync(out,{recursive:true});const results=[];
 for(const width of [360,390,430,768,1024,1366]){
   const p=await browser.newPage();await p.setViewport({width,height:844});
   const problems=[];p.on('pageerror',e=>problems.push(e.message));
   await p.goto(pathToFileURL(path.join(__dirname,'index.html')).href,{waitUntil:'load'});
   const v=await p.evaluate(()=>({links:[...document.querySelectorAll('#areas .item-name a')].map(a=>a.getAttribute('href')),overflow:document.documentElement.scrollWidth,viewport:innerWidth,bodyHeight:document.body.scrollHeight,missing:[...document.querySelectorAll('a[href^="#"]')].filter(a=>!document.querySelector(a.getAttribute('href'))).length,pdfLinks:document.querySelectorAll('a[href$=".pdf"]').length}));
   assert.equal(v.links.length,5);assert(v.overflow<=width+2,'horizontal overflow '+width);
   assert.equal(v.missing,0);assert.equal(v.pdfLinks,0);
   for(const href of v.links){await p.goto(pathToFileURL(path.join(__dirname,href)).href,{waitUntil:'load'});const b=await p.evaluate(()=>document.documentElement.scrollWidth);assert(b<=width+2,'overflow in '+href+' at '+width);}
   if([390,1366].includes(width)){
      await p.goto(pathToFileURL(path.join(__dirname,'index.html')).href,{waitUntil:'load'});
      await p.screenshot({path:path.join(out,'compacto-'+width+'.png'),fullPage:true});
      if(width===390){await p.goto(pathToFileURL(path.join(__dirname,'areas','operacoes.html')).href,{waitUntil:'load'});await p.screenshot({path:path.join(out,'area-390.png'),fullPage:true})}
   }
   assert.equal(problems.length,0);
   results.push({width,areaLinks:5,scrollWidth:v.overflow,height:v.bodyHeight,noPdf:true,jsErrors:0});
   await p.close()
 }
 await browser.close();console.log(JSON.stringify({passed:results.length,details:results},null,2))
})().catch(e=>{console.error(e.stack);process.exitCode=1})