"""Create source-grounded draft lessons for native-text Balcão Físico and Virtual pages.
Content is taken from the provided 107-page manual; no invented UI clicks.
Each operational step has an explicit human-supervision disclaimer.
Editorial approval remains False, and use depends on current regulations.
"""
from pathlib import Path
import json,re
ROOT=Path(__file__).resolve().parent.parent
INDEX=json.loads((ROOT/'dados/procedimentos.json').read_text(encoding='utf8'))
SRC={x['pagina']:x['linhas'] for x in json.loads((ROOT/'dados/conteudo_integral.json').read_text(encoding='utf8'))}
def joined(xs):return ' '.join(' '.join(x.strip().split()) for x in xs if x.strip())
def parse_steps(row):
 lines=SRC[row['pagina']]
 start_label='PASSO A PASSO NO BALCÃO' if row['categoria']=='BF' else 'FLUXO DO ATENDIMENTO • ETAPAS PRÁTICAS'
 try:start=lines.index(start_label)
 except ValueError:
  start=next((i for i,x in enumerate(lines) if start_label in x),None)
 if start is None:return None
 # Some pages have a checklist title immediately after marker.
 if row['categoria']=='BF':
  nextpos=next((i for i in range(start+1,len(lines)) if lines[i].strip()=='1'),None)
 else:nextpos=next((i for i in range(start+1,len(lines)) if lines[i].strip()=='1'),None)
 if nextpos is None:return None
 stop_at='CONFERÊNCIA FINAL' if row['categoria']=='BV' else 'ATENÇÃO — LIMITE / PONTO A VALIDAR'
 stop=next((j for j in range(nextpos+1,len(lines)) if lines[j].startswith(stop_at)),len(lines))
 # BF includes checklist short labels after numeric steps and before warning; stop once 5 finished.
 count=5 if row['categoria']=='BF' else 4
 records=[]
 pos=nextpos
 for k in range(1,count+1):
  expected=str(k)
  if pos>=stop or lines[pos].strip()!=expected: return None
  start_body=pos+1
  end=next((j for j in range(start_body,stop) if lines[j].strip()==str(k+1)),stop)
  group=lines[start_body:end]
  if not group:return None
  title=group[0].strip()
  # Body may have wrapped lines. Avoid checklists appended after BF final fifth step:
  descs=group[1:]
  if row['categoria']=='BF' and k==5:
   descs=descs[:3]
  description=joined(descs)
  if len(description)>350:description=description[:350].rsplit(' ',1)[0]+'…'
  records.append((title,description))
  pos=end
 return records
def get_safety(lines):
 for prefix in ('ATENÇÃO — LIMITE / PONTO A VALIDAR','ATENÇÃO:'):
  for i,t in enumerate(lines):
   if t.startswith(prefix):
    if prefix.startswith('ATENÇÃO:'):return t.split(':',1)[1].strip()
    seg=[]
    for x in lines[i+1:]:
     if x.startswith('REFERÊNCIA / ORIGEM'):break
     seg.append(x)
    return joined(seg)[:310]
 return 'Os procedimentos devem seguir a regra vigente, o perfil autorizado e a supervisão do servidor.'
def make(row,steps):
 file=ROOT/'data/lessons'/(row['codigo']+'.json')
 x=json.loads(file.read_text(encoding='utf8'))
 title=row['titulo'];page=row['pagina']
 s=SRC[page];safety=get_safety(s)
 intro=next((v.strip() for v in s[1:6] if len(v.strip())>22 and 'PASSO' not in v and 'ROTA' not in v),None)
 intro=intro or ('Roteiro de atendimento apresentado na página '+str(page)+' do manual.')
 intro=intro.replace('FINALIDADE OPERACIONAL','').strip()
 # A separate clear purpose and detailed source steps, with presentation not authorization.
 x['state']='author_draft'
 x['authored_batch']='native_source_bf_bv'
 x['objective']=f'Compreender o objetivo de “{title}”, reconhecer os registros que precisam de conferência e explicar quando pedir apoio ao servidor.'
 x['plain']=f'{intro} O material apresenta orientações de conferência. Os comandos e rotinas locais precisam ser verificados com o servidor responsável antes de uso real.'
 x['terms']=[{'term':a,'meaning':b,'example':f'Na fonte, este tópico integra a conferência do assunto “{title}”.'} for a,b in steps[:4]]
 x['observe']=[{'title':a,'detail':b} for a,b in steps[:4]]
 x['steps']=[{'title':a,'instruction':b,'why':'A ordem foi registrada no infográfico. Conferir autorização, perfil de acesso e possíveis exceções com o responsável antes da execução.'} for a,b in steps]
 x['scene']['regions']=[{'title':a,'detail':b} for a,b in steps[:4]]
 x['decision']={'question':f'No atendimento de “{title}”, há dúvida sobre a regra atual ou o perfil permitido. Qual conduta é adequada?',
   'options':[
     {'label':'Conferir a fonte e encaminhar a dúvida à supervisão antes de executar.','feedback':'Correto. O manual não substitui regras atuais e atribuições.','correct':True},
     {'label':'Seguir o roteiro antigo mesmo sem validação.','feedback':'Incorreto. A rotina pode ter mudado.','correct':False},
     {'label':'Usar a sessão ou senha de outra pessoa para concluir.','feedback':'Incorreto. Credenciais são individuais e os atos exigem perfil autorizado.','correct':False}
   ]}
 x['practice']={'scenario':f'Exemplo fictício de atendimento: o procedimento “{title}” exige atenção ao seguinte ponto: {steps[0][0]} — {steps[0][1]}',
   'question':'Qual ação preserva a qualidade e os limites do atendimento?',
   'options':[
     {'label':'Conferir o fato e seguir o encaminhamento autorizado pela unidade.','feedback':'Adequado: o roteiro é um apoio, não autorização autônoma.','correct':True},
     {'label':'Afirmar que o resultado judicial já foi garantido.','feedback':'Não é possível prometer decisão judicial.','correct':False},
     {'label':'Omitir a conferência de identidade ou da documentação pertinente.','feedback':'A verificação e o sigilo continuam importantes.','correct':False}
   ]}
 x['mistakes']=[{'mistake':'Ignorar alerta da fonte','correct':safety},
  {'mistake':'Tratar o tutorial como permissão de acesso','correct':'Usar apenas perfil próprio e atividades autorizadas.'},
  {'mistake':'Prometer resultado judicial','correct':'Informar apenas registros e encaminhamentos confirmados.'}]
 x['mastery']=[f'Sei explicar o que significa “{steps[0][0]}”.',
    f'Consigo reconhecer quando conferir “{steps[1][0]}”.',
    'Sei identificar dúvida que exige orientação do servidor.']
 x['status_note']='Roteiro de leitura reconstruído da camada textual do PDF. Pendente de revisão normativa e validação local; não autoriza execução.'
 x['source_highlights']=[f'{a}: {b}' for a,b in steps[:3]]
 x['source_highlight_status']='camada_textual_pdf'
 x['pedagogical_ready']=False;x['technical_approved']=False;x['student_tested']=False
 file.write_text(json.dumps(x,ensure_ascii=False,indent=2),encoding='utf8')
 return x
done=[];fail=[]
for row in INDEX:
 if row['codigo']=='BF-01' or row['codigo']=='BV-01' or row['categoria'] not in ('BF','BV'):continue
 steps=parse_steps(row)
 if steps:
  make(row,steps);done.append(row['codigo'])
 else:fail.append(row['codigo'])
print('NATIVE_AUTHORED',len(done),done,'NEEDS_CUSTOM',fail)
