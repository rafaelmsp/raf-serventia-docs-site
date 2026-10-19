from pathlib import Path
import json,re,datetime
r=Path(__file__).resolve().parents[1]
i=json.loads((r/'dados/procedimentos.json').read_text(encoding='utf8'))
qa=json.loads((r/'tests/full-visual-qa.json').read_text(encoding='utf8'))
manifest=json.loads((r/'data/learning-visuals-manifest.json').read_text(encoding='utf8'))
assert len(i)==len(manifest)==96
assert qa.get('pages_passed')==qa.get('scenes_loaded')==qa.get('diagrams_loaded')==96 and qa.get('failed')==0
authored=[x for x in i if json.loads((r/'data/lessons'/(x['codigo']+'.json')).read_text(encoding='utf8'))['state']=='author_draft']
assert len(authored)==14
for ent in manifest:
 assert (r/ent['illustration']).exists() and (r/ent['flow']).exists()
p=r/'data/progresso-pedagogico.json'
d=json.loads(p.read_text(encoding='utf8'))
credits={'M00':7,'M01':12,'M02':11,'M03':8,'M04':2,'M05':0,'M06':0,'M07':0,'M08':0,'M09':4,'M10':2}
# M02 retains 1 point for human visual scrutiny, M03 retains 7 for student and legal validation.
for part in d['phases']:
 part['credited']=credits[part['id']]
 if part['id']=='M02':part['evidence']='96 ilustrações e 96 mapas premium com testes de carregamento; revisão artística e pedagógica individual pendente.'
 if part['id']=='M03':part['evidence']='Seis pilotos e oito roteiros adicionais redigidos; revisão jurídico-pedagógica e teste com iniciantes pendentes.'
 if part['id']=='M04':part['evidence']='10 de 49 fichas de Operações com roteiro específico ainda em revisão; demais prévias possuem conteúdo visual.'
 if part['id']=='M09':part['evidence']='96/96 rotas e 192/192 SVGs carregados no navegador; faltam validação de conteúdo e leitor de tela.'
 if part['id']=='M10':part['evidence']='V2 anterior publicada, atualização visual completa aguardando novo deploy.'
d['percent']=sum(credits.values())
d['authored_lessons']=14;d['authored_pilots']=6;d['unreviewed_previews']=82
d['images_with_premium_coverage']=96;d['diagrams_with_premium_coverage']=96
d['approved_lessons']=0;d['version']='v2.2-premium-draft'
d['qa']['full_visual_pages']=96
d['qa']['full_visual_scenes']=96
d['qa']['full_visual_diagrams']=96
d['qa']['full_visual_failures']=0
d['modified_at']=datetime.datetime.now(datetime.timezone.utc).isoformat()
p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf8')
lp=r/'data/lessons-index.json'
ld=json.loads(lp.read_text(encoding='utf8'))
ld['authored_lessons']=14
ld['needs_source_review']=82
ld['approved']=0
ld['preview_count']=82
ld['full_visual_coverage']=96
ld['premium_diagrams']=96
ld['notes']='192 imagens SVG premium em 96 páginas; 14 roteiros autorais em revisão; 82 leituras provisórias, não homologadas.'
lp.write_text(json.dumps(ld,ensure_ascii=False,indent=2),encoding='utf8')
panel=r/'andamento-pedagogico.html'
text=panel.read_text(encoding='utf8')
text=re.sub(r'\d+% de implementação V2',str(d['percent'])+'% de implementação V2',text)
text=text.replace('Há 6 pilotos escritos e 90 prévias ainda pendentes de conteúdo validado.',
 'Há 14 roteiros específicos em revisão e 82 prévias; as 96 páginas têm ilustrações e mapas. Nenhuma aula foi homologada.')
for phase in d['phases']:
 num=phase['id']
 pat=r'('+num+r' · [^<]*</b><strong>)\d+( / '+str(phase['weight'])+r' pontos</strong>)'
 text=re.sub(pat,lambda m:m.group(1)+str(phase['credited'])+m.group(2),text)
parts=iter(d['phases'])
text=re.sub(r'<progress max="\d+" value="\d+"></progress>',
 lambda m:(lambda a:f'<progress max="{a["weight"]}" value="{a["credited"]}"></progress>')(next(parts)),text)
panel.write_text(text,encoding='utf8')
lines=['# RAF Serventia Docs V2 — Progresso verificável','',
f'**Implementação ponderada:** {d["percent"]}% — não representa homologação nem competência comprovada.','',
'**Cobertura visual:** 96/96 cenas SVG e 96/96 diagramas SVG.','**Roteiros autorais em revisão:** 14/96.','**Prévias ainda não revisadas:** 82/96.','**Lições homologadas:** 0/96.','',
'## Etapas','',
'| Fase | Pontos | Peso | Evidência |','|---|---:|---:|---|']
for a in d['phases']:lines.append(f"| {a['id']} | {a['credited']} | {a['weight']} | {a['evidence']} |")
lines+=['','## Testes','',
'- 96/96 rotas abertas no Chromium a 390 px.',
'- 96/96 cenas premium carregadas, 96/96 diagramas premium carregados.',
'- 96 hotspots e navegações de estudo disponíveis; testes automatizados não validam interpretação jurídica.',
'- Os itens dependentes de OCR continuam com referência visual para conferência.',
'','## Bloqueios','',
'- Revisão editorial e jurídica específica das 82 prévias restantes.',
'- Conferência técnica dos 14 roteiros autorais e eventual atualização das normas.',
'- Testes com estagiários iniciantes, tecnologia assistiva e dispositivo físico.',
'','O website não executa atos processuais. As ilustrações são fictícias e independentes, não reproduções oficiais do PJe.']
(r/'docs/progresso-pedagogico.md').write_text('\n'.join(lines)+'\n',encoding='utf8')
print('PROGRESS_REFRESHED',d['percent'],'AUTHORED',len(authored),'VISUAL',d['images_with_premium_coverage'])
