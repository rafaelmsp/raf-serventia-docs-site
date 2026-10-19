# RAF Serventia Docs — Cobertura integral de imagens e mapas V2

**Versão:** v2.2-premium-draft  
**Fonte primária:** Manual Operacional do Estagiário na Serventia — PJe, 107 páginas, edição 15/10/2026.  
**Autor da referência:** Rafael MS Passos.

## Entrega desta rodada

- **96/96 cenas SVG premium** (cada código com arte e título próprios, ícones temáticos, organização de tela ilustrada e blocos explicativos).
- **96/96 mapas SVG** (quatro pontos de compreensão de leitura da fonte, sem representar autorização de execução).
- **96/96 páginas HTML** exibem cenas na abertura e na etapa Reconhecer; diagramas aparecem na etapa Observar e fazer, inclusive quando o procedimento ainda depende de conferência editorial.
- **96/96 itens do catálogo** apresentam miniatura ilustrada associada ao código.
- Sete telas de aprendizagem com glossário, hotspots, decisões simuladas, prática, checklist e links à página correspondente no PDF.
- **14 roteiros específicos redigidos**: os seis pilotos e O-01, O-02, O-04, O-05, O-06, O-07, O-09 e O-10.
- **82 fichas** receberam temas visuais individualizados e prompts de estudo, com ressalvas sobre OCR e ausência de roteiro processual validado.
- Rotas técnicas anteriores e PDF original preservados.

## Resultado de testes

O script `tests/full-visual-qa.cjs` percorreu todos os itens em Chromium 390 px:

| Grupo | Aulas testadas | Cenas carregadas | Mapas carregados |
|---|---:|---:|---:|
| Operações (O) | 49 | 49 | 49 |
| Pauta (P) | 16 | 16 | 16 |
| Relatórios (R) | 5 | 5 | 5 |
| Balcão Físico (BF) | 12 | 12 | 12 |
| Balcão Virtual (BV) | 14 | 14 | 14 |
| **Total** | **96** | **96** | **96** |

**Falhas detectadas nesta bateria: zero.** Catalogo carregou miniaturas em duas categorias verificadas, sem overflow global.

O teste `tests/full-responsive-qa.cjs` verificou uma amostra de seis aulas nas larguras de 360, 390, 768 e 1366 px: 24 cenários aprovados sem cortes horizontais da página.

## Fidelidade editorial e ressalvas

Os 65 itens cujo texto de origem depende de OCR provisório continuam exigindo conferência do infográfico. A camada editorial nunca deve ser automaticamente aprovada por um gerador. As 82 fichas sem roteiro específico ainda não ensinam integralmente os passos operacionais. Os diagramas de leitura são visuais didáticos e NÃO são o sistema PJe ou reprodução oficial da interface.

**Nenhuma das 96 aulas recebeu homologação jurídico-pedagógica; não usar como procedimento autônomo na serventia.** Necessários: revisão técnica, teste com estagiários reais e auditoria aprofundada de acessibilidade.

## Artefatos

- `assets/learning/{codigo}/ilustracao-premium.svg` — uma cena por código.
- `assets/learning/{codigo}/fluxo-premium.svg` — um mapa por código.
- `data/learning-visuals-manifest.json` — rastreabilidade individual.
- `data/lessons/{codigo}.json` — roteiro didático e estado editorial.
- `scripts/build_all_visuals.py` — pipeline determinístico e reproduzível das 90 artes adicionais.
- `scripts/author_batch_two.py` — oito roteiros autorais adicionados.
- `scripts/enrich_previews.py` — estudo seguro das outras 82 prévias.
- `tests/full-visual-qa.json` e `tests/full-responsive-qa.json` — evidência do funcionamento.
- `data/progresso-pedagogico.json` — andamento técnico ponderado.

## Próxima fase editorial

Transformar cada uma das 82 prévias em roteiro específico, com explicações extraídas do PDF e revisão humana de passos, atos e referências normativas. Depois aplicar teste de compreensão com iniciantes e corrigir as dificuldades observadas. Não inferir procedimentos a partir da aparência de um infográfico.
