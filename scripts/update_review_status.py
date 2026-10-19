from pathlib import Path
import json
r=Path(__file__).resolve().parents[1]
js=r/'assets/js/auditoria.js'
s=js.read_text(encoding='utf8')
s=s.replace("['O-09','O-39','O-43','O-45','P-14','P-16','BV-07']",
 "['O-09','O-19','O-25','O-32','O-38','O-39','O-41','O-43','O-45','P-14','P-15','P-16','BF-04','BV-06','BV-07']")
js.write_text(s,encoding='utf8')
test=r/'tests/editorial-audit-ui-qa.cjs';t=test.read_text(encoding='utf8')
t=t.replace("textContent==='7'","textContent==='15'")
t=t.replace("textContent),'89'","textContent),'81'")
t=t.replace("e=>e.length),7","e=>e.length),9") # filtered results first page =9, paginated
t=t.replace("e=>e.length),2","e=>e.length),3")
t=t.replace("visual_checked:7,pending:89","visual_checked:15,pending:81")
test.write_text(t,encoding='utf8')
panel=r/'andamento-pedagogico.html';h=panel.read_text(encoding='utf8')
h=h.replace('7/96 páginas confrontadas visualmente; 89 pendentes','15/96 páginas confrontadas visualmente; 81 pendentes')
panel.write_text(h,encoding='utf8')
prog=r/'data/progresso-pedagogico.json';d=json.loads(prog.read_text(encoding='utf8'))
d['source_image_checked']=15;d['source_image_pending']=81;d['approved_lessons']=0
prog.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf8')
print('DATA_AND_UX_COUNTS_UPDATED',d['source_image_checked'],d['source_image_pending'])
