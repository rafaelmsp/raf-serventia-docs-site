from pathlib import Path
r=Path(__file__).resolve().parents[1]
p=r/'assets/js/lesson-engine.js'
s=p.read_text(encoding='utf8')
s=s.replace("if(data.is_pilot){ b.append(visualFigure('scene','Prévia ilustrada da lição'));","if(data.visual_coverage){ b.append(visualFigure('scene','Prévia ilustrada da lição'));")
s=s.replace("if(data.is_pilot){b.append(visualFigure('scene','Explore os elementos da cena'));}else{","if(data.visual_coverage){b.append(visualFigure('scene','Explore os elementos da cena'));}else{")
s=s.replace("if(data.is_pilot)b.append(visualFigure('diagram','Mapa visual da sequência de conferência'));",
            "if(data.visual_coverage)b.append(visualFigure('diagram',data.steps.length?'Mapa visual da sequência de conferência':'Mapa conceitual de leitura da fonte'));")
needle="if(!data.steps.length){\n   b.append(E('p','edu-warning','A sequência operacional ainda não foi validada."
assert needle in s
s=s.replace(needle,"if(!data.steps.length){\n   if(data.visual_coverage)b.append(visualFigure('diagram','Mapa ilustrado dos tópicos de estudo'));\n   b.append(E('p','edu-warning','A sequência operacional ainda não foi validada.")
# visible status in intro:
s=s.replace("const path=['O-03','BF-01','O-08','P-01','R-01','BV-01'];",
            "const path=['O-03','BF-01','O-08','P-01','R-01','BV-01'];")
p.write_text(s,encoding='utf8')
print('ALL_LESSONS_VISUAL_INTEGRATION_OK')

import json
items=json.loads((r/'dados/procedimentos.json').read_text(encoding='utf-8'))
for item in items:
 file=r/'data/lessons'/(item['codigo']+'.json')
 d=json.loads(file.read_text(encoding='utf-8'))
 d['visual_coverage']=True
 d['visual_scene']='../assets/learning/'+item['codigo']+'/ilustracao-premium.svg'
 d['visual_map']='../assets/learning/'+item['codigo']+'/fluxo-premium.svg'
 if not d['is_pilot']:
  d['status_note']='Ilustração e mapa conceitual disponíveis; ainda não são passos operacionais conferidos. Abra o infográfico original para estudar este assunto.'
 file.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
print('ENABLED_ALL_96',len(items))
