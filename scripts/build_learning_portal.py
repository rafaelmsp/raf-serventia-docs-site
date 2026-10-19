"""Gera trilha inicial e painel pedagogico. Números fundamentados nos arquivos.
"""
from pathlib import Path
from html import escape
import json,datetime
r=Path(__file__).resolve().parent.parent
d=json.loads((r/'dados/procedimentos.json').read_text(encoding='utf8'))
index=json.loads((r/'data/lessons-index.json').read_text(encoding='utf8'))
codes=index['first_learning_path']
lessons={x['codigo']:json.loads((r/'data/lessons'/(x['codigo']+'.json')).read_text(encoding='utf8')) for x in d}
css='<link rel="stylesheet" href="assets/css/documentacao.css"><link rel="stylesheet" href="assets/css/portal-v2.css">'
head='''<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'''+css+'''<title>Trilha inicial — RAF Serventia Docs</title></head><body>
<header class="head"><a class="logo" href="index.html">◆ RAF <strong>Serventia Docs</strong></a><nav class="head-nav" aria-label="Navegação principal"><a href="index.html">Catálogo</a><a href="andamento-pedagogico.html">Progresso V2</a></nav></header>'''
rows=[]
for i,code in enumerate(codes):
 l=lessons[code]
 colors={'O':'#1679B6','P':'#7859C6','R':'#16967B','BF':'#C38442','BV':'#3B79D0'}
 rows.append('<article class="v2-path"><span class="v2-symbol" style="border:2px solid '+colors[l['section']]+'">'+str(i+1).zfill(2)+'</span><h2>'+escape(l['title'])+'</h2><p><strong>O que você vai aprender:</strong> '+escape(l['objective'])+'</p><small style="color:#647b8c">Pág. '+str(l['page'])+' · Aula piloto em revisão · sete etapas</small><p><a href="itens/'+code+'.html">Começar esta lição →</a></p></article>')
body='''<main class="home-main" id="main"><section class="v2-hero"><div><p class="v2-kicker">TRILHA INICIAL · APRENDER DO ZERO</p><h1>Primeiro entenda. Depois pratique.</h1><p>Seis aulas piloto organizadas do mais básico para situações de conferência, atendimento e análise. Cada aula tem sete etapas, exemplos fictícios e feedback explicativo.</p><div class="hero-actions"><a class="hero-primary" href="itens/O-03.html">Começar pela árvore do processo →</a><a class="hero-secondary" href="index.html#catalogo">Voltar ao catálogo</a></div></div><div class="hero-stat"><strong>06</strong><span>roteiros iniciais</span><small>Não homologados; teste com estagiários pendente</small></div></section>
<div class="status-note"><strong>Treinamento supervisionado.</strong> As aulas não substituem normas, orientação do servidor ou a leitura dos autos. A plataforma não executa atos no PJe.</div>
<section aria-labelledby="path-title"><h2 id="path-title" style="font-size:25px">Sua jornada de aprendizagem</h2><p style="color:#5E7B8D">Faça uma aula por vez; não há punição por tentar novamente.</p><div class="v2-paths">'''+''.join(rows)+'''</div></section>
<section class="source-footer"><h2>Quer apenas consultar?</h2><p>O índice continua com 96 referências, incluindo 90 prévias que aguardam explicações operacionais revisadas.</p><a href="index.html#catalogo">Consultar os 96 códigos →</a><a href="docs/manual-fonte.pdf" target="_blank" rel="noopener noreferrer">Abrir manual fonte ↗</a></section></main>
<footer>RAF Serventia Docs · Rafael MS Passos · Material não oficial, não homologado.</footer></body></html>'''
(r/'aprender.html').write_text(head+body,encoding='utf8')

