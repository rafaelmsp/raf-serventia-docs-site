from pathlib import Path
r=Path(__file__).resolve().parents[1]/'scripts/review_source_batch.py'
s=r.read_text(encoding='utf8')
marker='entries=[]'
assert marker in s
extra="""CHECKS.update({
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
"""
assert 'CHECKS.update' not in s
s=s.replace(marker,extra+marker)
s=s.replace("assert len(entries)==96 and sum(e['visual_checked'] for e in entries)==7","assert len(entries)==96 and sum(e['visual_checked'] for e in entries)==15")
r.write_text(s,encoding='utf8')
print('EXPANDED_AUDIT_BATCH',15)
