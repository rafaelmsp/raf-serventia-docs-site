"""RAF Serventia Docs: premium art program for 90 remaining lesson pages.
Output: 90 unique large illustrative SVG scenes + 90 unique five-part visual maps.
Separate from original 6 authored pilots; preserves their visual work.
Every graphic is a simulated educational scene, never a PJe screenshot.
Individual headings ground to title and sourced labels when reliable.
"""
from pathlib import Path
import re,json,math,hashlib,textwrap
from xml.sax.saxutils import escape as xe
ROOT=Path(__file__).resolve().parents[1]
INDEX=json.loads((ROOT/'dados/procedimentos.json').read_text(encoding='utf-8'))
SOURCE={x['pagina']:x for x in json.loads((ROOT/'dados/conteudo_integral.json').read_text(encoding='utf-8'))}
PILOTS={'O-03','O-08','P-01','R-01','BF-01','BV-01'}
COLORS={'O':('#1688CE','#71D2F5'),'P':('#8A62DD','#D0B4FA'),'R':('#129B84','#92E5D4'),
        'BF':('#D58B3A','#F5D89C'),'BV':('#467DDC','#ACC7F9')}
def e(t):return xe(str(t),{'"':'&quot;'})
def rect(x,y,w,h,fill='#FFFFFF',r=13,stroke=None,sw=1):
 return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}"'+(f' stroke="{stroke}" stroke-width="{sw}"' if stroke else '')+'/>'
def circle(x,y,r,fill,stroke=None):
 return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}"'+(f' stroke="{stroke}" stroke-width="2"' if stroke else '')+'/>'
def path(d,stroke='#80AAC7',width=3,fill='none'):
 return f'<path d="{d}" stroke="{stroke}" stroke-width="{width}" fill="{fill}" stroke-linecap="round" stroke-linejoin="round"/>'
def text(x,y,s,size=18,col='#143E5B',bold=False,anchor='start'):
 return f'<text x="{x}" y="{y}" font-family="Arial,Segoe UI,sans-serif" font-size="{size}" font-weight="{800 if bold else 500}" fill="{col}" text-anchor="{anchor}">{e(s)}</text>'
def wrapped(s,limit=27,maxlines=2):
 words=str(s).strip().split();out=[];temp=''
 for word in words:
  if len(temp+' '+word)>limit and temp:out.append(temp);temp=word
  else:temp=(temp+' '+word).strip()
 if temp:out.append(temp)
 if len(out)>maxlines:out=out[:maxlines];out[-1]=out[-1][:max(0,limit-1)]+'…'
 return out
def multiline(x,y,s,limit=27,maxlines=2,size=18,color='#143E5B',gap=25,bold=True,anchor='start'):
 return ''.join(text(x,y+i*gap,l,size,color,bold,anchor) for i,l in enumerate(wrapped(s,limit,maxlines)))
