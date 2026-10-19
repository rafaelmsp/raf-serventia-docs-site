# RAF Serventia Docs — Manual Online UX Premium

Projeto de documentação técnica interativa, baseado no Manual Operacional do Estagiário na Serventia — PJe, de Rafael MS Passos, edição de 15/10/2026.

**Site:** https://rafaelmsp.github.io/raf-serventia-docs-site/

## Nova interface ilustrada (v0.2, editorialmente preliminar)

O catálogo tem busca, filtros por área e sete resultados por página. Cada uma das **96 fichas HTML** apresenta cinco abas: Visão geral, Mapa, Etapas, Conferência e Fonte original.

Foram criadas **96 ilustrações SVG originais** e **96 mapas SVG** ligados a JSON estruturado. O usuário pode selecionar cada nó do mapa para abrir sua explicação, navegar com teclado, ampliar os SVGs em outra aba e marcar checklists locais, com opção de limpeza. O sistema funciona apenas com HTML/CSS/JS, sem integração ao PJe.

As 107 páginas da fonte em HTML e o PDF original permanecem acessíveis pelos links de cada procedimento.

## Exemplos de acesso

- Catálogo: https://rafaelmsp.github.io/raf-serventia-docs-site/
- Anatomia da Árvore: https://rafaelmsp.github.io/raf-serventia-docs-site/itens/O-03.html
- PAC: https://rafaelmsp.github.io/raf-serventia-docs-site/itens/O-08.html
- Recepção e Identificação: https://rafaelmsp.github.io/raf-serventia-docs-site/itens/BF-01.html
- Base legal do Balcão Virtual: https://rafaelmsp.github.io/raf-serventia-docs-site/itens/BV-01.html
- Manual HTML: https://rafaelmsp.github.io/raf-serventia-docs-site/fonte-html/index.html
- PDF original: https://rafaelmsp.github.io/raf-serventia-docs-site/docs/manual-fonte.pdf

## Limites editoriais

**Material não oficial, não homologado pelo TJRJ.** O manual de origem declara uso restrito; a disponibilização pública foi solicitada pelo autor. A publicação não valida a vigência de normas, nem autoriza qualquer ato processual.

**Arquivos visuais produzidos não equivalem a páginas revisadas:** os pilotos O-03, O-08, BF-01 e BV-01 receberam explicações específicas. Os outros mapas são rascunhos de leitura a partir de títulos e trechos da fonte. As 65 fichas dependentes de OCR exigem conferência; não considerar os rótulos automaticamente extraídos como orientação definitiva.

## Arquitetura

- itens: 96 páginas HTML individuais.
- assets/illustrations: 96 ilustrações SVG específicas.
- assets/flows: 96 mapas SVG específicos.
- assets/css/ux-premium.css: design responsivo e impressão.
- assets/js/ficha-premium.js: abas, detalhes interativos e checklist.
- data/procedures: fichas JSON, com rastreabilidade e aviso editorial.
- data/flows: nós e arestas estruturados.
- data/assets-manifest.json: manifestos de 96 ativos, hashes e texto alternativo.
- data/editorial-audit.json: estado editorial por código.
- data/progress.json e docs/progresso-execucao.md: percentuais calculados.
- scripts/build_illustrated.py: gerador reproduzível.
- tests: validadores e testes em navegador.

## Testes

A validação estrutural confirmou 96 ilustrações únicas, 96 mapas e zero links locais quebrados nas 205 páginas HTML examinadas. Os seis pilotos passaram em 42 testes interativos, em sete larguras (360, 390, 430, 768, 1024, 1366 e 1920 px). As 96 rotas passaram no teste de abertura a 390 px.

## Desenvolvimento local

Na raiz do projeto, execute: python -m http.server 8765 --bind 127.0.0.1

Depois acesse http://127.0.0.1:8765/.

Para reconstituir as fichas ilustradas: python scripts/build_illustrated.py

Consulte docs/progresso-execucao.md para o estado real e as pendências. Não declarar 100% até haver revisão e aceitação técnica completa.

## Andamento
Acompanhe os percentuais e as evid�ncias em https://rafaelmsp.github.io/raf-serventia-docs-site/andamento.html . A pontua��o global n�o representa aprova��o editorial.

