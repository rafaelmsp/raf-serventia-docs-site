"""RAF Serventia Docs: build 96 source-grounded didactic HTML pages + unique SVG diagrams.

Do not promote OCR to validated judicial instructions. Asset creation is separate
from human editorial acceptance. Existing PDF and source-html files are preserved.
"""
from pathlib import Path
import json,re,html,hashlib,textwrap,unicodedata,datetime,math
ROOT=Path(__file__).resolve().parent.parent
INDEX=json.loads((ROOT/'dados/procedimentos.json').read_text(encoding='utf-8'))
SRC_FILE=ROOT/'dados'/'conteudo_integral.json'
assert SRC_FILE.exists(),'Original PDF-derived source corpus is required'
SOURCE={int(p['pagina']):p for p in json.loads(SRC_FILE.read_text(encoding='utf-8'))}
assert len(INDEX)==96 and len(SOURCE)==107
SECTIONS={'O':('Operações no PJe','#2c7aa8','processo'),'P':('Pauta e audiências','#8865bd','pauta'),'R':('Relatórios e controle','#259883','indicadores'),'BF':('Balcão físico','#bc7950','atendimento'),'BV':('Balcão virtual','#567ed6','remoto')}
COUNTS={k:sum(x['categoria']==k for x in INDEX) for k in SECTIONS}
assert COUNTS=={'O':49,'P':16,'R':5,'BF':12,'BV':14}
for n in ['assets/illustrations','assets/flows','data/procedures','data/flows','data']:
 (ROOT/n).mkdir(parents=True,exist_ok=True)
def esc(x):return html.escape(str(x),quote=True)
def compact(x):return re.sub(r'\s+',' ',str(x or '')).strip()
def norm(x):return ''.join(c for c in unicodedata.normalize('NFD',x.lower()) if unicodedata.category(c)!='Mn')
def wrapped(s,n=22):
 words=s.split();out=[];line=''
 for w in words:
  if len(line+' '+w)>n and line:out.append(line);line=w
  else:line=(line+' '+w).strip()
 if line:out.append(line)
 return out[:3]
def clean_line(raw):
 s=compact(raw).strip('–—.- ')
 if not 13<=len(s)<=145 or not re.search('[a-záéíóúàâêôãõç]',s,re.I):return False
 if len(re.findall(r'[a-záéíóúàâêôãõç]',s,re.I)) < len(s)*.61:return False
 if re.search(r'(?:\\uFFFD|[<>|]{2,}|\.{4})',s):return False
 if norm(s).startswith(('material de apoio','desenvolvido por','fluxos operacionais, tarefas','tribunal de justica')):return False
 if re.fullmatch(r'(?i)(?:[a-záéíóúãõç]+\s*){1,2}',s) and len(s)<25:return False
 return True

