"""Custom authored draft notes from verified native PDF text pages 50-54, 98.
No operational/institutional approval; all examples fictitious.
"""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parent.parent
MAP={
'O-45':{
 'objective':'Reconhecer a matriz de sete gabinetes descrita no material de treinamento e seus limites.',
 'plain':'A fonte organiza etiquetas e atribuições internas por assunto. A etiqueta, isoladamente, NÃO determina conclusão nem substitui a análise do processo.',
 'steps':[
 ('Gabinete 1 — Conhecimento','Na matriz de treinamento: feitos em fase de conhecimento, ressalvadas exceções.'),
 ('Gabinete 2 — Embargos de declaração','Etiqueta citada para essa classe de manifestação.'),
 ('Gabinete 3 — Suspensos','Matéria vinculada à suspensão no material; motivos e vigência devem ser conferidos.'),
 ('Gabinete 4 — Embargos à execução','Etiqueta de referência para embargos à execução.'),
 ('Gabinete 5 — Cumprimento de sentença','A fonte associa à execução de título judicial.'),
 ('Gabinete 6 — Urgências','A fonte associa à tutela pendente e pedidos urgentes.'),
 ('Gabinete 7 — Título extrajudicial','A fonte associa a execução fundada em título extrajudicial.')],
 'caution':'Matriz obtida de notas de treinamento. Confirmar vigência, alçadas e roteamento atual com a chefia. Etiquetas não autorizam conclusões automáticas.'},
'O-46':{
 'objective':'Entender as atribuições descritas para o Gabinete 1 e reconhecer situações que exigem conferência prévia.',
 'plain':'A folha original reúne hipóteses de conhecimento, audiência, citação, sentenças e recursos. Não afirma que cada petição origine conclusão automática.',
 'steps':[
 ('Regra geral','Abrange processos desde a distribuição até o trânsito em julgado, ressalvadas exceções da matriz.'),
 ('Pedidos antes da audiência','O material inclui redesignação, modalidade virtual e pedidos incidentais.'),
 ('Citação e AR','Em certos casos a folha sugere análise; conferir histórico, decisões anteriores e rotina vigente.'),
 ('Sentenças e extinções','O rol de matérias da folha não autoriza o estagiário a decidir ou sentenciar.'),
 ('Recursos e gratuidade','Conferir determinações e documentos; os atos competem à unidade e ao juízo.')],
 'caution':'Contestação, AR negativo ou simples pedido de audiência não acarretam conclusão automática. Confirmar a atuação do Gabinete 1 com a serventia.'},
'O-47':{
 'objective':'Distinguir providência cartorária e questão que exige apreciação judicial, usando a árvore como mapa de análise.',
 'plain':'A fonte orienta ler contexto, fato novo, requisitos e determinações anteriores antes de considerar conclusão. A decisão final é supervisionada.',
 'steps':[
 ('01 — Ler o histórico','Conferir classe, fase, decisão e tarefa atual.'),
 ('02 — Identificar o fato novo','Reconhecer petição, contestação, AR, tutela, recurso ou incidente.'),
 ('03 — Conferir requisitos','Examinar documentos, representação, comunicação e prazos.'),
 ('04 — Verificar ato já determinado','Observar se há ordem clara e perfil de execução autorizado.'),
 ('05 — Verificar necessidade de intimação','Identificar lacuna real e rotina válida, sem presumir PAC.'),
 ('06 — Avaliar necessidade de decisão','Submeter ao responsável quando a questão exigir apreciação judicial.'),
 ('07 — Encaminhar e conferir','Conferir a matriz e o resultado sob a responsabilidade da unidade.')],
 'caution':'A etiqueta e o histórico isolados não determinam conclusão; não usar logins de terceiros ou acessar documentos sigilosos sem permissão.'},
'O-48':{
 'objective':'Reconhecer diferentes manifestações incidentais sem encaminhar automaticamente toda contestação para conclusão.',
 'plain':'O manual relaciona contestação e pedidos de audiência, acordo, tutela, embargos e execução a atribuições que dependem da fase e das decisões anteriores.',
 'steps':[
 ('Contestação no JEC','A fonte cita art. 30 da Lei 9.099/1995; conferir fase, audiência, documentos e determinação.'),
 ('Reagendamento e audiência virtual','Pedido exige exame das condições e rotina competente, não decisão do estagiário.'),
 ('Acordo e desistência','Conferir representação e eventual necessidade de apreciação/homologação.'),
 ('Tutela incidental','A folha vincula urgências ao Gabinete 6, sujeito à matriz vigente.'),
 ('Embargos de declaração','A folha identifica como atribuição distinta, a confirmar com a unidade.'),
 ('Execução e incidentes','Distinguir cumprimento de sentença, embargos e título extrajudicial.')],
 'caution':'Mera juntada de contestação não gera conclusão automática; primeiro verificar se há comando para ato de serventia, PAC, intimação ou controle de prazo.'},
'O-49':{
 'objective':'Diferenciar emenda, aditamento e renúncia de advogado e reconhecer por que os efeitos dependem do caso.',
 'plain':'As três rotinas aparecem nos apontamentos consolidados do manual, mas não são etiquetas autônomas da matriz dos sete gabinetes.',
 'steps':[
 ('Emenda da petição inicial','Localizar determinação, identificar exigência e conferir a resposta documental.'),
 ('Aditamento ou alteração de pedido','Diferenciar complemento documental de alteração da pretensão e conferir fase e participação da parte contrária.'),
 ('Renúncia ao mandato','Conferir representação, comunicação e documentos conforme regras aplicáveis.'),
 ('Encaminhamento','Examine o último ato, a pendência concreta e a necessidade de análise do servidor competente.')],
 'caution':'Não alterar pedidos, excluir patrono ou presumir suspensão automática. O art. 112 do CPC depende de aplicação ao caso e norma vigente.'},
'BV-07':{
 'objective':'Aprender a iniciar o atendimento remoto com cordialidade, verificação de identidade e transparência sobre regras.',
 'plain':'O manual transcreve mensagem dirigida a advogados e cita o Ato TJ/CGJ 15/2026, mas sua redação consolidada e possíveis exceções precisam ser confirmadas antes de utilizar o texto como regra vigente.',
 'steps':[
 ('Cumprimente','Realize abertura respeitosa e apresente a natureza informativa do atendimento.'),
 ('Explique as regras documentadas','O manual relata parâmetros de identificação OAB, câmera, tempo e processos; conferir fonte oficial atual.'),
 ('Confirme identidade','Para advogados, conferir identificação conforme norma; para demais cidadãos, adotar procedimento adequado.'),
 ('Pergunte a demanda','Identifique processo e motivo, solicitando somente dados necessários.'),
 ('Proteja informações','Se houver segredo, dúvida ou exceção, interrompa a divulgação e consulte o servidor.')],
 'caution':'Não tratar mensagem do treinamento como norma consolidada. Confirme a redação atual do ato e exceções; não exigir carteira OAB de cidadãos não advogados.'},
}
def main():
 for code,v in MAP.items():
  p=ROOT/'data/lessons'/(code+'.json')
  d=json.loads(p.read_text(encoding='utf8'))
  d['state']='author_draft';d['authored_batch']='native_source_special'
  d['objective']=v['objective'];d['plain']=v['plain']
  d['terms']=[{'term':a,'meaning':b,'example':'Conceito apresentado no infográfico; requer conferência com o caso concreto.'} for a,b in v['steps'][:4]]
  d['observe']=[{'title':a,'detail':b} for a,b in v['steps'][:4]]
  d['steps']=[{'title':a,'instruction':b,'why':'A fonte ajuda na leitura; qualquer ato real depende de perfil próprio, regra vigente e orientação de servidor.'} for a,b in v['steps']]
  d['scene']['regions']=[{'title':a,'detail':b} for a,b in v['steps'][:4]]
  d['mistakes']=[{'mistake':'Aplicar a fonte sem validar vigência','correct':v['caution']},
    {'mistake':'Transformar um rótulo em ordem','correct':'Ler os autos e submeter dúvidas à supervisão.'},
    {'mistake':'Ultrapassar o papel do estagiário','correct':'Confirmar atribuições e encaminhar a decisão ao responsável.'}]
  d['decision']={'question':f'Em “{d["title"]}”, o manual sugere uma interpretação, mas a rotina local pode ter mudado. O que fazer?',
    'options':[{'label':'Conferir a norma e o responsável antes do encaminhamento.','feedback':'Correto. A fonte não basta para validar competência ou vigência.','correct':True},
       {'label':'Seguir a folha histórica sem checar o processo.','feedback':'Incorreto: falta conferência do caso e da regra atual.','correct':False},
       {'label':'Executar sem supervisão porque consta em infográfico.','feedback':'Incorreto: ilustração didática não é autorização.','correct':False}]}
  d['practice']={'scenario':f'Exemplo fictício: você encontra um documento referente a “{d["title"]}”, mas não sabe a providência autorizada.',
    'question':'Qual conduta é mais segura?',
    'options':[{'label':'Ler o documento, conferir o contexto e consultar o servidor responsável.','feedback':'Correto: observação antes de encaminhamento.','correct':True},
      {'label':'Abrir conclusão automaticamente.','feedback':'A conclusão depende de análise da situação e autorização.','correct':False},
      {'label':'Ignorar o pedido e não comunicar a dúvida.','feedback':'A pendência deve ser descrita ao responsável.','correct':False}]}
  d['mastery']=[f'Consigo diferenciar os tópicos principais de “{d["title"]}”.','Sei reconhecer quando a matrícula e as atribuições exigem supervisão.','Não confundo treino e decisão processual.']
  d['status_note']='Roteiro autoral a partir do texto nativo do PDF; matrizes e normas internas precisam de conferência atual.'
  d['source_highlights']=[a+': '+b for a,b in v['steps'][:3]]
  d['source_highlight_status']='camada_textual_pdf'
  d['pedagogical_ready']=d['technical_approved']=d['student_tested']=False
  p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf8')
 print('SPECIAL_AUTHORED',len(MAP))
if __name__=='__main__':main()
