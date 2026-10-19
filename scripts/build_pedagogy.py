"""Constrói o currículo V2. Sem inventar ações no PJe ou aprovação editorial.
Os seis pilotos têm texto revisado na imagem de referência nesta rodada,
ainda pendente de revisão institucional e testes com aprendizes.
"""
from pathlib import Path
import json,re,datetime,hashlib,shutil
from html import escape
from pedagogy_content import PILOTS

ROOT=Path(__file__).resolve().parent.parent
INDEX=json.loads((ROOT/'dados/procedimentos.json').read_text(encoding='utf8'))
assert len(INDEX)==96
for name in ('data/lessons','assets/learning','arquivo-tecnico','docs','tests'):
    (ROOT/name).mkdir(parents=True,exist_ok=True)
# Executar uma única vez: preservar as fichas premium anteriores e suas URLs de consulta.
for row in INDEX:
    old=ROOT/'itens'/(row['codigo']+'.html')
    archive=ROOT/'arquivo-tecnico'/(row['codigo']+'.html')
    if not archive.exists() and old.exists():
        shutil.copy2(old,archive)

SECTION={
 'O':('Operações no PJe','#1378B4','Processo'),
 'P':('Pauta e audiências','#7954CE','Audiência'),
 'R':('Relatórios','#0D937F','Indicadores'),
 'BF':('Balcão físico','#BA743B','Atendimento presencial'),
 'BV':('Balcão virtual','#3777D6','Atendimento remoto'),
}
INITIAL={
 'O-03':1,'BF-01':2,'O-08':3,'P-01':4,'R-01':5,'BV-01':6
}
def norm(x):
 return re.sub(r'\s+',' ',str(x or '')).strip()
def preliminary(row):
 p=row['pagina']
 summary='O manual apresenta o assunto “'+row['titulo']+'” na página '+str(p)+'. Esta lição ainda depende de revisão da fonte para explicar cada procedimento com segurança.'
 return {
  'objective':'Reconhecer o tema desta página e identificar quais informações precisam ser confirmadas na fonte antes de qualquer atuação.',
  'plain':summary,
  'terms':[['Tema da ficha','É o assunto identificado no índice do manual.','Consulte a imagem da página '+str(p)+' para compreender os elementos apresentados.'],
           ['Conferência documental','Leitura da fonte e dos documentos relevantes antes de interpretar uma situação.','Não conclua a situação a partir do título de um evento.'],
           ['Supervisão','Acompanhamento das atividades por servidor habilitado.','Em caso de dúvida, explique o que observou e pergunte ao responsável.']],
  'scene':'Mapa de leitura provisório — '+row['titulo'],
  'hotspots':[['Tema principal','Identifique o título do infográfico.' ],
              ['Fonte original','Abra a página '+str(p)+' do manual.' ],
              ['Palavras novas','Anote os termos cujo significado ainda precisa compreender.' ],
              ['Dúvidas','Marque trechos ilegíveis ou que dependam de decisão do servidor.' ]],
  'observe':[['Leia o título do infográfico','Diga com suas palavras qual assunto está sendo apresentado.'],
             ['Encontre uma explicação visual','Procure exemplos, números e setas que precisem de conferência.'],
             ['Não use como roteiro validado','Se a imagem não sustenta a ação, não invente instruções.']],
  'steps':[],
  'decision':{'question':'Você encontrou um trecho que parece incompleto ou distorcido no texto transcrito. O que fazer?',
              'options':[['Seguir o texto sem conferir.','Não. Uma transcrição pode ter erro.',False],
                         ['Abrir a imagem original e consultar a supervisão quando necessário.','Correto. Esta ficha está em revisão.',True],
                         ['Criar a regra que parecer mais lógica.','Não. Regras não podem ser inventadas.',False]]},
  'practice':{'scenario':'Exercício de leitura da fonte, não de execução de atos: você encontra uma palavra ilegível em uma transcrição automática.',
              'question':'Qual atitude preserva a fidelidade ao manual?',
              'options':[['Conferir a página original antes de explicar ou aplicar.','Correto. Uma transcrição incerta não é fonte suficiente.',True],
                         ['Copiar e executar mesmo com dúvida.','Incorreto: exige conferência.',False],
                         ['Supor um botão do sistema que não aparece na fonte.','Não invente controles ou fluxos.',False]]},
  'mistakes':[['Repetir o OCR como verdade','A grafia e a ordem de leitura podem estar erradas.'],
              ['Confundir roteiro didático com ato autorizado','As decisões do órgão seguem competências e supervisão.']],
  'mastery':['Consigo localizar a página original.','Identifico o que preciso perguntar ao servidor.','Não confundo transcrição provisória e instrução validada.'],
 }