def icon(x,y,k,accent='#1981B5',scale=1):
 # Vector icons that do not depend on external fonts.
 transform=f'transform="translate({x} {y}) scale({scale})"'
 common={'file':'M12 4H32L42 14V52H12Z M32 4V14H42 M19 26H35 M19 34H34 M19 42H31',
         'calendar':'M8 14H45V49H8Z M8 25H45 M16 7V20 M36 7V20 M16 33H24 M30 33H39 M16 41H24',
         'person':'M26 26A10 10 0 1 0 25 26 M8 52Q9 29 26 31Q42 30 44 52',
         'scale':'M24 9V49 M9 14H41 M10 18L4 36H18Z M40 18L34 36H48Z M16 49H34',
         'lock':'M14 26V18A12 12 0 0 1 38 18V26 M10 26H42V50H10Z M26 34V41',
         'branch':'M24 8V46 M24 23H44V12 M24 36H6V45 M20 6H29V14H20Z M40 9H48V17H40Z M2 42H11V51H2Z',
         'chart':'M8 48V30H18V48 M23 48V18H33V48 M38 48V9H48V48 M5 51H52',
         'message':'M8 10H47V42H24L12 51V42H8Z M16 21H40 M16 29H36',
         'warning':'M27 5L3 49H51Z M27 21V34 M27 40V42',
         'clock':'M26 4A22 22 0 1 0 26 48A22 22 0 1 0 26 4 M26 12V26L36 32',
         'meeting':'M8 14H48V43H8Z M18 50H38 M27 43V50 M20 27H36 M8 12H48',
         'money':'M8 12H47V47H8Z M27 22A8 8 0 1 0 27 38A8 8 0 1 0 27 22 M12 20H16 M39 39H44',
         'list':'M8 10H15V17H8Z M21 14H49 M8 25H15V32H8Z M21 29H49 M8 40H15V47H8Z M21 44H49',
         'arrow':'M4 27H50 M35 11L51 27L35 43',
         'shield':'M27 4L46 12V29Q44 42 27 50Q10 42 8 29V12Z M18 27L25 34L38 19',
         'folder':'M5 15H24L30 21H49V48H5Z M5 15V11H23L27 16',
         'check':'M11 28L22 39L45 15'}
 d=common.get(k,common['file'])
 return f'<g {transform}><path d="{d}" fill="none" stroke="{accent}" stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round"/></g>'
def identify(row):
 s=row['titulo'].lower()
 if row['categoria']=='BV':return 'video'
 if row['categoria']=='BF':return 'service'
 if row['categoria']=='P':return 'calendar'
 if row['categoria']=='R':return 'metrics'
 for kws,kind in [
 (['sisbajud','bloqueio','pagamento','transferência','teimosinha'],'finance'),
 (['sigilo','habilitação','cadastro de participantes','corrigir partes','retificar autuação'],'privacy'),
 (['árvore','autos digitais','eventos','leitura','triagem'],'tree'),
 (['certidão','petição','documento','mandado','carta precatória','perito'],'document'),
 (['intimação','citação','ar ','ato de comunicação','expedição'],'message'),
 (['conclusão','gabinete','juiz leigo','tutela','liminar'],'decision'),
 (['prazo','execução','cumprimento','recurso','recurso inominado','trânsito','sentença'],'timeline'),
 (['arquivamento','desarquivamento','redistribuição','suspensão'],'folder')]:
  if any(k in s for k in kws):return kind
 return 'workflow'
ICON={'tree':'branch','document':'file','message':'message','calendar':'calendar','metrics':'chart','service':'person',
      'video':'meeting','finance':'money','privacy':'lock','decision':'scale','timeline':'clock','folder':'folder','workflow':'list'}
def reliable_line(s):
 s=s.strip()
 if not (6<=len(s)<=54):return False
 if any(a in s.lower() for a in ('lgpd','página','copyright','rafael','celERIDADE'.lower(),'justiça mais','poder judiciário','oab ','tribunal de justiça','manual do estagiário','jéc','j.e.c')):return False
 if re.search(r'[\[\]{}<>ªº§~•\\|]',s):return False
 if len(re.findall(r'[a-zA-ZÀ-ÿ]',s))<len(s)*.68:return False
 if len(re.findall(r'[A-ZÀ-Ü]',s))>3 and s.count(' ')>8:return False
 return True
