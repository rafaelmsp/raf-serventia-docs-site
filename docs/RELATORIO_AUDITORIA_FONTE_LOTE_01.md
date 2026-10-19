# RAF Serventia Docs — Auditoria da Fonte, Lote 01

**Edição:** 19 de outubro de 2026  
**Projeto:** RAF Serventia Docs · V2.5 · Material didático não oficial  
**Documento primário:** Manual Operacional do Estagiário na Serventia — PJe, 107 páginas, 15/10/2026.

## Objetivo e limites

Esta fase confronta o conteúdo de aulas HTML com **a imagem original de determinadas páginas do PDF**. Não constitui revisão jurídica integral, validação de procedimento, checagem de vigência de matriz interna, certificação institucional, ensaio com estagiários ou autorização para praticar atos no sistema PJe.

**Situação:** 96/96 roteiros didáticos construídos; **15/96 fontes confrontadas visualmente**; **81/96 ainda pendentes**. **0/96 homologadas**.

## Páginas examinadas diretamente no documento original

| Aula | PDF | Ponto da revisão | Alerta |
|---|---:|---|---|
| O-09 | 14 | Citação, intimação, AR e estados do retorno | Não presumir ciência válida e prazo por título do evento |
| O-19 | 24 | Conclusão, minuta e assinatura | Nem toda petição implica conclusão; perfis e competência distintos |
| O-25 | 30 | Trânsito em julgado | Prazo recursal, comunicações, recursos e pendências impeditivas |
| O-32 | 37 | Recurso inominado | Recursos múltiplos e preparo/gratuidade devem ser individualizados |
| O-38 | 43 | Tutela/liminar | Distinguir pedido pendente, deferimento e prova de cumprimento |
| O-39 | 44 | SISBAJUD | Bloqueio, resultado, desbloqueio, transferência e retorno não se confundem |
| O-41 | 46 | Tempestividade do recurso | Termo inicial, horário de protocolo, feriados e suspensões |
| O-43 | 48 | Mandado de pagamento | Ordem, preenchimento, assinatura, expedição e resultado distintos |
| O-45 | 50 | Sete gabinetes | Matriz de treinamento; atualidade e atribuições não comprovadas |
| P-14 | 69 | Diligência negativa e pauta | Se outra diligência está pendente, não retirar pauta automaticamente |
| P-15 | 70 | Intimação não expedida | Diferente de comunicação expedida sem êxito; não cancelar por conta própria |
| P-16 | 71 | Marco de 72h | Regra relatada oralmente; confirmar vigência antes de usar |
| BF-04 | 82 | Salvar e assinar petição | Arquivo salvo e assinado não equivalem a protocolo |
| BV-06 | 97 | Identificação remota | OAB apenas para advogado; verificar legitimidade e sigilo |
| BV-07 | 98 | Mensagem de abertura | Modelo de treinamento; verificar texto e exceções do ato normativo |

Todos os 15 registros possuem uma `source_observation` descritiva e `risk_note` para orientar o confronto, em `data/editorial-audit.json`. Essas informações também aparecem em `data/lessons/{código}.json` para ser exibidas ao leitor no HTML.

## Referência oficial externa localizada

A página de Informes da CGJ/TJRJ contém registro em 24/08/2026 do **Ato Normativo Conjunto TJ/CGJ nº 15/2026**, que altera o nº 05/2021 e trata do Balcão Virtual. O registro comprova a existência da publicação, **não sua redação integral, limites, exceções ou vigência consolidada**.

- Consulta institucional: https://www.tjrj.jus.br/pt/web/cgj/informes
- Orientação institucional sobre falsa identidade no atendimento virtual: https://www.tjrj.jus.br/falsa-identidade-em-atendimento-virtual

Nenhum limite foi elevado ao status de norma validada nesta auditoria.

## Implementação HTML

- Novo painel: `auditoria-fonte.html`.
- Índice: 96 registros com busca, filtros por área e por revisão, paginação de nove itens, links para aula e PDF na página exata.
- Para cada fonte confrontada: observação e alerta, recolhidos por padrão, com classificação visual.
- Na abertura da aula: seção de auditoria resumida, distinguindo fonte confrontada de fonte pendente e link ao painel.
- A situação de todas as páginas continua `technical_approved=false` e `pedagogical_ready=false`.
- O percentual geral de V2 permanece **68%**: não foram fabricados pontos de aprovação normativa ou pedagógica.

## Testes

- `tests/editorial-audit-ui-qa.cjs` → **4/4 cenários** em 360, 390, 768 e 1366 px: índices, filtros, pesquisa de P-16, retorno do PDF para página 71, banners nas aulas, ausência de overflow.
- `tests/v2-static.py` → 96 fichas presentes e sem falhas estruturais.
- `tests/full-content-qa.py` → 96 rascunhos estruturados, 192 vetores individuais e nenhum roteiro marcado como aprovado.
- Capturas de QA: `qa/review-pages/auditoria-390.png` e `auditoria-1366.png`, mantidas somente para exame do layout, não como documentação oficial.

## Próximos bloqueios da revisão

1. Comparar visualmente o restante das **81 páginas**.
2. Verificar integralmente fontes normativas, versão do PJe, atuação autorizada e fluxos locais.
3. Reescrever trechos derivados de OCR nos quais o texto ou as instruções não coincidam com o infográfico.
4. Testar clareza com estagiários iniciantes, critérios de acerto e tecnologia assistiva.
5. Solicitar revisão do responsável da unidade antes de chamar qualquer roteiro de validado.

**Status de todos os 96 roteiros: rascunho didático para revisão; não certificado para execução autônoma.**