def esc(s):return escape(str(s),quote=True)
def scene_svg(lesson):
    theme=lesson['color'];code=lesson['code'];hot=lesson['scene']['regions']
    name=lesson['title']
    # Diagramas originais e responsivos; representações conceituais, não cópias oficiais do PJe.
    units=[]
    positions=[(95,165),(310,165),(525,165),(202,337),(420,337)]
    for i,hotspot in enumerate(hot[:5]):
        x,y=positions[i]
        s=hotspot['title']
        words=s.split();lines=[];line=''
        for word in words:
            if len(line+' '+word)>16 and line:lines.append(line);line=word
            else:line=(line+' '+word).strip()
        if line:lines.append(line)
        texts=''.join('<text x="'+str(x+85)+'" y="'+str(y+71+j*22)+'" text-anchor="middle" font-family="Arial,sans-serif" font-size="16" fill="#eaf6ff" font-weight="600">'+esc(t)+'</text>' for j,t in enumerate(lines[:2]))
        units.append('<rect x="'+str(x)+'" y="'+str(y)+'" width="170" height="125" rx="18" fill="#24465F" stroke="'+theme+'" stroke-width="3"/>'+
            '<circle cx="'+str(x+85)+'" cy="'+str(y+17)+'" r="21" fill="'+theme+'"/>'+
            '<text x="'+str(x+85)+'" y="'+str(y+24)+'" font-family="Arial" font-size="20" text-anchor="middle" fill="white">'+str(i+1)+'</text>'+texts)
    elements=''.join(units)
    svg=f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 530" role="img" aria-labelledby="t d">
<title id="t">Ilustração didática de {esc(name)}</title><desc id="d">Representação conceitual de {len(hot)} tópicos de estudo, sem reprodução de interface oficial do tribunal.</desc>
<defs><linearGradient id="base" x2="1" y2="1"><stop stop-color="#12304A"/><stop offset="1" stop-color="#1B405C"/></linearGradient></defs>
<rect width="800" height="530" rx="26" fill="url(#base)"/>
<text x="42" y="52" fill="#A0CCED" font-family="Arial" font-size="15" font-weight="bold">RAF SERV­ENTIA · {esc(code)} · SIMULAÇÃO DIDÁTICA</text>
<text x="42" y="94" fill="#fff" font-family="Arial" font-size="24" font-weight="bold">{esc(name[:47])}</text>
<path d="M180 290 V325 H507 M395 290 V325" stroke="'+theme+'" fill="none" stroke-width="4" opacity=".6"/>{elements}
<text x="42" y="493" fill="#A9C7D9" font-family="Arial" font-size="14">Selecione os números da página para ler cada explicação.</text></svg>'''
    return svg

LESSONS=[]
for row in INDEX:
 code=row['codigo'];sec=row['categoria'];d=dict(PILOTS.get(code) or preliminary(row))
 is_pilot=code in PILOTS
 theme=SECTION[sec]
 lesson={
  'code':code,'title':row['titulo'],'section':sec,'section_name':row['categoria_nome'],'color':theme[1],
  'page':row['pagina'],'source':'Manual Operacional do Estagiário na Serventia — PJe (15/10/2026)',
  'source_method':row.get('origemTexto',''), 'state':'author_draft' if is_pilot else 'needs_source_review',
  'pedagogical_ready':False,'technical_approved':False,'student_tested':False,'estimated_minutes':None,
  'order':INITIAL.get(code), 'is_pilot':is_pilot,
  'objective':d['objective'],'plain':d['plain'],
  'terms':[{'term':a,'meaning':b,'example':c} for a,b,c in d['terms']],
  'scene':{'title':d['scene'],'alt':'Ilustração conceitual, não tela oficial do sistema.','regions':[{'title':a,'detail':b} for a,b in d['hotspots']]},
  'observe':[{'title':a,'detail':b} for a,b in d['observe']],
  'steps':[{'title':a,'instruction':b,'why':c} for a,b,c in d['steps']],
  'decision':{'question':d['decision']['question'],'options':[{'label':a,'feedback':b,'correct':c} for a,b,c in d['decision']['options']]},
  'practice':{'scenario':d['practice']['scenario'],'question':d['practice']['question'],
    'options':[{'label':a,'feedback':b,'correct':c} for a,b,c in d['practice']['options']]},
  'mistakes':[{'mistake':a,'correct':b} for a,b in d['mistakes']],
  'mastery':d['mastery'],'source_image':'../assets/thumbs/p%03d.jpg'%row['pagina'],
  'pdf':'../docs/manual-fonte.pdf#page='+str(row['pagina']),
  'archive':'../arquivo-tecnico/'+code+'.html',
  'status_note':('Lição piloto autoral baseada no manual; pendente de revisão técnica e teste com aprendizes.' if is_pilot else 'Prévia de estudo: explicação operacional desta ficha ainda não revisada.'),
  'revised_by':None,'revised_at':None
 }
 LESSONS.append(lesson)
 (ROOT/'data/lessons'/(code+'.json')).write_text(json.dumps(lesson,ensure_ascii=False,indent=2),encoding='utf8')
 directory=ROOT/'assets/learning'/code
 directory.mkdir(parents=True,exist_ok=True)
 (directory/'simulacao.svg').write_text(scene_svg(lesson),encoding='utf8')
 # stable original item URL, lesson data loaded by JS.
 item_html=f'''<!doctype html><html lang="pt-BR"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="Aula guiada de {esc(lesson['title'])}, com simulação, glossário e exercícios. Material não oficial, em revisão.">