def topics(row):
 # Source-derived short labels, not claimed to be authorized actions.
 src=SOURCE[row['pagina']]['linhas']
 original=next((x['titulo'] for x in INDEX if x['codigo']==row['codigo']),row['titulo'])
 headings=[];keys=set()
 for l in src:
  s=' '.join(l.strip().split());n=s.casefold()
  if not reliable_line(s) or n in keys or n==row['titulo'].casefold():continue
  if s.upper()==s and len(s)<=38 or s.startswith(('1 ','2 ','3 ','4 ','5 ')) and len(s)<=50:
   headings.append(s.title() if s.upper()==s else s);keys.add(n)
 if len(headings)<3:
  for l in src:
   s=' '.join(l.strip().split());n=s.casefold()
   if reliable_line(s) and n not in keys and len(s)<=34:
    headings.append(s);keys.add(n)
   if len(headings)>=5:break
 def cleaner(s):
  s=' '.join(re.sub(r'[^\wÀ-ÿ\s\-\/]', '', s).split())
  if len(s)>36:s=s[:34].rstrip()+'…'
  return s
 vals=[cleaner(x) for x in headings if x]
 fallback={'tree':['Origem do processo','Histórico processual','Atos e documentos','Providência a verificar'],
 'document':['Peça/documento','Conferência','Informação registrada','Encaminhamento supervisionado'],
 'message':['Comunicação','Destinatário','Comprovação','Pendência'],
 'calendar':['Audiência','Pauta','Documentos','Encaminhamento'],
 'metrics':['Indicadores','Período analisado','Proporções','Alertas'],
 'service':['Atendimento','Identificação','Conferência','Encaminhamento'],
 'video':['Solicitação','Identificação','Atendimento','Encerramento'],
 'finance':['Determinação','Resultado','Valores','Análise supervisionada'],
 'privacy':['Solicitante','Permissão de acesso','Documentos','Sigilo'],
 'decision':['Pedido','Autos','Ato judicial','Encaminhamento'],
 'timeline':['Marco inicial','Movimentações','Prazo','Conferência'],
 'folder':['Histórico','Tarefa','Estado atual','Providência'],
 'workflow':['Localizar','Examinar','Conferir','Encaminhar']}
 k=identify(row)
 if row['origemTexto']!='camada_textual_pdf':
  # Reject OCR headings that may be garbled; title grounded + standard source concerns.
  vals=[original]+fallback[k][:3]
 else:
  vals=vals[:4]
  if len(vals)<4:vals+=fallback[k][:4-len(vals)]
 return vals[:4]
def canvas(row,label):
 color,light=COLORS[row['categoria']]
 s=(f'<defs><linearGradient id="bg" x2="1" y2="1"><stop stop-color="#0D2B45"/><stop offset="1" stop-color="#17466A"/></linearGradient>'
    f'<filter id="s"><feDropShadow dx="0" dy="12" stdDeviation="17" flood-color="#0B2030" flood-opacity=".19"/></filter></defs>')
 s+=rect(0,0,1200,760,'url(#bg)',25)+circle(1080,75,225,'#225879')+circle(1080,75,165,'#214E70')
 s+=circle(78,735,195,'#1E5272')
 s+=text(54,64,'RAF SERVENTIA DOCS  /  '+row['codigo'],20,'#CBE6F5',True)
 s+=multiline(54,111,row['titulo'],57,2,34,'#FFFFFF',39)
 s+=text(54,180,label,17,'#B9D9E9')
 s+=rect(975,50,168,42,color,21)+text(1059,78,'ILUSTRAÇÃO',15,'#FFFFFF',True,'middle')
 s+=rect(50,690,1100,43,'#09273E',12)+text(69,719,'CENA DIDÁTICA FICTÍCIA • CONFERIR MANUAL P. '+str(row['pagina'])+' • NÃO É TELA OFICIAL DO PJe',14,'#C0D9E9',True)
 return s
def frame(row,body,label='Simulação para entender o assunto',height=760):
 svg=(f'<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="{height}" viewBox="0 0 1200 {height}" '
      f'role="img" aria-labelledby="title desc"><title id="title">{e(row["codigo"])} — {e(row["titulo"])}</title>'
      f'<desc id="desc">Ilustração original para aprendizado do tema com elementos fictícios; consulte a página {row["pagina"]} do manual e peça supervisão.</desc>'
      +canvas(row,label)+body+'</svg>')
 return svg