PILOTS={
'O-03':{
 'summary':'A árvore do processo é apresentada como uma representação da evolução dos autos. O infográfico utiliza raízes, tronco, galhos, folhas e frutos para distinguir história, decisões, comunicações, movimentações e desdobramentos.',
 'kind':'conceptual','names':['Raízes · histórico','Tronco · atos decisórios','Galhos · comunicações','Folhas · andamento','Frutos · providência'],
 'details':['História e informações que sustentam a compreensão do processo.','Despachos, decisões, sentenças e atos ordinatórios.','Citação, intimação, manifestação, juntada e certidão.','Cumprimento, resposta das partes e movimentação.','Próxima providência, resultado ou encaminhamento.'],
 'warnings':['O desenho é uma analogia didática, não uma reprodução oficial da interface do PJe.','A leitura de um evento isolado não substitui a conferência do documento e do histórico.'],
 'source':'Infográfico da página 8; termos raízes/tronco/galhos/folhas/frutos registrados na fonte.','mode':'mapa da estrutura'},
'O-08':{
 'summary':'O manual apresenta o PAC como um percurso de identificação de pendência, comunicação e verificação do cumprimento. A transcrição OCR desta página contém palavras distorcidas e ainda exige conferência visual.',
 'kind':'provisional','names':['Identificar pendência','Conferir origem da pendência','PAC / intimação','Verificar cumprimento','Registrar situação'],
 'details':['No infográfico aparecem exemplos de documento ausente ou incompleto e erro formal.','Ler o que falta nos autos, evitando concluir a partir de OCR incerto.','A página menciona PAC e intimação, mas forma e cabimento dependem de orientação da serventia.','Conferir a providência apresentada e os documentos dos autos antes de registrar conclusão.','Encaminhar dúvida ao responsável; não executar ato automaticamente por meio do portal.'],
 'warnings':['Roteiro visual provisório. O PDF na página 13 é a referência para validar cada decisão e etapa.'],
 'source':'Pág. 13 do manual — termos PAC, pendência, intimação e cumprimento.','mode':'fluxo preliminar'},
'BF-01':{
 'summary':'O atendimento inicial no balcão físico identifica a demanda, a condição de quem comparece e o encaminhamento adequado, resguardando sigilo e atendimento prioritário.',
 'kind':'operational','names':['Acolher e ouvir','Localizar a demanda','Conferir o vínculo','Verificar prioridade','Definir o fluxo'],
 'details':['Identificar o motivo do comparecimento com linguagem respeitosa e clara.','Perguntar sobre processo existente e número disponível sem expor autos de terceiros.','Distinguir parte, representante, advogado e acompanhante; dúvida de representação deve ser dirigida ao servidor.','Observar acessibilidade e atendimento prioritário sem exigir dados desnecessários.','Identificar consulta, juntada, petição genérica, audiência ou primeiro atendimento e encaminhar ao serviço adequado.'],
 'warnings':['Verificar sigilo e permissão de acesso antes de transmitir informações.','Dúvidas de representação devem ser encaminhadas ao servidor.'],
 'source':'Página 79 — cinco passos e checklist do balcão físico.','mode':'fluxo de atendimento'},
'BV-01':{
 'summary':'O manual distingue as normas públicas do Balcão Virtual das rotinas locais. O atendimento é informativo, humano e supervisionado.',
 'kind':'normative','names':['Base nacional','Regulação do TJRJ','Atendimento humano','Aplicação cautelosa'],
 'details':['A fonte cita a Resolução CNJ nº 372/2021 e orienta consultar seu texto compilado.','A fonte menciona os Atos TJ/CGJ nº 05/2021 e nº 15/2026.','Estagiário atua sob supervisão de servidor, conforme norma indicada no manual.','Os parâmetros de tempo, processos e câmera mencionados em fontes secundárias devem ser conferidos na redação oficial.'],
 'warnings':['O manual registra que não obteve o texto integral consolidado do Ato 15/2026; não considerar a referência como validação normativa atual.','Balcão Virtual é atendimento informativo, não protocolo processual.'],
 'source':'Página 92 — seção Bases legais e regras, com ressalvas explícitas.','mode':'mapa normativo'}
}

