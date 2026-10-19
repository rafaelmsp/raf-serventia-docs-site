"""Custom source-grounded draft lessons for P-02..P-16 and R-02..R-05.
Each value is conceptually read from the PDF infographic, not legal validation.
"""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parent.parent
GUIDES={
'P-02':([
('Comece pela árvore','Localize o histórico e identifique os atos que explicam a situação da audiência.'),
('Confira comunicação','Observe citações, intimações, prazos e pendências.'),
('Distinga funções','Conheça designar, redesignar e cancelar, sem presumir autorização para usá-las.'),
('Consulte a supervisão','A decisão de alterar a audiência deve partir do responsável.')],
'Uma audiência não deve ser alterada apenas porque aparece um botão de gerenciamento.'),
'P-03':([
('Comunicação','Procure nos autos provas de citação ou intimação pertinente.'),
('Prazos e respostas','Verifique manifestações e marcos necessários à conferência.'),
('Documentos','Consulte peças essenciais e determinações anteriores.'),
('Viabilidade','Descreva pendências ao servidor antes de qualquer alteração na pauta.')],
'A presença na pauta não demonstra automaticamente que a audiência está viável.'),
'P-04':([
('Abra a pauta','A fonte descreve Audiências e sessões > Pauta de audiência; confirme a interface atual.'),
('Use filtros','Localize por data, sala, processo, parte ou outro campo disponível.'),
('Confira o agendamento','Leia data, horário, modalidade, sala e processo associado.'),
('Abra a árvore quando necessário','Divergências e pendências precisam de leitura dos autos e supervisão.')],
'Consultar não equivale a redesignar ou cancelar. A interface e os filtros dependem da versão atual do PJe.'),
'P-05':([
('Confirme o agendamento','Consulte data, horário, tipo de audiência e status.'),
('Leia comunicações','Verifique AR, mandado, intimação ou outro retorno.'),
('Examine os autos','Procure petições recentes, procurações e atos anteriores.'),
('Relate pendências','Divergências devem ser comunicadas antes de qualquer movimentação.')],
'Ao estagiário não cabe cancelar, redesignar, deferir modalidade virtual ou homologar acordo.'),
'P-06':([
('Reconheça Aguardar Audiência','Identifique a tarefa mencionada no manual de realização de audiência.'),
('Observe Minutar Ata','A fonte relata fluxo automático em momento próximo da audiência, a confirmar no sistema atual.'),
('Confira a tarefa atual','Compare a tarefa exibida com o agendamento e o histórico.'),
('Informe anomalias','Se o processo não seguiu o fluxo previsto, comunique ao servidor.')],
'A existência de transição no PJe não autoriza o estagiário a realizar ou presidir audiência.'),
'P-07':([
('Reconheça as funções','A fonte distingue designação, redesignação, cancelamento e conversão em diligência.'),
('Identifique o ato correto','Verifique a audiência e seu estado atual nos autos.'),
('Confira a autorização','Qualquer alteração requer orientação e perfil autorizado.'),
('Confira o novo status','Se houver ato autorizado, verifique a atualização e a movimentação correspondente.')],
'Disponibilidade de botão não significa competência para decidir a alteração.'),
'P-08':([
('Entenda as alternativas','A fonte diferencia designação sugerida e designação manual.'),
('Reconheça os campos','Tipo, duração, sala, data e horário exigem conferência.'),
('Observe conflito de agenda','Divergências devem ser levadas ao responsável.'),
('Confira o resultado','Somente após orientação, compare o status e a reserva registrada.')],
'Escolha da data e confirmação final dependem da competência e da rotina do setor.'),
'P-09':([
('Localize a audiência','Consulte o ato agendado e seu histórico.'),
('Diferencie redesignar e cancelar','São providências distintas e registram resultados distintos.'),
('Verifique o motivo','O motivo e a autorização devem estar claros na rotina aplicável.'),
('Confira movimentação','Após ato autorizado, observe a atualização da árvore e da pauta.')],
'Ausência de ata no histórico não prova que a audiência não ocorreu.'),
'P-10':([
('Abra a petição','Entenda se foi solicitada audiência virtual.'),
('Confira a audiência existente','Verifique data, modalidade, status e documentos relevantes.'),
('Registre a pendência','Anote a informação conforme o controle autorizado da unidade.'),
('Encaminhe à decisão competente','A mudança de modalidade não é decidida pelo estagiário.')],
'O pedido de audiência virtual não implica deferimento ou redesignação automática.'),
'P-11':([
('Leia o acordo apresentado','Confira a petição e sua presença nos autos.'),
('Verifique representação','Identifique signatários e documentação necessária.'),
('Compare à pauta','Observe se a petição pretende impactar audiência marcada.'),
('Submeta à análise','O responsável definirá homologação e providência de pauta.')],
'Acordo juntado não significa cancelamento ou homologação automáticos.'),
'P-12':([
('Consulte o status','Veja se a audiência consta como realizada, cancelada ou remarcada.'),
('Confira a ata','Procure a peça e os registros correlatos.'),
('Identifique o resultado','Observe acordo, ausência, prosseguimento e determinações.'),
('Comunique divergências','Ata não visível não comprova, isoladamente, que o ato não ocorreu.')],
'Não redesignar uma audiência apenas porque a ata não aparece na primeira consulta.'),
'P-13':([
('Antes da audiência','Confira pauta, árvore, comunicação, documentos e petições recentes.'),
('No dia','Confirme processo, tarefa e eventuais solicitações urgentes.'),
('Depois','Leia ata, status, resultado, prazos e tarefa seguinte.'),
('Peça supervisão','Decisões, validações e alterações de pauta não cabem ao estagiário.')],
'O aluno deve conferir, preparar e encaminhar, não decidir a alteração da audiência.'),
'P-14':([
('Confira todos os meios','Identifique resultados de AR, mandado ou outros expedientes.'),
('Diferencie retornos','Um resultado negativo não implica que as demais diligências terminaram.'),
('Procure diligência pendente','Verifique se outra tentativa ainda aguarda retorno.'),
('Leve ao servidor','A retirada de pauta ou nova comunicação depende de instrução competente.')],
'Um único retorno negativo não é razão automática para cancelar ou retirar audiência.'),
'P-15':([
('Distinga os cenários','Ato não expedido é diferente de diligência expedida com resultado negativo.'),
('Confira nos autos','Determine apenas o que o histórico mostra sobre expedição e retorno.'),
('Verifique tempo disponível','O manual cita modelo de certidão quando não há tempo hábil, sujeito à rotina atual.'),
('Consulte o servidor','A decisão sobre pauta e conclusão depende do perfil competente.')],
'Não retirar audiência da pauta por conta própria por falta de expedição.'),
'P-16':([
('Localize as datas','Confira o registro da petição e o agendamento da audiência.'),
('Calcule o intervalo','A fonte relata marco de 72 horas na rotina local; verificar vigência antes de aplicar.'),
('Reconheça os destinatários relatados','O infográfico diferencia juiz togado e juiz leigo conforme antecedência informada.'),
('Peça confirmação','A regra local e exceções devem ser validadas pelo servidor antes do encaminhamento.')],
'O marco de 72 horas é relatado pelo treinamento e precisa de confirmação atual; não automatizar roteamento.'),
'R-02':([
('Identificação','Reconheça fase, partes e objeto do processo.'),
('Último ato','Localize decisão, comunicação e prazo relacionado.'),
('Conferência de resposta','Compare manifestação, documentos e cumprimento.'),
('Encaminhamento','Descreva o que aconteceu, o que foi pedido e o que falta.')],
'O checklist é leitura orientada; a providência precisa observar a autorização da unidade.'),
'R-03':([
('Revisite a determinação','Identifique o que o ato anterior solicitou.'),
('Confira comunicação','Veja os registros de ciência e eventual prazo.'),
('Leia a resposta','Verifique o que foi efetivamente juntado e sua relação com a ordem.'),
('Descreva o resultado','Identifique pendência e necessidade de nova análise com supervisão.')],
'Uma juntada não prova automaticamente cumprimento do pedido.'),
'R-04':([
('Entenda o que aconteceu','Leia a sequência da árvore e o ato relevante.'),
('Confira comunicação e prazo','Não presuma ciência válida ou término de prazo.'),
('Identifique o cenário','O manual compara intimação pendente, AR inválido e situação da audiência.'),
('Encaminhe à supervisão','Fluxos possíveis precisam ser escolhidos pelo responsável conforme a regra atual.')],
'A presença de um cenário no infográfico não autoriza o aluno a executar o próximo ato sem supervisão.'),
'R-05':([
('Localize o expediente','Encontre comunicação ou diligência na árvore ou controle autorizado.'),
('Identifique situação','Verifique se consta expedido, recebido, devolvido ou ainda pendente.'),
('Confira destinatário e meio','Leia dados da comunicação e seu retorno.'),
('Relate o resultado','Compare à determinação e ao prazo; informe pendência ao servidor.')],
'O status da comunicação exige prova documental e não é substituído por uma marcação de controle.')
}
def generate():
 done=[]
 for code,(steps,caution) in GUIDES.items():
  file=ROOT/'data/lessons'/(code+'.json')
  d=json.loads(file.read_text(encoding='utf8'))
  d['state']='author_draft';d['authored_batch']='ocr_interpreted_guided'
  d['objective']=f'Compreender como reconhecer e conferir “{d["title"]}” no histórico, sem executar mudanças sem autorização.'
  d['plain']=f'O infográfico aborda {d["title"].lower()} sob o ponto de vista de leitura do processo. As etapas abaixo resumem a análise documentada, mas precisam de revisão do texto original e da rotina vigente.'
  d['steps']=[{'title':a,'instruction':b,'why':'A conferência fornece contexto; executar um ato exige regra atual e supervisão.'} for a,b in steps]
  d['terms']=[{'term':a,'meaning':b,'example':'Na aula, encontre esse aspecto no infográfico da página '+str(d['page'])+'.'} for a,b in steps]
  d['observe']=[{'title':a,'detail':b} for a,b in steps]
  d['scene']['regions']=[{'title':a,'detail':b} for a,b in steps]
  d['mistakes']=[{'mistake':'Confundir leitura com autorização','correct':caution},
      {'mistake':'Ignorar os documentos e a fase','correct':'Consultar registros e decisões anteriores antes de concluir.'},
      {'mistake':'Decidir a pauta sem competência','correct':'Submeter a dúvida ao responsável.'}]
  d['decision']={'question':f'Ao estudar “{d["title"]}”, o manual mostra um caminho de análise. Como proceder diante de dúvidas?',
  'options':[{'label':'Confirmar o registro e a orientação do servidor antes de agir.','feedback':'Correto: a segurança exige fonte e supervisão.','correct':True},
             {'label':'Executar automaticamente a movimentação sugerida no desenho.','feedback':'A imagem não concede autorização.','correct':False},
             {'label':'Ignorar uma possível pendência documental.','feedback':'A pendência precisa ser examinada.','correct':False}]}
  d['practice']={'scenario':f'Exemplo fictício de conferência: durante “{d["title"]}”, o histórico aponta um fato e você precisa interpretar sua relevância antes de qualquer encaminhamento.',
  'question':'Qual é a melhor sequência de aprendizagem?',
  'options':[{'label':f'Primeiro {steps[0][0].lower()}, depois {steps[1][0].lower()}, conferindo os autos.','feedback':'Esse é um caminho seguro de estudo.','correct':True},
             {'label':'Pular a leitura e escolher diretamente a próxima tarefa.','feedback':'Não: a árvore e os documentos precisam de conferência.','correct':False},
             {'label':'Alterar a situação da audiência ou do processo sem autorização.','feedback':'A atuação depende de perfil e orientação do responsável.','correct':False}]}
  d['mastery']=[f'Sei explicar o objetivo de “{d["title"]}”.',
      f'Consigo reconhecer o ponto de estudo “{steps[0][0]}”.',
      'Consigo distinguir conferência documental de decisão processual.']
  d['source_highlights']=[a+': '+b for a,b in steps[:3]]
  d['source_highlight_status']='ocr_interpretacao_didatica_a_conferir'
  d['status_note']='Roteiro explicativo criado por interpretação didática de página com OCR provisório; ainda exige conferência visual e normativa.'
  d['pedagogical_ready']=d['technical_approved']=d['student_tested']=False
  file.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf8')
  done.append(code)
 print('OCR_LESSONS_AUTHORED',len(done),done)
if __name__=='__main__':generate()