def motif_tree(row,color,seed):
 z='<path d="M 310 618 C 307 530 322 483 325 440 M325 477L214 393 M324 438L447 347 M312 429L263 320 M332 427L402 300" fill="none" stroke="#9A744A" stroke-width="24" stroke-linecap="round"/>'
 for x,y in [(204,375),(250,307),(401,275),(445,329),(317,280),(179,280),(425,421)]:
  z+=f'<ellipse cx="{x+5*(seed%4)}" cy="{y}" rx="73" ry="49" fill="#238A77" opacity=".78"/>'
 z+=path('M315 590 Q270 625 209 635 M315 590 Q366 622 421 636','#AB8456',9)
 for i,(x,y) in enumerate([(220,390),(401,336),(296,265),(352,485)]):
  z+=circle(x,y,24,color,'#F3FCFF')+text(x,y+7,str(i+1),18,'#FFFFFF',True,'middle')
 return z
def motif_calendar(row,color,seed):
 z=rect(108,258,510,349,'#FFFFFF',20,'#C8DCE8',2)
 z+=rect(108,258,510,74,color,20)+rect(108,307,510,25,color,0)
 z+=text(140,305,'AGENDA DIDÁTICA',23,'#FFFFFF',True)
 for c in range(7):
  x=140+c*64
  z+=text(x,365,'DSTQQSS'[c],13,'#60819B',True,'middle')
  for k in range(4):
   y=386+k*47
   z+=rect(x-22,y-17,47,39,'#F0F6FB' if (c+k+seed)%5!=0 else '#DCEBF7',9,'#DFEAF2')
   z+=text(x+2,y+8,str((c+1)+(k*7)),16,'#426984',True,'middle')
 z+=rect(150,581,424,22,'#DBF3EE',7)
 return z
def motif_document(row,color,seed):
 z=rect(119,278,498,320,'#F9FCFF',16,'#BDD3E2',1.5)
 z+=rect(139,294,458,58,'#EAF4FC',9)+text(163,332,'DOCUMENTO FICTÍCIO',20,'#2B648A',True)
 for i in range(6):
  z+=rect(160,384+i*30,352-(i%3)*47,10,'#BFCFDC' if i%3 else '#96C8E6',4)
 z+=rect(159,566,195,18,'#DDEDF8',5)
 z+=icon(439,501,'file',color,1.2)
 return z
def motif_message(row,color,seed):
 z=rect(99,277,530,324,'#E8F3FA',23,'#B2D7EB',1.5)
 z+=rect(130,299,331,94,'#FFFFFF',20,'#C1D7E6')
 z+=multiline(152,337,'Comunicação processual',25,2,20,'#235B7D',26)
 z+=rect(234,410,358,94,'#D2F1EA',20,'#95D8C5')
 z+=multiline(256,448,'Identificar destinatário',26,2,18,'#1E6E5D',24)
 z+=rect(125,525,344,55,'#FFFFFF',14)+text(147,559,'CONFIRA O DOCUMENTO',16,'#236C98',True)
 return z
def motif_service(row,color,seed):
 z=rect(109,266,527,347,'#E6F1FA',20,'#BAD7E9',2)
 z+=circle(267,382,66,'#327FA7')+circle(267,367,35,'#DBAC88')
 z+=path('M194 489Q200 414 267 424Q337 414 345 489Z','#0A6A94',3,'#176FA1')
 z+=circle(504,399,58,'#52A9A0')+circle(504,383,33,'#C58F73')
 z+=path('M442 508Q450 426 504 438Q560 429 566 508Z','#188476',3,'#208D81')
 z+=rect(150,523,431,62,'#1C6187',12)+rect(148,513,431,11,'#90C6E3',5)
 z+=rect(290,291,202,66,'#FFFFFF',14,'#D0DEE9')
 z+=text(393,320,'Como posso',16,'#31647F',True,'middle')+text(393,343,'ajudar?',16,'#31647F',True,'middle')
 return z
