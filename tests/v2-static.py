from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import json,xml.etree.ElementTree as ET
r=Path(__file__).resolve().parent.parent
idx=json.loads((r/'dados/procedimentos.json').read_text(encoding='utf8'))
assert len(idx)==96
pilots=[]
errors=[]
for row in idx:
 c=row['codigo'];file=r/'data/lessons'/(c+'.json')
 if not file.exists():errors.append(c+' missing JSON');continue
 d=json.loads(file.read_text(encoding='utf8'))
 if (d['code']!=c or d['page']!=row['pagina'] or d['section']!=row['categoria']):errors.append(c+' origin mismatch')
 if len(d['terms'])<3 or len(d['scene']['regions'])<4:errors.append(c+' missing learning elements')
 if len(d['decision']['options'])<3 or len(d['practice']['options'])<3:errors.append(c+' missing exercises')
 for name in ('decision','practice'):
  if sum(bool(o['correct']) for o in d[name]['options'])!=1:errors.append(c+' quiz answer error '+name)
 if d['state']=='author_draft':
  pilots.append(c)
  if len(d['steps'])<4 or len(d['mastery'])<3:errors.append(c+' incomplete pilot')
 else:
  if d['steps']:errors.append(c+' unreviewed procedure steps exposed')
 if d['pedagogical_ready'] or d['technical_approved']:errors.append(c+' improperly approved')
 svg=r/'assets/learning'/c/'simulacao.svg'
 if not svg.exists():errors.append(c+' missing scene');continue
 try:ET.parse(svg)
 except Exception as e:errors.append(c+' invalid SVG '+str(e))
 if not (r/'arquivo-tecnico'/(c+'.html')).exists():errors.append(c+' archive missing')
 if not (r/'itens'/(c+'.html')).exists():errors.append(c+' lesson HTML missing')
class Parser(HTMLParser):
 def __init__(self):super().__init__();self.links=[]
 def handle_starttag(self,t,attrs):
  if t in ('link','a','script','img'):
   dd=dict(attrs);v=dd.get('href') or dd.get('src')
   if v:self.links.append(v)
files=[r/'index.html',r/'aprender.html',r/'andamento-pedagogico.html',*list((r/'itens').glob('*.html'))]
for file in files:
 p=Parser();p.feed(file.read_text(encoding='utf8'))
 for href in p.links:
  uri=urlsplit(href)
  if uri.scheme or uri.netloc or not uri.path or href.startswith('#'):continue
  path=(file.parent/unquote(uri.path)).resolve()
  if not path.exists():errors.append(str(file.name)+' broken '+href)
assert len(pilots)==96,(len(pilots),pilots)
print(json.dumps({'lessons':len(idx),'pilot_codes':pilots,'draft_previews':0,'approved':0,'errors':errors[:20],'error_count':len(errors)},ensure_ascii=False))
if errors:raise SystemExit(1)
