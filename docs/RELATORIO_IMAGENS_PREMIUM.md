# RAF Serventia Docs — Lote visual premium

**Data:** 19/10/2026  
**Versão:** pacote visual dos seis pilotos da V2  
**Natureza:** material didático não oficial, com exemplos e interfaces fictícias.

## Entrega

Foram criadas, integradas e vinculadas **12 imagens vetoriais originais**, assim distribuídas:

| Código | Cena ilustrada | Diagrama de estudo |
|---|---|---|
| O-03 | Visualizador fictício de autos, linha do tempo e peça documental | Quatro verificações de leitura do histórico |
| O-08 | Fluxo do PAC, determinação, destinatário, resposta e saídas | Conferência documental e supervisão |
| P-01 | Agenda simulada, AR, prazo, manifestações e avaliação | Etapas preliminares da pauta |
| R-01 | Indicadores, percentual e gráficos expressamente fictícios | Leitura de métricas |
| BF-01 | Atendimento presencial ilustrado e falas de acolhimento | Identificação e encaminhamento |
| BV-01 | Videoconferência fictícia com orientações de atendimento | Identificação, informações e supervisão |

Local dos arquivos: `assets/learning/<codigo>/ilustracao-premium.svg` e `assets/learning/<codigo>/fluxo-premium.svg`. Manifesto com caminhos e hashes: `data/learning-visuals-manifest.json`.

## Integração efetiva ao HTML

- Página inicial: seis miniaturas clicáveis no novo conjunto “Aprenda vendo, não só lendo”.
- Trilha inicial: cartões das seis aulas com suas ilustrações.
- Etapa 1: prévia visual e botão para abrir diretamente a etapa ilustrada.
- Etapa 3: cena premium com ampliação, rolagem própria no celular, botões de hotspots e infográfico original recolhível.
- Etapa 5: diagrama SVG ampliável e etapas explicadas individualmente, sem substituir o conteúdo textual por imagem.
- PDFs e HTMLs antigos preservados, com avisos de origem.

## Evidências técnicas

- 12 SVGs novos com marcação XML válida e sem dependências de imagens externas.
- `tests/premium-visual-qa.cjs`: **24/24** testes responsivos em 360, 390, 768 e 1366 px cobrindo os seis códigos. Validou carregamento de imagens e diagramas, links de ampliação, hotspots, ausência de rolagem horizontal global e rolagem interna no celular.
- `tests/premium-gallery-qa.cjs`: **6/6** cenários em 390, 768 e 1366 px, com 6 miniaturas carregadas na página inicial e na trilha.
- `tests/v2-static.py`: 96 aulas verificadas, sem falhas de integridade.
- Capturas para auditoria em `tests/premium-visual-shots/`.

## Revisão ainda necessária

A construção e a publicação de imagens profissionais não equivalem à conclusão pedagógica: **0/96 aulas homologadas**. As outras 90 fichas continuam como prévias não verificadas; os seis pilotos precisam de avaliação humana, revisão técnica e teste com iniciantes. Nenhum diagrama autoriza atos judiciais.

Progresso da implementação V2: **40%**, calculado com crédito apenas pelas novas evidências técnicas, em `data/progresso-pedagogico.json`.
