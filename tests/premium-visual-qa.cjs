const puppeteer=require('puppeteer'),assert=require('node:assert/strict'),fs=require('fs'),path=require('path'),http=require('http');
const root=path.resolve(__dirname,'..');
const mime={'.html':'text/html;charset=utf-8','.css':'text/css','.js':'application/javascript','.json':'application/json','.svg':'image/svg+xml','.jpg':'image/jpeg','.pdf':'application/pdf'};
const server=http.createServer((req,res)=>{
 const target=path.resolve(root,'.'+decodeURIComponent(new URL(req.url,'http://localhost').pathname));
 if(!target.startsWith(root+path.sep)){res.writeHead(403).end();return}
 fs.readFile(target,(err,data)=>{if(err){res.writeHead(404).end();return}
 res.writeHead(200,{'Content-Type':mime[path.extname(target)]||'application/octet-stream'});res.end(data)});
});
(async()=>{
 await new Promise(r=>server.listen(0,'127.0.0.1',r));
 const base='http://127.0.0.1:'+server.address().port;
 const b=await puppeteer.launch({headless:true,executablePath:'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',args:['--no-sandbox']});
 const cases=[],problems=[],shots=path.join(root,'tests','premium-visual-shots');
 fs.mkdirSync(shots,{recursive:true});
 try {
  for(const width of [360,390,768,1366]){
   const p=await b.newPage();await p.setViewport({width,height:840,deviceScaleFactor:1});
   for(const code of ['O-03','O-08','P-01','R-01','BF-01','BV-01']){
    const errors=[];p.on('pageerror',e=>errors.push(e.message));
    try{
     const r=await p.goto(base+'/itens/'+code+'.html',{waitUntil:'domcontentloaded',timeout:15000});
     assert.equal(r.status(),200);
     await p.evaluate(c=>{localStorage.removeItem('raf-learn-v2-'+c)},code);
     await p.reload({waitUntil:'domcontentloaded'});
     await p.waitForFunction(()=>!document.getElementById('lesson-app').hidden,{timeout:10000});
     await p.waitForFunction(()=>document.querySelector('.premium-scene img')?.complete&&document.querySelector('.premium-scene img')?.naturalWidth>0,{timeout:10000});
     const href=await p.$eval('.premium-scene .edu-zoom-link',a=>a.getAttribute('href'));
     assert(href.includes(code+'/ilustracao-premium.svg'),'correct asset '+href);
     await p.$eval('.preview-action',x=>x.click());
     assert((await p.$eval('.meter-head',x=>x.textContent)).includes('3 de 7'));
     assert(await p.$eval('.premium-scene img',x=>x.complete&&x.naturalWidth>0));
     assert.equal(await p.$$eval('.hotspot-btn',n=>n.length),(code==='O-03'?5:5));
     await p.$eval('.hotspot-btn:nth-child(3)',x=>x.click());
     assert(await p.$eval('.hotspot-explain p',x=>x.innerText.length>16));
     const overflow=await p.evaluate(()=>document.documentElement.scrollWidth-innerWidth);
     assert(overflow<=2,'horizontal body overflow '+overflow);
     const scroller=await p.$eval('.edu-visual-viewport',e=>({w:e.clientWidth,scroll:e.scrollWidth}));
     if(width<700)assert(scroller.scroll>scroller.w,'zoom scroll on mobile');
     await p.$eval('.control-primary',x=>x.click());
     await p.$eval('.control-primary',x=>x.click());
     await p.waitForFunction(()=>document.querySelector('.premium-diagram img')?.complete&&document.querySelector('.premium-diagram img')?.naturalWidth>0,{timeout:10000});
     assert(await p.$eval('.premium-diagram .edu-zoom-link',x=>x.href.includes('fluxo-premium.svg')));
     if(width===390||width===1366) {
       await p.screenshot({path:path.join(shots,code+'-'+width+'-flow.png'),fullPage:false});
       await p.$eval('.control-secondary',x=>x.click());
       await p.$eval('.control-secondary',x=>x.click());
       await p.screenshot({path:path.join(shots,code+'-'+width+'-scene.png'),fullPage:false});
     }
     cases.push({width,code,illustration:true,flow:true,touch:true,scrollable:true});
    }catch(e){problems.push({width,code,error:e.message.slice(0,350)})}
   }
   await p.close();
  }
 }finally{await b.close();server.close()}
 const out={passed:cases.length,expected:24,problems,examples:cases.filter(x=>x.width===390)};
 fs.writeFileSync(path.join(root,'tests','premium-visual-qa.json'),JSON.stringify(out,null,2),'utf8');
 console.log(JSON.stringify(out,null,2));
 if(problems.length)process.exitCode=1;
})().catch(e=>{console.error(e.stack);server.close();process.exitCode=1});
