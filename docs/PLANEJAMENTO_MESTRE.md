# RAF Serventia Docs — Plano Mestre e contrato da execução contínua

Versão de referência: Prompt Mestre UX Premium Ilustrada v1.0, datado de 18/10/2026.
Fonte: Manual Operacional do Estagiário na Serventia — PJe, 107 páginas, edição 15/10/2026.

## Objetivo

Produzir 96 fichas técnicas HTML explicativas (O 49, P 16, R 5, BF 12, BV 14), cada uma com ilustração original, fluxo/mapeamento didático, etapas, alertas, checklist, FAQ, rastreabilidade e link à fonte. O PDF permanece como referência, não substituto das páginas HTML.

## Fases e pesos

| Código | Fase | Peso |
|---|---|---:|
| F00 | Auditoria de fonte e risco | 8% |
| F01 | Sistema UX premium | 10% |
| F02 | Revisão editorial e OCR | 9% |
| F03 | Pipeline de arte SVG, mapas e manifestos | 8% |
| F04 | 49 fichas de Operações | 20% |
| F05 | 16 fichas de Pauta | 9% |
| F06 | 5 fichas de Relatórios | 5% |
| F07 | 12 fichas de Balcão Físico | 7% |
| F08 | 14 fichas de Balcão Virtual | 8% |
| F09 | Busca, favoritos, checklists, navegação e PDF | 6% |
| F10 | Testes, acessibilidade e revisão | 7% |
| F11 | GitHub Pages e comprovação do deploy | 3% |
| TOTAL | | 100% |

## Micropesos por ficha

- Texto reescrito e fundamentado no manual: 25%.
- Ilustração original própria: 20%.
- Fluxo ou mapa com explicações coerentes: 20%.
- Etapas/atenções coerentes e supervisão: 15%.
- Checklist/FAQ funcional e pertinente: 10%.
- Teste e registro da conferência: 10%.

O sistema de progresso concede apenas crédito parcial quando há rascunho ainda não revisado. A geração de 96 SVGs não significa 96 fichas prontas.

## Políticas fundamentais

1. A fonte é não oficial e originalmente restrita. A publicação solicitada pelo autor não comprova homologação institucional.
2. Identificar conteúdo como FONTE, INTERPRETAÇÃO DIDÁTICA, EXEMPLO SIMULADO ou PENDENTE. Jamais inventar procedimentos, normas, prazos, direitos de acesso e atos automatizados.
3. As ilustrações SVG são representações didáticas, não reproduções oficiais do PJe.
4. Fluxos conceituais não devem aparentar comandos processuais. O checklist é apenas para estudo e conferência.
5. Conservar as 107 páginas-fonte e o PDF intacto; disponibilizar URLs estáveis por código.
6. Testar no mínimo 360, 390, 430, 768, 1024, 1366 e 1920 pixels.
7. Não declarar 100% sem revisão humana apropriada, auditoria de links, acessibilidade, segurança, GitHub Actions concluído e URLs online verificadas.

## Continuidade

Reabrir data/progress.json e docs/progresso-execucao.md para recuperar estado real. Executar a próxima ficha pendente de revisão editorial, atualizar todos os artefatos relacionados e repetir os testes após mudanças. Não reiniciar a contagem nem apagar os estados já aprovados.

### Comandos de reconstrução

python scripts/build_illustrated.py

python tests/validate-premium.py

node tests/qa-premium.cjs

node tests/qa-all-96.cjs

python scripts/update_progress.py

A partir de 19/10/2026, a primeira geração premium produz SVGs, mapas e páginas como rascunho. As fichas geradas permanecem com status de revisão pendente até serem validadas.
