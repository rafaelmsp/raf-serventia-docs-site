# Auditoria de interface — RAF Serventia Docs

**Data:** 18/10/2026  
**Ambiente de teste:** Chromium headless (Puppeteer), HTML local da branch pública, Windows.  
**Escopo:** navegação da página pública de apresentação; **não é** uma auditoria WCAG completa nem avaliação da documentação privada.

## Resultado

| Largura | Menu | Âncoras | Atalhos de áreas | Rolagem horizontal | JS |
|---|---|---|---|---|---|
| 360px | Responsivo | Válidas | 6 visíveis | Não | Sem erro |
| 390px | Responsivo | Válidas | 6 visíveis | Não | Sem erro |
| 430px | Responsivo | Válidas | 6 visíveis | Não | Sem erro |
| 768px | Responsivo | Válidas | 6 visíveis | Não | Sem erro |
| 1024px | Responsivo | Válidas | 6 visíveis | Não | Sem erro |
| 1366px | Desktop | Válidas | 6 visíveis | Não | Sem erro |

Foram executadas duas suítes de verificação, cobrindo seis tamanhos de tela cada (12 execuções): abertura/fechamento do menu mobile, tecla Escape, navegação por âncora e retorno, ausência de IDs duplicados e links sem destino, presença dos atalhos, integridade básica dos links externos, botão "Topo" condicionado à rolagem e ausência de overflow horizontal.

## Defeitos encontrados e corrigidos

1. CSS anterior ocultava cinco de seis links internos no Android; seletor corrigido.
2. Botão flutuante "Topo" sobrepunha o início do conteúdo; oculto até rolar.
3. Rótulos azul-claro sobre fundo claro tinham contraste visual insuficiente; escurecidos.
4. Menu principal não possuía expansão mobile; implementados controle semântico, foco, Escape e fechamento.
5. Cartões de áreas não tinham destinos próprios; acrescentadas âncoras e atalhos.

## Cobertura real do conteúdo

**Acesso público:** página de apresentação, áreas, descrição geral, fluxo editorial, política de acesso, autoria, link GitHub.  
**Não acessível publicamente:** 96 fichas de procedimentos, conteúdo integral dos infográficos e PDF original, por classificação restrita. Nenhuma disponibilidade foi simulada.

## Evidências visuais

- `qa/screenshots/site-390.png`: página em Android (390 px).
- `qa/screenshots/menu-390.png`: menu mobile expandido.
- `qa/screenshots/site-1366.png`: página desktop.

## Pendências

- Auditoria com leitor de tela real e critérios WCAG formais.
- Revisão normativa e autorização expressa antes de exibir a documentação interna.
- Homologação com usuário no dispositivo físico.
