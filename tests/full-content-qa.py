from pathlib import Path
import json,re,collections,xml.etree.ElementTree as ET,hashlib
root=Path(__file__).resolve().parent.parent
ix=json.loads((root/'dados/procedimentos.json').read_text(encoding='utf8'))
manifest=json.loads((root/'data/learning-visuals-manifest.json').read_text(encoding='utf8'))
assert len(ix)==96 and len(manifest)==96
errors=[];stats=collections.Counter();hashes={'scene':set(),'map':set()}
source=json.loads((root/'dados/conteudo_integral.json').read_text(encoding='utf8'))
assert len(source)==107
for item in ix:
 code=item['codigo'];f=root/'data/lessons'/(code+'.json')
 d=json.loads(f.read_text(encoding='utf8'))
 if d['code']!=code or d['page']!=item['pagina']:errors.append(f'{code} source mismatch')
 if d['state']!='author_draft':errors.append(f'{code} not authored draft')
 if any((d['pedagogical_ready'],d['technical_approved'],d['student_tested'])):errors.append(f'{code} wrongly approved')
 for key,low in [('terms',3),('observe',3),('steps',4),('mastery',3)]:
  if len(d.get(key,[]))<low:errors.append(f'{code} insufficient {key}')
 for section in ('practice','decision'):
  v=d[section]
  if len(v.get('options',[]))!=3 or sum(x['correct'] for x in v['options'])!=1:errors.append(f'{code} quiz malformed {section}')
  if len(v.get('question',''))<15:errors.append(f'{code} missing question {section}')
 if len(d['scene']['regions'])<4:errors.append(f'{code} missing regions')
 if d.get('visual_coverage') is not True:errors.append(f'{code} missing visual flag')
 for name,tail in (('scene','ilustracao-premium.svg'),('map','fluxo-premium.svg')):
  f=root/'assets/learning'/code/tail
  if not f.exists():errors.append(f'{code} missing {tail}');continue
  try:ET.parse(f)
  except Exception as e:errors.append(f'{code} svg {str(e)}')
  hashes[name].add(hashlib.sha256(f.read_bytes()).hexdigest())
 stats[d.get('authored_batch','original_six_pilots')]+=1
 if d.get('source_highlight_status','').startswith('ocr'):stats['ocr_draft']+=1
 if d['technical_approved']:stats['technical_approved']+=1
 if any(k in d['plain'].lower() for k in ('processo real 000','senha:','token:')):errors.append(code+' potentially sensitive text')
if len(hashes['scene'])!=96 or len(hashes['map'])!=96:errors.append('duplicate SVG assets')
data={'total_lessons':len(ix),'source_pages':len(source),'authored_drafts':96,
      'source_review_pending':96,'editorial_approved':0,'unique_illustrations':len(hashes['scene']),
      'unique_diagrams':len(hashes['map']),'by_origin':dict(stats),'errors':errors}
(root/'tests/full-content-qa.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(data,ensure_ascii=False,indent=2))
if errors:raise SystemExit(1)
