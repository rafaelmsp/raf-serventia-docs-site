const puppeteer=require('puppeteer'),http=require('http'),fs=require('fs'),path=require('path'),assert=require('node:assert/strict');
const root=path.resolve(__dirname,'..'),mime={'.html':'text/html','.css':'text/css','.js':'application/javascript','.json':'application/json','.svg':'image/svg+xml','.jpg':'image/jpeg'};
const server=http.createServer((req,res)=>{const f=path.resolve(root,'.'+decodeURIComponent(new URL(req.url,'http://localhost').pathname));if(!f.startsWith(root+path.sep)){res.writeHead(403).end();return}fs.readFile(f,(err,data)=>{if(err){res.writeHead(404).end();return}res.writeHead(200,{'Content-Type':mime[path.extname(f)]||'application/octet-stream'});res.end(data)})});
(async()=>{
 await new Promise(r=>server.listen(0,'127.0.0.1',r));
 const base='http://127.0.0.1:'+server.address().port, browser=await puppeteer.launch({headless:true,executablePath:'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',args:['--no-sandbox']});
 const folder=path.join(root,'tests','v2-screenshots');fs.mkdirSync(folder,{recursive:true});const findings=[];
 try{
  for(const width of [390,1366]){
   const page=await browser.newPage();await page.setViewport({width,height:900});
   const errors=[];page.on('pageerror',e=>errors.push(e.message));
   for(const route of ['index.html','aprender.html','introducao.html','andamento-pedagogico.html']){
    await page.goto(base+'/'+route,{waitUntil:'networkidle0'});
    assert(await page.evaluate(()=>document.documentElement.scrollWidth-innerWidth)<=2,'overflow '+route+' '+width);
    await page.screenshot({path:path.join(folder,route.replace('.html','')+'-'+width+'.png'),fullPage:false});
   }
   await page.goto(base+'/itens/O-03.html',{waitUntil:'networkidle0'});
   await page.evaluate(()=>localStorage.removeItem('raf-learn-v2-O-03'));
   await page.reload({waitUntil:'networkidle0'});
   await page.screenshot({path:path.join(folder,'O-03-welcome-'+width+'.png'),fullPage:false});
   await page.$eval('.control-primary',x=>x.click());await page.$eval('.control-primary',x=>x.click());
   await page.waitForFunction(()=>document.querySelector('.visual-figure img')?.complete&&document.querySelector('.visual-figure img')?.naturalWidth>0);
   await page.screenshot({path:path.join(folder,'O-03-recognize-'+width+'.png'),fullPage:false});
   await page.$eval('.original-compare summary',x=>x.click());
   assert(await page.$eval('.original-compare',x=>x.open));
   assert(await page.evaluate(()=>document.documentElement.scrollWidth-innerWidth)<=2,'overflow O-03 '+width);
   assert.equal(errors.length,0,'JS exceptions');
   findings.push({width,pages:5,errors:0,originalComparison:true});
   await page.close();
  }
 }finally{await browser.close();server.close()}
 console.log(JSON.stringify({passed:findings.length,detail:findings},null,2));
})().catch(e=>{console.error(e.stack);server.close();process.exitCode=1});
