'use strict';
const shortNames={
 fichas_html:'Fichas em HTML',novas_ilustracoes_svg:'Ilustrações SVG novas',
 novos_mapas_svg:'Mapas SVG',paginas_fonte_html:'Páginas-fonte',
 fichas_editorialmente_aprovadas:'Fichas com revisão editorial',
 pilotos_parcialmente_conferidos:'Pilotos parcialmente conferidos',
 testes_navegador_aprovados:'Testes interativos aprovados',
 rotas_verificadas_android:'Rotas verificadas no Android',
 deploy_premium_confirmado:'Deploy Pages confirmado'
};
const phaseNames={
 F00:'Auditoria',F01:'Sistema visual',F02:'Revisão do conteúdo',
 F03:'Ilustrações e mapas',F04:'Operações (O)',F05:'Pauta (P)',
 F06:'Relatórios (R)',F07:'Balcão físico (BF)',F08:'Balcão virtual (BV)',
 F09:'Integração',F10:'Testes e segurança',F11:'Publicação'
};
function element(tag,className,text){
 const e=document.createElement(tag);
 if(className)e.className=className;
 if(text!==undefined)e.textContent=String(text);
 return e;
}
fetch('data/progress.json').then(r=>{
 if(!r.ok)throw Error('Não foi possível carregar os dados: HTTP '+r.status);
 return r.json();
}).then(d=>{
 const pct=Number(d.global_percent)||0;
 document.getElementById('global').textContent=pct.toLocaleString('pt-BR',{minimumFractionDigits:1})+'%';
 document.getElementById('global-bar').style.width=Math.max(0,Math.min(100,pct))+'%';
 const metrics=document.getElementById('metrics');
 Object.entries(d.metrics).forEach(([k,v])=>{
   const box=element('div','metric');
   box.append(element('strong','',typeof v==='boolean'?(v?'Sim':'Não'):v));
   box.append(element('span','',shortNames[k]||k));
   metrics.append(box);
 });
 const container=document.getElementById('phase-list');
 Object.entries(d.phases).sort((a,b)=>a[0].localeCompare(b[0])).forEach(([key,phase])=>{
   const box=element('article','phase');
   const head=element('div','phase-head');
   head.append(element('span','',key+' · '+(phaseNames[key]||key)));
   head.append(element('span','',Number(phase.phase_percent).toLocaleString('pt-BR')+'%'));
   box.append(head);
   const track=element('div','track');
   const bar=element('span');bar.style.width=Math.min(100,Math.max(0,Number(phase.phase_percent)))+'%';
   track.append(bar);box.append(track);
   box.append(element('p','',phase.notes));
   container.append(box);
 });
}).catch(err=>{
 document.getElementById('global').textContent='Dados indisponíveis';
 document.getElementById('phase-list').textContent=err.message;
});