def motif_video(row,color,seed):
 z=rect(103,278,530,320,'#203C57',18,'#6FA8CA',2)
 for i,(x,c) in enumerate([(122,'#2D718E'),(368,'#208D80')]):
  z+=rect(x,305,230,233,c,15)+circle(x+114,374,48,'#D1A182')
  z+=path(f'M{x+60} 493Q{x+68} 425 {x+115} 434Q{x+169} 422 {x+182} 493Z','#DDECF8',3,'#123F69' if i==0 else '#0B6E63')
  z+=rect(x+17,507,156,22,'#142E45',7)
 z+=rect(254,558,246,31,'#345B77',15)
 for i in range(3):z+=circle(309+i*66,573,11,'#D6E7F2' if i!=2 else '#C95B62')
 return z
def motif_metrics(row,color,seed):
 z=rect(116,275,514,327,'#F8FCFE',19,'#C6D8E4',2)
 z+=text(152,319,'PAINEL ILUSTRATIVO',19,'#356F98',True)
 for i,(x,h) in enumerate([(171,71),(241,130),(311,98),(381,154),(451,118)]):
  z+=rect(x,547-h,44,h,['#3A91C9','#1A9A8D','#8262D9','#53ADD8','#D69643'][i],7)
 z+=path('M157 551H530','#7294B2',3)
 z+=circle(519,345,52,'#DFF3EB')+text(519,351,'%',39,'#238A78',True,'middle')
 return z
def motif_finance(row,color,seed):
 z=rect(113,284,514,300,'#ECF4FA',19,'#C1D8E7',1.5)
 z+=rect(145,303,448,94,'#FFFFFF',14)+icon(155,318,'money',color,1.03)
 z+=text(233,346,'CONTROLE DE VALORES',18,'#286B91',True)
 z+=text(235,376,'Exemplo inteiramente fictício',14,'#66859A')
 z+=rect(145,420,448,144,'#FFFFFF',13)
 for i in range(3):
  z+=circle(180,453+i*39,11,['#249D84','#D19C3C','#8D6DD6'][i])
  z+=rect(208,449+i*39,315-i*38,10,'#C2DAE9',6)
 return z
def motif_privacy(row,color,seed):
 z=rect(126,268,492,330,'#F2F8FD',20,'#C2D8E8',2)
 z+=path('M367 292L529 350V440Q514 527 367 586Q222 528 207 440V350Z',color,7,'#E7F8F1')
 z+=icon(287,379,'lock','#208775',1.7)+text(364,513,'ACESSO',23,'#235E7A',True,'middle')
 return z
def motif_decision(row,color,seed):
 z=rect(128,282,487,319,'#F5F9FD',17,'#C9DDE9')
 z+=rect(162,311,419,67,'#FFFFFF',10,'#C6DCE8')+text(191,355,'PEDIDO / DETERMINAÇÃO',18,'#2E6C98',True)
 z+=path('M367 401L511 460L367 529L223 460Z',color,4,'#E5F1F9')
 z+=text(367,453,'O QUE FOI',20,'#255A78',True,'middle')
 z+=text(367,476,'DETERMINADO?',20,'#255A78',True,'middle')
 z+=path('M223 460H165 M511 460H562','#7DAAC7',3)
 return z
def motif_timeline(row,color,seed):
 z=rect(102,277,519,314,'#F8FCFE',20,'#BED7E8')
 z+=path('M148 424H567','#A4C9DF',7)
 for i,(x,yy) in enumerate([(161,420),(288,420),(417,420),(547,420)]):
  z+=circle(x,yy,27,['#418CB8','#25A28B','#C68C37','#8762D0'][i])
  z+=text(x,yy+7,i+1,20,'#FFF',True,'middle')
  z+=rect(x-52,318 if i%2==0 else 473,105,55,'#EBF5FC',10,'#C9DEEB')
  z+=text(x,350 if i%2==0 else 506,['MARCO','ATO','PRAZO','RETORNO'][i],12,'#326D91',True,'middle')
 return z
