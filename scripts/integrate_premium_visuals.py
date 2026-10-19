from pathlib import Path
r=Path.home()/'Documents'/'raf-serventia-public'
p=r/'assets/js/lesson-engine.js'
s=p.read_text(encoding='utf8')
needle="function welcome(){"
assert needle in s
helper="""function visualFigure(kind,title) {
 const codePart=data.code;
 const asset=kind==='scene'?'ilustracao-premium.svg':'fluxo-premium.svg';
 const src='../assets/learning/'+codePart+'/'+asset;
 const outer=E('figure',kind==='scene'?'edu-visual premium-scene':'edu-visual premium-diagram');
 const top=E('div','edu-visual-bar');
 top.append(E('strong','',title));
 const link=E('a','edu-zoom-link','Ampliar imagem ↗');link.href=src;link.target='_blank';link.rel='noopener noreferrer';
 top.append(link);
 const viewport=E('div','edu-visual-viewport');
 viewport.tabIndex=0;
 viewport.setAttribute('role','region');
 viewport.setAttribute('aria-label','Ilustração de estudo, com rolagem horizontal no celular');
 const picture=E('img');
 picture.src=src;
 picture.alt=(kind==='scene'?'Cena ilustrada: ':'Diagrama: ')+data.title+'. Material simulado, não é interface oficial.';
 picture.loading='lazy';picture.decoding='async';
 viewport.append(picture);
 outer.append(top,viewport);
 outer.append(E('figcaption','edu-visual-caption','SIMULAÇÃO PEDAGÓGICA · dados fictícios · veja as explicações nos botões abaixo.'));
 return outer;
}
"""
s=s.replace(needle,helper+needle,1)
needle=" E('p','edu-small','Fonte: página '+data.page+' do manual de 15/10/2026.'));return b;"
assert needle in s, 'welcome'
s=s.replace(needle," E('p','edu-small','Fonte: página '+data.page+' do manual de 15/10/2026.'));if(data.is_pilot){ b.append(visualFigure('scene','Prévia ilustrada da lição'));const go=E('button','preview-action','Explorar imagem e elementos →');go.type='button';go.addEventListener('click',()=>move(2));b.append(go); }return b;",1)
needle="add(fig,img,E('figcaption','',data.scene.title+' · simulação didática'));b.append(fig);"
assert needle in s, 'recognize'
s=s.replace(needle,"if(data.is_pilot){b.append(visualFigure('scene','Explore os elementos da cena'));}else{add(fig,img,E('figcaption','',data.scene.title+' · simulação didática'));b.append(fig);}",1)
needle="b.append(sequence(data.steps,(s,i)=>{"
assert needle in s,'steps'
s=s.replace(needle,"if(data.is_pilot)b.append(visualFigure('diagram','Mapa visual da sequência de conferência'));b.append(sequence(data.steps,(s,i)=>{",1)
p.write_text(s,encoding='utf8')
css=r/'assets/css/lesson-ux.css'
with css.open('a',encoding='utf8') as f:
 f.write("""
/* Elementos premium desenhados individualmente para as seis lições piloto */
.edu-visual{margin:19px 0 22px;background:#0F2B44;border-radius:17px;overflow:hidden;border:1px solid #B9D3E4;box-shadow:0 14px 30px #16364D17}
.edu-visual-bar{min-height:55px;display:flex;align-items:center;justify-content:space-between;gap:12px;padding:12px 17px;background:linear-gradient(100deg,#163A58,#19567C);color:#EFF9FF}
.edu-visual-bar strong{font-size:13px;font-weight:850;letter-spacing:.1px}
.edu-zoom-link{display:inline-flex;align-items:center;justify-content:center;min-height:37px;border-radius:8px;padding:7px 11px;background:#DFF1FB;color:#215B7C;font-size:11px;font-weight:900;white-space:nowrap}
.edu-visual-viewport{background:#102F49;overflow-x:auto;overflow-y:hidden;overscroll-behavior-x:contain;scrollbar-color:#70ACCE #183F5D;scrollbar-width:thin}
.edu-visual-viewport img{display:block;width:100%;height:auto;max-height:none;object-fit:contain}
.edu-visual-caption{background:#E9F3FA;color:#47697F;font-size:10px;letter-spacing:.25px;font-weight:800;padding:10px 16px}
.preview-action{min-height:45px;padding:10px 17px;border-radius:10px;color:#fff;background:#177FB6;border:1px solid #177FB6;font-weight:850;font-size:12px}
.premium-diagram{margin-bottom:17px}
@media(max-width:700px){
.edu-visual{margin:17px -8px 19px;border-radius:11px}
.edu-visual-viewport img{width:820px;max-width:none;height:auto}
.edu-visual-bar{padding:10px 11px}
.edu-visual-bar strong{font-size:11px}
.edu-zoom-link{font-size:10px}
.edu-visual-caption{font-size:9px;padding:9px 11px}
}
""")
print('INTEGRATED_PREMIUM_ASSETS',len(s))
