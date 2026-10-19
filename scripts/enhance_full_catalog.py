from pathlib import Path
root=Path(__file__).resolve().parents[1]
p=root/'assets/js/catalogo.js'
s=p.read_text(encoding='utf-8')
needle="""+'</span><div class="item-name"><a href="'+href+'">"""
assert needle in s
new="""+'</span><a class="item-visual-link" href="'+href+'" tabindex="-1" aria-hidden="true"><img class="item-visual" src="assets/learning/'+encodeURIComponent(r.codigo)+'/ilustracao-premium.svg" alt="" loading="lazy" decoding="async"></a><div class="item-name"><a href="'+href+'">"""
s=s.replace(needle,new)
p.write_text(s,encoding='utf-8')
css=root/'assets/css/portal-v2.css'
with css.open('a',encoding='utf-8') as f:
 f.write("""
/* Ilustrações individuais no catálogo — 96 cartões com referência visual */
.item-visual-link{display:block;flex:none;width:100px;height:64px;overflow:hidden;border-radius:9px;border:1px solid #CFDFE9;background:#153B57}
.item-visual{display:block;width:100%;height:100%;object-fit:cover}
.item-row:hover .item-visual-link{border-color:#489CCD}
@media(max-width:700px){.item-visual-link{width:75px;height:55px}.item-row{gap:8px}}
@media(max-width:390px){.item-visual-link{width:62px;height:52px}.item-name a{font-size:12px}}
""")
print('CATALOG_VISUALS_96')
