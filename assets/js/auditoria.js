'use strict';
(()=>{
const qs=s=>document.querySelector(s);
const escape=s=>String(s||'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const normalize=s=>String(s||'').normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase();
const labels={O:'Operações',P:'Pauta',R:'Relatórios',BF:'Balcão físico',BV:'Balcão Virtual'};
const highRisk=new Set(['O-09','O-19','O-25','O-32','O-38','O-39','O-41','O-43','O-45','P-14','P-15','P-16','BF-04','BV-06','BV-07']);
let records=[],term='',section='ALL',filter='ALL',page=1;
const perPage=9;
function makeCard(r){
 const card=document.createElement('article');
 card.className='audit-item'+(highRisk.has(r.code)?' audit-priority':'');
 const title=escape(r.title),code=escape(r.code);
 const state=r.visual_checked?'Fonte confrontada visualmente':'Conferência visual pendente';
 const stateClass=r.visual_checked?'audit-done':'audit-pending';
 card.innerHTML='<div class="audit-item-top"><span class="audit-code">'+code+'</span>'+
   '<div class="audit-item-name"><h3>'+title+'</h3><p>'+escape(labels[r.section])+' · Página '+r.page+' de 107 · '+
   (r.source_method==='camada_textual_pdf'?'Texto nativo':'OCR provisório')+'</p></div>'+
   '<span class="audit-tag '+stateClass+'">'+escape(state)+'</span></div>'+
   '<div class="audit-actions"><a href="itens/'+encodeURIComponent(r.code)+'.html">Estudar aula ↗</a>'+
   '<a href="docs/manual-fonte.pdf#page='+r.page+'" target="_blank" rel="noopener noreferrer">Ver PDF p. '+r.page+' ↗</a></div>';
 if(r.visual_checked){
  const details=document.createElement('details');
  details.className='audit-source-details';
  const summary=document.createElement('summary');summary.textContent='Ver confronto visual e alertas';
  const body=document.createElement('div');body.className='audit-source-body';
  const p=document.createElement('p');const strong=document.createElement('strong');strong.textContent='Consta da fonte: ';p.append(strong,document.createTextNode(r.source_observation));
  const caution=document.createElement('p');caution.className='audit-risk';
  const bold=document.createElement('strong');bold.textContent='Alerta para o roteiro: ';caution.append(bold,document.createTextNode(r.risk_note));
  const foot=document.createElement('p');foot.className='audit-disclaimer';foot.textContent='Confronto visual da página original em 19/10/2026. Não equivale a validar norma, operação ou competência.';
  body.append(p,caution,foot);details.append(summary,body);card.append(details);
 }else{
  const p=document.createElement('p');p.className='audit-unchecked';
  p.textContent='A aula já tem roteiro e imagem. Falta confrontar cuidadosamente o texto com a página original antes de confiar na sequência ensinada.';
  card.append(p);
 }
 return card;
}
function render(){
 const values=records.filter(r=>(section==='ALL'||r.section===section)
  && (filter==='ALL'||(filter==='checked'&&r.visual_checked)||(filter==='pending'&&!r.visual_checked))
  && normalize([r.code,r.title,r.section,r.source_observation,r.risk_note].join(' ')).includes(normalize(term)));
 const pages=Math.max(1,Math.ceil(values.length/perPage));page=Math.min(page,pages);
 const list=qs('#audit-list');list.replaceChildren();
 values.slice((page-1)*perPage,page*perPage).forEach(v=>list.append(makeCard(v)));
 if(values.length===0){const p=document.createElement('p');p.className='audit-empty';p.textContent='Nenhum registro encontrado. Experimente outro termo ou filtro.';list.append(p)}
 qs('#results').textContent=values.length+' de '+records.length+' registros';
 qs('#audit-page').textContent='Página '+page+' de '+pages;
 qs('#audit-prev').disabled=page<=1||values.length===0;
 qs('#audit-next').disabled=page>=pages;
}
qs('#audit-search').addEventListener('input',e=>{term=e.target.value;page=1;render()});
qs('#audit-section').addEventListener('change',e=>{section=e.target.value;page=1;render()});
qs('#audit-filter').addEventListener('change',e=>{filter=e.target.value;page=1;render()});
qs('#audit-prev').addEventListener('click',()=>{page--;render();qs('.audit-panel-head').scrollIntoView({behavior:'instant',block:'start'})});
qs('#audit-next').addEventListener('click',()=>{page++;render();qs('.audit-panel-head').scrollIntoView({behavior:'instant',block:'start'})});
fetch('data/editorial-audit.json',{cache:'no-store'}).then(r=>{if(!r.ok)throw Error('HTTP '+r.status);return r.json()}).then(d=>{
 if(!Array.isArray(d)||d.length!==96)throw Error('Dados incompletos da auditoria');
 records=d;qs('#total').textContent=String(records.length);
 qs('#checked').textContent=String(records.filter(r=>r.visual_checked).length);
 qs('#pending').textContent=String(records.filter(r=>!r.visual_checked).length);
 render();
}).catch(e=>{qs('#audit-list').textContent='Não foi possível carregar a auditoria: '+e.message;qs('#results').textContent='Erro de carregamento'});
})();
