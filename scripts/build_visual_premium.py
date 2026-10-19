"""RAF Serventia Docs | visual premium art direction, 2026
Six original vector lesson illustrations and six step diagrams.
Only fictitious UI, documents and scenarios. Never render actual PJe branding.
Reproducible SVG, accessible title/desc, no external font or image references.
"""
from pathlib import Path
from xml.sax.saxutils import escape
import json, math, hashlib
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'assets'/'learning'
DATA=ROOT/'data'/'lessons'
SECTIONS={
'O':('#1688D0','#65C4F6'), 'P':('#865CE5','#D1BCFF'),
'R':('#16A585','#88E1CE'), 'BF':('#D99840','#F3D391'),
'BV':('#497FEA','#A9C8FC')}
def e(s):return escape(str(s), {'"':'&quot;'})
def tag(t,attrs='',body=''):return f'<{t} {attrs}>{body}</{t}>'
def rect(x,y,w,h,fill='#ffffff',rx=16,stroke=None,sw=1,extra=''):
 return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}"'+(f' stroke="{stroke}" stroke-width="{sw}"' if stroke else '')+(' '+extra if extra else '')+'/>'
def circ(x,y,r,fill,stroke=None,sw=1):
 return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}"'+(f' stroke="{stroke}" stroke-width="{sw}"' if stroke else '')+'/>'
def line(x1,y1,x2,y2,col='#ABCADB',w=2,style=''):
 return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{col}" stroke-width="{w}" stroke-linecap="round" '+style+'/>'
def path(d,col='#9CC7DE',w=3,fill='none',style=''):
 return f'<path d="{d}" stroke="{col}" stroke-width="{w}" fill="{fill}" stroke-linejoin="round" stroke-linecap="round" {style}/>'
def t(x,y,s,size=19,col='#17344C',weight=500,anchor='start',extra=''):
 return f'<text x="{x}" y="{y}" font-family="Segoe UI,Arial,sans-serif" font-size="{size}" font-weight="{weight}" fill="{col}" text-anchor="{anchor}" {extra}>{e(s)}</text>'
def mtext(x,y,lines,size=16,col='#5F788B',gap=25,weight=500):
 return ''.join(t(x,y+i*gap,txt,size,col,weight) for i,txt in enumerate(lines))
def shadow():return 'filter="url(#ds)"'
def iconcheck(cx,cy,color='#149B80'):
 return circ(cx,cy,12,color)+path(f'M {cx-6} {cy} l4 4 8 -9','#FFFFFF',2.6)
def no(cx,cy,color='#C4544C'):
 return circ(cx,cy,12,color)+line(cx-4,cy-4,cx+4,cy+4,'#FFF',2.5)+line(cx+4,cy-4,cx-4,cy+4,'#FFF',2.5)
def badge(x,y,label,accent='#1782C4',w=160):
 return rect(x,y,w,35,accent,17)+t(x+w/2,y+23,label,13,'#FFF',800,'middle')
def pin(x,y,number,accent='#1389C8',r=19):
 return circ(x,y,r,accent,'#FFFFFF',3)+t(x,y+6,number,18,'#FFFFFF',800,'middle')
def paper(x,y,w,h,title='DOCUMENTO FICTÍCIO'):
 v=rect(x,y,w,h,'#FFFFFF',12,'#CBD9E6',1.5,shadow())
 v+=rect(x+14,y+16,w-28,31,'#ECF4FB',6)+t(x+25,y+37,title,14,'#1C5377',800)
 for i,l in enumerate([.80,.70,.92,.66,.80,.45]):
  v+=rect(x+24,y+72+i*26,(w-48)*l,7,'#CAD8E4',3)
 return v
def arrow(x1,y1,x2,y2,clr='#6F9AB6'):
 return line(x1,y1,x2,y2,clr,3)+path(f'M{x2-9} {y2-6}L{x2} {y2}L{x2-9} {y2+6}',clr,2.6)
