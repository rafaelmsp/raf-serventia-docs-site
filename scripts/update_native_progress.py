from pathlib import Path
import json,re,datetime
r=Path(__file__).resolve().parents[1]
idx=json.loads((r/'dados/procedimentos.json').read_text(encoding='utf8'))
all_lessons=[json.loads((r/'data/lessons'/(x['codigo']+'.json')).read_text(encoding='utf8')) for x in idx]
auth=[l for l in all_lessons if l['state']=='author_draft']
previews=[l for l in all_lessons if l['state']!='author_draft']
assert len(auth)==43 and len(previews)==53
p=r/'tests/v2-static.py'
s=p.read_text(encoding='utf8')
s=s.replace('assert len(pilots)==14,(len(pilots),pilots)','assert len(pilots)==43,(len(pilots),pilots)')
s=s.replace("'draft_previews':82","'draft_previews':53")
p.write_text(s,encoding='utf8')
q=r/'data/lessons-index.json'
meta=json.loads(q.read_text(encoding='utf8'))
meta.update(authored_lessons=43,needs_source_review=53,preview_count=53,approved=0)
meta['notes']='96/96 cenários e mapas premium; 43 roteiros didáticos baseados no manual em revisão e 53 prévias a aprofundar; nenhum homologado.'
q.write_text(json.dumps(meta,ensure_ascii=False,indent=2),encoding='utf8')
p=r/'data/progresso-pedagogico.json'
d=json.loads(p.read_text(encoding='utf8'))
credits={'M00':7,'M01':12,'M02':11,'M03':9,'M04':5,'M05':0,'M06':0,'M07':2,'M08':2,'M09':4,'M10':2}
for x in d['phases']:
 x['credited']=credits[x['id']]
 if x['id']=='M03':x['evidence']='43 roteiros didáticos redigidos a partir da fonte; revisão jurídico-pedagógica e avaliação com alunos ainda pendentes.'
 if x['id']=='M04':x['evidence']='15 roteiros específicos de Operações (inclusive matriz interna); os demais aguardam revisão de OCR.'
 if x['id']=='M07':x['evidence']='12 roteiros de Balcão Físico com etapas da camada textual nativa; revisão da rotina local pendente.'
 if x['id']=='M08':x['evidence']='14 roteiros de Balcão Virtual com observações de fonte e segurança; regras vigentes a confirmar.'
d['percent']=sum(credits.values())
d['authored_lessons']=43;d['unreviewed_previews']=53;d['approved_lessons']=0
d['version']='v2.3-premium-education-draft'
d['modified_at']=datetime.datetime.now(datetime.timezone.utc).isoformat()
p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf8')
p=r/'andamento-pedagogico.html';html=p.read_text(encoding='utf8')
html=re.sub(r'\d+% de implementação V2',str(d['percent'])+'% de implementação V2',html)
html=re.sub(r'Há \d+ roteiros específicos em revisão e \d+ prévias;', 'Há 43 roteiros específicos em revisão e 53 prévias;',html)
for phase in d['phases']:
 pat=r'('+phase['id']+r' · [^<]+</b><strong>)\d+( / '+str(phase['weight'])+r' pontos</strong>)'
 html=re.sub(pat,lambda m:m.group(1)+str(phase['credited'])+m.group(2),html)
its=iter(d['phases'])
html=re.sub(r'<progress max="\d+" value="\d+"></progress>',
 lambda m:(lambda v:f'<progress max="{v["weight"]}" value="{v["credited"]}"></progress>')(next(its)),html)
p.write_text(html,encoding='utf8')
p=r/'docs/progresso-pedagogico.md'
s=p.read_text(encoding='utf8')
s=re.sub(r'\*\*Implementação ponderada:\*\* \d+%',f'**Implementação ponderada:** {d["percent"]}%',s)
s=re.sub(r'\*\*Roteiros autorais em revisão:\*\* \d+/96', '**Roteiros autorais em revisão:** 43/96',s)
s=re.sub(r'\*\*Prévias ainda não revisadas:\*\* \d+/96', '**Prévias ainda não revisadas:** 53/96',s)
for x in d['phases']:
 pat=r'(\| '+x['id']+r' \| )[\d.]+( \| '+str(x['weight'])+r' \|)[^|]*( \|)'
 s=re.sub(pat,lambda m:m.group(1)+str(x['credited'])+m.group(2)+' '+x['evidence']+m.group(3),s)
s=s.replace('82 prévias restantes','53 prévias restantes')
p.write_text(s,encoding='utf8')
readme=r/'README.md';txt=readme.read_text(encoding='utf8')
txt=txt.replace('Quatorze roteiros foram escritos especificamente para as respectivas páginas, incluindo seis pilotos','Quarenta e três roteiros foram escritos especificamente a partir do manual, incluindo seis pilotos')
txt=txt.replace('As outras 82 fichas são prévias de estudo','As outras 53 fichas são prévias de estudo')
readme.write_text(txt,encoding='utf8')
print('UPDATED_META',d['percent'],'AUTHORED',len(auth),'PREVIEWS',len(previews))