def derive(item):
 code=item['codigo'];pg=item['pagina'];raw=SOURCE[pg]['linhas']
 if code in PILOTS:
  d=dict(PILOTS[code]);d['verified_from_source']=code in ('O-03','BF-01','BV-01')
  d['source_method']=item['origemTexto']
  return d
 good=[compact(x) for x in raw if clean_line(x)]
 unique=[];seen=set()
 for x in good:
  key=norm(x)
  if key in seen or key==norm(item['titulo']):continue
  seen.add(key);unique.append(x)
 common=['Situação documentada','Elementos do tema','Contexto da página','Conferência da fonte','Revisão supervisionada']
 headings=[]
 for x in unique:
  n=norm(x)
  if len(x)<=67 and (x.isupper() or x[:2].isdigit() or x.startswith(('•','–'))) and x not in headings:
   headings.append(x)
 # Prefer actual labels from source. Never turn OCR fragments into asserted steps.
 labels=headings[:5]
 for x in unique:
  if len(labels)>=5:break
  if 14<=len(x)<=68 and x not in labels:labels.append(x)
 while len(labels)<4:labels.append(common[len(labels)])
 details=[]
 for label in labels:
  match=next((x for x in unique if x!=label and norm(label)[:20] in norm(x)),None)
  details.append((match if match else 'Tópico destacado na página do manual. Consulte o infográfico para conferir o contexto.'))
 intro=next((x for x in unique if 35<=len(x)<=140 and not x.isupper()),None)
 if not intro:intro='Mapa de leitura da fonte para compreender os assuntos reunidos neste item.'
 method=item['origemTexto']
 if method=='ocr_ptbr_provisorio':
  intro='A página apresenta o tema “'+item['titulo']+'”. O mapa abaixo reúne tópicos extraídos automaticamente do infográfico e requer comparação com a fonte original.'
 kind='reading' if method=='ocr_ptbr_provisorio' else 'documentary'
 warnings=['Pág. '+str(pg)+' — roteiro de leitura didático, não sequência autorizada de atos processuais.']
 if method=='ocr_ptbr_provisorio':
  warnings.append('Rótulos extraídos automaticamente: confirme números, prazos e grafia na imagem antes de usar.')
 return {'summary':intro,'names':labels[:5],'details':details[:5],'warnings':warnings,'kind':kind,
         'source':'Pág. '+str(pg)+' do manual de 15/10/2026. Texto '+('OCR provisório.' if method=='ocr_ptbr_provisorio' else 'nativo do PDF.'),
         'source_method':method,'verified_from_source':False,'mode':'mapa documental preliminar'}

