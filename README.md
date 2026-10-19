# RAF Serventia Docs — Manual pedagógico V2

**Site:** https://rafaelmsp.github.io/raf-serventia-docs-site/

O projeto tem duas experiências complementares:

- **Aprender do zero** — introdução para o primeiro dia e lições de sete etapas com linguagem simples, glossário, SVG ilustrado, regiões clicáveis, observação guiada, passos supervisionados, questões e feedback.
- **Consulta rápida** — catálogo por código e categoria, com 96 links permanentes, referência técnica anterior e o PDF original.

## Estado da V2

Há 96 arquivos de lição, 96 ilustrações premium novas e 96 mapas SVG próprios por código. Quatorze roteiros foram escritos especificamente para as respectivas páginas, incluindo seis pilotos: O-03 (Árvore do Processo), BF-01 (Recepção e Identificação), O-08 (PAC), P-01 (Pauta), R-01 (Indicadores) e BV-01 (Balcão Virtual). As outras 82 fichas são prévias de estudo; nenhuma apresenta instruções operacionais validadas sem conferência da fonte.

**0 de 96 aulas possuem homologação editorial, técnica ou institucional.** O progresso percentual registrado mede implementação, não competência de estagiários. O material é didático, não oficial, contém exemplos fictícios e não executa atos no PJe.

## Estrutura principal

- index.html — duas portas de entrada e catálogo.
- aprender.html — seis roteiros guiados.
- introducao.html — glossário e orientação para o primeiro dia.
- itens/{codigo}.html — sete etapas de cada aula V2, com URL estável.
- arquivo-tecnico/{codigo}.html — páginas técnicas premium da versão anterior, preservadas para consulta.
- data/lessons/{codigo}.json — currículo e estado editorial de cada item.
- assets/learning/{codigo}/simulacao.svg — ilustração SVG original de estudo.
- assets/js/lesson-engine.js — motor de navegação, hotspots e exercícios com feedback.
- assets/css/lesson-ux.css — identidade UX com cores por área, cartões, estados e responsividade.
- data/progresso-pedagogico.json — progresso real da reconstrução V2.
- andamento-pedagogico.html — painel por fase M00 a M10.
- docs/LOG_REVISAO_PEDAGOGICA.md — fontes conferidas e pendências.
- docs/progresso-pedagogico.md — checkpoint e pesos.
- docs/manual-fonte.pdf — manual original, 107 páginas, 15/10/2026.

## Reprodução local

Na raiz do projeto:

    python -m http.server 8765 --bind 127.0.0.1

Acesse http://127.0.0.1:8765/ . Depois:

    python scripts/build_pedagogy.py
    python scripts/build_pilot_art.py
    python scripts/build_learning_portal.py
    python tests/v2-static.py
    node tests/v2-qa.cjs
    python scripts/compute_pedagogy_progress.py

**Atenção:** regenerar o portal pode reescrever o painel de andamento. Execute o atualizador de progresso após os geradores. Não marcar lições como aprovadas automaticamente.

## Limites de utilização

Manual original identificado como material não oficial e originalmente de uso restrito; divulgação pública foi solicitada pelo autor. Não indica homologação pelo TJRJ. Atividades reais dependem de orientações atuais, atribuições e supervisão de servidor responsável. Capturas ilustradas são simulações esquemáticas; não contêm processos reais. Os números de indicadores são didáticos, e os atos normativos citados no manual exigem verificação de vigência e texto oficial.

Autoria da fonte: Rafael MS Passos, 2026.
