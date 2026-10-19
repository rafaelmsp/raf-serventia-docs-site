const http=require('http'),fs=require('fs'),path=require('path'),assert=require('node:assert/strict'),puppeteer=require('puppeteer');
const ROOT=path.resolve(__dirname,'..');const mime={'.html':'text/html','.css':'text/css','.js':'application/javascript','.json':'application/json','.svg':'image/svg+xml','.jpg':'image/jpeg'};
const server=http.createServer((req,res)=>{const f=path.resolve(ROOT,'.'+new URL(req.url,'http://local').pathname);if(!f.startsWith(ROOT+path.sep)){res.writeHead(403).end();return}fs.readFile(f,(e,d)=>{if(e){res.writeHead(404).end();return}res.writeHead(200,{'Content-Type':mime[path.extname(f)]||'application/octet-stream'});res.end(d)})});
(async()=>{
 await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));const base='http://127.0.0.1:'+server.address().port;
 const b=await puppeteer.launch({headless:true,executablePath:'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',args:['--no-sandbox'],protocolTimeout:60000});
 const p=await b.newPage();let failures=[],passes=0;
 try{
  for(const width of [360,390,430,768,1024,1366,1920]){
   await p.setViewport({width,height:850});
   for(const code of ['O-03','O-08','BF-01','BV-01','P-01','R-01']){
    try{
     const rsp=await p.goto(base+'/itens/'+code+'.html',{waitUntil:'domcontentloaded',timeout:15000});assert.equal(rsp.status(),200);
     await p.waitForFunction(()=>{const i=document.querySelector('.premium-illustration img');return i&&i.complete&&i.naturalWidth>0},{timeout:10000});
     const initial=await p.evaluate(()=>({n:document.querySelectorAll('[role="tab"]').length,w:document.documentElement.scrollWidth-innerWidth}));
     assert.equal(initial.n,5);assert(initial.w<=2);
     await p.$eval('[data-tab="fluxo"]',e=>e.click());
     await p.waitForFunction(()=>document.querySelector('#node-title')?.textContent!=='Explore o mapa',{timeout:8000});
     await p.$eval('.node-button[data-index="1"]',e=>e.click());
     assert(await p.$eval('#node-title',e=>e.textContent.length>3));
     await p.$eval('[data-tab="conferencia"]',e=>e.click());
     await p.$eval('.check input',e=>e.click());
     assert((await p.$eval('#checkProgress',e=>e.textContent)).startsWith('1 de '));
     await p.$eval('#clearChecks',e=>e.click());
     assert((await p.$eval('#checkProgress',e=>e.textContent)).startsWith('0 de '));
     passes++;
    }catch(err){failures.push({width,code,error:String(err.message).slice(0,300)});}
   }
  }
 }finally{await b.close();server.close()}
 const out={passed:passes,expected:42,errors:failures,method:'Chromium DOM interaction and real asset loading'};
 fs.writeFileSync(path.join(ROOT,'tests','qa-premium-fast.json'),JSON.stringify(out,null,2),'utf8');
 console.log(JSON.stringify(out,null,2));if(failures.length)process.exitCode=1;
})().catch(err=>{console.error(err.stack);server.close();process.exitCode=1});