def person(cx,cy,shirt='#116F9B',skin='#D99D7C',hair='#203D54',scale=1):
 # Bust illustration: silhouette without personal characteristics
 r=31*scale
 return (circ(cx,cy-35*scale,r,skin)+
         path(f'M {cx-r*.98} {cy-40*scale} q{-r*.1} {-r*1.3} {r} {-r*1.25} q{r*1.3} {r*.05} {r*.9} {r*1.4}',hair,13*scale)+
         f'<path d="M {cx-57*scale} {cy+74*scale} q {8*scale} {-80*scale} {57*scale} {-60*scale} q{52*scale} {-13*scale} {60*scale} {60*scale}Z" fill="{shirt}"/>'+
         path(f'M{cx-20*scale} {cy-9*scale}Q{cx} {cy+6*scale} {cx+18*scale} {cy-8*scale}','#A86153',1.7))
def window(x,y,w,h,name,accent='#1676B7'):
 z=rect(x,y,w,h,'#FFFFFF',19,'#CCDCE8',1.5,shadow())
 z+=rect(x,y,w,48,'#F0F6FB',19)+rect(x,y+26,w,22,'#F0F6FB',0)
 z+=circ(x+24,y+24,6,'#D27D79')+circ(x+43,y+24,6,'#ECC16F')+circ(x+62,y+24,6,'#86C8AF')
 z+=t(x+90,y+30,name,16,'#35566C',700)
 return z
def cover(code,title,subtitle,body,accent=None,w=1200,h=760):
 cat=code.split('-')[0]
 if accent is None:accent=SECTIONS[cat][0]
 defs="""<defs>
 <linearGradient id="bg" x2="1" y2="1"><stop stop-color="#0C2942"/><stop offset=".60" stop-color="#15446A"/><stop offset="1" stop-color="#0F2E4B"/></linearGradient>
 <linearGradient id="card" x2="0" y2="1"><stop stop-color="#FFFFFF"/><stop offset="1" stop-color="#E9F3FB"/></linearGradient>
 <filter id="ds" x="-20%" y="-25%" width="150%" height="175%"><feDropShadow dx="0" dy="10" stdDeviation="14" flood-color="#061C2B" flood-opacity=".20"/></filter>
 <marker id="end" markerWidth="10" markerHeight="10" refX="6" refY="3" orient="auto"><path d="M 0 0 L 6 3 L 0 6" fill="none" stroke="#7CAFC7" stroke-width="1.4"/></marker>
 </defs>"""
 scaffold=rect(0,0,w,h,'url(#bg)',28)
 scaffold+=circ(1050,130,245,accent)+circ(1050,130,213,'#113958')+circ(185,700,185,'#1E5579')
 scaffold+=t(52,62,'RAF SERVENTIA DOCS',19,'#BADAF0',800,extra='letter-spacing="2"')
 scaffold+=t(52,111,title,36,'#FFFFFF',800)
 scaffold+=t(53,147,subtitle,18,'#C2DFEF')
 scaffold+=badge(942,50,'CENA SIMULADA',accent,206)
 scaffold+=rect(52,691,1096,43,'#09243D',13)+t(75,719,'MODELO PARA TREINAMENTO · DADOS FICTÍCIOS · NÃO É UMA TELA OFICIAL DO PJe',15,'#B0D2E7',700)
 return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="ti de"><title id="ti">{e(code)} — {e(title)}</title><desc id="de">{e(subtitle)}. Diagrama ilustrativo. Não é captura nem material oficial do PJe.</desc>{defs}{scaffold}{body}</svg>'