def svg_illustration(item,d):
 code=item['codigo'];group=item['categoria'];accent=SECTIONS[group][1]
 name=item['titulo'];names=d['names'];index=int(code.split('-')[1])
 W,H=1120,560
 defs='<defs><linearGradient id="bg" x2="1" y2="1"><stop stop-color="#101f34"/><stop offset="1" stop-color="#1e3d58"/></linearGradient><filter id="shadow"><feDropShadow dx="0" dy="8" stdDeviation="9" flood-color="#071322" flood-opacity=".18"/></filter></defs>'
 base=f'<rect width="{W}" height="{H}" rx="28" fill="url(#bg)"/><circle cx="1010" cy="70" r="210" fill="{accent}" opacity=".13"/><circle cx="90" cy="500" r="160" fill="{accent}" opacity=".08"/>'
 title=f'<text x="58" y="61" font-family="Arial,sans-serif" fill="#99bed7" font-size="15" letter-spacing="2">RAF SERVENTIA DOCS • ESQUEMA DIDÁTICO {esc(code)}</text>'
 title+=f'<text x="58" y="110" font-family="Arial,sans-serif" fill="white" font-size="31" font-weight="700">{esc(name[:62])}</text>'
 def label(x,y,s,i,wide=225):
  ls=wrapped(s,25)
  text=''.join(f'<text x="{x}" y="{y+j*24}" text-anchor="middle" font-family="Arial" fill="#e9f4fe" font-weight="600" font-size="17">{esc(line)}</text>' for j,line in enumerate(ls))
  return f'<circle cx="{x}" cy="{y-43}" r="17" fill="{accent}" stroke="#9dd4fa" stroke-width="1.5"/><text x="{x}" y="{y-37}" fill="#fff" text-anchor="middle" font-family="Arial" font-weight="bold" font-size="15">{i}</text>'+text
 # illustrate per category, individualized labels
 art=''
 if group=='O':
  # Process-tree themed scheme: one trunk, varied event branches for topic.
  art=f'<path d="M560 475 V300 M560 348 Q400 260 282 245 M560 348 Q710 270 838 240 M560 320 Q475 205 440 184 M560 320 Q656 205 685 175" fill="none" stroke="{accent}" stroke-width="17" stroke-linecap="round"/><path d="M560 485 V365" stroke="#a5c9dc" stroke-width="25" stroke-linecap="round"/>'
  spots=[(200,255),(400,190),(690,184),(925,250),(560,440)]
  for i,(x,y) in enumerate(spots):
   art+=f'<rect x="{x-108}" y="{y-71}" width="216" height="110" rx="16" fill="#243d58" stroke="#6693b0" filter="url(#shadow)"/>'
   art+=label(x,y,names[i%len(names)],i+1)
 elif group=='P':
  art+='<path d="M98 303 H1020" stroke="#7c9ab1" stroke-width="7" stroke-dasharray="12 12"/>'
  for i in range(5):
   x=150+i*204;y=268 if i%2==0 else 352
   art+=f'<rect x="{x-87}" y="{y-67}" width="174" height="130" rx="20" fill="#243d58" stroke="{accent}" stroke-width="2"/><line x1="{x}" y1="{303}" x2="{x}" y2="{y}" stroke="{accent}" stroke-width="6"/>'
   art+=label(x,y+30,names[i%len(names)],i+1)
 elif group=='R':
  for i in range(5):
   x=152+200*i;v=100+((index*29+i*23)%120)
   art+=f'<rect x="{x-46}" y="{448-v}" width="92" height="{v}" rx="12" fill="{accent}" opacity="{.45+i*.12:.2f}"/><line x1="{x-65}" y1="460" x2="{x+65}" y2="460" stroke="#7291ad" stroke-width="2"/>'
   art+=label(x,510,names[i%len(names)],i+1)
 elif group=='BF':
  art+='<rect x="102" y="285" width="912" height="135" rx="23" fill="#243c55" stroke="#698ba3"/><path d="M130 330 H982" stroke="#87b0c9" stroke-dasharray="8 12" stroke-width="2"/>'
  for i in range(5):
   x=180+i*190
   art+=f'<circle cx="{x}" cy="260" r="48" fill="#2c506b" stroke="{accent}" stroke-width="3"/><path d="M{x-25} 283 Q{x} 235 {x+25} 283" fill="none" stroke="#b7d2e3" stroke-width="6"/>'
   art+=label(x,475,names[i%len(names)],i+1)
 else:
  art+='<rect x="120" y="175" width="880" height="290" rx="22" fill="#203a55" stroke="#8eb2d2" stroke-width="6"/><rect x="150" y="209" width="820" height="219" rx="12" fill="#10243b"/><path d="M65 484 H1055 L990 510 H130 Z" fill="#527895"/>'
  for i in range(5):
   x=223+i*171
   art+=f'<rect x="{x-72}" y="248" width="144" height="125" rx="13" fill="#28496b" stroke="{accent}"/>'
   art+=label(x,330,names[i%len(names)],i+1)
 foot=f'<text x="58" y="544" fill="#a8bed2" font-size="13" font-family="Arial">Fonte: manual, p. {item["pagina"]} • Diagrama esquemático, não captura do PJe • Revisão editorial pendente</text>'
 content=f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="t d"><title id="t">{esc(name)} — ilustração explicativa</title><desc id="d">Mapa didático original com {len(names)} tópicos extraídos da fonte, ainda sujeito a revisão.</desc>{defs}{base}{title}{art}{foot}</svg>'
 return content

