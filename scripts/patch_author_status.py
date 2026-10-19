from pathlib import Path
r=Path(__file__).resolve().parents[1]
j=r/'assets/js/lesson-engine.js';s=j.read_text(encoding='utf8')
s=s.replace("data.is_pilot?'Aula piloto em revisão. Os exemplos são fictícios.':'Prévia de estudo: ainda não há procedimento operacional revisado nesta ficha.'",
            "data.state==='author_draft'?'Lição didática autoral em revisão. Os exemplos são fictícios.':'Prévia de estudo: ainda não há procedimento operacional revisado nesta ficha.'")
s=s.replace("if(!data.is_pilot?'","if(!data.is_pilot?'") # noop
s=s.replace("data.is_pilot&&correct&&tick","data.state==='author_draft'&&correct&&tick")
s=s.replace("!data.is_pilot?'Prévia em revisão.","data.state!=='author_draft'?'Prévia em revisão.")
s=s.replace("data.is_pilot?'Aprenda com imagens, exemplos e escolhas comentadas.':'Prévia de estudo — roteiro específico pendente de revisão.'",
            "data.state==='author_draft'?'Aprenda com imagens, exemplos e escolhas comentadas.':'Prévia de estudo — roteiro específico pendente de revisão.'")
s=s.replace("data.is_pilot?'AULA PILOTO EM REVISÃO':'PRÉVIA NÃO REVISADA'",
            "data.state==='author_draft'?'ROTEIRO DIDÁTICO EM REVISÃO':'PRÉVIA NÃO REVISADA'")
j.write_text(s,encoding='utf8')
test=r/'tests/v2-static.py';z=test.read_text(encoding='utf8')
z=z.replace("assert len(pilots)==6,(len(pilots),pilots)","assert len(pilots)==14,(len(pilots),pilots)")
z=z.replace("'draft_previews':90","'draft_previews':82")
test.write_text(z,encoding='utf8')
print('UPDATED_AUTHORING_STATUS')
