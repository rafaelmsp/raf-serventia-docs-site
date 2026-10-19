"""Source-grounded learning summaries for the final 34 OCR-heavy operation pages.
All wording is educational draft; no action is authorized or technically approved.
"""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parent.parent
GUIDES={
'O-11':([
('Leia a manifestação','Verifique se há petição de habilitação, procuração, substabelecimento ou pedido de atualização.'),
('Confira representação','Identifique qual pessoa o advogado pretende representar e se os poderes constam dos autos.'),
('Compare vínculos','Veja se cadastro e documentos correspondem ao representante e à parte indicados.'),
('Encaminhe dúvidas','Alterações de participantes ou representação dependem de perfil e orientação do servidor.')],
'Petição de habilitação não comprova automaticamente que os vínculos já foram validados.'),
'O-12':([
('Identifique o pedido','Diferencie acordo, desistência e pedido que exige decisão judicial.'),
('Verifique quem se manifestou','Consulte signatários, representação e abrangência do pedido.'),
('Leia a situação da audiência','Observe atos anteriores e eventual reflexo no prosseguimento.'),
('Submeta à análise competente','Homologação, extinção e consequências não são decisões do estagiário.')],
'Acordo ou desistência juntados não significam encerramento automático do processo.'),
'O-13':([
('Reconheça a fase','Diferencie conhecimento, em que se discute o direito, e execução, que busca efetivar o título.'),
('Leia sentença ou título','Identifique o conteúdo que estaria sujeito a cumprimento.'),
('Confira comunicação e prazo','Procure intimação, resposta e atos de cumprimento registrados.'),
('Descreva o estado','Relate providências já documentadas e dúvidas ao servidor.')],
'Na fase executiva, penhora ou outras medidas coercitivas dependem de competência e decisão pertinentes.'),
'O-14':([
('Caso: documento parcial','Compare o que foi pedido ao que efetivamente foi juntado.'),
('Caso: AR irregular','Leia o retorno, sem presumir citação válida.'),
('Caso: acordo incompleto','Confira quais partes se manifestaram e a representação.'),
('Explique a dúvida','Descreva os fatos e peça análise antes de definir o caminho.')],
'O exercício ensina interpretação de documentos, não execução automática de conclusão ou comunicação.'),
'O-15':([
('Abra os autos','Conheça a árvore e a lista cronológica de registros.'),
('Leia o ato relevante','Identifique qual decisão ou comunicação explica o estado atual.'),
('Confira ciência, prazo e resposta','Procure registros associados e peças relevantes.'),
('Reconheça o limite','A seleção da tarefa segue autorização da serventia, não apenas o mapa.')],
'O fluxo didático não substitui a avaliação do servidor nem concede permissões de sistema.'),
'O-16':([
('Encontre o processo','No ambiente autorizado, reconheça painel, tarefa e identificação dos autos.'),
('Abra a visão de Autos Digitais','Identifique a área de consulta do histórico, sem alterar registros.'),
('Reconheça árvore e peças','Diferencie movimentos cronológicos e documentos juntados.'),
('Confira um evento na fonte','Abra a peça correspondente à movimentação que deseja compreender.')],
'Nome e posição dos controles variam conforme versão do PJe e perfil autorizado.'),
'O-17':([
('Localize a determinação','Procure nos autos a necessidade de citar, intimar ou comunicar.'),
('Identifique destinatário','Confirme pessoa, endereço ou representação nos documentos.'),
('Observe modalidade e documento','Via de comunicação e peça a vincular dependem de determinação e rotina.'),
('Examine a validação','Expedição e assinatura exigem perfil autorizado e supervisão.')],
'Preparar ato de comunicação não significa poder expedir, assinar ou definir autonomamente prazo.'),
'O-18':([
('Distinga o ato','Citação e intimação possuem finalidades diversas.'),
('Localize o registro','Encontre evento de comunicação e documento associado.'),
('Leia o retorno','AR, certidão ou mandado podem registrar sucesso, ausência ou irregularidade.'),
('Confira consequências','Prazo ou providência seguinte dependem de ciência, regra e orientação.')],
'AR juntado não prova, sozinho, validade da comunicação ou início do prazo.'),
'O-19':([
('Identifique a questão','Localize manifestação ou situação que pede exame judicial.'),
('Verifique se existe comando cartorário','Leia determinações e compare com atos já cumpridos.'),
('Reconheça a competência','O gabinete e a conclusão dependem da matriz e rotina atual.'),
('Relate ao servidor','Somente encaminhar ou preparar minuta dentro das atribuições autorizadas.')],
'Mera juntada de petição não determina automaticamente conclusão ao juiz.'),
'O-20':([
('Leia a sentença','Identifique o que foi decidido e eventuais ordens complementares.'),
('Confira ciência das partes','Examine intimações ou comunicações constantes do histórico.'),
('Observe prazo e manifestações','Não presuma trânsito em julgado nem cumprimento apenas pela data.'),
('Informe a situação','Aguardo de prazo ou nova providência precisa seguir a rotina válida.')],
'Sentença não equivale automaticamente a encerramento definitivo do processo.'),
'O-21':([
('Identifique o título','Consulte sentença ou documento que embasa a fase executiva.'),
('Diferencie as fases','Conhecimento e execução possuem objetivos distintos.'),
('Confira a sequência','Observe intimação, prazo, resposta e eventual pagamento registrados.'),
('Encaminhe a análise','Medidas de execução dependem de decisão, documentos e perfil competente.')],
'Não presumir cumprimento ou liberar valores a partir de movimentação isolada.'),
'O-22':([
('Identifique o erro','Examine dados de autuação como classe, assunto e informações iniciais.'),
('Compare com os autos','Verifique onde aparece divergência documental.'),
('Confirme alcance da correção','Entenda se é dado cadastral ou questão que exige decisão.'),
('Consulte o responsável','Retificação efetiva requer orientação e perfil autorizado.')],
'Não alterar classe, assunto ou dados pessoais sem verificar os autos e a competência.'),
'O-23':([
('Confira quem participa','Localize partes, advogados e outros participantes.'),
('Identifique a divergência','Observe cadastro, representação, vínculo ou documento inconsistente.'),
('Compare documentos','Verifique procuração e dados nos autos.'),
('Solicite validação','Alterar, excluir ou incluir participantes depende da rotina autorizada.')],
'Associação errada pode afetar comunicação e acesso; mudanças exigem conferência da serventia.'),
'O-24':([
('Leia a determinação','Identifique necessidade de diligência por Oficial de Justiça.'),
('Confira tentativas anteriores','Verifique AR, endereço, mandado e comunicações existentes.'),
('Reconheça a Central de Mandados','Entenda que expedição, distribuição e retorno são fases diferentes.'),
('Relate o resultado','Qualquer nova diligência depende da determinação e do agente competente.')],
'Um AR negativo não significa, sozinho, autorização para expedir mandado.'),
'O-25':([
('Localize a sentença','Confira que a decisão está nos autos e a fase correspondente.'),
('Verifique comunicações','Leia registros de intimação pertinentes às partes.'),
('Examine prazos e recursos','Confira contagem, manifestações e eventuais pendências.'),
('Submeta à certificação','Certificar trânsito em julgado é providência sujeita a conferência e competência.')],
'Não certificar trânsito em julgado sem verificar os recursos, prazos e outras pendências.'),
'O-26':([
('Releia a fase final','Confira sentença, decisões e cumprimentos necessários.'),
('Procure pendências','Veja tarefas, prazos, intimações ou diligências ainda abertas.'),
('Reconheça os critérios','Aptidão para arquivamento exige situação processual documentada.'),
('Encaminhe à supervisão','Baixa e arquivamento devem seguir rotina autorizada.')],
'Arquivamento não pode ser presumido porque parece não haver tarefas na árvore.'),
'O-27':([
('Encontre a solicitação','Leia petição ou decisão que trata de desarquivamento.'),
('Examine a história','Verifique fase e motivos do arquivamento anterior.'),
('Identifique a providência necessária','Diferencie consulta a autos de retomada da tramitação.'),
('Solicite encaminhamento','A reativação depende de competência e da rotina da unidade.')],
'Processo arquivado não é automaticamente reaberto por qualquer pedido; exige análise apropriada.'),

'O-28':([
('Diferencie os níveis','Sigilo geral do processo e sigilo de documento específico têm alcances diferentes.'),
('Leia a fundamentação','Identifique determinação judicial ou regra que fundamenta a restrição.'),
('Confira quem pode acessar','Permissões dependem da legitimidade, do documento e do perfil.'),
('Peça revisão competente','Não altere sigilo ou compartilhe dados sem autorização expressa.')],
'Não exponha autos ou documentos restritos; classificação de sigilo não é decisão autônoma do estagiário.'),
'O-29':([
('Leia o motivo','Identifique a alegação de incompetência, erro ou determinação de redistribuição.'),
('Compare dados cadastrais','Confira classe, assunto e indicação de destino conforme os autos.'),
('Diferencie correção e transferência','Retificação de autuação não é a mesma coisa que redistribuição entre unidades.'),
('Confirme o responsável','Destino e execução da movimentação exigem competência e autorização.')],
'Não redistribuir processo por suposta incompetência sem determinação ou rotina competente.'),
'O-30':([
('Identifique o participante','O infográfico cita testemunha, perito, terceiro interessado e outros papéis.'),
('Leia o ato de vinculação','Verifique se a inclusão é pertinente e documentada.'),
('Confira o vínculo','Diferencie parte principal de participante especial e compare os dados.'),
('Submeta o cadastro','A inclusão em sistema depende de perfil e supervisão.')],
'Não cadastrar terceiros ou alterar vínculos apenas por inferência, sem documento e autorização.'),
'O-31':([
('Reconheça o problema','Erros de autuação, cadastro, acesso ou diligência exigem tratamentos diferentes.'),
('Associe ao tema','Classifique se é informação, comunicação, conclusão, arquivamento ou outro assunto.'),
('Confira ato e tarefa','Uma tabela de exceções auxilia a leitura, mas não confirma a situação real.'),
('Escolha com supervisão','As funções do sistema são usadas somente pelo perfil competente.')],
'O quadro de exceções não é atalho para executar atos sem conferir o processo.'),
'O-32':([
('Identifique o recurso','Verifique petição de recurso inominado e a decisão recorrida.'),
('Confira datas e peças','Observe intimação, protocolo e eventuais outros recursos.'),
('Examine preparo ou gratuidade','Procure os documentos e determinações relativos a custas ou benefício.'),
('Encaminhe ao responsável','Admissibilidade e atos subsequentes dependem da rotina competente.')],
'Certidão automática de tempestividade ou juntada não dispensam conferência das peças e decisões.'),
'O-33':([
('Identifique o retorno','Procure acórdão, certidão de baixa ou comunicação da Turma Recursal.'),
('Leia o resultado','Entenda se houve manutenção, reforma ou determinação de providência.'),
('Confira as partes intimadas','Verifique registros de ciência e ordens de cumprimento.'),
('Informe a situação','O retorno pode exigir prosseguimento, execução ou arquivamento conforme decisão.')],
'Não tratar todo acórdão como ordem de arquivamento ou encerramento automático.'),
'O-34':([
('Leia a ordem','Verifique se há determinação de expedir carta precatória para outra unidade.'),
('Reconheça o destino','Confira juízo deprecado, diligência e elementos necessários.'),
('Identifique peças','Observe quais documentos acompanham o pedido de cooperação.'),
('Submeta a expedição','Assinatura, envio e cadastro dependem do perfil e do procedimento vigente.')],
'Não emitir ou assinar carta precatória por iniciativa própria.'),
'O-35':([
('Localize o retorno','Encontre nos autos a carta ou a certidão devolvida.'),
('Classifique o resultado','Diligência cumprida, frustrada ou parcialmente realizada exigem leituras distintas.'),
('Leia os documentos','Consulte certidão do juízo destinatário e peças anexas.'),
('Relate pendências','Nova diligência ou outra providência depende de determinação e supervisão.')],
'Devolução da carta não prova automaticamente que o ato foi cumprido.'),
'O-36':([
('Encontre o envio','Localize registro de remessa ao juiz leigo.'),
('Leia a proposta','Diferencie minuta ou manifestação de decisão homologada.'),
('Verifique retorno','Observe se houve apreciação pelo magistrado competente.'),
('Acompanhe o estado','Encaminhamento e próximos atos exigem supervisão da unidade.')],
'Minuta do juiz leigo não substitui apreciação/homologação quando legalmente necessária.'),
'O-37':([
('Reconheça as características','A fonte cita justiça gratuita, prioridade, valor da causa e pedidos de tutela.'),
('Compare com os autos','Verifique se dados cadastrais e petições correspondem.'),
('Identifique inconsistências','Dados faltantes ou divergentes podem exigir análise.'),
('Encaminhe a correção','Não alterar características ou direitos sem orientação competente.')],
'Prioridade ou tutela pedida não é automaticamente concedida nem deve ser inserida por suposição.'),
'O-38':([
('Identifique o pedido urgente','Procure petição de tutela ou liminar e sua situação nos autos.'),
('Confira decisão existente','Diferencie pedido pendente, tutela deferida ou indeferida.'),
('Leia o comando','Observe prazo, destinatário e necessidade de comprovação de cumprimento.'),
('Leve ao responsável','Medidas de urgência e alterações são decididas pelo juiz e cumpridas no perfil apropriado.')],
'Uma petição de tutela não equivale a decisão concedendo o pedido.'),
'O-39':([
('Leia a decisão','Diferencie ordem de bloqueio, desbloqueio e transferência no SISBAJUD.'),
('Verifique o retorno','Confira resposta positiva, negativa ou saldo parcial registrado.'),
('Identifique valores e alcance','Leia o documento e os montantes, sem presumir disponibilidade.'),
('Encaminhe o controle','Operações bancárias e transferências exigem determinação e autorização específica.')],
'Não efetuar bloqueio, transferência ou liberação com base apenas em indicação da árvore.'),
'O-40':([
('Reconheça o mecanismo','O infográfico apresenta bloqueio reiterado e retornos sucessivos.'),
('Leia a sequência','Compare tentativas por data e respostas, inclusive resultados parciais.'),
('Confira a decisão','Verifique alcance temporal e eventual nova ordem ou encerramento.'),
('Relate o consolidado','Somatório, continuidade e encerramento dependem de análise competente.')],
'Um retorno parcial não equivale ao resultado final da ordem reiterada.'),
'O-41':([
('Localize o recurso','Procure a interposição e a decisão recorrida.'),
('Identifique o marco de ciência','Confira intimação e regras que definem início do prazo.'),
('Compare protocolo e período','Não faça contagem automática sem feriados/suspensões aplicáveis.'),
('Submeta a certificação','Tempestividade exige revisão conforme a determinação e o perfil autorizado.')],
'Não certificar tempestividade apenas comparando duas datas sem examinar os marcos legais.'),
'O-42':([
('Leia a determinação','Identifique motivo documentado de suspensão ou sobrestamento.'),
('Diferencie hipóteses','Há situações ligadas a evento externo, tema repetitivo ou ordem do juízo.'),
('Observe condição de retorno','Verifique evento, marco ou prazo associado à retomada.'),
('Mantenha rastreabilidade','Alteração de situação processual requer rotina e perfil competentes.')],
'Não aplicar suspensão por suposto tema repetitivo sem verificar abrangência e decisão vigente.'),
'O-43':([
('Identifique a ordem de pagamento','Leia decisão ou ato que fundamenta o mandado.'),
('Confira beneficiário','Verifique dados e documentos necessários à emissão no perfil competente.'),
('Diferencie etapas','Requisição, digitação, assinatura, expedição e efetivação são fases distintas.'),
('Encaminhe o controle','Não libere valores, assine ou prometa pagamento sem confirmação.')],
'Mandado solicitado não significa expedido ou pago; valores exigem controle rigoroso.'),
'O-44':([
('Leia a nomeação','Identifique decisão que designa perito e a finalidade da perícia.'),
('Confira os dados','Verifique identificação, cadastro e forma de comunicação indicada.'),
('Observe resposta e prazo','O especialista pode aceitar, recusar ou apresentar esclarecimentos e laudo.'),
('Comunique pendências','Cadastro, intimação e exigências dependem de determinação e autorização.')],
'Não presumir aceitação do encargo nem alterar prazo pericial sem decisão competente.')
}
def main():
 done=[]
 for code,(steps,caution) in GUIDES.items():
  path=ROOT/'data/lessons'/(code+'.json')
  d=json.loads(path.read_text(encoding='utf8'))
  d['state']='author_draft'
  d['authored_batch']='ocr_topic_review_draft'
  d['objective']=f'Aprender a identificar, conferir e explicar as principais situações de “{d["title"]}”, com atenção aos limites da atuação supervisionada.'
  d['plain']=f'O infográfico aborda {d["title"].lower()} e situações encontradas nos autos. O roteiro organiza as perguntas mais importantes e aponta os documentos a examinar, sem conferir autorização para executar atos.'
  d['steps']=[{'title':a,'instruction':b,'why':'A verificação contextualiza o processo; encaminhamento ou ato real dependem de norma atual, decisão e perfil competente.'} for a,b in steps]
  d['observe']=[{'title':a,'detail':b} for a,b in steps]
  d['terms']=[{'term':a,'meaning':b,'example':f'Observe esse ponto no infográfico da página {d["page"]}, sem inferir efeitos jurídicos só pelo desenho.'} for a,b in steps]
  d['scene']['regions']=[{'title':a,'detail':b} for a,b in steps]
  d['decision']={'question':f'Em um processo fictício relativo a “{d["title"]}”, o que deve ser feito antes de qualquer providência?',
   'options':[{'label':f'{steps[0][0]} e conferir o documento, a regra e a competência.','feedback':'Correto. A leitura documental precede qualquer ato autorizado.','correct':True},
              {'label':'Executar imediatamente a função ilustrada, sem consultar a fonte.','feedback':'A imagem não autoriza a execução de atos.','correct':False},
              {'label':'Ignorar documentos ou prazos pertinentes.','feedback':'Documentos e marcos legais precisam de conferência.','correct':False}]}
  d['practice']={'scenario':f'Exemplo fictício: surge no histórico uma questão de “{d["title"]}” e o estagiário precisa relatar seu estado ao servidor.',
   'question':'Qual sequência inicial é mais adequada?',
   'options':[{'label':f'Identificar o registro, {steps[1][0].lower()}, descrever o fato e pedir orientação quando necessário.','feedback':'Adequado. A análise é uma atividade de conferência, não decisão autônoma.','correct':True},
              {'label':'Presumir que o ato já foi totalmente cumprido.','feedback':'Um registro isolado não prova cumprimento integral.','correct':False},
              {'label':'Encerrar ou alterar a tarefa sem conferir quem determinou o quê.','feedback':'Isso pode ultrapassar a atribuição do estagiário.','correct':False}]}
  d['mistakes']=[{'mistake':'Aplicar a interpretação sem fonte','correct':caution},
     {'mistake':'Ignorar a fase processual','correct':'Leia as decisões e os documentos anteriores.'},
     {'mistake':'Usar função sem perfil ou ordem','correct':'Peça orientação e siga a rotina vigente do servidor responsável.'}]
  d['mastery']=[f'Consigo explicar o tema “{d["title"]}”.',
               f'Sei o que conferir em “{steps[0][0]}”.',
               'Reconheço quando uma providência é reservada ao servidor ou magistrado.']
  d['source_highlights']=[a+': '+b for a,b in steps[:3]]
  d['source_highlight_status']='ocr_interpretacao_a_revisar'
  d['status_note']='Roteiro pedagógico provisório reconstruído a partir do infográfico e OCR; conferência técnica e jurídica ainda necessária.'
  d['pedagogical_ready']=d['technical_approved']=d['student_tested']=False
  path.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf8')
  done.append(code)
 print('OPERATION_34_AUTHORED',len(done),'CODES',done)
if __name__=='__main__':main()
