from pathlib import Path
from html import escape
import re,json
r=Path(__file__).resolve().parents[1]
codes=['O-03','BF-01','O-08','P-01','R-01','BV-01']
# Add image preview to first six pilot cards, preserving authored texts.
p=r/'aprender.html';s=p.read_text(encoding='utf8')
needle='<article class="v2-path">'
parts=s.split(needle)
assert len(parts)==7,len(parts)
for i,code in enumerate(codes):
 preview=f'<div class="lesson-card-visual"><img loading="eager" src="assets/learning/{code}/ilustracao-premium.svg" alt="Cena ilustrada da aula {code}; simulação com dados fictícios."></div>'
 if 'lesson-card-visual' not in parts[i+1]:
  parts[i+1]=preview+parts[i+1]
s=needle.join(parts)
p.write_text(s,encoding='utf8')
# Create an artwork carousel grid on the main index, distinct from the catalog.
ix=r/'index.html';html=ix.read_text(encoding='utf8')
marker='<section id="catalogo"'
assert marker in html
if 'id="aulas-ilustradas"' not in html:
 cards=[]
 for code in codes:
  d=json.loads((r/'data/lessons'/(code+'.json')).read_text(encoding='utf8'))
  cards.append(
   f'<a class="v2-art-card" href="itens/{code}.html" aria-label="Estudar {escape(d["title"])}">'
   f'<img src="assets/learning/{code}/ilustracao-premium.svg" loading="eager" alt="Representação ilustrada de {escape(d["title"])}">'
   f'<div class="v2-art-details"><span>{code} · SIMULAÇÃO DIDÁTICA</span><strong>{escape(d["title"])}</strong>'
   f'<small>7 etapas, exemplos e exercícios</small></div></a>')
 gallery='<section id="aulas-ilustradas" class="v2-gallery"><div class="v2-gallery-head"><div><p class="v2-kicker">VISUALIZAÇÃO PREMIUM</p><h2>Aprenda vendo, não só lendo</h2><p>Seis aulas com cenas ilustradas, diagramas, decisões e exemplos fictícios.</p></div><a href="aprender.html">Explorar trilha →</a></div><div class="v2-gallery-grid">'+''.join(cards)+'</div></section>\n'
 html=html.replace(marker,gallery+marker,1)
 ix.write_text(html,encoding='utf8')
style=r/'assets/css/portal-v2.css'
css="""
.v2-gallery{margin:24px 0 32px}
.v2-gallery-head{display:flex;justify-content:space-between;align-items:flex-end;gap:18px;margin-bottom:15px}
.v2-gallery-head .v2-kicker{color:#1577A8}
.v2-gallery-head h2{font-size:25px;letter-spacing:-.5px;color:#1E465F;margin:5px 0}
.v2-gallery-head p:not(.v2-kicker){font-size:12px;color:#657F90;margin:0}
.v2-gallery-head>a{font-size:12px;font-weight:900;color:#187AAD;white-space:nowrap;min-height:44px;display:inline-flex;align-items:center}
.v2-gallery-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:13px}
.v2-art-card{display:block;min-width:0;overflow:hidden;border-radius:14px;border:1px solid #D5E4EE;background:#FFF;box-shadow:0 6px 20px #153C5210}
.v2-art-card img{width:100%;height:auto;display:block;aspect-ratio:12/7.6;object-fit:cover;background:#143855}
.v2-art-details{padding:13px 15px 16px;display:grid;gap:3px}
.v2-art-details span{font-size:9px;color:#2679A6;font-weight:900;letter-spacing:.5px}
.v2-art-details strong{font-size:14px;color:#1D435B;line-height:1.35}
.v2-art-details small{font-size:10px;color:#647E8F}
.v2-art-card:hover,.v2-art-card:focus-visible{border-color:#2C91C7;box-shadow:0 8px 20px #184C681D;transform:translateY(-1px)}
.lesson-card-visual{aspect-ratio:12/7.6;overflow:hidden;border-radius:10px;margin-bottom:16px;background:#143852}
.lesson-card-visual img{display:block;width:100%;height:100%;object-fit:cover}
@media(max-width:790px){.v2-gallery-grid{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media(max-width:440px){.v2-gallery-grid{grid-template-columns:1fr}.v2-art-card img{aspect-ratio:12/6.6}.v2-gallery-head{align-items:flex-start}.v2-gallery-head h2{font-size:21px}.v2-gallery-head>a{font-size:10px}}
"""
with style.open('a',encoding='utf8') as f:f.write(css)
print('GALLERY_PREVIEW_INSERTED',len(cards))
