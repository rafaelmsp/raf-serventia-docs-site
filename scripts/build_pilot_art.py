"""Painéis SVG específicos dos seis pilotos — ilustração pedagógica, sem telas oficiais."""
from pathlib import Path
from html import escape
import json
ROOT=Path(__file__).resolve().parent.parent
LESSON=ROOT/'data/lessons'
def rect(x,y,w,h,color='#173B56',radius=13,stroke='#5E89A5'):
 return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="{color}" stroke="{stroke}"/>'
def txt(x,y,s,sz=17,fill='#E7F5FF',weight=600,anchor='start'):
 return f'<text x="{x}" y="{y}" font-family="Arial,sans-serif" font-size="{sz}" font-weight="{weight}" fill="{fill}" text-anchor="{anchor}">{escape(s)}</text>'
def pill(x,y,s,c='#116C9C',w=166):
 return rect(x,y,w,42,c,13,c)+txt(x+14,y+27,s,15,'#FFFFFF')
def frame(code,title,body,subtitle):
 base=rect(0,0,800,530,'#0F2B44',26,'#0F2B44')
 return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 530" role="img" aria-labelledby="title desc"><title id="title">{escape(title)} — cena explicativa</title><desc id="desc">{escape(subtitle)}. Ilustração original e esquemática, não é uma captura oficial do PJe.</desc><defs><linearGradient id="bg" x2="1" y2="1"><stop stop-color="#0F2B44"/><stop offset="1" stop-color="#1B4967"/></linearGradient></defs><rect width="800" height="530" rx="26" fill="url(#bg)"/>'''+txt(35,43,'RAF SERVENTIA DOCS · '+code,14,'#9DD6F6')+txt(35,86,title[:50],26,'#FFFFFF',700)+body+txt(35,502,'ILUSTRAÇÃO DIDÁTICA · EXEMPLO FICTÍCIO · NÃO É TELA OFICIAL',12,'#AACBDE')+'</svg>'
def tree():
 body='<path d="M390 430 C384 363 394 321 395 257 M395 323 L280 247 M396 310 L498 224 M391 276 L335 177 M397 261 L458 146" fill="none" stroke="#B98950" stroke-width="22" stroke-linecap="round"/>'
 body+='<path d="M388 420 Q288 441 241 477 M396 431 Q488 463 553 477 M392 434 Q355 466 350 480" fill="none" stroke="#BC9258" stroke-width="6"/>'
 for x,y in [(322,210),(443,210),(267,270),(517,259),(339,146),(472,137),(405,115),(230,207),(558,218)]:
  body+=f'<ellipse cx="{x}" cy="{y}" rx="55" ry="35" fill="#277F66" opacity=".7"/>'
 for x,y,s in [(252,173,'Galhos'),(430,151,'Tronco'),(225,330,'Folhas'),(450,330,'Frutos'),(310,438,'Raízes')]:
  body+=rect(x,y,140,45,'#F4FAF6',13,'#E0C48A')+txt(x+70,y+30,s,18,'#215B57',700,'middle')
 return frame('O-03','Árvore do Processo',body,'Raízes, tronco, galhos, folhas e frutos representam uma analogia para os eventos dos autos')
def pac():
 body=''
 for i,(title,sub) in enumerate([('1. Identificar','O que falta?'),('2. Conferir','Ordem, prazo e parte'),('3. Comunicar','Sob supervisão'),('4. Examinar','Resposta recebida')]):
  x=46+i*188
  body+=rect(x,164,170,140,'#244B69',16,'#5E9ABB')+txt(x+85,211,title,20,'#FFFFFF',700,'middle')+txt(x+85,247,sub,14,'#BEE1F6',500,'middle')
  if i<3:body+=txt(x+172,243,'→',25,'#F2C270',700)
 body+=pill(70,365,'Cumpriu', '#1B8268',185)+pill(308,365,'Parcial', '#B87D2B',185)+pill(546,365,'Não cumpriu','#B84A47',185)
 body+=txt(97,448,'Comparar a resposta com a determinação; consultar servidor.',15,'#BDD7E6')
 return frame('O-08','PAC na prática',body,'Ciclo didático do PAC com três resultados de conferência')
