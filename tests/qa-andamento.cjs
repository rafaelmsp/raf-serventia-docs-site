const puppeteer=require('puppeteer'),http=require('http'),fs=require('fs'),path=require('path'),assert=require('node:assert/strict');
const root=path.resolve(__dirname,'..');const mime={'.html':'text/html','.css':'text/css','.js':'application/javascript','.json':'application/json'};
const s=http.createServer((req,res)=>{const f=path.resolve(root,'.'+new URL(req.url,'http://localhost').pathname);if(!f.startsWith(root+path.sep)){res.writeHead(403).end();return}fs.readFile(f,(e,d)=>{if(e){res.writeHead(404).end();return}res.writeHead(200,{'Content-Type':mime[path.extname(f)]||'application/octet-stream'});res.end(d)})});
(async()=>{
 await new Promise(r=>s.listen(0,'127.0.0.1',r));
 const browser=await puppeteer.launch({headless:true,executablePath:'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',args:['--no-sandbox']});
 try{
   const p=await browser.newPage();
   for(const width of [390,1366]){
     await p.setViewport({width,height:850});
     await p.goto('http://127.0.0.1:'+s.address().port+'/andamento.html',{waitUntil:'domcontentloaded'});
     await p.waitForFunction(()=>document.querySelector('.phase')&&document.querySelectorAll('.phase').length===12);
     const d=await p.evaluate(()=>({pct:document.querySelector('#global').textContent,phases:document.querySelectorAll('.phase').length,overflow:document.documentElement.scrollWidth-innerWidth,metrics:document.querySelectorAll('.metric').length}));
     assert.equal(d.phases,12);assert(d.pct.includes('53,5'));assert(d.overflow<=2);
     await p.screenshot({path:path.join(root,'tests','screenshots','andamento-'+width+'.png'),fullPage:true});
     console.log('PASS',width,JSON.stringify(d));
   }
 }finally{await browser.close();s.close()}
})().catch(e=>{console.error(e.stack);process.exitCode=1});
