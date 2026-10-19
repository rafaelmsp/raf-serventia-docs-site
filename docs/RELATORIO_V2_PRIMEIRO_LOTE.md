# RAF Serventia Docs — Relatório técnico da reconstrução pedagógica V2

Data: 19/10/2026. Repositório: rafaelmsp/raf-serventia-docs-site.

## Entrega desta rodada

- Duas portas de entrada: Aprender do zero e Consulta rápida.
- Introdução para o primeiro dia com termos básicos, supervisão e proteção de informação.
- Seis aulas piloto autorais em sete etapas: O-03, BF-01, O-08, P-01, R-01 e BV-01.
- 96 páginas HTML adaptadas ao motor de aulas, mantendo os endereços por código.
- 96 ilustrações SVG conceituais, com seis cenas específicas dos pilotos.
- Hotspots acessíveis por botões, glossário expansível, observação guiada e explicação das etapas.
- Duas situações simuladas com feedback por piloto, checklist e salvamento local do estado de estudo.
- 96 cópias preservadas das páginas técnicas anteriores na pasta arquivo-tecnico.
- Fontes: 107 páginas-fonte HTML, imagens e PDF original mantidos.

## Resultados de testes

- Validador de conteúdo e rastreabilidade: 96/96 JSON de aulas, 96/96 SVGs XML válidos, correspondência de páginas e fonte: aprovado.
- Todas as 90 fichas não revisadas possuem passos operacionais vazios, sem fingir ações confirmadas.
- Questões estruturadas com exatamente uma alternativa correta: 96/96 fichas válidas no esquema.
- Chromium: 36/36 cenários de interação com seis pilotos em seis larguras (360 a 1366 px).
- Rotas HTML individuais: 96/96 carregadas a 390 px.
- Inspeção visual em 390 e 1366 px: navegação, figuras, catálogo, trilha, introdução e progresso testados sem overflow.
- As lições não realizam qualquer integração com o PJe e não coletam dados processuais.

## Pendências que impedem concluir 100%

- Revisão normativa/operacional e de linguagem das seis aulas piloto por responsável técnico.
- Teste de compreensão com estagiários iniciantes e ajuste a partir das dificuldades observadas.
- Autoria e revisão pedagógica substantiva das 90 fichas que permanecem como prévias.
- Correção e conferência das fontes OCR e revisão específica das imagens.
- Auditoria aprofundada de acessibilidade WCAG com leitor de tela real.
- Homologação institucional não presumida.

## Qualidade e responsabilidade

Ilustrações e exemplos são fictícios, não capturas oficiais. O infográfico original permanece disponível por link para conferência. Nenhuma lição está aprovada; não se deve entender o resultado do exercício como permissão para executar um ato judicial. Os percentuais constam de data/progresso-pedagogico.json.

## Continuação autônoma de lotes

A próxima implementação deve partir de docs/LOG_REVISAO_PEDAGOGICA.md e do JSON de estado, elaborando conteúdo específico a partir da página-fonte de cada código, testando e submetendo à revisão antes de mudar status editorial. A geração em lote não aprova procedimentos.