def svg_flow(item,d):
 nodes=d['names'];accent=SECTIONS[item['categoria']][1];code=item['codigo'];title=item['titulo']
 w=1100;h=290
 edges=''.join(f'<path d="M{190+205*i} 143 h50" stroke="{accent}" stroke-width="4" fill="none"/><path d="m{226+205*i} 134 l14 9 -14 9" fill="none" stroke="{accent}" stroke-width="4"/>' for i in range(len(nodes)-1))
 cells=''
 for i,node in enumerate(nodes):
  x=20+i*205;ty=113
  txt=''.join(f'<text x="{x+90}" y="{153+23*j}" fill="#eaf5fd" text-anchor="middle" font-family="Arial" font-size="16" font-weight="600">{esc(t)}</text>' for j,t in enumerate(wrapped(node,19)))
  cells+=f'<rect x="{x}" y="104" width="180" height="120" rx="17" fill="#253e56" stroke="{accent}" stroke-width="2"/><circle cx="{x+90}" cy="107" r="19" fill="{accent}"/><text x="{x+90}" y="114" text-anchor="middle" font-size="17" font-family="Arial" fill="#fff">{i+1}</text>'+txt
 svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="t d"><title id="t">Mapa explicativo de {esc(title)}</title><desc id="d">Representação visual dos {len(nodes)} pontos de leitura; confira o texto interativo.</desc><rect width="{w}" height="{h}" rx="22" fill="#15283c"/><text x="25" y="50" fill="#94cce9" font-size="18" font-family="Arial"> {esc(code)} — {esc(d["mode"].upper())}</text>{edges}{cells}</svg>'
 return svg

def make_record(item):
 d=derive(item);code=item['codigo'];index=int(code.split('-')[1]);pg=item['pagina']
 nodes=[{'id':f'{code}-n{i+1}','number':i+1,'label':s,'detail':d['details'][i] if i<len(d['details']) else 'Conferir referência original.',
  'source_page':pg,'editorial_status':'source_checked_draft' if d['verified_from_source'] else 'ocr_or_source_review_pending'}
   for i,s in enumerate(d['names'])]
 edges=[{'from':nodes[i]['id'],'to':nodes[i+1]['id'],'meaning':'ordem de apresentação didática, não execução de ato judicial'} for i in range(len(nodes)-1)]
 data={
 'code':code,'title':item['titulo'],'section':item['categoria'],'section_name':item['categoria_nome'],
 'source_page':pg,'source_method':item['origemTexto'],
 'summary':d['summary'],'kind':d['kind'],'mode':d['mode'],'nodes':nodes,'edges':edges,
 'steps': [{'title':n['label'],'detail':n['detail'],'source_page':pg} for n in nodes],
 'warnings':d['warnings'],'source_evidence':d['source'],
 'status':'didactic_draft_human_review_pending','source_checked':d['verified_from_source'],
 'visual':{'src':f'../assets/illustrations/{code}.svg','alt':f'Ilustração vetorial original sobre {item["titulo"]}; contém {len(nodes)} tópicos esquemáticos.'},
 'checklist':[f'Identifiquei na fonte: {n["label"]}' for n in nodes[:4]]+
   [f'Comparei a síntese com a página {pg} do PDF antes de utilizar.'],
 'faq':[{'q':'Este esquema reproduz a interface oficial do PJe?','a':'Não. Trata-se de uma representação didática de leitura do manual, sem conexão com o PJe.'},
        {'q':'O texto desta ficha já está homologado?','a':'Não. A ficha está em revisão. Use a página original e a orientação do servidor responsável para conferência.'}],
 }
 return data

