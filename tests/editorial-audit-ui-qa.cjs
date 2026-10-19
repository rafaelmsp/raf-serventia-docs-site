const puppeteer=require('puppeteer'),assert=require('node:assert/strict'),fs=require('fs'),path=require('path'),http=require('http');
const root=path.resolve(__dirname,'..');const mime={'.html':'text/html;charset=utf-8','.js':'text/javascript','.css':'text/css','.json':'application/json','.svg':'image/svg+xml','.pdf':'application/pdf'};
const server=http.createServer((req,res)=>{
 const f=path.resolve(root,'.'+decodeURIComponent(new URL(req.url,'http://localhost').pathname));
 if(!f.startsWith(root+path.sep)){res.writeHead(403).end();return}
 fs.readFile(f,(e,data)=>{if(e){res.writeHead(404).end();return}
 res.writeHead(200,{'Content-Type':mime[path.extname(f)]||'application/octet-stream'});res.end(data)});
});
(async()=>{
 await new Promise(r=>server.listen(0,'127.0.0.1',r));
 const base='http://127.0.0.1:'+server.address().port;
 const browser=await puppeteer.launch({headless:true,executablePath:'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',args:['--no-sandbox']});
 const results=[],fails=[];
 try{
  for(const width of [360,390,768,1366]){
   const p=await browser.newPage();await p.setViewport({width,height:840});
   p.on('pageerror',e=>fails.push('javascript '+width+' '+e.message));
   try{
    const httpResult=await p.goto(base+'/auditoria-fonte.html',{waitUntil:'domcontentloaded'});
    assert.equal(httpResult.status(),200);
    await p.waitForFunction(()=>document.querySelector('#checked').textContent==='15',{timeout:13000});
    assert.equal(await p.$eval('#pending',e=>e.textContent),'81');
    assert.equal(await p.$$eval('.audit-item',x=>x.length),9);
    await p.select('#audit-filter','checked');
    assert.equal(await p.$$eval('.audit-item',x=>x.length),9);
    await p.$eval('.audit-source-details summary',e=>e.click());
    assert(await p.$eval('.audit-source-details .audit-risk',e=>e.textContent.length>55));
    await p.select('#audit-section','P');
    assert.equal(await p.$$eval('.audit-item',x=>x.length),3);
    await p.$eval('#audit-search',e=>e.value='');await p.type('#audit-search','72 horas');
    assert.equal(await p.$$eval('.audit-item',x=>x.length),1);
    assert((await p.$eval('.audit-item h3',x=>x.innerText)).includes('72'));
    const pdfHref=await p.$eval('.audit-item a[href*="#page="]',e=>e.getAttribute('href'));
    assert(pdfHref.endsWith('#page=71'));
    let over=await p.evaluate(()=>document.documentElement.scrollWidth-innerWidth);
    assert(over<=2,'audit overflow '+over);
    if(width===390||width===1366){
     await p.screenshot({path:path.join(root,'qa','review-pages','auditoria-'+width+'.png'),fullPage:false});
    }
    // Lesson that has a review record
    await p.goto(base+'/itens/P-16.html',{waitUntil:'domcontentloaded'});
    await p.waitForFunction(()=>!document.getElementById('lesson-app').hidden);
    await p.$eval('details.edu-review summary',e=>e.click());
    assert((await p.$eval('.edu-review-risk',e=>e.textContent)).includes('72 horas'));
    const lessonRef=await p.$eval('details.edu-review a',e=>e.getAttribute('href'));
    assert(lessonRef.endsWith('auditoria-fonte.html'));
    // Unchecked class should never falsely show original source checked
    await p.goto(base+'/itens/O-10.html',{waitUntil:'domcontentloaded'});
    await p.waitForFunction(()=>!document.getElementById('lesson-app').hidden);
    assert((await p.$eval('details.edu-review summary',e=>e.textContent)).includes('pendente'));
    results.push({width,audit_list:96,visual_checked:15,pending:81,filters:true,source_links:true,lesson_banners:true,no_overflow:true});
   }catch(e){fails.push(width+' '+e.message)}
   await p.close();
  }
 }finally{await browser.close();server.close()}
 const out={passed:results.length,expected:4,failures:fails,results};
 fs.writeFileSync(path.join(root,'tests','editorial-audit-ui-qa.json'),JSON.stringify(out,null,2),'utf8');
 console.log(JSON.stringify(out,null,2));if(fails.length)process.exitCode=1;
})().catch(e=>{console.error(e.stack);server.close();process.exitCode=1});