def motif_folder(row,color,seed):
 z=rect(138,338,464,234,'#FFFFFF',17,'#AFCDE2',2)
 z+=path('M139 367L139 319H299L340 355H601V562H139Z',color,5,'#E5F1FB')
 z+=icon(310,414,'folder',color,1.6)+text(368,506,'ACERVO',20,'#2A698E',True,'middle')
 return z
def motif_workflow(row,color,seed):
 z=rect(110,283,510,311,'#F9FCFE',19,'#C7DCEB')
 for i in range(4):
  y=312+i*67
  z+=circle(150,y+13,17,['#2486C3','#2F9E94','#C49043','#8563CF'][i])
  z+=text(150,y+20,i+1,14,'#FFF',True,'middle')
  z+=rect(183,y-5,383,44,'#EAF3FB',10)
  z+=rect(202,y+10,172+i*31,10,'#B5D1E4',5)
 return z
MOTIFS={'tree':motif_tree,'document':motif_document,'message':motif_message,'calendar':motif_calendar,
 'metrics':motif_metrics,'service':motif_service,'video':motif_video,'finance':motif_finance,
 'privacy':motif_privacy,'decision':motif_decision,'timeline':motif_timeline,'folder':motif_folder,
 'workflow':motif_workflow}

def premium_scene(row):
 seed=int(re.findall(r'\d+',row['codigo'])[-1])
 kind=identify(row);color,light=COLORS[row['categoria']]
 words=topics(row)
 body=''
 # Rich simulated instructional interface with distinct semantic motif and side annotations.
 body+=rect(65,212,1070,439,'#E9F3FB',20,'#B6D5E6',2)
 body+=rect(83,231,1034,44,'#FFFFFF',11)
 for j,c in enumerate(['#C75F5F','#E8BA68','#5FBF9E']):body+=circle(104+j*22,253,6,c)
 body+=text(197,260,'PAINEL DE ESTUDO / '+row['codigo'],17,'#4D738E',True)
 body+=rect(84,292,572,333,'#F6FAFD',16)
 body+=MOTIFS[kind](row,color,seed)
 # four clickable concept cards represented by numbered vector overlays.
 body+=rect(675,292,421,333,'#F5FAFD',14,'#C9DCE9')
 body+=text(699,327,'O QUE OBSERVAR',17,'#2D6488',True)
 for i,label in enumerate(words[:4]):
  y=344+i*66
  bg='#FFFFFF' if i%2==0 else '#E9F4FB'
  body+=rect(695,y,377,59,bg,10,'#D3E5F0')
  body+=circle(720,y+29,18,color)
  body+=text(720,y+35,str(i+1),16,'#FFFFFF',True,'middle')
  body+=multiline(749,y+24,label,31,2,15,'#234F6B',19)
 body+=rect(685,616,402,21,'#E9F3FA',9)
 return frame(row,body,'Leitura ilustrada — consulte o manual para confirmar os detalhes')
