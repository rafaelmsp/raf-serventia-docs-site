const http=require('http'),fs=require('fs'),path=require('path'),assert=require('node:assert/strict'),puppeteer=require('puppeteer');
const ROOT=path.resolve(__dirname,'..');
const MIME={'.html':'text/html;charset=utf-8','.css':'text/css','.js':'application/javascript','.json':'application/json','.svg':'image/svg+xml','.jpg':'image/jpeg','.pdf':'application/pdf'};
const server=http.createServer((req,res)=>{
 const target=path.resolve(ROOT,'.'+decodeURIComponent(new URL(req.url,'http://localhost').pathname));
 if(!target.startsWith(ROOT+path.sep)){res.writeHead(403).end();return}
 fs.readFile(target,(err,content)=>{if(err){res.writeHead(404).end();return}res.writeHead(200,{'Content-Type':MIME[path.extname(target)]||'application/octet-stream'});res.end(content)});
});
(async()=>{
 await new Promise(r=>server.listen(0,'127.0.0.1',r));
 const base='http://127.0.0.1:'+server.address().port;
 const browser=await puppeteer.launch({headless:true,executablePath:'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',args:['--no-sandbox']});
 const report=[];const images=path.join(ROOT,'tests','screenshots');fs.mkdirSync(images,{recursive:true});
 let problems=[];
 try{
  const all=JSON.parse(fs.readFileSync(path.join(ROOT,'dados','procedimentos.json'),'utf8'));
  assert.equal(all.length,96);
  for(const width of [360,390,430,768,1024,1366,1920]){
   const page=await browser.newPage();await page.setViewport({width,height:860,deviceScaleFactor:1});
   const errors=[];page.on('pageerror',e=>errors.push(e.message));
   for(const code of ['O-03','O-08','BF-01','BV-01','P-01','R-01']){
     const response=await page.goto(base+'/itens/'+code+'.html',{waitUntil:'networkidle0'});
     assert.equal(response.status(),200);
     const initial=await page.evaluate(()=>({
        title:document.querySelector('h1').textContent,
        overflow:document.documentElement.scrollWidth-innerWidth,
        illustration:document.querySelector('.premium-illustration img').naturalWidth,
        tabs:document.querySelectorAll('[role="tab"]').length,
        panels:document.querySelectorAll('[data-panel]').length
     }));
     assert(initial.overflow<=2,'OVERFLOW '+width+' '+code+' '+initial.overflow);
     assert(initial.illustration>0,'ILLUSTRATION LOAD '+code);
     assert.equal(initial.tabs,5);
     assert.equal(initial.panels,5);
     console.log('GEOMETRY',width,code,await page.evaluate(()=>{const x=document.querySelector('[data-tab=fluxo]');const a=x.getBoundingClientRect();const h=document.querySelector('.premium-header').getBoundingClientRect();return {target:{x:a.x,y:a.y,width:a.width,height:a.height},header:{bottom:h.bottom,top:h.top},scrollY}}));await page.click('[data-tab="fluxo"]');
     console.log('DEBUG',code,width,page.url(),await page.evaluate(()=>({location:location.href,panels:[...document.querySelectorAll('[data-panel]')].map(x=>x.dataset.panel),html:document.body.innerHTML.length})));assert(await page.$eval('[data-panel="fluxo"]',e=>!e.hidden),'map shown');
     await page.click('.node-button[data-index="1"]');
     assert(await page.$eval('#node-title',e=>e.textContent.length>4),'node details');
     await page.click('[data-tab="conferencia"]');
     await page.click('.check input');
     assert((await page.$eval('#checkProgress',e=>e.textContent)).startsWith('1 de '),'checklist');
     await page.reload({waitUntil:'networkidle0'});
     await page.click('[data-tab="conferencia"]');
     assert(await page.$eval('.check input',e=>e.checked),'check persists');
     await page.click('#clearChecks');
     assert(!(await page.$eval('.check input',e=>e.checked)),'reset');
     await page.click('[data-tab="fonte"]');
     assert((await page.$eval('.source-actions a.primary-action',e=>e.href)).includes('manual-fonte.pdf#page='));
     assert(errors.length===0,'JS ERRORS '+errors.join('|'));
     if(width===390||width===1366){
       await page.goto(base+'/itens/'+code+'.html',{waitUntil:'networkidle0'});
       await page.screenshot({path:path.join(images,'premium-'+code+'-'+width+'.png'),fullPage:false});
     }
     report.push({width,code,interactive:true,noOverflow:true,jsErrors:0});
   }
   await page.close();
  }
  // HTML, asset and source references for all 96 entries without browser interaction.
  for (const item of all){
    const code=item.codigo;
    for(const f of ['itens/'+code+'.html','assets/illustrations/'+code+'.svg','assets/flows/'+code+'.svg',
     'data/procedures/'+code+'.json','data/flows/'+code+'.json']){
      assert(fs.existsSync(path.join(ROOT,f)),'missing '+f);
    }
  }
 }catch(e){problems.push(e.stack)}
 finally{await browser.close();server.close()}
 const output={passed:report.length,expected:42,errors:problems,examples:report.filter(r=>r.width===390)};
 fs.writeFileSync(path.join(ROOT,'tests','qa-premium.json'),JSON.stringify(output,null,2),'utf8');
 console.log(JSON.stringify(output,null,2));
 if(problems.length)process.exitCode=1;
})().catch(e=>{console.error(e.stack);process.exitCode=1});
