'use strict';
(()=>{
const code=document.body.dataset.code;if(!code)return;
const app=document.getElementById('lesson-app'), loading=document.getElementById('lesson-loading');
const key='raf-learn-v2-'+code;
let data=null,step=0,region=0,answers={decision:null,practice:null},checks=[];
try{const s=JSON.parse(localStorage.getItem(key)||'{}');step=Math.max(0,Math.min(6,s.step||0));answers=s.answers||answers;checks=s.checks||[]}catch{}
const E=(tag,cls,text)=>{const e=document.createElement(tag);if(cls)e.className=cls;if(text!==undefined)e.textContent=String(text);return e};
const add=(parent,...children)=>{children.forEach(x=>parent.append(x));return parent};
const persist=()=>{try{localStorage.setItem(key,JSON.stringify({step,answers,checks}))}catch{}};
const box=(title,subtitle)=>{const b=E('section','edu-card');add(b,E('h2','edu-title',title),E('p','edu-muted',subtitle));return b};
const sequence=(values,fn)=>{const list=E('div','edu-stack');values.forEach((v,i)=>list.append(fn(v,i)));return list};
function visualFigure(kind,title) {
 const codePart=data.code;
 const asset=kind==='scene'?'ilustracao-premium.svg':'fluxo-premium.svg';
 const src='../assets/learning/'+codePart+'/'+asset;
 const outer=E('figure',kind==='scene'?'edu-visual premium-scene':'edu-visual premium-diagram');
 const top=E('div','edu-visual-bar');
 top.append(E('strong','',title));
 const link=E('a','edu-zoom-link','Ampliar imagem ↗');link.href=src;link.target='_blank';link.rel='noopener noreferrer';
 top.append(link);
 const viewport=E('div','edu-visual-viewport');
 viewport.tabIndex=0;
 viewport.setAttribute('role','region');
 viewport.setAttribute('aria-label','Ilustração de estudo, com rolagem horizontal no celular');
 const picture=E('img');
 picture.src=src;
 picture.alt=(kind==='scene'?'Cena ilustrada: ':'Diagrama: ')+data.title+'. Material simulado, não é interface oficial.';
 picture.loading='lazy';picture.decoding='async';
 viewport.append(picture);
 outer.append(top,viewport);
 outer.append(E('figcaption','edu-visual-caption','↔ No celular, deslize o desenho para os lados ou toque em Ampliar imagem. SIMULAÇÃO · dados fictícios.'));
 return outer;
}
function welcome(){
 const b=box('O que você vai aprender?','Você não precisa conhecer previamente o PJe.');
 add(b,E('p','welcome-objective',data.objective),E('p','edu-readable',data.plain),
 E('div','edu-notice',data.is_pilot?'Aula piloto em revisão. Os exemplos são fictícios.':'Prévia de estudo: ainda não há procedimento operacional revisado nesta ficha.'),
 E('p','edu-small','Fonte: página '+data.page+' do manual de 15/10/2026.'));if(data.is_pilot){ b.append(visualFigure('scene','Prévia ilustrada da lição'));const go=E('button','preview-action','Explorar imagem e elementos →');go.type='button';go.addEventListener('click',()=>move(2));b.append(go); }return b;
}
function understand(){
 const b=box('Entender sem complicação','Abra cada expressão para conhecer o significado e um exemplo.');
 b.append(sequence(data.terms,(t,i)=>{const d=E('details','term-card');
 add(d,E('summary','',t.term));const body=E('div','term-detail');
 add(body,E('p','',t.meaning),E('p','edu-example','Exemplo: '+t.example));d.append(body);if(i===0)d.open=true;return d}));return b;
}
function recognize(){
 const b=box('Reconhecer na prática','Uma ilustração conceitual. Não é captura do PJe nem interface oficial.');
 const fig=E('figure','visual-figure'),img=E('img');img.src='../assets/learning/'+code+'/simulacao.svg';
 img.alt=data.scene.alt;img.loading='lazy';
 if(data.is_pilot){b.append(visualFigure('scene','Explore os elementos da cena'));}else{add(fig,img,E('figcaption','',data.scene.title+' · simulação didática'));b.append(fig);}
 const original=E('details','original-compare');
 const picture=E('img');picture.src=data.source_image;picture.loading='lazy';
 picture.alt='Infográfico original da página '+data.page;
 add(original,E('summary','','Comparar com o infográfico original'),picture,
 E('p','edu-small','A imagem original permite conferir o que a simulação simplificou.'));
 b.append(original);
 const controls=E('div','hotspot-grid');
 data.scene.regions.forEach((h,i)=>{
 const bt=E('button','hotspot-btn'+(region===i?' chosen':''),(i+1)+' · '+h.title);
 bt.type='button';bt.setAttribute('aria-pressed',String(region===i));
 bt.addEventListener('click',()=>{region=i;render()});controls.append(bt);
 });b.append(controls);
 const desc=E('div','hotspot-explain');desc.setAttribute('role','status');
 add(desc,E('strong','',data.scene.regions[region].title),E('p','',data.scene.regions[region].detail));
 b.append(desc);return b;
}
function observe(){
 const b=box('O que preciso observar?','Conferir é compreender a fonte, não presumir o resultado.');
 b.append(sequence(data.observe,(o,i)=>{const x=E('article','coach-item');
 const body=E('div');add(body,E('h3','',o.title),E('p','',o.detail));
 return add(x,E('span','coach-number',i+1),body)}));
 b.append(E('p','edu-notice','Antes de uma providência real, confira os documentos, as regras e os limites de atuação.'));return b;
}
function doWithHelp(){
 const b=box('Observar e fazer com supervisão','Passos de leitura orientada, sem execução de atos pelo portal.');
 if(!data.steps.length){
   b.append(E('p','edu-warning','A sequência operacional ainda não foi validada. Não é seguro transformar OCR em comandos do sistema.'));
   const a=E('a','source-link','Conferir página original ↗');a.href=data.pdf;a.target='_blank';a.rel='noopener noreferrer';b.append(a);return b;
 }
 if(data.is_pilot)b.append(visualFigure('diagram','Mapa visual da sequência de conferência'));b.append(sequence(data.steps,(s,i)=>{const x=E('article','coach-item'),body=E('div');
 add(body,E('h3','',s.title),E('p','',s.instruction));
 const d=E('details','why-detail');add(d,E('summary','','Por que isso importa?'),E('p','',s.why));body.append(d);
 return add(x,E('span','coach-number',i+1),body)}));
 b.append(E('p','edu-warning','Na dúvida, solicite supervisão. A aula não autoriza expedir atos, alterar pautas ou acessar autos restritos.'));return b;
}
function question(q,type){
 const area=E('div','quiz-options');add(area,E('h3','quiz-question',q.question));
 q.options.forEach((o,i)=>{
 const bt=E('button','quiz-option'+(answers[type]===i?' selected':''),o.label);
 bt.type='button';bt.setAttribute('aria-pressed',String(answers[type]===i));
 bt.addEventListener('click',()=>{answers[type]=i;persist();render()});area.append(bt);
 });
 const picked=answers[type];
 if(Number.isInteger(picked)&&q.options[picked]){
  const o=q.options[picked];
  const f=E('div','quiz-feedback '+(o.correct?'correct':'retry'));
  f.setAttribute('role','status');add(f,E('strong','',o.correct?'Boa análise!':'Reveja o raciocínio.'),E('p','',o.feedback));
  area.append(f);
 }return area;
}
function decide(){
 const b=box('E se acontecer isto?','Escolha uma resposta e entenda o motivo.');
 b.append(question(data.decision,'decision'));
 const d=E('details','mistakes');d.append(E('summary','','Erros comuns e o que fazer em vez disso'));
 data.mistakes.forEach(m=>{const p=E('p');add(p,E('strong','',m.mistake+': '),document.createTextNode(m.correct));d.append(p)});
 b.append(d);return b;
}
function practice(){
 const b=box('Praticar e concluir','Caso fictício. Este exercício avalia raciocínio, não atuação em processo real.');
 add(b,E('blockquote','case-story',data.practice.scenario),question(data.practice,'practice'));
 b.append(E('h3','competence-title','Consegui compreender estes pontos?'));
 const list=E('div','competence-list');
 data.mastery.forEach((v,i)=>{
 const label=E('label','mastery-item'),input=E('input');input.type='checkbox';input.checked=!!checks[i];
 input.addEventListener('change',()=>{checks[i]=input.checked;persist();updateResult()});
 add(label,input,E('span','',v));list.append(label);
 });b.append(list);
 const result=E('p','mastery-result');result.id='mastery-result';result.setAttribute('aria-live','polite');b.append(result);
 const links=E('div','source-row');
 const pdf=E('a','source-link','Ver infográfico original ↗');pdf.href=data.pdf;pdf.target='_blank';pdf.rel='noopener noreferrer';
 const tech=E('a','source-link','Consulta técnica anterior →');tech.href=data.archive;
 add(links,pdf,tech);
 const path=['O-03','BF-01','O-08','P-01','R-01','BV-01'];
 const pos=path.indexOf(code);
 if(pos>=0&&pos<path.length-1){
   const nextLesson=E('a','source-link','Próxima lição da trilha →');
   nextLesson.href='../itens/'+path[pos+1]+'.html';links.append(nextLesson);
 }
 b.append(links);Promise.resolve().then(updateResult);return b;
}
function updateResult(){
 const out=document.getElementById('mastery-result');if(!out)return;
 const correct=['decision','practice'].every(t=>Number.isInteger(answers[t])&&data[t].options[answers[t]]?.correct);
 const tick=data.mastery.every((_,i)=>checks[i]===true);
 const done=data.is_pilot&&correct&&tick;
 out.textContent=!data.is_pilot?'Prévia em revisão. Não há certificação de aprendizagem nesta ficha.':
 done?'Compreensão demonstrada nestas simulações. Isso não autoriza trabalhar sem supervisão.':
 'Responda corretamente aos dois desafios e confira a lista de competências para concluir o treino.';
 out.classList.toggle('mastery-ok',done);
}
function move(next){
 step=Math.max(0,Math.min(6,next));persist();render();
 document.querySelector('.lesson-meter')?.scrollIntoView({block:'start',behavior:'instant'});
}
function render(){
 if(!data)return;app.replaceChildren();
 const hero=E('section','lesson-hero');hero.style.setProperty('--accent',data.color);
 add(hero,E('span','hero-kicker',data.code+'  ·  '+data.section_name),
 E('h1','',data.title),E('p','',data.is_pilot?'Aprenda com imagens, exemplos e escolhas comentadas.':'Prévia de estudo — roteiro específico pendente de revisão.'),
 E('span','editorial-chip',data.is_pilot?'AULA PILOTO EM REVISÃO':'PRÉVIA NÃO REVISADA'));app.append(hero);
 const bar=E('div','lesson-meter'),track=E('div','meter-track'),fill=E('div','meter-fill');
 fill.style.width=((step+1)/7*100)+'%';track.append(fill);
 add(bar,E('div','meter-head','Etapa '+(step+1)+' de 7 · '+['Começar','Entender','Reconhecer','Observar','Fazer','Decidir','Praticar'][step]),track);
 app.append(bar);
 const views=[welcome,understand,recognize,observe,doWithHelp,decide,practice];
 app.append(views[step]());
 const controls=E('div','lesson-controls'),prev=E('button','control-secondary','← Anterior'),
 next=E('button','control-primary',step===6?'Rever a aula':'Próxima etapa →');
 prev.type=next.type='button';prev.disabled=step===0;prev.addEventListener('click',()=>move(step-1));
 next.addEventListener('click',()=>move(step===6?0:step+1));
 add(controls,prev,E('span','control-status',(step+1)+' / 7'),next);app.append(controls);
 const foot=E('aside','source-footnote');
 const pdf=E('a','','Abrir fonte original ↗');pdf.href=data.pdf;pdf.target='_blank';pdf.rel='noopener noreferrer';
 add(foot,E('strong','','Fonte: '),document.createTextNode('manual de 15/10/2026, pág. '+data.page+'. Material não oficial e não homologado. '),pdf);
 app.append(foot);
}
fetch('../data/lessons/'+encodeURIComponent(code)+'.json').then(r=>{if(!r.ok)throw Error('HTTP '+r.status);return r.json()}).then(d=>{
 if(d.code!==code||!Array.isArray(d.terms)||!d.practice)throw Error('Estrutura não reconhecida');
 data=d;loading.hidden=true;app.hidden=false;render();
}).catch(e=>{
 loading.textContent='Não foi possível abrir a lição: '+e.message+'. ';
 const a=E('a','source-link','Consultar documentação técnica anterior →');a.href='../arquivo-tecnico/'+code+'.html';loading.append(a);
});
})();