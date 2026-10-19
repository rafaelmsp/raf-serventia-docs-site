from pathlib import Path
import json,datetime
ROOT=Path(__file__).resolve().parents[1]
INDEX=json.loads((ROOT/'dados/procedimentos.json').read_text(encoding='utf8'))
CHECKS={
'O-09':('Citação, intimação e AR','PDF p.14',
  'O infográfico distingue citação, intimação e AR; apresenta retornos positivo, negativo, destinatário ausente, endereço insuficiente, horário irregular e ausência de devolução.',
  'Um AR positivo não deve ser tratado como ciência válida sem conferir documento, destinatário e contexto. Não presumir início de prazo.'),
'O-39':('SISBAJUD — bloqueio/desbloqueio/transferência','PDF p.44',
  'O documento distingue decisão, retorno positivo, retorno negativo, bloqueio parcial/integral, desbloqueio e transferência e indica controle do resultado na árvore.',
  'Operação no SISBAJUD, assinatura, transferências e liberação são atos exclusivos do agente competente. Roteiro didático não concede acesso.'),
'O-43':('Mandado de pagamento','PDF p.48',
  'O documento separa decisão, dados do beneficiário, valor, preenchimento, assinatura, expedição e registro do resultado.',
  'Requisição, mandado digitado, mandado assinado, mandado expedido e pagamento efetivado não são situações equivalentes. Conferir beneficiário e decisão atual.'),
'O-45':('Matriz dos sete gabinetes','PDF p.50',
  'A folha contém os sete gabinetes e respectivas etiquetas; o próprio manual esclarece que a etiqueta não determina, isoladamente, abertura de conclusão.',
  'A matriz foi reproduzida de material de treinamento e não demonstra vigência atual. Confirmar com a chefia e não automatizar conclusões.'),
'P-14':('Diligências e permanência na pauta','PDF p.69',
  'O fluxo bifurca diante de um retorno negativo: se houver outra diligência pendente, manter a pauta e aguardar; havendo retornos relevantes negativos, há fluxo observado na serventia sob orientação.',
  'O prazo de cinco dias é exemplo de treinamento, não regra geral comprovada. Cancelar pauta, certificar e expedir PAC dependem de comando, servidor e perfil.'),
'P-16':('Marco relatado de 72 horas','PDF p.71',
  'A fonte separa mais de 72 horas (juiz togado) e até 72 horas (juiz leigo), expressamente como encaminhamento relatado em treinamento oral.',
  'Não apresentar o marco de 72 horas como norma geral vigente. Confirmar horário exato, orientação atual e autoridade de destino antes de movimentar.'),
'BV-07':('Mensagem de abertura do Balcão Virtual','PDF p.98',
  'A página reproduz mensagem dirigida a advogados sobre apresentação de OAB/câmera e limites de 10 minutos e três processos por atendimento.',
  'Ato 15/2026 teve publicação identificada no portal da CGJ; sua redação consolidada, aplicação e exceções ainda requerem verificação antes de torná-lo regra operacional.')
}
CHECKS.update({
'O-19':('Conclusão ao juiz, minuta e assinatura','PDF p.24',
 'A página descreve quando o assunto exige apreciação judicial e apresenta o fluxo da tarefa Conclusão ao Juiz — Minuta e subsequente remessa para assinatura.',
 'Nem toda petição exige conclusão; minuta e assinatura são atos com funções e perfis próprios. Verificar despacho anterior, competência e supervisão.'),
'O-25':('Certificação de trânsito em julgado','PDF p.30',
 'O checklist exige sentença, comunicação às partes, prazo recursal encerrado, inexistência de recurso em processamento e ausência de outras pendências impeditivas.',
 'Não certificar trânsito em julgado com recurso ou prazo aberto; a data de término precisa de conferência da ciência e do calendário aplicável.'),
'O-32':('Recurso inominado no JEC','PDF p.37',
 'A página apresenta tarefa de análise de petição recursal, identificação de recursos múltiplos e conferência de custas ou gratuidade antes do encaminhamento.',
 'Cada recurso pode gerar tarefa própria. Certificação de custas ou gratuidade não se confunde com julgamento do recurso. O fluxo documentado pode variar por perfil e versão.'),
'O-38':('Tutela ou liminar na árvore','PDF p.43',
 'O infográfico distingue pedido sem decisão, deferimento, indeferimento, comunicação urgente e prova de cumprimento; determina leitura integral da decisão.',
 'Pedido de tutela não representa tutela deferida. Conferir comando, destinatário e prazos; atos urgentes e conclusão exigem perfil e determinação competente.'),
'O-41':('Certificação de tempestividade do recurso','PDF p.46',
 'A página orienta identificar a data da ciência, conferir prazo legal, protocolo do recurso, feriados e suspensões, e elaborar registro claro da conclusão.',
 'Contagem de prazo não se deduz apenas da data da petição. Confirmar termo inicial, calendário aplicável e eventual suspensão; certidão exige agente competente.'),
'P-15':('AR ou intimação não expedido','PDF p.70',
 'A página diferencia diligência negativa (expedida e devolvida sem êxito) de ato não expedido; no segundo caso mostra conferência, modelo de certidão, assinatura e conclusão.',
 'A audiência permanece na pauta até determinação diversa. Falta de expedição não autoriza cancelamento automático; conferência e encaminhamento dependem da serventia.'),
'BF-04':('Petição — salvar e assinar','PDF p.82',
 'O fluxo descrito compreende revisar pedido, definir formato, salvar em local institucional, conferir assinatura legítima e confirmar encaminhamento/protocolo.',
 'Arquivo salvo, papel assinado e juntada efetiva no PJe não são equivalentes. O próprio manual alerta que o botão/caminho de salvar requer validação local.'),
'BV-06':('Identificar solicitante no Balcão Virtual','PDF p.97',
 'O infográfico orienta reconhecer se a pessoa é advogado, parte ou terceiro, conferir identificação adequada, vínculo, representação e restrição de acesso.',
 'Carteira OAB não deve ser exigida de cidadão que não é advogado. Não fotografar documento por iniciativa própria nem divulgar informação sigilosa sem legitimidade confirmada.')
})
entries=[]
for item in INDEX:
 code=item['codigo'];lesson_file=ROOT/'data/lessons'/(code+'.json')
 lesson=json.loads(lesson_file.read_text(encoding='utf8'))
 audited=code in CHECKS
 entry={'code':code,'title':item['titulo'],'section':item['categoria'],'page':item['pagina'],
  'source_method':item['origemTexto'],'visual_checked':audited,
  'review_status':'confronto_visual_fonte' if audited else 'revisao_visual_pendente',
  'technical_approved':False,'pedagogical_approved':False,'reviewed_at':'2026-10-19' if audited else None}
 if audited:
  heading,page_label,seen,risk=CHECKS[code]
  entry.update({'source_observation':seen,'risk_note':risk,'heading':heading,'pdf_label':page_label,
   'review_scope':'Confronto visual de fonte primária; não equivale a validação operacional ou jurídica.'})
  lesson['editorial_audit']={
   'status':'source_image_checked','source_page':item['pagina'],'checked_date':'2026-10-19',
   'source_observation':seen,'risk_note':risk,
   'remaining':'Faltam norma vigente, validação do setor e teste de compreensão com aprendizes.'}
  lesson['technical_approved']=False;lesson['pedagogical_ready']=False
  lesson_file.write_text(json.dumps(lesson,ensure_ascii=False,indent=2),encoding='utf8')
 entries.append(entry)
dest=ROOT/'data/editorial-audit.json';dest.write_text(json.dumps(entries,ensure_ascii=False,indent=2),encoding='utf8')
assert len(entries)==96 and sum(e['visual_checked'] for e in entries)==15
print('EDITORIAL_SOURCE_CHECK',sum(e['visual_checked'] for e in entries),'PENDING',sum(not e['visual_checked'] for e in entries))
