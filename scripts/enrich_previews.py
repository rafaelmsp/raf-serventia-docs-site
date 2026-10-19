"""Safety-preserving editorial enrichment for the 82 lessons not yet authored.
Adds unique topic-oriented reading prompts grounded to PDF text or title.
Does NOT fabricate step-by-step judicial actions. Keeps approval false.
"""
from pathlib import Path
import json,re
from build_all_visuals import INDEX,SOURCE,topics,identify
ROOT=Path(__file__).resolve().parents[1]
LABELS={
'tree':('histórico do processo','reconhecer eventos','localizar documentos'),
'document':('documentação do processo','distinguir peças','verificar o conteúdo'),
'message':('comunicação processual','identificar destinatários','conferir retorno'),
'calendar':('audiências e pauta','identificar o agendamento','conferir os registros'),
'metrics':('indicadores de acompanhamento','interpretar dados','reconhecer limites dos números'),
'service':('atendimento presencial','acolher a demanda','respeitar os limites de atuação'),
'video':('atendimento remoto','reconhecer etapas da chamada','proteger informações'),
'finance':('registro de valores','diferenciar situações','consultar decisão e resultado'),
'privacy':('representação e acesso','identificar restrições','respeitar o sigilo'),
'decision':('atos judiciais e encaminhamentos','ler determinações','conferir a competência'),
'timeline':('sequência processual','identificar marcos','revisar prazos'),
'folder':('organização do processo','entender a situação atual','localizar registros'),
'workflow':('organização da rotina','compreender etapas','reconhecer supervisão'),
}
def clean(s):
 return re.sub(r'\s+',' ',str(s)).strip()
def highlight(row):
 lines=SOURCE[row['pagina']]['linhas']
 s=[]
 for raw in lines:
  x=clean(raw)
  if len(x)<18 or len(x)>130:continue
  if x.casefold()==row['titulo'].casefold():continue
  if any(t in x.lower() for t in ('poder judiciário','rafael','estado do rio','cidadania','data de impressão','matéria não oficial','jaque','justiça mais eficiente','manual do estagiário')):continue
  if re.search(r'[<>\[\]�]',x):continue
  if len(x.split())<4:continue
  if re.search(r'\b(?:pje|pj[eé]|tjrj)\b',x,re.I) and len(x.split())<=5:continue
  s.append(x)
 if row['origemTexto']=='camada_textual_pdf':
  # Keep compact source highlights without converting quotes into imperative.
  return s[:3]
 # OCR can be damaged; never turn it into verified source excerpt.
 return []
def run():
 changed=0
 for row in INDEX:
  code=row['codigo'];dest=ROOT/'data/lessons'/(code+'.json')
  d=json.loads(dest.read_text(encoding='utf8'))
  if d['state']=='author_draft':continue
  kind=identify(row);subject,verb,check=LABELS[kind]
  heading=row['titulo']
  tps=topics(row)
  d['objective']=f'Entender como o manual apresenta “{heading}” e aprender a {verb}, sem executar providências sem autorização.'
  d['plain']=f'Esta ficha aborda {subject}. Observe o infográfico original e identifique os elementos relacionados a {heading.lower()}. Compare os rótulos à página do manual antes de interpretar qualquer encaminhamento.'
  d['terms']=[
   {'term':tps[0],'meaning':f'Primeiro aspecto visual da página {row["pagina"]} relacionado ao assunto estudado.','example':f'Identifique no infográfico onde aparece “{tps[0]}” e observe o contexto.'},
   {'term':tps[1],'meaning':f'Segundo ponto apresentado no mapa de leitura.','example':f'Compare “{tps[1]}” com o tema central da aula.'},
   {'term':tps[2],'meaning':f'Aspecto que exige conferência do documento, da regra e da supervisão.','example':f'Localize “{tps[2]}” na fonte e verifique seu significado.'},
   {'term':tps[3],'meaning':f'Último elemento deste mapa conceitual, ainda sem revisão técnica.','example':'Explique o que você entendeu e consulte o responsável para confirmar.'}
  ]
  d['observe']=[{'title':tps[0],'detail':f'Localize este tópico na página {row["pagina"]} e diga, com suas palavras, que informação ele traz.'},
    {'title':tps[1],'detail':'Leia a parte correspondente e compare-a ao documento ou situação que está sendo estudada.'},
    {'title':tps[2],'detail':'Identifique possíveis dúvidas sobre documentos, regras ou limites da atuação do estagiário.'},
    {'title':tps[3],'detail':'Descreva o que precisa de confirmação antes de qualquer encaminhamento real.'}]
  d['scene']['title']=f'Cena conceitual: {heading}'
  d['scene']['regions']=[{'title':label,'detail':f'Na página {row["pagina"]}, este bloco corresponde a um aspecto do assunto “{heading}”. Consulte a imagem de origem e identifique o significado no contexto.'} for label in tps]
  d['source_highlights']=highlight(row)
  d['source_highlight_status']='camada_textual_pdf' if d['source_highlights'] else 'requer_conferencia_visual'
  d['practice']['scenario']=f'Exercício fictício de consulta documental: durante o estudo de “{heading}”, você encontra informação que não consegue confirmar apenas pela transcrição.'
  d['practice']['question']='Qual atitude demonstra uma leitura segura?'
  d['practice']['options']=[
    {'label':'Abrir o infográfico original, conferir o contexto e consultar a supervisão se necessário.','feedback':'Correto. A fonte original precisa ser conferida antes de aplicar uma regra.','correct':True},
    {'label':'Usar o primeiro rótulo extraído automaticamente como instrução processual.','feedback':'Incorreto: OCR e rótulos não são procedimento validado.','correct':False},
    {'label':'Inventar a próxima tarefa no sistema com base na aparência do desenho.','feedback':'Incorreto: nenhuma ilustração concede autorização para agir.','correct':False}]
  d['decision']['question']=f'Você precisa explicar “{heading}”, mas a fonte apresenta uma dúvida de leitura. Como deve proceder?'
  d['decision']['options']=[
    {'label':'Identificar a informação certa na imagem original e indicar o que ainda precisa de revisão.','feedback':'Correto. Separe o que está documentado do que permanece incerto.','correct':True},
    {'label':'Tratar a transcrição provisória como norma vigente.','feedback':'Isso pode reproduzir erro ou norma desatualizada.','correct':False},
    {'label':'Afirmar que já está autorizado a praticar o ato.','feedback':'A autorização e os perfis dependem da unidade.','correct':False}]
  d['mastery']=[f'Consigo identificar na fonte o assunto “{heading}”.',
                 f'Sei explicar o primeiro aspecto: {tps[0]}.',
                 'Sei quando consultar o infográfico original e pedir supervisão.']
  d['pedagogical_ready']=False;d['technical_approved']=False
  d['status_note']='Mapa e cenário individualizados para estudo; sequência operacional ainda precisa de revisão na fonte.'
  dest.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf8')
  changed+=1
 print('INDIVIDUALIZED_STUDY_PREVIEWS',changed)
if __name__=='__main__':run()
