from pathlib import Path
r=Path(__file__).resolve().parents[1]
p=r/'assets/js/lesson-engine.js'
s=p.read_text(encoding='utf-8')
needle="b.append(sequence(data.terms,(t,i)=>{"
assert needle in s
needle2="}));return b;\n}\nfunction recognize(){"
assert needle2 in s
replacement="""}));
 const evidence=E('details','source-evidence');
 evidence.append(E('summary','','O que está escrito na página original?'));
 const content=E('div','source-evidence-body');
 if(Array.isArray(data.source_highlights)&&data.source_highlights.length) {
   content.append(E('p','edu-muted','Trechos extraídos da camada textual do PDF. Use-os como referência de leitura, não como instruções suficientes para atuar.'));
   const quotes=E('ul','source-highlight-list');
   data.source_highlights.slice(0,3).forEach(txt=>quotes.append(E('li','',txt)));
   content.append(quotes);
 } else {
   content.append(E('p','edu-muted','A transcrição desta página depende de conferência visual. Consulte o infográfico original para não reproduzir erros de OCR.'));
 }
 const original=E('a','source-link','Abrir o infográfico da página '+data.page+' ↗');
 original.href=data.pdf;original.target='_blank';original.rel='noopener noreferrer';content.append(original);
 evidence.append(content);b.append(evidence);
 return b;
}
function recognize(){"""
s=s.replace(needle2,replacement,1)
p.write_text(s,encoding='utf-8')
css=r/'assets/css/lesson-ux.css'
with css.open('a',encoding='utf-8') as f:
 f.write('''\n.source-evidence{margin:18px 0 0;border:1px solid #C9DFEC;border-radius:11px;background:#F7FBFE;padding:12px 15px}.source-evidence summary{min-height:35px;color:#225D7E;font-size:13px;font-weight:800;cursor:pointer}.source-evidence-body{padding-top:10px}.source-highlight-list{padding-left:21px;color:#2D526C;font-size:13px;line-height:1.65}.source-highlight-list li{margin-bottom:10px}.source-evidence-body .source-link{margin-top:8px}\n''')
print('SOURCE_EVIDENCE_PANEL_ADDED')
