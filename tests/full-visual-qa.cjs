const fs=require('fs'),path=require('path'),http=require('http'),assert=require('node:assert/strict'),puppeteer=require('puppeteer');
const ROOT=path.resolve(__dirname,'..'),ext={'.html':'text/html;charset=utf-8','.css':'text/css','.js':'application/javascript','.json':'application/json','.svg':'image/svg+xml','.jpg':'image/jpeg','.pdf':'application/pdf'};
const server=http.createServer((req,res)=>{const file=path.resolve(ROOT,'.'+decodeURIComponent(new URL(req.url,'http://localhost').pathname));if(!file.startsWith(ROOT+path.sep)){res.writeHead(403).end();return}fs.readFile(file,(err,data)=>{if(err){res.writeHead(404).end();return}res.writeHead(200,{'Content-Type':ext[path.extname(file)]||'application/octet-stream'});res.end(data)})});
(async()=>{
 await new Promise(done=>server.listen(0,'127.0.0.1',done));
 const base='http://127.0.0.1:'+server.address().port;
 const browser=await puppeteer.launch({headless:true,executablePath:'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',args:['--no-sandbox']});
 const rows=JSON.parse(fs.readFileSync(path.join(ROOT,'dados/procedimentos.json'),'utf8'));
 const failures=[];let reviewed=0;let visualOk=0;let diagramsOk=0;const bySection={};
 try{
  const page=await browser.newPage();await page.setViewport({width:390,height:860});
  page.on('pageerror',e=>failures.push({code:'browser',error:e.message}));
  for(const row of rows){
   try{
    const response=await page.goto(base+'/itens/'+row.codigo+'.html',{waitUntil:'domcontentloaded',timeout:16000});
    assert.equal(response.status(),200,'http');
    await page.waitForFunction(()=>!document.querySelector('#lesson-app').hidden,{timeout:12000});
    // State may be restored across runs; inspect visual in DOM after fresh local progress.
    await page.evaluate(c=>localStorage.removeItem('raf-learn-v2-'+c),row.codigo);
    await page.reload({waitUntil:'domcontentloaded'});
    await page.waitForFunction(()=>!document.querySelector('#lesson-app').hidden,{timeout:12000});
    await page.waitForFunction(()=>document.querySelector('.premium-scene img')?.complete&&document.querySelector('.premium-scene img')?.naturalWidth>0,{timeout:12000});
    const state=await page.evaluate(()=>({
     visual:document.querySelector('.premium-scene img')?.naturalWidth,
     src:document.querySelector('.premium-scene img')?.getAttribute('src'),
     width:document.documentElement.scrollWidth-innerWidth,
     hasButton:!!document.querySelector('.preview-action')
    }));
    assert(state.visual>0&&state.src.includes(row.codigo),'scene not loaded');
    assert(state.width<=2,'overflow '+state.width);
    assert(state.hasButton,'preview button missing');
    visualOk++;
    await page.$eval('.preview-action',e=>e.click());
    assert(await page.$eval('.hotspot-btn',e=>!!e),'hotspots');
    await page.$eval('.hotspot-btn:nth-child(3)',e=>e.click());
    assert(await page.$eval('.hotspot-explain p',e=>e.textContent.length>12),'hotspot content');
    await page.$eval('.control-primary',e=>e.click());await page.$eval('.control-primary',e=>e.click());
    await page.waitForFunction(()=>document.querySelector('.premium-diagram img')?.complete&&document.querySelector('.premium-diagram img')?.naturalWidth>0,{timeout:13000});
    diagramsOk++;
    reviewed++;
    bySection[row.categoria]=(bySection[row.categoria]||0)+1;
   }catch(err){failures.push({code:row.codigo,message:err.message.slice(0,180)})}
  }
  // 7 cards per pagination page with thumbnails:
  await page.goto(base+'/index.html',{waitUntil:'domcontentloaded'});
  await page.waitForFunction(()=>document.querySelectorAll('.item-visual').length===7,{timeout:13000});
  await page.waitForFunction(()=>[...document.querySelectorAll('.item-visual')].every(x=>x.complete&&x.naturalWidth>0),{timeout:16000});
  let ov=await page.evaluate(()=>document.documentElement.scrollWidth-innerWidth);
  assert(ov<=2,'catalog overflow '+ov);
  // view another category with its own assets:
  await page.$eval('button[data-cat="BF"]',e=>e.click());
  await page.waitForFunction(()=>document.querySelectorAll('.item-visual').length===7);
  await page.waitForFunction(()=>[...document.querySelectorAll('.item-visual')].every(x=>x.complete&&x.naturalWidth>0),{timeout:15000});
  await page.screenshot({path:path.join(ROOT,'tests','premium-catalog-full-390.png'),fullPage:false});
  await page.close();
 }finally{await browser.close();server.close()}
 const output={total:rows.length,pages_passed:reviewed,scenes_loaded:visualOk,diagrams_loaded:diagramsOk,
  by_section:bySection,failed:failures.length,failures};
 fs.writeFileSync(path.join(ROOT,'tests','full-visual-qa.json'),JSON.stringify(output,null,2),'utf8');
 console.log(JSON.stringify(output,null,2));if(failures.length)process.exitCode=1;
})().catch(e=>{console.error(e.stack);server.close();process.exitCode=1});