def render_html(rec):
 code=rec['code'];title=rec['title'];group=rec['section'];pg=rec['source_page']
 nodes=rec['nodes'];pieces=[]
 for i,n in enumerate(nodes):
  pieces.append(f'<button class="node-button" type="button" data-index="{i}" aria-pressed="false"><span class="node-counter">{i+1:02d}</span><span>{esc(n["label"])}</span><span class="node-chevron" aria-hidden="true">›</span></button>')
 steps=''.join(f'<article class="reading-step"><span class="step-marker">{i+1:02d}</span><div><h3>{esc(s["title"])}</h3><p>{esc(s["detail"])}</p></div></article>' for i,s in enumerate(rec['steps']))
 checks=''.join(f'<label class="check"><input type="checkbox" data-check="{i}"><span>{esc(s)}</span></label>' for i,s in enumerate(rec['checklist']))
 warnings=''.join(f'<li>{esc(w)}</li>' for w in rec['warnings'])
 faqs=''.join(f'<details class="faq"><summary>{esc(q["q"])}</summary><p>{esc(q["a"])}</p></details>' for q in rec['faq'])
 review='Trechos conferidos parcialmente com a fonte; revisão humana pendente.' if rec['source_checked'] else 'Síntese de leitura provisória: confirmar rótulos e conteúdo no manual.'
 navitems=[x for x in INDEX if x['categoria']==group];idx=next(i for i,r in enumerate(navitems) if r['codigo']==code)
 prev=navitems[idx-1]['codigo'] if idx>0 else None;nextn=navitems[idx+1]['codigo'] if idx+1<len(navitems) else None
 adj=(f'<a href="{prev}.html" class="navlink">← {prev}</a>' if prev else '<span></span>') + (f'<a href="{nextn}.html" class="navlink">{nextn} →</a>' if nextn else '<span></span>')
 method='Texto reconhecido automaticamente (OCR)' if rec['source_method']=='ocr_ptbr_provisorio' else 'Texto da camada original do PDF'
 srcfile=ROOT/'fonte-html'/f'p{pg:03d}.html'
 old=srcfile.read_text(encoding='utf-8')
 # The raw prior transcription remains linked and is not duplicated in the main reading pane.
 flowlabel='Fluxo ilustrativo' if rec['kind']=='operational' else 'Mapa de compreensão'
 extra= '<span class="state-provisional">OCR em revisão</span>' if rec['source_method']=='ocr_ptbr_provisorio' else '<span class="state-provisional">Edição técnica em revisão</span>'
 text=f'''<!doctype html>
<html lang="pt-BR"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="index,follow"><meta name="referrer" content="strict-origin-when-cross-origin">
<title>{esc(code)} · {esc(title)} — RAF Serventia Docs</title>
<meta name="description" content="Documentação técnica didática do procedimento {esc(code)}, com diagrama, etapas, checklist e fonte original. Material não oficial em revisão.">
<link rel="stylesheet" href="../assets/css/documentacao.css">
<link rel="stylesheet" href="../assets/css/ux-premium.css">
<script src="../assets/js/pagina.js" defer></script>
<script src="../assets/js/ficha-premium.js" defer></script>
</head><body class="premium-body" data-code="{esc(code)}">
<a class="skip" href="#main">Pular para o conteúdo</a>
<header class="premium-header">
<a class="premium-brand" href="../index.html"><span class="brand-symbol">◆</span><span><b>RAF Serventia</b><small>DOCS · MANUAL INTERATIVO</small></span></a>
<nav class="premium-head-actions" aria-label="Navegação da documentação"><a href="../index.html?tema={esc(group)}#catalogo">← Catálogo</a>
<a href="../docs/manual-fonte.pdf#page={pg}" target="_blank" rel="noopener noreferrer">Fonte PDF ↗</a><button id="theme" type="button" aria-label="Alternar tema">◐</button></nav>
</header>
<main id="main" class="premium-container">
<nav class="premium-breadcrumbs" aria-label="Localização"><a href="../index.html">Documentação</a><span>›</span><a href="../index.html?tema={esc(group)}#catalogo">{esc(rec['section_name'])}</a><span>›</span><span>{esc(code)}</span></nav>
<section class="premium-intro"><div class="premium-intro-copy"><span class="premium-eyebrow">{esc(code)} · FONTE P. {pg}/107</span>
<h1>{esc(title)}</h1><p>{esc(rec['summary'])}</p>
<div class="status-row">{extra}<span>Material não oficial</span><span>{esc(rec['mode'])}</span></div></div>
<div class="premium-intro-side"><span>ORIGEM DOCUMENTAL</span><strong>15.10.2026</strong><p>{esc(method)}</p><a href="../fonte-html/p{pg:03d}.html">Consultar transcrição →</a></div></section>
<div class="premium-tabs" role="tablist" aria-label="Seções do procedimento">
<button role="tab" type="button" data-tab="visao" aria-selected="true">Visão geral</button>
<button role="tab" type="button" data-tab="fluxo" aria-selected="false">{esc(flowlabel)}</button>
<button role="tab" type="button" data-tab="etapas" aria-selected="false">Etapas</button>
<button role="tab" type="button" data-tab="conferencia" aria-selected="false">Conferência</button>
<button role="tab" type="button" data-tab="fonte" aria-selected="false">Fonte original</button>
</div>
<section class="premium-panel" data-panel="visao" id="visao" aria-label="Visão geral">
<div class="premium-panel-head"><span>01 / ESQUEMA VISUAL</span><h2>Entenda a estrutura deste assunto</h2><p>Ilustração vetorial original, preparada especificamente para esta ficha. Não reproduz a interface oficial do PJe.</p></div>
<figure class="premium-illustration"><a href="../assets/illustrations/{esc(code)}.svg" target="_blank" rel="noopener noreferrer" aria-label="Ampliar ilustração em nova aba"><img src="../assets/illustrations/{esc(code)}.svg" alt="{esc(rec['visual']['alt'])}" loading="eager"></a><figcaption>Representação didática da página {pg}. A leitura das etapas deve ser conferida com a fonte.</figcaption></figure>
<div class="quick-notes"><div><span>PARA QUE SERVE</span><p>{esc(rec['summary'])}</p></div><div><span>ESTADO EDITORIAL</span><p>{esc(review)}</p></div></div>
</section>
<section class="premium-panel" data-panel="fluxo" id="fluxo" aria-label="Diagrama interativo">
<div class="premium-panel-head"><span>02 / EXPLORAÇÃO GUIADA</span><h2>{esc(flowlabel)} com explicações</h2><p>Selecione os elementos para ler o significado. A ordem no mapa é de apresentação didática.</p></div>
<figure class="flow-figure"><a href="../assets/flows/{esc(code)}.svg" target="_blank" rel="noopener noreferrer" aria-label="Ampliar o mapa em nova aba"><img src="../assets/flows/{esc(code)}.svg" alt="Mapa vetorial de {esc(title)}. A sequência textual interativa aparece abaixo." loading="lazy"></a><figcaption>Mapa editável derivado de dados JSON do procedimento.</figcaption></figure>
<div class="flow-explorer"><div class="node-list" role="group" aria-label="Elementos do mapa">{''.join(pieces)}</div>
<div class="node-detail" role="status" aria-live="polite"><span id="node-count">SELECIONE UM ELEMENTO</span><h3 id="node-title">Explore o mapa</h3><p id="node-description">Clique ou use Tab e Enter para visualizar a explicação de cada elemento. A transcrição original pode ser consultada na aba Fonte.</p></div></div>
</section>
<section class="premium-panel" data-panel="etapas" id="etapas" aria-label="Etapas explicadas">
<div class="premium-panel-head"><span>03 / LEITURA ORIENTADA</span><h2>Explicação ponto a ponto</h2><p>Os itens abaixo explicam o conteúdo da fonte. Não representam autorização para movimentar autos.</p></div>
<div class="step-list">{steps}</div>
</section>
<section class="premium-panel" data-panel="conferencia" id="conferencia" aria-label="Atenções e checklist">
<div class="premium-panel-head"><span>04 / QUALIDADE E SUPERVISÃO</span><h2>Pontos de atenção e checklist</h2><p>Este checklist verifica a leitura do material. Não registra nenhum ato processual.</p></div>
<div class="conference-layout"><div class="note-panel"><h3>Antes de aplicar</h3><ul>{warnings}</ul><p>Quando houver dúvida, consultar o infográfico original e o servidor responsável.</p></div>
<div class="check-panel"><div class="check-head"><h3>Minha conferência</h3><button id="clearChecks" type="button">Limpar</button></div>{checks}
<p id="checkProgress" aria-live="polite" class="check-progress">0 de {len(rec['checklist'])} itens de leitura conferidos</p></div></div>
<div class="faq-panel"><h3>Perguntas rápidas</h3>{faqs}</div>
</section>
<section class="premium-panel" data-panel="fonte" id="fonte" aria-label="Documentação original">
<div class="premium-panel-head"><span>05 / RASTREABILIDADE</span><h2>Conferência na fonte original</h2><p>Fonte: Manual Operacional do Estagiário na Serventia — PJe, edição de 15/10/2026, página {pg}.</p></div>
<div class="source-actions"><a href="../docs/manual-fonte.pdf#page={pg}" target="_blank" rel="noopener noreferrer" class="primary-action">Abrir página {pg} no PDF ↗</a><a href="../fonte-html/p{pg:03d}.html">Texto extraído e status →</a></div>
<details class="original-image"><summary>Mostrar infográfico original (página {pg})</summary><img src="../assets/thumbs/p{pg:03d}.jpg" alt="Reprodução da página {pg} do manual de referência." loading="lazy"></details>
<p class="editorial-disclaimer">{esc(rec['source_evidence'])} · Documento de uso originalmente classificado como restrito. Divulgação pública pelo autor; não implica homologação do TJRJ.</p>
</section>
<div class="premium-bottom-nav">{adj}</div>
</main><footer class="premium-footer">RAF Serventia Docs · Rafael MS Passos · 2026 · Manual didático não oficial · Página {pg} da fonte</footer>
</body></html>'''
 return text

