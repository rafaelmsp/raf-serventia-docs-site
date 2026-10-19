/* Catálogo RAF Serventia Docs: navegação estática, sem integração ao PJe. */
'use strict';
const $=s=>document.querySelector(s);
const safe=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const normal=s=>String(s??'').normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase();
const groups={ALL:'Todos',O:'Operações',P:'Pauta e audiências',R:'Relatórios',BF:'Balcão físico',BV:'Balcão virtual',FAV:'Favoritos'};
const params=new URLSearchParams(location.search);
let cat=Object.hasOwn(groups,params.get('tema'))?params.get('tema'):'ALL';
let page=Math.max(1,Math.min(999,Number(params.get('pagina'))||1));
let term='';let records=[];const perPage=7;
function readFav(){try{const a=JSON.parse(localStorage.getItem('raf-serventia-favoritos')||'[]');return new Set(Array.isArray(a)?a:[])}catch{return new Set()}}
let fav=readFav();
function saveFav(){try{localStorage.setItem('raf-serventia-favoritos',JSON.stringify([...fav]))}catch{}}
function switchFav(code){fav.has(code)?fav.delete(code):fav.add(code);saveFav();render()}
function setTheme(mode){document.documentElement.classList.toggle('dark',mode==='dark');try{localStorage.setItem('raf-serventia-theme',mode)}catch{}}
try{if(localStorage.getItem('raf-serventia-theme')==='dark')document.documentElement.classList.add('dark')}catch{}
$('#theme').addEventListener('click',()=>setTheme(document.documentElement.classList.contains('dark')?'light':'dark'));
function setCategory(c){cat=c;page=1;render(true)}
function setPage(n){page=n;render(true);$('#catalogo').scrollIntoView({block:'start',behavior:'instant'})}
function updateUrl(){
 const u=new URL(location.href);
 if(cat==='ALL')u.searchParams.delete('tema');else u.searchParams.set('tema',cat);
 if(page===1)u.searchParams.delete('pagina');else u.searchParams.set('pagina',String(page));
 history.replaceState(null,'',u.pathname+u.search+u.hash);
}
function render(update=false){
 const filtered=records.filter(r=>(cat==='ALL'||r.categoria===cat||(cat==='FAV'&&fav.has(r.codigo)))&&normal([r.codigo,r.titulo,r.categoria_nome,r.pagina,r.buscaTexto||''].join(' ')).includes(normal(term)));
 const n=Math.max(1,Math.ceil(filtered.length/perPage));page=Math.min(page,n);
 const start=(page-1)*perPage;
 $('#counter').textContent=filtered.length+' itens · exibindo '+(filtered.length?start+1:0)+'–'+Math.min(start+perPage,filtered.length);
 $('#empty').hidden=filtered.length>0;
 $('#items').hidden=filtered.length===0;
 $('#items').innerHTML=filtered.slice(start,start+perPage).map(r=>{
   const code=safe(r.codigo),title=safe(r.titulo);
   const href='itens/'+encodeURIComponent(r.codigo)+'.html';
   return '<article class="item-row"><span class="item-code">'+code+'</span><div class="item-name"><a href="'+href+'">'+title+'</a><small>'+safe(r.categoria_nome)+' · pág. '+r.pagina+'</small></div><a class="open-item" href="'+href+'" aria-label="Abrir ficha '+code+'">Abrir →</a><button type="button" class="favorite '+(fav.has(r.codigo)?'is-fav':'')+'" data-fav="'+code+'" aria-pressed="'+fav.has(r.codigo)+'" aria-label="'+(fav.has(r.codigo)?'Remover dos':'Adicionar aos')+' favoritos: '+code+'">'+(fav.has(r.codigo)?'★':'☆')+'</button></article>';
 }).join('');
 $('#pages').hidden=filtered.length===0;
 $('#pages').innerHTML='<button type="button" id="prevPage" '+(page<=1?'disabled':'')+'>← Anterior</button><span>Página '+page+' de '+n+'</span><button type="button" id="nextPage" '+(page>=n?'disabled':'')+'>Próxima →</button>';
 $('#pages #prevPage')?.addEventListener('click',()=>setPage(page-1));
 $('#pages #nextPage')?.addEventListener('click',()=>setPage(page+1));
 $('#items').querySelectorAll('button[data-fav]').forEach(b=>b.addEventListener('click',()=>switchFav(b.dataset.fav)));
 document.querySelectorAll('[data-cat]').forEach(b=>{b.classList.toggle('selected',b.dataset.cat===cat);b.setAttribute('aria-pressed',String(b.dataset.cat===cat))});
 if(update)updateUrl();
}
document.querySelectorAll('[data-cat]').forEach(b=>b.addEventListener('click',()=>setCategory(b.dataset.cat)));
$('#search').addEventListener('input',e=>{term=e.target.value;page=1;render(true)});
$('#reset').addEventListener('click',()=>{$('#search').value='';term='';page=1;render(true);$('#search').focus()});
fetch('dados/procedimentos.json').then(r=>{if(!r.ok)throw Error('HTTP '+r.status);return r.json()}).then(d=>{
 if(!Array.isArray(d)||d.length!==96)throw Error('Catálogo inválido');
 records=d;
 render();
}).catch(e=>{$('#counter').textContent='Falha ao carregar';$('#empty').hidden=false;$('#empty').textContent='Não foi possível carregar o catálogo ('+e.message+'). Abra o projeto com servidor HTTP local.'});