def scene_tree():
 z=window(68,188,1065,465,'VISUALIZADOR DE AUTOS — EXEMPLO FICTÍCIO')
 # navigation sidebar
 z+=rect(83,247,115,384,'#EAF2F9',11)
 for i,(txt1,col) in enumerate([('Autos','#328BBD'),('Peças','#83A2BA'),('Histórico','#328BBD'),('Tarefas','#83A2BA'),('Ajuda','#83A2BA')]):
  yy=292+i*58
  z+=circ(109,yy-7,12,col)+t(133,yy,txt1,13,'#416782',700)
 # process tree
 z+=rect(215,250,405,381,'#F8FBFD',12,'#D8E4EC')
 z+=t(239,280,'LINHA DO TEMPO DOS AUTOS',15,'#4F7794',800)
 entries=[('Petição inicial','Origem · peça 01','#2E83C9'),('Despacho','Ato judicial · peça 02','#B08734'),
 ('Citação','Comunicação · peça 03','#2CA1A8'),('Certidão','Registro · peça 04','#20A28C'),
 ('Manifestação','Resposta · peça 05','#8562D7')]
 z+=line(253,331,253,570,'#A9C6DB',5)
 for i,(head,sub,c) in enumerate(entries):
  y=330+i*57
  z+=circ(253,y,12,c,'#FFFFFF',2)+t(280,y+2,head,16,'#1F485F',800)+t(281,y+23,sub,12,'#6A8798')
 z+=badge(425,574,'5 eventos fictícios','#E7F1F8',175)
 # Overwrite badge label color? default white invisible due light. Draw overlay
 z+=t(512,596,'CONFERÊNCIA',13,'#256A99',800,'middle')
 # Document pane
 z+=rect(632,249,482,382,'#E7F0F8',12)
 z+=rect(649,263,446,43,'#FFFFFF',10)
 z+=t(671,290,'Peça selecionada: CERTIDÃO',17,'#274E68',800)
 z+=paper(674,318,396,270,'DOCUMENTO SIMULADO')
 z+=rect(698,555,245,11,'#BED3E2',5)
 # five visual pins referencing textual hotspots
 for num,x,y,col in [(1,239,334,'#176FAB'),(2,254,391,'#D99A2D'),(3,253,449,'#0A9591'),(4,252,504,'#3D8C8E'),(5,953,324,'#835BDD')]:
  z+=pin(x,y,str(num),col,15)
 z+=rect(864,585,224,32,'#DDF3ED',12)
 z+=iconcheck(884,601,'#238C71')+t(903,607,'Leia a peça antes de concluir',12,'#236852',700)
 return cover('O-03','Anatomia da Árvore do Processo',
              'Leia a sequência e abra a peça correspondente a cada evento.',z)
def scene_pac():
 z=''
 z+=rect(64,185,1070,450,'#F5FAFE',20,'#A8D0E6',1.5,shadow())
 z+=t(96,228,'COMO CONFERIR UMA PENDÊNCIA?',23,'#173D58',800)
 # action progression
 nodes=[('1','O que falta?','Identifique a falha','#197EB8'),
 ('2','O que foi pedido?','Leia a determinação','#187EB8'),
 ('3','A quem e quando?','Confirme destinatário','#197EB8')]
 for i,(number,title,desc,c) in enumerate(nodes):
  x=98+i*343
  z+=rect(x,272,300,118,'#FFFFFF',14,'#D1E1EB',1.5)
  z+=pin(x+32,304,number,c,19)+t(x+62,311,title,17,'#224960',800)
  z+=t(x+26,357,desc,14,'#6A8496')
  if i<2:z+=arrow(x+302,335,x+338,335,'#729FB8')
 z+=arrow(589,390,589,426)
 # decision diamond, branches
 z+=f'<path d="M589 420 L760 485 L589 550 L418 485 Z" fill="#DDF0FA" stroke="#3188BD" stroke-width="3"/>'
 z+=t(589,478,'A resposta',19,'#1D5476',800,'middle')+t(589,502,'cumpriu?',19,'#1D5476',800,'middle')
 for x,col,name in [(158,'#1A987F','Integral'),(480,'#C98B31','Parcial'),(822,'#D16057','Não cumpriu')]:
  z+=rect(x,570,220,45,col,12)+t(x+110,600,name,16,'#FFF',800,'middle')
 # branch connectors from decision towards 3 output bands
 z+=path('M418 485 H268 V566','#2C91AB',2.5)
 z+=path('M589 550 V565','#2C91AB',2.5)
 z+=path('M760 485 H930 V565','#2C91AB',2.5)
 z+=rect(947,210,158,35,'#FFF4E5',11)+t(1026,232,'SOB SUPERVISÃO',12,'#94632A',800,'middle')
 return cover('O-08','PAC na prática','Fluxo didático de conferência documental e comunicação supervisionada.',z)
