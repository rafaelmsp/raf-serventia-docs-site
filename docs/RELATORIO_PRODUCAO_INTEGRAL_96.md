# RAF Serventia Docs — Fechamento da produção integral de aulas (rascunho V2.4)

**Data:** 19/10/2026  
**Fonte primária:** Manual Operacional do Estagiário na Serventia — PJe (15/10/2026, 107 páginas).  
**Modalidade:** documentação didática não oficial; o conteúdo depende de validação das rotinas atualmente vigentes.

## Entrega integral de produção

| Área | Códigos | Roteiros didáticos específicos | Cenas premium SVG | Diagramas premium SVG |
|---|---:|---:|---:|---:|
| Operações no PJe | 49 | 49 | 49 | 49 |
| Pauta e audiências | 16 | 16 | 16 | 16 |
| Relatórios | 5 | 5 | 5 | 5 |
| Balcão Físico | 12 | 12 | 12 | 12 |
| Balcão Virtual | 14 | 14 | 14 | 14 |
| **Total** | **96** | **96** | **96** | **96** |

Todas as páginas continuam com sete telas: objetivo, termos explicados, ilustração com hotspots, tópicos de observação, passos didáticos, decisão e prática com feedback. Cada procedimento tem link à página original e à consulta técnica legada.

## Proveniência do conteúdo

- **6 pilotos iniciais** redigidos especificamente a partir do manual.
- **8 aulas adicionais** de Operações redigidas da fonte e infográficos.
- **23 roteiros** de Balcão Físico/Virtual adaptados da camada textual nativa do PDF.
- **6 roteiros especiais** de matriz, conclusão e abertura do Balcão Virtual preparados manualmente a partir de texto nativo.
- **19 roteiros** de Pauta/Relatórios reconstruídos a partir das imagens e transcrições OCR provisórias.
- **34 roteiros** de Operações reconstruídos a partir das imagens e transcrições OCR provisórias.

**53 aulas exigem conferência prioritária de OCR e conteúdo jurídico.** As outras 43 também carecem de revisão normativa, editorial e de conformidade com as atribuições atuais. A interface não deve apresentar sínteses como transcrição literal; informa sua procedência por status.

## Testes concluídos

- `tests/full-content-qa.py`: 96/96 roteiros com objetivo, glossário, etapas, exercícios de resposta única, hotspots e quatro ou mais etapas; todos em rascunho e nenhum aprovado.
- `tests/v2-static.py`: verificação de correspondência entre código, página, links, ilustração e integridade XML dos 192 SVGs.
- `tests/full-visual-qa.cjs`: 96/96 páginas abertas no Chromium; 96 cenas e 96 diagramas carregados sem falhas, com interações de hotspots e catálogo.
- `tests/full-responsive-qa.cjs`: 24/24 amostras em 360, 390, 768 e 1366 px, sem rolagem horizontal global.
- `tests/full-live-qa.cjs`: verificação online do release visual anterior, 10/10 cenários em 390 e 1366 px.
- Todos os temas mantêm informação de fonte e rotulagem de material não oficial.

## Conclusão de escopo

**Produção integral de conteúdo inicial e material gráfico: concluída (96/96).**
**Homologação editorial e pedagógica: 0/96.**

O percentual de implementação de 68% é ponderado pelo modelo de execução e **não mede eficácia de aprendizagem**. As etapas remanescentes exigem revisão por servidor responsável, verificação da normatização atual, teste com estagiários reais, auditoria de acessibilidade e eventuais correções.

A plataforma não executa atos judiciais. Os exemplos são fictícios. O infográfico original permanece como fonte de conferência, não substituído pelos desenhos. Acesso técnico não implica autorização de assinatura, expedição, movimentação ou leitura de autos restritos.

## Para retomar a revisão humana

1. Abrir `data/lessons-index.json`, `data/progresso-pedagogico.json` e `docs/LOG_REVISAO_PEDAGOGICA.md`.
2. Priorizar páginas com `source_highlight_status=ocr_interpretacao_a_revisar` ou análogo.
3. Registrar revisor, data, norma vigente, divergência encontrada e evidência do teste com estagiários.
4. Alterar `pedagogical_ready`, `technical_approved` ou `student_tested` somente após comprovação.
5. Executar testes novamente e publicar o lote revisado.

## Repositórios

- Público: https://github.com/rafaelmsp/raf-serventia-docs-site
- Desenvolvimento privado: https://github.com/rafaelmsp/raf-serventia-docs
- Pages: https://rafaelmsp.github.io/raf-serventia-docs-site/
