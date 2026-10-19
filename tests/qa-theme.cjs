const puppeteer=require('puppeteer'),http=require('http'),fs=require('fs'),path=require('path'),assert=require('node:assert/strict');
const root=path.resolve(__dirname,'..');const types={'.html':'text/html','.css':'text/css','.js':'application/javascript','.json':'application/json','.svg':'image/svg+xml'};
const server=http.createServer((req,res)=>{const f=path.resolve(root,'.'+new URL(req.url,'http://localhost').pathname);if(!f.startsWith(root+path.sep)){res.writeHead(403).end();return}fs.readFile(f,(e,b)=>{if(e){res.writeHead(404).end();return}res.writeHead(200,{'Content-Type':types[path.extname(f)]||'application/octet-stream'});res.end(b)})});
(async()=>{
 await new Promise(r=>server.listen(0,'127.0.0.1',r));
 const b=await puppeteer.launch({headless:true,executablePath:'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',args:['--no-sandbox']});
 try{
  const p=await b.newPage();await p.setViewport({width:390,height:844});
  await p.goto('http://127.0.0.1:'+server.address().port+'/itens/O-03.html',{waitUntil:'domcontentloaded'});
  const before=await p.$eval('body',x=>getComputedStyle(x).backgroundColor);
  await p.$eval('#theme',x=>x.click());
  const after=await p.$eval('body',x=>getComputedStyle(x).backgroundColor);
  assert.notEqual(after,before,'dark mode must change background');
  assert(await p.$eval('html',x=>x.classList.contains('dark')));
  console.log(JSON.stringify({darkMode:'PASS',light:before,dark:after,width:390}));
 }finally{await b.close();server.close()}
})().catch(e=>{console.error(e.stack);process.exitCode=1});
