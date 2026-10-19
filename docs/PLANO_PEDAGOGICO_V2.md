# RAF Serventia Docs — Plano Pedagógico Mestre V2

Fonte primária: Manual Operacional do Estagiário na Serventia — PJe, 107 páginas, de 15/10/2026. Objetivo: transformar 96 referências técnicas em aulas adequadas a estagiários iniciantes, com aprendizagem orientada em vez de transcrição OCR.

## Dois modos

1. **Aprender do zero:** introdução, glossário e lições guiadas.
2. **Consulta rápida:** busca por código e categoria, documentos técnicos legados e PDF original.

## Contrato de cada lição

Cada lição deve permitir: entender o objetivo, reconhecer conceitos, identificar elementos em simulação, observar evidências, explicar passos supervisionados, decidir em exemplo fictício, praticar, receber feedback e reconhecer quando pedir ao servidor responsável.

Sete telas: Começar → Entender → Reconhecer → Observar → Fazer com supervisão → Decidir → Praticar e concluir. Não criar páginas com rolagem infinita nem expor OCR incerto como ato processual.

## Fases e pesos

| Fase | Entrega | Peso |
|---|---|---:|
| M00 | Inventário e fontes | 7% |
| M01 | UX e motor didático | 12% |
| M02 | Cenas e ilustrações explicativas | 12% |
| M03 | Seis pilotos O-03, BF-01, O-08, P-01, R-01, BV-01 | 15% |
| M04 | Operações, 49 lições revisadas | 20% |
| M05 | Pauta, 16 lições revisadas | 8% |
| M06 | Relatórios, 5 lições revisadas | 4% |
| M07 | Balcão físico, 12 lições revisadas | 5% |
| M08 | Balcão virtual, 14 lições revisadas | 5% |
| M09 | Usabilidade, aprendizado e acessibilidade | 7% |
| M10 | Deploy, evidências e relatório final | 5% |

O progresso deve ser calculado a partir de evidências reais. Separar cobertura HTML de conteúdo validado. **Não herdar automaticamente os 53,5% técnicos da fase V1.** O total atual, métricas e pendências ficam em data/progresso-pedagogico.json.

## Critérios obrigatórios para aprovar uma aula

- Objetivo mensurável e linguagem do primeiro dia.
- Glossário com exemplos contextualizados.
- Ilustração fiel ao que se deseja observar e claramente simulada.
- Passos baseados em fonte identificável e conferidos com a realidade local.
- Fluxo condicional e limites de atuação explícitos.
- Casos fictícios, erros comuns, exercícios e feedback útil.
- Fonte original acessível por link e página correta.
- Sem credenciais ou informações identificáveis de processos reais.
- Responsividade e acesso por teclado testados.
- Revisão técnica, pedagógica e teste com estagiários registrados por responsável e data.

Estados: rascunho → fonte conferida → revisão didática → revisão técnica → testada com aluno → aprovada. Nenhum gerador automático pode marcar a aprovação.

## Próxima etapa

O motor V2 e as cenas dos seis pilotos foram implementados, mas continuam em revisão. Revisar cada piloto com servidor responsável, realizar testes formativos com 3–5 estagiários, registrar dúvidas e corrigir. Em seguida, desenvolver as 90 fichas restantes a partir da imagem original, em lotes, sem completar lacunas de OCR com suposições.

## Comandos

- python scripts/build_pedagogy.py
- python scripts/build_pilot_art.py
- python scripts/build_learning_portal.py
- python tests/v2-static.py
- node tests/v2-qa.cjs
- python scripts/compute_pedagogy_progress.py

Material não oficial, sem homologação institucional. O site não executa atos judiciais nem substitui a supervisão.
