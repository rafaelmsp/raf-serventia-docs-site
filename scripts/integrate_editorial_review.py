from pathlib import Path
import json,re
r=Path(__file__).resolve().parents[1]
js=r/'assets/js/lesson-engine.js'
s=js.read_text(encoding='utf8')
assert s.count("));if(data.visual_coverage){")==1
s=s.replace("));if(data.visual_coverage){",'''));
 const audit=E('details','edu-review');
 const checked=!!data.editorial_audit;
 audit.append(E('summary','',checked?'Fonte original confrontada — ler ressalvas':'Conferência detalhada da fonte pendente'));
 const auditBody=E('div','edu-review-body');
 if(checked){
  auditBody.append(E('p','',data.editorial_audit.source_observation));
  auditBody.append(E('p','edu-review-risk','Atenção: '+data.editorial_audit.risk_note));
  auditBody.append(E('p','edu-small','A imagem original foi examinada; a aplicação normativa e a autorização operacional ainda dependem de validação.'));
 }else{
  auditBody.append(E('p','', 'Esta página tem texto didático, mas ainda não passou pelo confronto editorial detalhado com o infográfico original.'));
 }
 const auditLink=E('a','source-link','Ver auditoria e estado da fonte ↗');
 auditLink.href='../auditoria-fonte.html';auditBody.append(auditLink);
 audit.append(auditBody);b.append(audit);
 if(data.visual_coverage){''',1)
js.write_text(s,encoding='utf8')
css=r/'assets/css/lesson-ux.css'
with css.open('a',encoding='utf8') as f:
 f.write('''\n/* Auditoria editorial visível na abertura das 96 aulas */\n.edu-review{margin:14px 0;padding:10px 15px;border:1px solid #BDD5E3;border-radius:11px;background:#F0F7FC;color:#285D7D}.edu-review summary{cursor:pointer;min-height:32px;font-size:12px;font-weight:900;line-height:1.5}.edu-review-body{font-size:12px;line-height:1.6;color:#42627A;padding:8px 0 4px}.edu-review-body p{margin:7px 0 11px}.edu-review-risk{background:#FFF3DE;border:1px solid #E8D2A9;color:#6C5029;padding:10px 12px;border-radius:8px}.edu-review-body a{display:inline-flex;min-height:40px;align-items:center}\n''')
homepage=r/'index.html';txt=homepage.read_text(encoding='utf8')
txt=txt.replace('<a href="andamento-pedagogico.html">Acompanhar revisão das aulas ↗</a>','<a href="andamento-pedagogico.html">Acompanhar revisão das aulas ↗</a><a href="auditoria-fonte.html">Auditoria da fonte — 96 aulas ↗</a>')
# Legacy encoding? append using anchor pre-end of section instead if above doesn't match
if 'href="auditoria-fonte.html"' not in txt:
 txt=txt.replace('</section>\n</main><footer>', '<a class="audit-home-link" href="auditoria-fonte.html">Conferir origem, riscos e pendências de cada aula ↗</a></section>\n</main><footer>',1)
homepage.write_text(txt,encoding='utf8')
panel=r/'andamento-pedagogico.html';h=panel.read_text(encoding='utf8')
h=h.replace('A versão V2 ainda não teve publicação confirmada','A V2.4 e a cobertura visual foram publicadas e verificadas no GitHub Pages.')
h=h.replace('96 esquemas conceituais gerados, seis com roteiro autoral; revisão visual individual pendente','96 ilustrações e 96 diagramas premium publicados; análise editorial individual em andamento.')
h=h.replace('Seis roteiros autorais inseridos; testes com estagiários iniciantes e revisão técnica pendentes','96 roteiros de estudo em rascunho; testes com iniciantes e revisão jurídica pendentes.')
# Keep 68% because this batch did not establish normative approvals.
phrase='Confronto visual da fonte: 7 de 96 páginas examinadas; 89 aguardam revisão. Nenhuma aula foi homologada.'
if phrase not in h:
 h=h.replace('<h2>Etapas M00 a M10</h2>', '<div class="status-note"><strong>Conferência editorial da fonte:</strong> 7/96 páginas confrontadas visualmente; 89 pendentes. Nenhum roteiro foi homologado. <a href="auditoria-fonte.html">Abrir painel de auditoria ↗</a></div><h2>Etapas M00 a M10</h2>')
panel.write_text(h,encoding='utf8')
state=r/'data/progresso-pedagogico.json';d=json.loads(state.read_text(encoding='utf8'))
d['source_image_checked']=7;d['source_image_pending']=89;d['approved_lessons']=0
for phase in d['phases']:
 if phase['id']=='M10':phase['evidence']='Produção V2.4 publicada e verificada no Pages; falta homologação final da documentação.'
 if phase['id']=='M02':phase['evidence']='192 SVGs premium publicados; iniciado confronto visual de 7 páginas da fonte.'
state.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf8')
print('AUDIT_PAGE_LINKED',txt.count('auditoria-fonte.html'),'LESSON_PANEL_INSERTED',s.count('edu-review'))
