# RAF Serventia Docs — QA e segurança da versão premium

Data: 19/10/2026 (execução inicial).

## Inventário

- 96 fichas HTML (O 49, P 16, R 5, BF 12, BV 14).
- 96 ilustrações SVG principais, com 96 hashes SHA-256 diferentes.
- 96 mapas SVG e 96 descrições de nós/arestas em JSON.
- 107 páginas-fonte HTML preservadas.
- PDF de 107 páginas preservado e vinculado.
- Textos alternativos, SVG title/desc, avisos de origem e estado editorial.

## Testes executados

**Validação estática:** tests/validate-premium.py. Verificou integridade de 96 pares de ativos, correspondência código/página, estrutura JSON, validade XML e links relativos em 205 HTMLs. Resultado: 0 links quebrados, 96 SVGs originais distintos.

**Interatividade responsiva:** tests/qa-premium.cjs. 42/42 cenários passaram, cobrindo seis fichas (O-03, O-08, BF-01, BV-01, P-01, R-01) nas larguras de 360, 390, 430, 768, 1024, 1366 e 1920 pixels. Verificações: cinco abas, ilustração carregada, ausência de overflow horizontal, abertura de mapa, seleção de nó, checklist, persistência após reload, limpeza e link ao PDF.

**Cobertura das rotas:** tests/qa-all-96.cjs. 96 de 96 fichas carregaram no Chromium a 390 px, sem erros de JavaScript nem overflow horizontal, com cinco painéis, checklist e links aos ativos presentes.

## Defeitos corrigidos

1. O fragmento de URL deslocava as abas para baixo do cabeçalho fixo no Android. Removido salto automático e aplicada posição sticky separada da barra superior.
2. Metadados da fonte ocupavam altura excessiva no celular. Aplicado cabeçalho compacto.
3. SVGs exigiam ampliação para conferir pequenos rótulos. Introduzidos links de ampliação em nova aba e mapa com botões explicativos independentes.

## Limitações e pendências

- O PDF de origem é material não oficial originalmente identificado como restrito; divulgação pública solicitada pelo autor não equivale à aprovação institucional.
- 65 fichas dependem de OCR e precisam de conferência manual do conteúdo. Todas as 96 fichas estão classificadas como rascunhos editoriais, não homologadas.
- Fluxos provisórios representam ordem de leitura didática; não significam execução de ato judicial.
- São necessários testes com leitores de tela reais, revisão WCAG AA completa e homologação em dispositivos físicos.
- Prazo, competência, norma e atribuição devem ser conferidos em fontes oficiais antes do uso.
- A varredura de expressões sensíveis por padrões não garante ausência de dados privados em imagens; exige inspeção humana complementar.

## Encerramento

Este documento registra implantação de componentes e resultados de automação. Não atesta exatidão jurídica integral. O progresso formal consta em data/progress.json e docs/progresso-execucao.md.

## Atualiza��o posterior ao deploy
A rodada longa original foi interrompida ap�s 19 casos por timeout de comunica��o do navegador. Uma su�te otimizada posterior (tests/qa-premium-fast.cjs) concluiu 42/42 casos sem erros; os 96 endere�os individuais passaram no teste independente Android. GitHub Actions do commit 45220c6 conclu�do; 13 recursos p�blicos verificados via HTTP 200. A verifica��o online por Chromium carregou O-03 com 5 abas e sem erros de JavaScript. A intera��o detalhada com dados carregados online permanece pendente de teste ampliado.

