const http=require('http'),fs=require('fs'),path=require('path'),assert=require('node:assert/strict'),puppeteer=require('puppeteer');
const ROOT=path.resolve(__dirname,'..');
const mime={'.html':'text/html;charset=utf-8','.css':'text/css','.js':'application/javascript','.json':'application/json','.svg':'image/svg+xml','.jpg':'image/jpeg','.pdf':'application/pdf'};
const s=http.createServer((req,res)=>{
 const file=path.resolve(ROOT,'.'+decodeURIComponent(new URL(req.url,'http://localhost').pathname));
 if(!file.startsWith(ROOT+path.sep)){res.writeHead(403).end();return}
 fs.readFile(file,(e,d)=>{if(e){res.writeHead(404).end();return}res.writeHead(200,{'Content-Type':mime[path.extname(file)]||'application/octet-stream'});res.end(d)});
});
(async()=>{
 await new Promise(r=>s.listen(0,'127.0.0.1',r));
 const base='http://127.0.0.1:'+s.address().port;
 const rows=JSON.parse(fs.readFileSync(path.join(ROOT,'dados/procedimentos.json'),'utf8'));
 const browser=await puppeteer.launch({headless:true,executablePath:'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',args:['--no-sandbox']});
 const page=await browser.newPage();await page.setViewport({width:390,height:850});
 const errors=[];page.on('pageerror',e=>errors.push(e.message));
 const failures=[];let done=0;
 try {
  for(const item of rows){
   const response=await page.goto(base+'/itens/'+item.codigo+'.html',{waitUntil:'domcontentloaded',timeout:10000});
   if(!response||response.status()!==200){failures.push(item.codigo+': http');continue}
   const state=await page.evaluate(()=>({
     code:document.body.dataset.code,
     title:document.querySelector('h1')?.textContent,
     panels:document.querySelectorAll('.premium-panel').length,
     overflow:document.documentElement.scrollWidth-innerWidth,
     svg:document.querySelector('.premium-illustration img')?.getAttribute('src'),
     map:document.querySelector('.flow-figure img')?.getAttribute('src'),
     checklist:document.querySelectorAll('.check input').length
   }));
   if(state.code!==item.codigo||state.panels!==5||state.overflow>2||state.checklist<4||!state.svg||!state.map)failures.push(item.codigo+': '+JSON.stringify(state));
   done++;
  }
 }finally{await browser.close();s.close()}
 const report={tested:done,expected:96,errors:errors,failures:failures,view_width:390};
 fs.writeFileSync(path.join(ROOT,'tests','qa-all-96.json'),JSON.stringify(report,null,2),'utf8');
 console.log(JSON.stringify(report,null,2));
 if(done!==96||failures.length||errors.length)process.exitCode=1;
})().catch(e=>{console.error(e.stack);process.exitCode=1});