def scene_pauta():
 z=window(72,186,1055,468,'PAUTA DE AUDIÊNCIA — DEMONSTRAÇÃO')
 # left agenda
 z+=rect(92,253,328,370,'#F3F7FD',13)
 z+=t(114,285,'AGENDA FICTÍCIA',17,'#355F80',800)
 z+=rect(112,303,286,67,'#E5F0FA',10)+t(129,334,'Sessão ilustrativa',16,'#236389',800)+t(129,357,'Horário e local simulados',12,'#587E96')
 z+=rect(112,383,286,100,'#FFFFFF',10,'#CADDE9')
 z+=rect(128,398,54,55,'#784ED3',10)+t(155,433,'14',19,'#FFF',800,'middle')
 z+=t(196,416,'Processo fictício',15,'#224C65',800)+t(196,440,'Audiência em pauta',13,'#698396')
 z+=rect(112,500,286,99,'#FFFFFF',10,'#CADDE9')+t(130,530,'ATENÇÃO',14,'#B07530',800)
 z+=mtext(130,555,['A pauta não comprova','a regularidade da citação.'],14,'#476A7F',22)
 # timeline on right
 z+=rect(442,252,660,372,'#FCFDFE',13,'#DBE6EE')
 z+=t(463,285,'CONFERÊNCIA PRELIMINAR',16,'#3E779E',800)
 z+=line(497,333,1047,333,'#C5D9E9',6)
 checks=[('AR / citação','Abrir a peça'),('Prazo','Conferir datas'),('Respostas','Ler manifestação'),('Pauta','Informar pendência')]
 for i,(head,desc) in enumerate(checks):
  x=490+i*147
  z+=circ(x,333,21,'#E2F1FC','#4E9CCA',2)+t(x,340,i+1,19,'#2374A5',800,'middle')
  z+=t(x-21,385,head,15,'#244A64',800)
  z+=t(x-21,410,desc,12,'#617D91')
 z+=rect(471,472,599,119,'#E7F5F0',13,'#B6D9CB')
 z+=iconcheck(496,505)+t(517,511,'Quando houver inconsistência:',17,'#256554',800)
 z+=mtext(492,542,['Descreva o que encontrou e encaminhe ao servidor.',
                  'Não retire audiências da pauta por conta própria.'],15,'#326B5E')
 return cover('P-01','Conferência de pauta e audiência',
              'Interprete AR, prazos, manifestações e documentos antes do encaminhamento.',z)

def scene_balcao_fisico():
 z=''
 # reception counter atmosphere and figures
 z+=rect(65,184,1070,452,'#E7F1F9',20,'#D4E6F0',1,shadow())
 z+=rect(91,218,1018,58,'#D4E8F6',11)
 z+=t(116,255,'ATENDIMENTO AO CIDADÃO',22,'#265778',800)
 z+=rect(126,308,420,232,'#D8EAF4',18)
 z+=person(306,407,'#136F9D','#C99175','#284254',1.13)
 z+=rect(94,535,700,71,'#23658E',11)
 z+=rect(93,527,700,18,'#75B9DB',7)
 z+=person(742,418,'#C38B4B','#DDAA88','#324554',1.12)
 z+=rect(405,435,136,100,'#173A54',8)
 z+=rect(415,447,116,71,'#E7F4FC',5)
 z+=rect(451,537,45,11,'#1D3444',3)
 # conversation bubble
 z+=rect(441,302,268,95,'#FFFFFF',17,'#D5E4EF',1.5)
 z+=path('M481 397 l-28 26 13-26','#D4E3EF',3,'#FFF')
 z+=mtext(465,338,['Boa tarde!','Como posso ajudar?'],19,'#2C5874',27,700)
 # checking panel
 z+=rect(819,303,262,294,'#FFFFFF',16,'#D3E3EC',1.2)
 z+=t(842,339,'O QUE CONFERIR',16,'#2B6589',800)
 checks=[('1','Ouvir a demanda'),('2','Localizar o processo'),('3','Verificar vínculo'),('4','Proteger sigilo'),('5','Encaminhar')]
 for i,(n,label) in enumerate(checks):
  yy=377+i*43
  z+=circ(853,yy-6,13,'#E2F3FB')+t(853,yy-1,n,13,'#277BA5',800,'middle')
  z+=t(874,yy,label,14,'#34596F',700)
 z+=badge(93,616,'ATENDIMENTO FICTÍCIO','#BF8138',235)
 return cover('BF-01','Recepção e identificação',
              'Aprenda como acolher, verificar o vínculo e encaminhar com respeito.',z)