# Contagem V2: pontos por evidência técnica, sem creditar aprovação editorial.
phases=[
 ('M00','Auditoria da fonte',7,7,'96 códigos e 107 páginas identificados; revisão normativa individual pendente'),
 ('M01','Motor das aulas e UX',12,10,'Sete etapas, duas portas de entrada, exercícios e retomada local; testes finais pendentes'),
 ('M02','Ilustrações explicativas',12,4,'96 esquemas conceituais gerados, seis com roteiro autoral; revisão visual individual pendente'),
 ('M03','Seis pilotos',15,5,'Seis roteiros autorais inseridos; testes com estagiários iniciantes e revisão técnica pendentes'),
 ('M04','Operações (49)',20,0,'0 lições com aprovação pedagógica e técnica'),
 ('M05','Pauta (16)',8,0,'0 lições com aprovação pedagógica e técnica'),
 ('M06','Relatórios (5)',4,0,'0 lições com aprovação pedagógica e técnica'),
 ('M07','Balcão físico (12)',5,0,'0 lições com aprovação pedagógica e técnica'),
 ('M08','Balcão virtual (14)',5,0,'0 lições com aprovação pedagógica e técnica'),
 ('M09','Usabilidade e acessibilidade',7,0,'Não há teste real com aprendizes ainda'),
 ('M10','Deploy V2',5,0,'A versão V2 ainda não teve publicação confirmada')
]
total=sum(p[3] for p in phases)
assert sum(p[2] for p in phases)==100
raw={'version':'v2.0-draft','published':False,'phases':[{'id':a,'name':b,'weight':w,'credited':v,'evidence':note} for a,b,w,v,note in phases],
'percent':total,'approved_lessons':0,'authored_pilots':6,'unreviewed_previews':90,
'source_pages':107,'modified_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),
'blockers':['Revisão técnica e normativa das seis aulas piloto','Correção e revisão editorial das outras 90 fichas','Teste de compreensão com estagiários iniciantes','Revisão de acessibilidade com tecnologias assistivas'],
'not_equivalent_to':'Progresso técnico V1 de 53,5% não integra a métrica de conclusão pedagógica.'}
(r/'data/progresso-pedagogico.json').write_text(json.dumps(raw,ensure_ascii=False,indent=2),encoding='utf8')
rows=[]
for phase in raw['phases']:
 rows.append('<article class="v2-progress-phase"><div><b>'+phase['id']+' · '+escape(phase['name'])+'</b><strong>'+str(phase['credited'])+' / '+str(phase['weight'])+' pontos</strong></div><progress max="'+str(phase['weight'])+'" value="'+str(phase['credited'])+'"></progress><p>'+escape(phase['evidence'])+'</p></article>')
panel='''<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'''+css+'''<title>Progresso pedagógico V2 — RAF Serventia Docs</title>
<style>.v2-progress-phase{padding:15px;background:#fff;border-radius:11px;border:1px solid #D9E5EC;margin-bottom:10px}.v2-progress-phase>div{display:flex;justify-content:space-between;gap:14px;font-size:12px}.v2-progress-phase p{font-size:12px;color:#536E80}.v2-progress-phase progress{width:100%;height:16px;accent-color:#1479B4;margin-top:11px}
@media(max-width:600px){.v2-progress-phase>div{display:block}.v2-progress-phase strong{display:block;margin-top:5px}}</style></head><body><header class="head"><a href="index.html" class="logo">◆ RAF <strong>Serventia Docs</strong></a><nav class="head-nav"><a href="aprender.html">Trilha de aulas</a></nav></header><main class="home-main">
<section class="v2-hero"><div><p class="v2-kicker">PROGRESSO REAL DA RECONSTRUÇÃO PEDAGÓGICA</p><h1>''' +str(raw['percent'])+'''% de implementação V2</h1><p>Percentual de entregas técnicas reconhecidas, não de aulas homologadas. Há 6 pilotos escritos e 90 prévias ainda pendentes de conteúdo validado.</p></div><div class="hero-stat"><strong>0</strong><span>aulas aprovadas / 96</span></div></section>
<div class="status-note"><strong>Importante:</strong> o percentual antigo de 53,5% pertence à fase técnica V1. A V2 mede evolução pedagógica separadamente. Nenhum processo real ou competência é validado por exercícios deste portal.</div>
<h2>Etapas M00 a M10</h2>'''+''.join(rows)+'''<section class="source-footer"><h2>O que falta?</h2><p>Revisar o conteúdo com base no manual; conferir normas e fluxos; testar compreensão com estagiários; executar auditoria de acessibilidade e validar o Pages.</p><a href="docs/LOG_REVISAO_PEDAGOGICA.md">Consultar registro de revisão ↗</a><a href="aprender.html">Ver as aulas piloto →</a></section></main><footer>RAF Serventia Docs · Relatório de progresso não institucional.</footer></body></html>'''
(r/'andamento-pedagogico.html').write_text(panel,encoding='utf8')
print('LEARNING_LANDING_AND_PROGRESS',len(rows),'PHASES',raw['percent'],'PERCENT')
