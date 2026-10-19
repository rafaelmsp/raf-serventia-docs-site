from pathlib import Path
r=Path(__file__).resolve().parents[1]
p=r/'assets/js/lesson-engine.js'
s=p.read_text(encoding='utf8')
old="content.append(E('p','edu-muted','Trechos extraídos da camada textual do PDF. Use-os como referência de leitura, não como instruções suficientes para atuar.'));"
new="""const message=data.source_highlight_status==='camada_textual_pdf'?
  'Tópicos de leitura organizados com base no texto nativo do PDF, sujeitos a revisão técnica. Confirme na imagem original antes de atuar.':
  'Síntese didática provisória baseada na imagem e em OCR. NÃO é transcrição literal nem procedimento homologado: confira a página original.';
 content.append(E('p','edu-muted',message));"""
assert old in s
s=s.replace(old,new)
p.write_text(s,encoding='utf8')
print('SOURCE_PROVENANCE_LABEL_CORRECTED')
