from pathlib import Path
import json,re,datetime
r=Path(__file__).resolve().parent.parent
idx=json.loads((r/'dados/procedimentos.json').read_text(encoding='utf8'))
a=[json.loads((r/'data/lessons'/(x['codigo']+'.json')).read_text(encoding='utf8')) for x in idx]
assert len(a)==96 and all(v['state']=='author_draft' and not v['technical_approved'] for v in a)
q=r/'data/lessons-index.json';meta=json.loads(q.read_text(encoding='utf8'))
meta.update(authored_lessons=96,needs_source_review=0,preview_count=0,approved=0,
  content_status='all_authored_drafts_source_review_pending')
meta['notes']='96 roteiros ilustrados escritos como rascunhos didáticos; 53 dependem de interpretação de fonte OCR e 43 receberam roteiro escrito a partir de texto nativo ou dos seis pilotos. Zero homologação.'
q.write_text(json.dumps(meta,ensure_ascii=False,indent=2),encoding='utf8')
p=r/'data/progresso-pedagogico.json';d=json.loads(p.read_text(encoding='utf8'))
credits={'M00':7,'M01':12,'M02':11,'M03':10,'M04':10,'M05':4,'M06':2,'M07':3,'M08':3,'M09':4,'M10':2}
for x in d['phases']:
 x['credited']=credits[x['id']]
 if x['id']=='M03':x['evidence']='96 roteiros de estudo específicos redigidos; revisão humana, testes com iniciantes e aprovação jurídica ainda pendentes.'
 if x['id']=='M04':x['evidence']='49/49 rascunhos de Operações com passos de estudo; conferência dos textos OCR e normas ainda necessária.'
 if x['id']=='M05':x['evidence']='16/16 rascunhos ilustrados de Pauta; regras locais e procedimentos precisam ser validados.'
 if x['id']=='M06':x['evidence']='5/5 rascunhos ilustrados de Relatórios, com fonte e exemplos de leitura.'
 if x['id']=='M07':x['evidence']='12/12 rascunhos de Balcão Físico; fluxos internos sujeitos a confirmação.'
 if x['id']=='M08':x['evidence']='14/14 rascunhos de Balcão Virtual; atos normativos e interface atual devem ser conferidos.'
d['percent']=sum(credits.values());d['authored_lessons']=96;d['unreviewed_previews']=0
d['editorial_review_pending']=96;d['approved_lessons']=0
d['version']='v2.4-full-teaching-draft';d['modified_at']=datetime.datetime.now(datetime.timezone.utc).isoformat()
p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf8')
p=r/'andamento-pedagogico.html';html=p.read_text(encoding='utf8')
html=re.sub(r'\d+% de implementação V2',str(d['percent'])+'% de implementação V2',html)
html=re.sub(r'Há \d+ roteiros específicos em revisão e \d+ prévias;', 'Há 96 roteiros específicos em revisão e nenhuma prévia sem conteúdo;',html)
for x in d['phases']:
 pat=r'('+x['id']+r' · [^<]+</b><strong>)\d+( / '+str(x['weight'])+r' pontos</strong>)'
 html=re.sub(pat,lambda m:m.group(1)+str(x['credited'])+m.group(2),html)
iterator=iter(d['phases'])
html=re.sub(r'<progress max="\d+" value="\d+"></progress>',lambda m:(lambda o:f'<progress max="{o["weight"]}" value="{o["credited"]}"></progress>')(next(iterator)),html)
p.write_text(html,encoding='utf8')
p=r/'index.html';html=p.read_text(encoding='utf8')
html=html.replace('6 aulas piloto · 90 prévias ainda em revisão','6 aulas em destaque · 96 roteiros em revisão')
p.write_text(html,encoding='utf8')
p=r/'aprender.html';html=p.read_text(encoding='utf8')
html=html.replace('incluindo 90 prévias que aguardam explicações operacionais revisadas','incluindo 96 roteiros didáticos ainda sujeitos a conferência')
p.write_text(html,encoding='utf8')
p=r/'README.md';s=p.read_text(encoding='utf8')
s=re.sub(r'Quarenta e três roteiros foram escritos especificamente[^.]+\.','Os 96 roteiros foram escritos para as respectivas fichas como rascunhos de aprendizagem, dos quais 53 dependem de interpretação de OCR.',s)
s=s.replace('As outras 53 fichas são prévias de estudo','Todas as 96 fichas têm roteiro de estudo e arte própria, ainda aguardando revisão humana')
p.write_text(s,encoding='utf8')
p=r/'docs/progresso-pedagogico.md'
lines=['# RAF Serventia Docs V2.4 — Acompanhamento auditável','',
f'**Implementação técnica e editorial preliminar:** {d["percent"]}%. **Homologação das aulas:** 0/96.','',
'**96/96 aulas com texto próprio e sete telas de aprendizagem.**',
'**96/96 ilustrações premium e 96/96 diagramas SVG.**',
'**53 aulas dependeram da interpretação didática de páginas OCR**, exigindo conferência da imagem original.',
'**43 aulas têm base em texto nativo ou pilotos trabalhados previamente**, ainda sem homologação.','',
'## Créditos por fase','',
'| Fase | Entrega | Crédito | Peso |','|---|---|---:|---:|']
for x in d['phases']:lines.append(f"| {x['id']} | {x['evidence']} | {x['credited']} | {x['weight']} |")
lines+=['','## Limitações que impedem 100%','',
'1. Leitura e revisão jurídico-editorial individual das 96 aulas, com prioridade para 53 páginas dependentes de OCR.',
'2. Verificação de normas vigentes e dos perfis/permissões da unidade.',
'3. Testes observados de compreensão com estagiários iniciantes.',
'4. Auditoria real de acessibilidade e revisão de fluxos em dispositivo móvel.',
'5. Aprovação institucional não solicitada nem presumida.','',
'Os SVGs são simulações fictícias. Nenhum material autoriza atos judiciais autônomos.']
p.write_text('\n'.join(lines)+'\n',encoding='utf8')
print('FINAL_DRAFT_PROGRESS',d['percent'],'ALL_AUTHORED',len(a),'APPROVED',d['approved_lessons'])
