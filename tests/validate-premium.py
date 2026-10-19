from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import hashlib,json,xml.etree.ElementTree as ET,re
root=Path(__file__).resolve().parent.parent
index=json.loads((root/'dados/procedimentos.json').read_text(encoding='utf-8'))
manifest=json.loads((root/'data/assets-manifest.json').read_text(encoding='utf-8'))
audit=json.loads((root/'data/editorial-audit.json').read_text(encoding='utf-8'))
assert len(index)==len(manifest)==len(audit)==96
assert len({x['code'] for x in manifest})==96
assert len({x['sha256'] for x in manifest})==96,'SVG files duplicated'
assert len(list((root/'assets/illustrations').glob('*.svg')))==96
assert len(list((root/'assets/flows').glob('*.svg')))==96
assert len(list((root/'data/flows').glob('*.json')))==96
class Parser(HTMLParser):
 def __init__(self):super().__init__();self.targets=[]
 def handle_starttag(self,t,attributes):
  if t in ('a','img','link','script'):
   args=dict(attributes);v=args.get('href') or args.get('src')
   if v:self.targets.append(v)
errors=[]
for item in index:
 code=item['codigo'];page=item['pagina']
 path=root/'itens'/(code+'.html')
 data=json.loads((root/'data/procedures'/(code+'.json')).read_text(encoding='utf-8'))
 source=json.loads((root/'data/flows'/(code+'.json')).read_text(encoding='utf-8'))
 assert data['source_page']==source['source_page']==page
 assert len(data['nodes'])==len(data['steps']) and len(data['checklist'])>=4
 assert all(n['source_page']==page for n in data['nodes'])
 svg=root/'assets/illustrations'/(code+'.svg');flow=root/'assets/flows'/(code+'.svg')
 ET.parse(svg);ET.parse(flow)
 asset=next(x for x in manifest if x['code']==code)
 assert hashlib.sha256(svg.read_bytes()).hexdigest()==asset['sha256']
 html=path.read_text(encoding='utf-8')
 for necessary in ('data-panel="fluxo"','data-panel="conferencia"','assets/illustrations/'+code+'.svg',
                  'assets/flows/'+code+'.svg','manual-fonte.pdf#page='+str(page)):
  if necessary not in html:errors.append((code,'missing markup '+necessary))
files=[root/'index.html',*sorted((root/'itens').glob('*.html')),*sorted((root/'fonte-html').glob('*.html'))]
for page in files:
 p=Parser()
 try:p.feed(page.read_text(encoding='utf-8'))
 except Exception as e:errors.append((str(page),str(e)));continue
 for target in p.targets:
  url=urlsplit(target)
  if url.scheme or url.netloc or target.startswith(('#','data:')) or not url.path:continue
  dest=(page.parent/unquote(url.path)).resolve()
  if not dest.exists():errors.append((str(page.relative_to(root)),target))
assert not errors,errors[:20]
print(json.dumps({'html_files':len(files),'procedures':96,'illustrations':96,'flow_svgs':96,'flow_json':96,
 'unique_sha':96,'links_broken':0,'source_pages':107,'drafts_pending_editorial':len([x for x in audit if not x['editorial_approved']])},ensure_ascii=False))
