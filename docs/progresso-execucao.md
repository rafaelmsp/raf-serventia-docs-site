# RAF Serventia Docs — Execução premium

**Progresso global apurado:** 53,5%

[██████████░░░░░░░░░░]

**Data (UTC):** 2026-10-19T03:26:05.067136+00:00

Os percentuais usam os pesos do Prompt Mestre e atribuem crédito parcial a ativos gerados mas ainda não revisados.

## Evidências de entrega

- Fichas html: 96
- Novas ilustracoes svg: 96
- Novos mapas svg: 96
- Paginas fonte html: 107
- Fichas editorialmente aprovadas: 0
- Pilotos parcialmente conferidos: 3
- Testes navegador aprovados: 42
- Rotas verificadas android: 96
- Deploy premium confirmado: True

## Progresso por fase

| Fase | Avanço | Peso | Observação |
|---|---:|---:|---|
| F00 | 71,4% | 8% | Auditoria de fonte, rotas e versões; privacidade editorial complementar pendente |
| F01 | 85,7% | 10% | Design system, layout, abas, tema, impressão, mobile; homologação em aparelho físico pendente |
| F02 | 22,2% | 9% | Mapeamento de páginas e status; correção integral do OCR pendente |
| F03 | 83,3% | 8% | 96 SVG ilustrados, 96 mapas, temas por seção, manifesto e fallback; revisão humana pendente |
| F09 | 83,3% | 6% | Integração com busca, histórico, links, PDF e checklist; performance pendente |
| F10 | 50,0% | 7% | 42 testes responsivos e 96/96 rotas verificadas; revisão editorial ainda pendente |
| F11 | 100,0% | 3% | GitHub Actions concluído e URLs da versão premium respondendo HTTP 200 |
| F04 | 38,8% | 20% | Ilustrações e fluxos gerados; revisão editorial individual pendente |
| F05 | 38,5% | 9% | Ilustrações e fluxos gerados; revisão editorial individual pendente |
| F06 | 38,5% | 5% | Ilustrações e fluxos gerados; revisão editorial individual pendente |
| F07 | 39,5% | 7% | Ilustrações e fluxos gerados; revisão editorial individual pendente |
| F08 | 39,4% | 8% | Ilustrações e fluxos gerados; revisão editorial individual pendente |

## Próximas prioridades

- Revisão humana da coerência de todas as 65 fichas dependentes de OCR.
- Auditoria editorial individual das 96 fichas antes de qualquer classificação como validada.
- Testes completos de acessibilidade e em dispositivo físico.
- Inspeção online ampliada de acessibilidade e interação dos procedimentos.

## Retomada técnica

Gerador: python scripts/build_illustrated.py
Validador: python tests/validate-premium.py
QA navegador: node tests/qa-premium.cjs
Atualizador: python scripts/update_progress.py

Este relatório não confunde documentação didática, atos judiciais e homologação institucional.