def scene_balcao_virtual():
 z=window(72,184,1052,469,'SALA REMOTA DE ATENDIMENTO — AMBIENTE FICTÍCIO')
 z+=rect(91,245,698,383,'#122940',13)
 # 2 conference attendees
 for x,shirt,skin,hair,label in [(108,'#276FA3','#DEAC8C','#344758','Atendente'),(457,'#238D7E','#BC836A','#223645','Pessoa atendida')]:
  z+=rect(x,259,322,308,'#294B68',12)
  z+=circ(x+161,340,93,'#315B7C')
  z+=person(x+161,378,shirt,skin,hair,1.35)
  z+=rect(x+17,520,181,33,'#0E263A',10)+t(x+35,542,label,14,'#EFF9FC',700)
 # call controls
 z+=rect(295,577,310,35,'#264C69',17)
 for i,label in enumerate(['◉','◻','✕','?']):
  z+=circ(337+i*72,595,15,'#D9E8F2' if i!=2 else '#D65E62')
  z+=t(337+i*72,601,label,16,'#235470' if i!=2 else '#FFF',800,'middle')
 # side panel
 z+=rect(807,244,299,382,'#F7FAFD',13)
 z+=t(828,281,'ORIENTAÇÃO AO VIVO',16,'#376783',800)
 for i,(title,sub) in enumerate([
  ('1 · Identificação','Verificar conforme regras'),
  ('2 · Solicitação','Atendimento informativo'),
  ('3 · Encaminhamento','Consultar supervisão'),
  ('4 · Privacidade','Não solicitar senhas')]):
  y=299+i*73
  z+=rect(823,y,270,66,'#FFFFFF',10,'#D7E5EE')
  z+=t(839,y+27,title,15,'#235B80',800)+t(839,y+49,sub,12,'#607E91')
 z+=rect(836,600,255,14,'#A9C8D7',7)
 return cover('BV-01','Balcão Virtual',
              'Atendimento remoto informativo, identificação e limites de supervisão.',z)
def scene_relatorio():
 z=window(70,183,1058,470,'PAINEL DE INDICADORES — DADOS DE EXEMPLO')
 z+=rect(87,244,1023,392,'#EEF5FB',12)
 z+=t(108,278,'INDICADORES ILUSTRATIVOS',15,'#2A6489',800)
 stats=[('20','processos hipotéticos','#287DB7'),('15','com uma condição','#169B8A'),('75%','proporção do exemplo','#885CD6')]
 for i,(num,label,col) in enumerate(stats):
  x=107+i*333
  z+=rect(x,299,316,120,'#FFFFFF',15,'#D6E5ED',1,shadow())
  z+=rect(x+17,314,7,85,col,4)
  z+=t(x+38,353,num,34,col,800)+t(x+39,382,label,15,'#5E778A')
 # charts
 z+=rect(106,440,494,177,'#FFFFFF',15,'#D6E5ED')
 z+=t(127,467,'DISTRIBUIÇÃO FICTÍCIA',15,'#376784',800)
 for i,height in enumerate([51,87,105,75,123]):
  z+=rect(152+i*73,593-height,43,height,['#57A5D7','#2D84C5','#157AB3','#4595CE','#8AC3E5'][i],7)
 z+=line(134,594,526,594,'#C6D7E4',2)
 z+=rect(617,440,475,177,'#FFFFFF',15,'#D6E5ED')
 z+=t(640,469,'COMO INTERPRETAR',15,'#376784',800)
 for i,(v,desc) in enumerate([('01','Verifique o período'),('02','Identifique o total'),('03','Compare critérios iguais')]):
  yy=498+i*35
  z+=circ(658,yy+1,14,'#DBF2EC')+t(658,yy+6,v,11,'#138473',800,'middle')+t(684,yy+6,desc,15,'#365E75',700)
 return cover('R-01','Indicadores processuais',
              'Aprenda a interpretar números, percentuais e prazos sem presumir conclusões.',z)