def educational_map(row):
 color,light=COLORS[row['categoria']]
 labels=topics(row)
 w,h=1200,670
 svg='<defs><linearGradient id="bg" x2="1" y2="1"><stop stop-color="#0E2D47"/><stop offset="1" stop-color="#1A5274"/></linearGradient><filter id="sd"><feDropShadow dx="0" dy="7" stdDeviation="9" flood-color="#041827" flood-opacity=".20"/></filter></defs>'
 svg+=rect(0,0,w,h,'url(#bg)',27)+circle(1075,80,220,'#1A4E70')
 svg+=text(50,62,'RAF SERVENTIA DOCS  /  '+row['codigo'],19,'#C0DFF0',True)
 svg+=multiline(50,112,row['titulo'],55,2,30,'#FFFFFF',36)
 svg+=text(51,185,'MAPA DE COMPREENSÃO  •  TÓPICOS DA FONTE',15,'#B6D8E9',True)
 xs=[63,350,637,924]
 for i,label in enumerate(labels):
  x=xs[i];y=250+((i+int(re.findall(r'\d+',row['codigo'])[-1]))%2)*21
  svg+=rect(x,y,241,235,'#F7FBFD',17,'#BBD5E5',2)
  svg+=rect(x,y,241,63,color,16)+rect(x,y+45,241,18,color,0)
  svg+=circle(x+34,y+30,19,'#FFFFFF')+text(x+34,y+36,i+1,17,color,True,'middle')
  svg+=icon(x+77,y+17,ICON[identify(row)],'#FFFFFF',.6)
  svg+=multiline(x+23,y+114,label,24,2,18,'#1B4D6E',24)
  svg+=rect(x+23,y+169,192,2,'#DDE9F0',1)
  svg+=text(x+24,y+197,'Revisar na fonte',13,'#64849A',True)
  if i<3:
   svg+=path(f'M{x+245} {y+115}h30','#9CD0ED',3.4)
   svg+=path(f'M{x+261} {y+107}l13 8 -13 8','#9CD0ED',3)
 svg+=rect(53,549,1092,72,'#143E59',12)
 svg+=icon(69,558,'shield','#A0E5D3',.75)
 svg+=text(130,579,'Esta é uma sequência de LEITURA, não uma ordem para executar atos.',19,'#E5F5FD',True)
 svg+=text(131,604,f'Material de treinamento não oficial; confira a página {row["pagina"]} e as atribuições do servidor.',14,'#BAD8EA')
 out=f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title desc"><title id="title">Mapa de estudo de {e(row["titulo"])}</title><desc id="desc">Quatro tópicos de leitura para o assunto, sem substituir procedimento oficial nem criar instruções não revisadas.</desc>{svg}</svg>'
 return out
def run():
 manifest=ROOT/'data'/'learning-visuals-manifest.json'
 older=json.loads(manifest.read_text(encoding='utf-8')) if manifest.exists() else []
 records={x['code']:x for x in older}
 results=[];new=0
 for row in INDEX:
  code=row['codigo'];base=ROOT/'assets'/'learning'/code
  base.mkdir(parents=True,exist_ok=True)
  if code not in PILOTS:
   scene=premium_scene(row);diagram=educational_map(row)
   (base/'ilustracao-premium.svg').write_text(scene,encoding='utf-8')
   (base/'fluxo-premium.svg').write_text(diagram,encoding='utf-8')
   record={'code':code,'reference_page':row['pagina'],
    'illustration':f'assets/learning/{code}/ilustracao-premium.svg',
    'flow':f'assets/learning/{code}/fluxo-premium.svg',
    'sha_illustration':hashlib.sha256(scene.encode()).hexdigest(),
    'sha_flow':hashlib.sha256(diagram.encode()).hexdigest(),
    'visual_family':identify(row),
    'source_method':row['origemTexto'],
    'source_label_status':'source_text' if row['origemTexto']=='camada_textual_pdf' else 'topic_and_safety_labels_not_checked_OCR',
    'review':'conceptual illustration; legal/pedagogical checking pending',
    'fictitious':True,'alt':f'Ilustração de {row["titulo"]}, cenário fictício sem interface real do tribunal.'}
   results.append(record);new+=1
  else:
   if code in records:results.append(records[code])
   else:
    results.append({'code':code,'illustration':f'assets/learning/{code}/ilustracao-premium.svg',
      'flow':f'assets/learning/{code}/fluxo-premium.svg','reference_page':row['pagina'],
      'review':'six source-grounded pilot diagrams; pedagogical approval pending'})
 manifest.write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
 print('VISUALS_COMPLETED',len(results),'NEW',new,'PILOTS_PRESERVED',len(PILOTS))
if __name__=='__main__':run()
