"""Atribui créditos somente às evidências verificáveis da V2."""
from pathlib import Path
import json,datetime,re
root=Path(__file__).resolve().parent.parent
path=root/'data/progresso-pedagogico.json'
state=json.loads(path.read_text(encoding='utf8'))
test=root/'tests/v2-qa.json'
qa=json.loads(test.read_text(encoding='utf8')) if test.exists() else {}
passed=qa.get('pilot_cases')==36 and qa.get('failures')==[] and qa.get('all_lesson_routes')==96
static=True
for code in [x['codigo'] for x in json.loads((root/'dados/procedimentos.json').read_text(encoding='utf8'))]:
 if not (root/'data/lessons'/(code+'.json')).exists() or not (root/'assets/learning'/code/'simulacao.svg').exists():static=False
deploy=root/'data/v2-deploy-verification.json'
published=False
if deploy.exists():
 info=json.loads(deploy.read_text(encoding='utf8'))
 published=info.get('status')=='success' and info.get('online_html')==200 and info.get('online_data')==200
visual_manifest=root/'data/learning-visuals-manifest.json'
visual_qa_file=root/'tests/premium-visual-qa.json'
visual_pack=json.loads(visual_manifest.read_text(encoding='utf8')) if visual_manifest.exists() else []
visual_qa=json.loads(visual_qa_file.read_text(encoding='utf8')) if visual_qa_file.exists() else {}
visuals_ok=len(visual_pack)==6 and all((root/entry['illustration']).exists() and (root/entry['flow']).exists() for entry in visual_pack)
visual_tests_ok=visuals_ok and visual_qa.get('passed')==24 and not visual_qa.get('problems')
credits={'M00':7 if static else 3,'M01':12 if passed else 10,
         'M02':(9 if visuals_ok else 6) if static else 0,'M03':(7 if visual_tests_ok else 6) if passed else 5,
         'M04':0,'M05':0,'M06':0,'M07':0,'M08':0,
         'M09':(3 if visual_tests_ok else 2) if passed else 0,'M10':2 if published else 0}
for phase in state['phases']:phase['credited']=credits[phase['id']]
state['percent']=sum(credits.values())
state['published']=published
state['qa']={'pilot_cases':qa.get('pilot_cases',0),'expected':36,'routes':96 if passed else 0,
              'defects':len(qa.get('failures',[])),'static':static,'premium_visual_cases':visual_qa.get('passed',0)}
state['approved_lessons']=0
state['modified_at']=datetime.datetime.now(datetime.timezone.utc).isoformat()
path.write_text(json.dumps(state,ensure_ascii=False,indent=2),encoding='utf8')
panel=root/'andamento-pedagogico.html'
html=panel.read_text(encoding='utf8')
html=re.sub(r'<h1>\d+% de implementação V2</h1>','<h1>'+str(state['percent'])+'% de implementação V2</h1>',html)
for phase in state['phases']:
 id=phase['id']
 # update numerical credits inside phase card, preserving weight and text
 pat=r'('+id+r' · [^<]+</b><strong>)\d+( / '+str(phase['weight'])+r' pontos</strong>)'
 html=re.sub(pat,lambda m:m.group(1)+str(phase['credited'])+m.group(2),html)
 # <progress max="12" value="10">
html=re.sub(r'<progress max="\d+" value="\d+"></progress>',lambda m:m.group(0),html)
# Rebuild progress tags in sequence using known phase order
iterator=iter(state['phases'])
html=re.sub(r'<progress max="\d+" value="\d+"></progress>',
 lambda m:(lambda p:'<progress max="'+str(p['weight'])+'" value="'+str(p['credited'])+'"></progress>')(next(iterator)),html)
panel.write_text(html,encoding='utf8')
lines=['# RAF Serventia Docs — Progresso Pedagógico V2','','**Percentual técnico evidenciado:** '+str(state['percent'])+'%','',
'**Lições pedagógicas homologadas:** 0/96. **Pilotos autorais em revisão:** 6. **Prévias pendentes:** 90.','',
'| Fase | Pontos creditados | Peso |','|---|---:|---:|']
for p in state['phases']:lines.append('| '+p['id']+' · '+p['name']+' | '+str(p['credited'])+' | '+str(p['weight'])+' |')
lines+=['','## Evidências','',
'- Fonte primária: manual de 107 páginas, edição 15/10/2026.',
'- 96 estruturas de aula, 96 imagens SVG conceituais e 96 cópias técnicas anteriores preservadas.',
'- 6 roteiros pilotos com objetivos, termos, cenas, decisões, exercícios e feedback.',
'- Testes navegador: '+str(state['qa']['pilot_cases'])+'/36 casos com seis pilotos em seis larguras.',
'- Rotas HTML: '+str(state['qa']['routes'])+'/96 verificadas em Android virtual de 390px.',
'- Imagens premium próprias: '+str(len(visual_pack))+' cenas e '+str(len(visual_pack))+' diagramas com fonte vinculada.',
'- Cenários responsivos dos visuais: '+str(visual_qa.get('passed',0))+'/24.',
'- Publicação V2 confirmada: '+('sim' if published else 'não')+'.',
'','## Bloqueios','',
'- Revisão técnica, normativa e pedagógica das seis aulas piloto.',
'- Testes com estudantes iniciantes reais e leitor de tela real.',
'- Revisão detalhada e redação didática das 90 prévias, incluindo OCR.',
'','Este percentual NÃO é aprovação do conteúdo ou autorização para trabalho independente.'
]
(root/'docs/progresso-pedagogico.md').write_text('\n'.join(lines)+'\n',encoding='utf8')
print('PEDAGOGICAL_PROGRESS',state['percent'],'QA',state['qa'],'published',published)
