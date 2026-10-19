from pathlib import Path
r=Path.home()/'Documents'/'raf-serventia-public'
p=r/'assets/js/lesson-engine.js'
s=p.read_text(encoding='utf8')
needle="outer.append(E('figcaption','edu-visual-caption','SIMULAÇÃO PEDAGÓGICA · dados fictícios · veja as explicações nos botões abaixo.'));"
assert needle in s
s=s.replace(needle,
  "outer.append(E('figcaption','edu-visual-caption','↔ No celular, deslize o desenho para os lados ou toque em Ampliar imagem. SIMULAÇÃO · dados fictícios.'));")
p.write_text(s,encoding='utf8')
style=r/'assets/css/lesson-ux.css'
with style.open('a',encoding='utf8') as f:
 f.write('\n.edu-visual-viewport{touch-action:pan-x pan-y;scroll-behavior:smooth}.edu-visual-viewport:focus-visible{outline:3px solid #70D2FC;outline-offset:-3px}.edu-visual-viewport img{user-select:none}.edu-visual-caption{line-height:1.5}\n')
print('SCROLL_CUE_UPDATED')