manifest=[];drafts=[];flows=[]
for item in INDEX:
 rec=make_record(item);code=rec['code'];ill=svg_illustration(item,derive(item));flow=svg_flow(item,derive(item))
 illfile=ROOT/'assets/illustrations'/f'{code}.svg'
 flowfile=ROOT/'assets/flows'/f'{code}.svg'
 illfile.write_text(ill,encoding='utf-8');flowfile.write_text(flow,encoding='utf-8')
 (ROOT/'data/procedures'/f'{code}.json').write_text(json.dumps(rec,ensure_ascii=False,indent=2),encoding='utf-8')
 (ROOT/'data/flows'/f'{code}.json').write_text(json.dumps({'type':rec['kind'],'nodes':rec['nodes'],'edges':rec['edges'],'source_page':rec['source_page']},ensure_ascii=False,indent=2),encoding='utf-8')
 (ROOT/'itens'/f'{code}.html').write_text(render_html(rec),encoding='utf-8')
 manifest.append({'asset_id':f'{code}-illustration-v1','code':code,'source_page':rec['source_page'],
  'illustration':f'assets/illustrations/{code}.svg','flow':f'assets/flows/{code}.svg',
  'sha256':hashlib.sha256(ill.encode('utf-8')).hexdigest(),'bytes':len(ill.encode('utf-8')),
  'alt':rec['visual']['alt'],'dimensions':{'width':1120,'height':560},
  'editorial_status':'draft_human_review_pending','is_original':True,
  'source_image':f'assets/thumbs/p{rec["source_page"]:03d}.jpg'})
 drafts.append({'code':code,'page':rec['source_page'],'source_method':rec['source_method'],
 'source_checked_pilot':rec['source_checked'],'visual_created':True,'flow_created':True,
 'semantic_steps_source_checked':rec['source_checked'],'editorial_approved':False,'qa_passed':False})
(ROOT/'data/assets-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
(ROOT/'data/editorial-audit.json').write_text(json.dumps(drafts,ensure_ascii=False,indent=2),encoding='utf-8')
(ROOT/'data/source-map.json').write_text(json.dumps({r['code']:{'source_page':r['source_page'],'source_method':r['source_method'],'document':'docs/manual-fonte.pdf'} for r in (json.loads((ROOT/'data/procedures'/f'{item["codigo"]}.json').read_text(encoding='utf-8')) for item in INDEX)},ensure_ascii=False,indent=2),encoding='utf-8')
print('ILLUSTRATED_BUILD_OK',len(manifest),'original illustrations',len(manifest),'flow SVGs','96 structured drafts')
