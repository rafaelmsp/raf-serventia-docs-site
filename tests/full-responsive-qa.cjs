const puppeteer=require('puppeteer'),assert=require('node:assert/strict'),fs=require('fs'),path=require('path'),http=require('http');
const root=path.resolve(__dirname,'..');const mim={'.html':'text/html','.css':'text/css','.js':'application/javascript','.json':'application/json','.svg':'image/svg+xml'};
const server=http.createServer((req,res)=>{const f=path.resolve(root,'.'+decodeURIComponent(new URL(req.url,'http://localhost').pathname));if(!f.startsWith(root+path.sep)){res.writeHead(403).end();return}fs.readFile(f,(e,d)=>{if(e){res.writeHead(404).end();return}res.writeHead(200,{'Content-Type':mim[path.extname(f)]||'application/octet-stream'});res.end(d)})});
(async()=>{
 await new Promise(done=>server.listen(0,'127.0.0.1',done));
 const b=await puppeteer.launch({headless:true,executablePath:'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',args:['--no-sandbox']});
 const result=[],dir=path.join(root,'tests','full-visual-screenshots');fs.mkdirSync(dir,{recursive:true});
 try{
  for(const width of [360,390,768,1366]){
   const page=await b.newPage();await page.setViewport({width,height:900});
   for(const code of ['O-25','O-39','P-09','R-05','BF-04','BV-12']){
    await page.goto('http://127.0.0.1:'+server.address().port+'/itens/'+code+'.html',{waitUntil:'domcontentloaded'});
    await page.evaluate(c=>localStorage.removeItem('raf-learn-v2-'+c),code);
    await page.reload({waitUntil:'domcontentloaded'});
    await page.waitForFunction(()=>!document.getElementById('lesson-app').hidden);
    await page.$eval('.preview-action',x=>x.click());
    await page.waitForFunction(()=>document.querySelector('.premium-scene img')?.naturalWidth>0,{timeout:15000});
    const obj=await page.evaluate(()=>({
     over:document.documentElement.scrollWidth-innerWidth,scene:document.querySelector('.premium-scene img').naturalWidth,
     notes:document.querySelectorAll('.hotspot-btn').length,
     title:document.querySelector('.lesson-hero h1').textContent
    }));
    assert(obj.over<=2);assert(obj.scene>0);assert(obj.notes>=4);
    if(width===390||width===1366){await page.$eval('.edu-visual',el=>el.scrollIntoView({block:'start'}));await page.screenshot({path:path.join(dir,code+'-'+width+'.png'),fullPage:false})}
    result.push({width,code,...obj});
   }
   await page.close();
  }
 }finally{await b.close();server.close()}
 console.log(JSON.stringify({passed:result.length,failures:0,samples:result.filter(x=>x.width===390)},null,2));
 fs.writeFileSync(path.join(root,'tests','full-responsive-qa.json'),JSON.stringify({passed:result.length,failures:0,results:result},null,2));
})().catch(e=>{console.error(e.stack);process.exitCode=1});
