from pathlib import Path
import json,math,datetime
r=Path(__file__).resolve().parent.parent
items=json.loads((r/'dados/procedimentos.json').read_text(encoding='utf-8'))
audit=json.loads((r/'data/editorial-audit.json').read_text(encoding='utf-8'))
test=r/'tests/qa-premium.json'
qa=json.loads(test.read_text(encoding='utf-8')) if test.exists() else {}
pilots={x['code'] for x in audit if x['source_checked_pilot']}
tested={'O-03','O-08','BF-01','BV-01','P-01','R-01'} if qa.get('passed')==42 and not qa.get('errors') else set()
weights={'F00':8,'F01':10,'F02':9,'F03':8,'F04':20,'F05':9,'F06':5,'F07':7,'F08':8,'F09':6,'F10':7,'F11':3}
assert sum(weights.values())==100
phases={
'F00':(5,7,'Auditoria de fonte, rotas e versões; privacidade editorial complementar pendente'),
'F01':(6,7,'Design system, layout, abas, tema, impressão, mobile; homologação em aparelho físico pendente'),
'F02':(2,9,'Mapeamento de páginas e status; correção integral do OCR pendente'),
'F03':(5,6,'96 SVG ilustrados, 96 mapas, temas por seção, manifesto e fallback; revisão humana pendente'),
'F09':(5,6,'Integração com busca, histórico, links, PDF e checklist; performance pendente'),
'F10':(3 if tested else 2,8,'Testes em 7 larguras e seis itens; ainda falta inspeção individual'),
'F11':(0,3,'Publicação da versão premium ainda não concluída')}
group={'F04':'O','F05':'P','F06':'R','F07':'BF','F08':'BV'}
for phase,section in group.items():
 entries=[x for x in items if x['categoria']==section]
 done=0.0
 for entry in entries:
  code=entry['codigo']
  if (r/'assets/illustrations'/(code+'.svg')).exists():done+=.20
  if (r/'assets/flows'/(code+'.svg')).exists() and (r/'data/flows'/(code+'.json')).exists():done+=.10
  if (r/'itens'/(code+'.html')).exists() and (r/'data/procedures'/(code+'.json')).exists():done+=.05
  if code in pilots:done+=.125
  if code in tested:done+=.035
 phases[phase]=(round(done,4),len(entries),'Ilustrações e fluxos gerados; revisão editorial individual pendente')
score=sum(weights[f]*p[0]/p[1] for f,p in phases.items())
percent=math.floor(score*10)/10
def progress(p):
 n=min(20,math.floor(p/5))
 return '█'*n+'░'*(20-n)
metrics={'fichas_html':len(list((r/'itens').glob('*.html'))),
'novas_ilustracoes_svg':len(list((r/'assets/illustrations').glob('*.svg'))),
'novos_mapas_svg':len(list((r/'assets/flows').glob('*.svg'))),
'paginas_fonte_html':len(list((r/'fonte-html').glob('p???.html'))),
'fichas_editorialmente_aprovadas':sum(1 for x in audit if x['editorial_approved']),
'pilotos_parcialmente_conferidos':len(pilots),
'testes_navegador_aprovados':qa.get('passed',0)}
payload={'updated_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
'version':'v0.2.0-draft','global_percent':percent,'global_raw':score,'bar':progress(percent),
'phases':{f:{'done':p[0],'total':p[1],'weight':weights[f],
'phase_percent':round(100*p[0]/p[1],1),'notes':p[2]} for f,p in phases.items()},
'metrics':metrics,'limitations':['Fonte não oficial e ainda não homologada',
'65 fichas dependem de OCR ainda a revisar','O mapa visual pode representar ordem didática, não ação autorizada',
'Uma ilustração gerada não significa ficha editorialmente aprovada']}
(r/'data/progress.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2),encoding='utf-8')
lines=['# RAF Serventia Docs — Execução premium','',
'**Progresso global apurado:** '+str(percent).replace('.',',')+'%','',
'['+progress(percent)+']','',
'**Data (UTC):** '+payload['updated_at_utc'],'',
'Os percentuais usam os pesos do Prompt Mestre e atribuem crédito parcial a ativos gerados mas ainda não revisados.','',
'## Evidências de entrega','']
for k,v in metrics.items():lines.append('- '+k.replace('_',' ').capitalize()+': '+str(v))
lines+=['','## Progresso por fase','','| Fase | Avanço | Peso | Observação |','|---|---:|---:|---|']
for f,p in payload['phases'].items():
 lines.append('| '+f+' | '+str(p['phase_percent']).replace('.',',')+'% | '+str(p['weight'])+'% | '+p['notes']+' |')
lines+=['','## Próximas prioridades','',
'- Revisão humana da coerência de todas as 65 fichas dependentes de OCR.',
'- Auditoria editorial individual das 96 fichas antes de qualquer classificação como validada.',
'- Testes completos de acessibilidade e em dispositivo físico.',
'- Publicação no Pages e conferência das URLs reais.',
'','## Retomada técnica','',
'Gerador: python scripts/build_illustrated.py',
'Validador: python tests/validate-premium.py',
'QA navegador: node tests/qa-premium.cjs',
'Atualizador: python scripts/update_progress.py',
'','Este relatório não confunde documentação didática, atos judiciais e homologação institucional.']
(r/'docs/progresso-execucao.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
print('PROGRESS',percent,metrics)
