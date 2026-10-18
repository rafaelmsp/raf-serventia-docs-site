from pathlib import Path
from html import escape
base=Path(__file__).resolve().parent
area=base/"areas";area.mkdir(exist_ok=True)
items=[
 ("operacoes","O","Operações no PJe",49,"Uma área de organização de referências e temas de movimentação processual."),
 ("pauta","P","Pauta e audiências",16,"Referências de organização e acompanhamento de atividades relacionadas a audiências."),
 ("relatorios","R","Relatórios e controle",5,"Informação organizada para acompanhamento e conferência documental."),
 ("balcao-fisico","BF","Balcão físico",12,"Temas de atendimento presencial e documentação auxiliar."),
 ("balcao-virtual","BV","Balcão virtual",14,"Temas de atendimento remoto e comunicação, em revisão editorial.")
]
css='assets/css/documentacao.css'
head='<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="RAF Serventia Docs — portal independente de documentação técnica"><title>RAF Serventia Docs — Documentação Técnica</title><link rel="stylesheet" href="'+css+'"></head>'
link=lambda slug:'areas/'+slug+'.html'
cards=''.join(f'<article class="item-row"><span class="item-code">{escape(code)}</span><div class="item-name"><a href="{link(slug)}">{escape(title)}</a><small>{num} tópicos catalogados no acervo privado · consulta pública indisponível</small></div><a class="open-item" href="{link(slug)}">Ver área →</a></article>' for slug,code,title,num,desc in items)
index=f'''<!doctype html><html lang="pt-BR">{head}<body>
<a class="skip" href="#main">Pular para o conteúdo</a>
<header class="head"><a href="index.html" class="logo">◆ <span>RAF <strong>Serventia Docs</strong></span></a><nav class="head-nav" aria-label="Navegação principal"><a href="#areas">Áreas</a><a href="#acesso">Acesso</a><a href="#sobre">Sobre</a><a href="https://github.com/rafaelmsp/raf-serventia-docs-site" target="_blank" rel="noopener noreferrer">GitHub ↗</a></nav></header>
<main class="home-main" id="main">
<section class="intro" id="inicio"><div><p class="overline">PORTAL DE DOCUMENTAÇÃO · APRESENTAÇÃO PÚBLICA</p><h1>Encontre a área.<br><em>Abra a página.</em></h1><p class="intro-desc">Navegação objetiva, com cada assunto em sua própria página. Sem listas gigantes nem rolagem interminável.</p></div><div class="intro-meta"><strong>05 <span>áreas</span></strong><span>96 itens no projeto privado</span></div></section>
<div class="notice slim" id="acesso"><strong>Conteúdo restrito.</strong> Esta é uma apresentação pública do projeto. O PDF e os procedimentos internos permanecem privados e não estão disponíveis neste site.</div>
<section id="areas"><div class="section-title"><div><p class="overline">NAVEGAÇÃO POR ÁREAS</p><h2>Escolha o assunto</h2></div><p>Uma página por área</p></div><div class="items">{cards}</div></section>
<details class="help" id="sobre"><summary>Sobre o projeto e a documentação</summary><p>RAF Serventia Docs é um projeto independente de Rafael MS Passos para organização de conhecimento técnico em HTML. O material didático de origem é não oficial. As 96 fichas documentais aguardam revisão e autorização antes de qualquer liberação pública. Este site não representa o TJRJ.</p></details></main>
<footer>RAF Serventia Docs · Rafael MS Passos · 2026 · Apresentação não oficial</footer></body></html>'''
(base/'index.html').write_text(index,encoding='utf-8')
for i,(slug,code,title,num,desc) in enumerate(items):
 prev=items[i-1] if i else None
 nxt=items[i+1] if i+1<len(items) else None
 def nav(r,t):return f'<a class="step-link" href="{r[0]}.html">{t} <strong>{escape(r[1])}</strong></a>' if r else ''
 page=f'''<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="{escape(title)} — RAF Serventia Docs">
<title>{escape(title)} — RAF Serventia Docs</title>
<link rel="stylesheet" href="../assets/css/documentacao.css"></head><body>
<a class="skip" href="#main">Pular para o conteúdo</a>
<header class="head"><a href="../index.html" class="logo">◆ <span>RAF <strong>Serventia Docs</strong></span></a><div class="head-actions"><a href="../index.html#areas">← Todas as áreas</a></div></header>
<main class="item-main" id="main">
<nav class="breadcrumbs" aria-label="Trilha de navegação"><a href="../index.html">Início</a><span>/</span><span aria-current="page">{escape(title)}</span></nav>
<div class="item-title"><div><p class="overline">ÁREA DOCUMENTAL · {escape(code)}</p><h1>{escape(title)}</h1><p class="subhead">{num} itens catalogados no projeto privado</p></div></div>
<section class="reader"><div class="reader-head"><strong>Descrição da área</strong><span>Acesso público limitado</span></div><div class="public-body"><p>{escape(desc)}</p><div class="notice"><strong>Acervo ainda não liberado.</strong> Esta página apresenta apenas a organização temática. Procedimentos, infográficos e o PDF de origem permanecem no repositório privado, sujeitos à revisão de divulgação.</div></div></section>
<div class="item-bottom"><div class="adjacent">{nav(prev,"← Anterior")}{nav(nxt,"Próxima →")}</div><a class="back" href="../index.html#areas">← Voltar ao índice das áreas</a></div>
</main><footer>RAF Serventia Docs · Rafael MS Passos · 2026 · Material não oficial</footer></body></html>'''
 (area/(slug+'.html')).write_text(page,encoding='utf-8')
print('SITE_PUBLICO_COMPACTO_OK',len(list(area.glob('*.html'))),'páginas por área, sem conteúdo restrito')