<meta name="referrer" content="strict-origin-when-cross-origin">
<title>{esc(code)} · {esc(lesson['title'])} — RAF Serventia Docs</title>
<link rel="stylesheet" href="../assets/css/lesson-ux.css">
<script src="../assets/js/lesson-engine.js" defer></script>
</head><body data-code="{esc(code)}" data-section="{esc(sec)}">
<a href="#lesson-main" class="sr-skip">Pular para a lição</a>
<header class="lesson-header"><a href="../index.html" class="lesson-brand"><span class="brand-mark">◆</span><span>RAF <strong>Serventia Docs</strong><small>APRENDER DO ZERO</small></span></a>
<nav aria-label="Navegação"><a href="../aprender.html">Trilha inicial</a><a href="../index.html#catalogo">Catálogo</a></nav></header>
<main class="lesson-main" id="lesson-main">
<div id="lesson-loading" role="status">Preparando a lição ilustrada…</div>
<div id="lesson-app" hidden></div>
<noscript>Esta aula interativa requer JavaScript. Consulte a <a href="../fonte-html/p{row['pagina']:03d}.html">página do manual em HTML</a> ou o <a href="../docs/manual-fonte.pdf#page={row['pagina']}">PDF de referência</a>.</noscript>
</main><footer class="lesson-footer">RAF Serventia Docs · Rafael MS Passos · Material de apoio não oficial, em revisão · Não executa atos no PJe.</footer>
</body></html>'''
 (ROOT/'itens'/(code+'.html')).write_text(item_html,encoding='utf8')

summary={'version':'v2.0-draft','count':len(LESSONS),'pilots_authored':sum(l['is_pilot'] for l in LESSONS),
 'needs_source_review':sum(l['state']=='needs_source_review' for l in LESSONS),
 'approved':0,'reviewed_with_students':0,
 'first_learning_path':[c for c in sorted(INITIAL,key=INITIAL.get)],
 'chapter_counts':{k:sum(l['section']==k for l in LESSONS) for k in SECTION},
 'notes':'Seis roteiros autorais de treinamento inicial; os demais 90 são prévias conceituais sem instrução operacional homologada.'}
(ROOT/'data/lessons-index.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf8')
print('LESSON_V2_CREATED',summary)