def pauta():
 body=txt(54,148,'ANTES',16,'#A7D9F7')+txt(361,148,'NA ANÁLISE',16,'#A7D9F7')+txt(630,148,'DEPOIS',16,'#A7D9F7')
 body+='<path d="M80 248 H718" stroke="#8CC3E0" stroke-width="8" stroke-dasharray="13 12"/>'
 for i,(title,sub) in enumerate([('Conferir AR','Citação e prazo'),('Examinar','Resposta e documentos'),('Encaminhar','Decisão supervisionada')]):
  x=44+i*249
  body+=rect(x,200,220,160,'#224766',17,'#6595B3')+txt(x+110,253,title,21,'#FFF',700,'middle')+txt(x+110,292,sub,15,'#C7DFEA',400,'middle')
 body+=rect(68,401,664,45,'#1E5D83')+txt(400,431,'A pauta não substitui a conferência dos autos',18,'#F8FCFF',700,'middle')
 return frame('P-01','Árvore e pauta de audiência',body,'Conferência documental antes de identificar pendências para supervisão')
def indicators():
 body=''
 labels=[('TEMPO MÉDIO','dias'),('CITAÇÃO','percentual'),('PENDÊNCIAS','proporção')]
 for i,(a,b) in enumerate(labels):
  x=49+i*244
  body+=rect(x,147,218,285,'#214663',17,'#5E8FAD')+txt(x+20,183,a,16,'#9DCCEB')
  if i==0:
   for j,h in enumerate([37,67,90,115]):body+=rect(x+30+j*40,350-h,27,h,'#5FBBE6',4,'#5FBBE6')
  elif i==1:
   body+=f'<circle cx="{x+110}" cy="297" r="60" stroke="#327656" stroke-width="24" fill="none"/><circle cx="{x+110}" cy="297" r="60" stroke="#9CE6C3" stroke-width="24" stroke-dasharray="242 134" fill="none"/>'
  else:
   for j,h in enumerate([55,93,122]):body+=rect(x+44+j*48,356-h,31,h,'#E6A35D',4,'#E6A35D')
  body+=txt(x+110,405,'EXEMPLO',15,'#CBE1EF',700,'middle')
 body+=txt(63,478,'Percentuais, quantidades e médias dependem de período e universo.',15,'#B7D7E9')
 return frame('R-01','Indicadores do processo',body,'Quadros ilustrativos de métricas que não correspondem a estatísticas reais')
def counter():
 body=rect(70,282,660,130,'#1E6087',18,'#65ADD3')
 body+='<circle cx="190" cy="220" r="60" fill="#327FA3"/><circle cx="570" cy="220" r="60" fill="#237F77"/>'
 body+='<path d="M128 286 Q190 195 252 286 M508 286 Q570 195 632 286" stroke="#B5DDEE" stroke-width="10" fill="none"/>'
 body+=rect(291,183,218,86,'#F5FBFF',13,'#C9E3F0')+txt(400,219,'Como posso',19,'#285B79',700,'middle')+txt(400,246,'ajudar?',19,'#285B79',700,'middle')
 for i,(t,sub) in enumerate([('OUVIR','Demanda'),('CONFERIR','Vínculo e sigilo'),('ENCAMINHAR','Serviço adequado')]):
  x=73+i*236
  body+=rect(x,430,204,47,'#224868',11,'#6CA4C4')+txt(x+102,459,t,16,'#FFF',700,'middle')
 return frame('BF-01','Recepção e identificação',body,'Cena fictícia de atendimento ao público com acolhimento e encaminhamento')
def virtual():
 body=rect(79,135,644,310,'#355F80',16,'#81B8D6')+rect(102,157,598,247,'#162E49',12,'#162E49')
 for i,(x,c) in enumerate([(130,'#427C98'),(416,'#278477')]):
  body+=rect(x,185,243,182,c,13,c)+f'<circle cx="{x+120}" cy="253" r="43" fill="#ADD6E6"/><path d="M{x+68} 333 Q{x+120} 255 {x+171} 333" stroke="#BEE8F3" stroke-width="9" fill="none"/>'
 body+=rect(269,410,257,20,'#466B86',7,'#466B86')
 body+=txt(200,469,'Atendimento informativo',17,'#B9E4F4',700,'middle')+txt(584,469,'Sempre supervisionado',17,'#B9E4F4',700,'middle')
 return frame('BV-01','Balcão Virtual',body,'Sala de atendimento remoto inteiramente fictícia')
makers={'O-03':tree,'O-08':pac,'P-01':pauta,'R-01':indicators,'BF-01':counter,'BV-01':virtual}
for code,maker in makers.items():
 dest=ROOT/'assets/learning'/code/'simulacao.svg';dest.parent.mkdir(parents=True,exist_ok=True)
 dest.write_text(maker(),encoding='utf8')
print('PILOT_ART_UPDATED',len(makers))