SCENES={
'O-03':scene_tree,'O-08':scene_pac,'P-01':scene_pauta,
'BF-01':scene_balcao_fisico,'BV-01':scene_balcao_virtual,'R-01':scene_relatorio
}

def scene_diagram(code,lesson):
 steps=lesson['steps']
 accent=SECTIONS[lesson['section']][0]
 title=lesson['title']
 w,h=1200,590
 body=rect(0,0,w,h,'#102D46',26)
 body+=t(49,59,'GUIA VISUAL DE ESTUDO',17,'#B5D8EA',800,extra='letter-spacing="2"')
 body+=t(49,107,title,32,'#FFF',800)
 body+=badge(934,48,'ROTEIRO DIDÁTICO',accent,214)
 body+=mtext(50,142,['Use este esquema para lembrar o que conferir.',
                     'A execução de atos depende da supervisão da unidade.'],15,'#B5CFE1',25)
 x_positions=[42,333,625,916]
 for i,step in enumerate(steps[:4]):
  x=x_positions[i];yy=213
  body+=rect(x,yy,247,227,'#F6FAFD',18,'#B7D2E5',2,shadow())
  body+=rect(x,yy,247,58,accent,16)+rect(x,yy+32,247,25,accent,0)
  body+=pin(x+32,yy+30,str(i+1),accent,17)
  titlewords=step['title'].split()
  ln1=' '.join(titlewords[:3])
  ln2=' '.join(titlewords[3:]) if len(titlewords)>3 else ''
  body+=t(x+23,yy+98,ln1[:26],18,'#174663',800)
  if ln2:body+=t(x+23,yy+119,ln2[:28],16,'#174663',700)
  content=step['instruction'].split()
  lines=[];line1=''
  for word in content:
   if len(line1+' '+word)>27 and line1:
    lines.append(line1);line1=word
   else:line1=(line1+' '+word).strip()
  if line1:lines.append(line1)
  body+=mtext(x+23,yy+(152 if ln2 else 138),lines[:3],14,'#607F95',24)
  if i<3:body+=arrow(x+251,324,x+286,324,'#96C5E5')
 body+=rect(54,478,1090,61,'#17455F',12)
 body+=iconcheck(87,509,'#259984')+t(113,516,'Depois da conferência: descreva o que foi observado e consulte o servidor quando necessário.',19,'#D5EEFB',700)
 body+=t(52,572,'DIAGRAMA ORIENTATIVO · ROTEIRO SIMULADO · NÃO É INSTRUÇÃO AUTOMÁTICA DO PJe',13,'#B0CFDD',700)
 return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="t d"><title id="t">{e(code)} — passos ilustrados</title><desc id="d">Quatro etapas resumidas para aprender a conferência sob supervisão. Não representa decisão processual.</desc><defs><filter id="ds"><feDropShadow dx="0" dy="10" stdDeviation="12" flood-color="#051B2C" flood-opacity=".23"/></filter></defs>{body}</svg>'
def create():
 rows=[]
 for code,maker in SCENES.items():
  folder=OUT/code;folder.mkdir(parents=True,exist_ok=True)
  lesson=json.loads((DATA/(code+'.json')).read_text(encoding='utf8'))
  first=maker();second=scene_diagram(code,lesson)
  (folder/'ilustracao-premium.svg').write_text(first,encoding='utf8')
  (folder/'fluxo-premium.svg').write_text(second,encoding='utf8')
  rows.append({'code':code,'reference_page':lesson['page'],
    'illustration':f'assets/learning/{code}/ilustracao-premium.svg',
    'flow':f'assets/learning/{code}/fluxo-premium.svg',
    'sha_illustration':hashlib.sha256(first.encode()).hexdigest(),
    'sha_flow':hashlib.sha256(second.encode()).hexdigest(),
    'review':'didactic visual; editorial check pending',
    'fictitious':True,'alt':f'Ilustração pedagógica original de {lesson["title"]}, com interface e dados fictícios.'})
 manifest=ROOT/'data'/'learning-visuals-manifest.json'
 manifest.write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf8')
 print('VISUALS_CREATED',len(rows),'premium illustrations and',len(rows),'premium diagrams')
if __name__=='__main__':create()
