/* RAF Serventia Docs / premium article. Static Pages, no judicial operations. */
'use strict';
(() => {
 const code=document.body.dataset.code;
 if(!code) return;
 const $=(selector)=>document.querySelector(selector);
 const $$=(selector)=>[...document.querySelectorAll(selector)];
 const tabs=$$('.premium-tabs [role="tab"]');
 const panels=$$('.premium-panel[data-panel]');
 const activate=(name,focus=false)=>{
   tabs.forEach(tab=>{
     const active=tab.dataset.tab===name;
     tab.setAttribute('aria-selected',String(active));
     tab.tabIndex=active?0:-1;
     if(active&&focus)tab.focus();
   });
   panels.forEach(panel=>{panel.hidden=panel.dataset.panel!==name});

 };
 tabs.forEach((tab,i)=>{
   const name=tab.dataset.tab;
   const panel=$('.premium-panel[data-panel="'+name+'"]');
   if(!panel)return;
   const id='tab-'+name;
   tab.id=id;tab.setAttribute('aria-controls',panel.id);
   panel.setAttribute('role','tabpanel');panel.setAttribute('aria-labelledby',id);
   tab.addEventListener('click',()=>activate(name));
   tab.addEventListener('keydown',e=>{
     if(!['ArrowLeft','ArrowRight','Home','End'].includes(e.key))return;
     e.preventDefault();
     const next=e.key==='Home'?0:e.key==='End'?tabs.length-1:(i+(e.key==='ArrowRight'?1:-1)+tabs.length)%tabs.length;
     activate(tabs[next].dataset.tab,true);
   });
 });
 const allowed=new Set(tabs.map(t=>t.dataset.tab));
 activate(allowed.has(location.hash.slice(1))?location.hash.slice(1):'visao');
 window.addEventListener('hashchange',()=>{
   const selected=location.hash.slice(1);
   if(allowed.has(selected))activate(selected);
 });
 const nodeButtons=$$('.node-button[data-index]');
 const nodeTitle=$('#node-title');
 const nodeDesc=$('#node-description');
 const nodeCount=$('#node-count');
 let nodes=[];
 const renderNode=(index)=>{
   const node=nodes[index];
   if(!node)return;
   nodeButtons.forEach(b=>b.setAttribute('aria-pressed',String(Number(b.dataset.index)===index)));
   nodeCount.textContent='ELEMENTO '+(index+1)+' DE '+nodes.length+' · '+code;
   nodeTitle.textContent=node.label;
   nodeDesc.textContent=node.detail;
 };
 nodeButtons.forEach((b,i)=>b.addEventListener('click',()=>renderNode(i)));
 fetch('../data/procedures/'+encodeURIComponent(code)+'.json')
 .then(response=>{if(!response.ok)throw new Error('HTTP '+response.status);return response.json()})
 .then(data=>{
   if(data.code!==code||!Array.isArray(data.nodes))throw new Error('Ficha inconsistente');
   nodes=data.nodes;
   renderNode(0);
 })
 .catch(error=>{
   nodeTitle.textContent='Conteúdo ilustrado disponível acima';
   nodeDesc.textContent='A explicação interativa não pôde ser carregada. As etapas textuais desta página continuam disponíveis.';
 });
 const checkboxes=$$('input[data-check]');
 const key='raf-serventia-leitura-'+code;
 const read=()=>{
   try{return JSON.parse(localStorage.getItem(key)||'[]')}catch{return []}
 };
 const refresh=()=>{
   const completed=checkboxes.filter(c=>c.checked).length;
   const target=$('#checkProgress');
   if(target)target.textContent=completed+' de '+checkboxes.length+' itens de leitura conferidos';
 };
 const saved=read();
 checkboxes.forEach((c,i)=>{c.checked=Array.isArray(saved)&&saved[i]===true;c.addEventListener('change',()=>{
   try{localStorage.setItem(key,JSON.stringify(checkboxes.map(x=>x.checked)))}catch{}
   refresh();
 })});
 $('#clearChecks')?.addEventListener('click',()=>{
   checkboxes.forEach(c=>c.checked=false);
   try{localStorage.removeItem(key)}catch{}
   refresh();
 });
 refresh();
})();
