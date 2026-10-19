const puppeteer=require('puppeteer'),assert=require('node:assert/strict'),http=require('http'),fs=require('fs'),path=require('path');
const root=path.resolve(__dirname,'..');const mime={'.html':'text/html;charset=utf-8','.js':'application/javascript','.css':'text/css','.svg':'image/svg+xml','.json':'application/json'};
const server=http.createServer((req,res)=>{const p=path.resolve(root,'.'+decodeURIComponent(new URL(req.url,'http://localhost').pathname));if(!p.startsWith(root+path.sep)){res.writeHead(403).end();return}fs.readFile(p,(e,b)=>{if(e){res.writeHead(404).end();return}res.writeHead(200,{'Content-Type':mime[path.extname(p)]||'application/octet-stream'});res.end(b)})});
(async()=>{
 await new Promise(r=>server.listen(0,'127.0.0.1',r));
 const browser=await puppeteer.launch({headless:true,executablePath:'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',args:['--no-sandbox']});
 const result=[];
 try{
  for(const width of [390,768,1366]){
   const page=await browser.newPage();await page.setViewport({width,height:880});
   for(const uri of ['/index.html','/aprender.html']){
    const response=await page.goto('http://127.0.0.1:'+server.address().port+uri,{waitUntil:'networkidle0'});
    assert.equal(response.status(),200);
    const selector=uri==='/index.html'?'.v2-art-card img':'.lesson-card-visual img';
    const state=await page.evaluate(selector=>({
     count:document.querySelectorAll(selector).length,
     imagesOk:[...document.querySelectorAll(selector)].every(x=>x.complete&&x.naturalWidth>0),
     overflow:document.documentElement.scrollWidth-innerWidth
    }),selector);
    assert.equal(state.count,6);assert(state.imagesOk);assert(state.overflow<=2);
    if(width===390||width===1366)await page.screenshot({path:path.join(root,'tests','premium-visual-shots','gallery-'+width+'-'+uri.slice(1)+'.png'),fullPage:false});
    result.push({uri,width,...state});
   }
   await page.close();
  }
 }finally{await browser.close();server.close()}
 console.log(JSON.stringify({passed:result.length,checks:result},null,2));
 fs.writeFileSync(path.join(root,'tests','gallery-qa.json'),JSON.stringify({passed:result.length,checks:result},null,2));
})().catch(e=>{console.error(e.stack);process.exitCode=1});
