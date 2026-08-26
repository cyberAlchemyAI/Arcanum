# Retornos preservados dos explorers

## Agente: Hewitt, Carl

## Evidência bruta — run reconstruído

Candidato: `arcana/task-session/development/invoke-runs/20260804T184514Z-pre-execution-owner-prerequisite-fast-path`. É o menor run recente que contém pacote Invoke, dispatch, recibos Task Session/lifecycle, bloqueio+retomada, validação, handoff e evidência de observação. Distingo o Invoke de planejamento da execução posterior: o primeiro declara explicitamente que não é evidência de implementação; a segunda contém a prova local de execução.

### Cronologia empírica

1. **Intenção e enquadramento.** O problema declarado era a descoberta tardia de um pré-requisito Invoke Refresh; o objetivo era classificador pré-execução, uma rota de owner, retorno na mesma tentativa e adoção no ponto de entrada. `DEFINE-CONTEXT.md:3-17`. O escopo inicial proibiu modificar fontes canônicas “neste Invoke run” e preservou limites entre Invoke, Router, WPR Audit e Task Session. `DEFINE-CONTEXT.md:15-17`.

2. **Descoberta limitada/waived.** Não houve descoberta ampla: o artefato registra uma waiver porque o defeito já era “source-evidenced” e de superfície de owners limitada. `DEFINE-CONTEXT.md:19-21`. Houve, porém, revisão local read-only: identificou que Task Session só roteava após Context Builder, que a autorização não era carregada, e que Refresh por continuação era proposal-only. `BOUNDED-HELPER-RECEIPT.md:3-11`.

3. **Define → design → plan.** Define passou e encaminhou a design. `DEFINE-RESULT.md:1-12`. Design passou, mas declarou teto de prova apenas arquitetural/contratual e encaminhou a plan. `DESIGN-RESULT.md:1-17`. Plan produziu seis SWUs e dispatch válido, mas registrou “fixtures are planned, not executed” e deixou autorização/baselines como lacunas. `PLAN-RESULT.md:1-18`.

4. **Tensão antes da execução.** O Distill registrado às `19:03:30Z–19:03:36Z` executou em modo `role_simulation`, não como agentes independentes; registrou objeções sobre ordem do Context Builder, autorização nua, multi-hop e SLO de tempo. `DISTILL-RUNTIME-EVENTS.jsonl:1-7`; `DISTILL-EXECUTION-RECEIPT.json:43-105`. As reconciliações aceitaram classificador pré-Context, entrada nua fail-closed e um hop; DAG foi deferido. `DISTILL-EXECUTION-RECEIPT.json:77-105`.

5. **Autoridade de partida.** O dispatch declara `execution_owner: parent-orchestrator`, estratégia serial de um helper e `authorization: approved`. `execution.dispatch.json:21-35,86-120`. O contrato B3 exige autorização exata do operador antes de S2–S5. `execution.dispatch.json:366-372`. Há estado `approved`, mas não há no pacote um recibo que identifique ou date a aprovação inicial humana; portanto a sua existência concreta além desse campo é **inferência fraca**, não prova independente. `orchestrate/.../state.json:1-13`.

6. **Execução inicial e bloqueio.** A primeira execução iniciou `2026-08-04T19:24:00Z`, serializou um agente, e fechou `20:02:30Z` com `block`: um fixture WPEG já existente omitia seis campos exigidos; a expansão de um arquivo exigia autorização do usuário. `orchestrate/.../native-receipts/spawn-0001.json:1-29`. O ledger de eventos confirma join `block` e decisão `gate_block`. `orchestrate/.../events.jsonl:1-29`; `orchestrate/.../reduced/gate-decision.json:1-20`.

7. **Retomada autorizada e implementação.** A autorização de retomada é explicitamente de `current-user-request`, limitada a `test_plan_once_admission.py`, sem alteração de validator/promoção/publicação. `retry-001/resume-authorization.json:1-12`. O retry começou `20:20:00Z`, resolveu o bloqueio e terminou `20:35:34Z`. `retry-001/native-receipts/spawn-0001.json:1-29`.

8. **Fechamento técnico.** SWU-001 (contratos) fechou 19:38:40, SWU-002 (classificador) 19:42:29, SWU-003 (Router) 19:49:00; os recibos registram owner `sigil-development` e validações específicas. `receipts/SWU-PEP-001.task-session.json:1-43`; `...002.task-session.json:1-39`; `...003.task-session.json:1-43`. SWU-004 fechou após a autorização, com 10 bloqueios adversariais e regressões passantes. `receipts/SWU-PEP-004.task-session.json:30-58`. SWU-005 foi validado por `spellcraft` para Invoke/Implementation Readiness. `receipts/SWU-PEP-005.spellcraft.json:1-20`. SWU-006 fechou às 20:35:34 com sete grupos canário/regressão e paridade gerada. `receipts/SWU-PEP-006.task-session.json:42-71`.

9. **Handoff/owner final.** A cadeia final junta seis recibos Task Session e seis de lifecycle owner, declara `COMPLETE`, fronteira vazia e `next_route: null`. `orchestrate/.../chain.json:1-40`. O owner do recibo de fechamento é `owner-routed-integration`, que junta `sigil-development` e `spellcraft`; não seleciona sucessor. `receipts/SWU-PEP-006.integration.json:1-20`. Isto é o **owner final da integração/closeout**, não um owner de promoção: promoção/release/deploy são explicitamente externos ao dispatch. `execution.dispatch.json:432-444`.

10. **Observabilidade.** O pacote afirma que Invoke e Distill foram registrados nas linhas 536 e 535 do ledger central e recomenda `reflect-now`, mas também diz que isso não autoriza implementação. `OBSERVABILITY-RESULT.md:1-12`. No checkout atual, `.arcanum/observability/signals/sigil-invocations.jsonl` está ausente; portanto não consegui verificar essas duas entradas diretamente. Há evidência verificável do runner: 29 eventos validados no run inicial e 8 no retry. `orchestrate/.../evidence-validation.json:1-8`; `retry-001/evidence-validation.json:1-8`.

### Mapa aos 13 passos CyberAlchemy

| Passo | Classificação | Evidência / limite |
|---|---|---|
| 1 Nomear seed | Evidência | Intenção em `DEFINE-CONTEXT.md:3-5`. |
| 2 Delimitar contexto | Evidência | Sinais, limites de owner e não-mudança inicial em `DEFINE-CONTEXT.md:7-17`. |
| 3 Nomear resultado | Evidência | Objetivo e `WORK-PACK.md` alvo em `execution.dispatch.json:4-8`. |
| 4 Descobrir incógnitas | Parcial | Revisão read-only e root cause em `BOUNDED-HELPER-RECEIPT.md:3-11`; descoberta ampla foi dispensada em `DEFINE-CONTEXT.md:19-21`. **Ausência:** sem discovery map/corpus de alternativas. |
| 5 Escolher rota | Evidência | Define→design→plan em `DEFINE-RESULT.md:1-12`, `DESIGN-RESULT.md:1-17`, `PLAN-RESULT.md:1-18`; execução serial autorizada em `execution.dispatch.json:21-35`. |
| 6 Criar artefato | Evidência | Pacote, dispatch, seis SWUs e recibos; outputs enumerados em `INVOKE-RESULT.md:3-29`. |
| 7 Introduzir tensão | Evidência qualificada | Objeções/reconciliações Distill em `DISTILL-EXECUTION-RECEIPT.json:43-105`; **inferência:** trata-se de tensão útil, mas `role_simulation`, não crítica independente. |
| 8 Revisar ao fechamento | Evidência | Reconciliações aceitas/deferidas; bloqueio inicial interrompeu mutação até autorização exata. `DISTILL-EXECUTION-RECEIPT.json:77-105`; `native-receipts/spawn-0001.json:24-29`; `resume-authorization.json:1-12`. |
| 9 Tornar navegável | Evidência parcial | `INVOKE-RESULT.md:8-29` indexa outputs/próxima rota; chain aponta recibos. **Ausência:** nenhum teste de navegabilidade humana. |
| 10 Preservar abertura | Evidência | Resíduos: autorização carregada, default plan-once, multi-hop, no-op, observabilidade e superfícies dirty. `RESIDUE.md:3-18`. |
| 11 Registrar trace | Evidência | Dispatch, eventos, recibos, chain e auditoria; chain completa em `chain.json:1-40`. |
| 12 Rotear próximo owner | Evidência + ausência | Durante execução owners são separados: `sigil-development`, `spellcraft`, integração. `execution.dispatch.json:375-381`; recibo final em `SWU-PEP-006.integration.json:1-20`. **Ausência:** após closeout, `next_route` é `null`; não há owner pós-fechamento/promoção selecionado. |
| 13 Refletir após uso | Ausência | Há recomendação `reflect-now` em `OBSERVABILITY-RESULT.md:9-12`, mas nenhum artefato de reflexão. O ledger central alegado não existe no checkout atual. |

Conclusão estrita: há forte evidência de um ciclo de planejamento seguido por execução local, bloqueio correto, autorização específica de retomada, validação e integração concluída. Não há evidência preservada de aprovação humana inicial além de campos `approved`, de descoberta ampla, de reflexão pós-uso, de entrada central de observabilidade hoje verificável, nem de owner selecionado para promoção/produção.

## Agente: Peirce, Charles Sanders

## Evidência bruta — run selecionado

**Norma:** `framework/CYBERALCHEMY-METHOD.md`. O método exige cinco âncoras [15–25], 13 passos [57–94], trace [87–91], navegação [273–289] e qualidade mínima [328–344].

**Run:** `spells/invoke/development/invoke-runs/20260619T203711Z-early-mode-dispatch-distill/`, ligado por IDs consistentes entre work-pack, context pack e resultado de Task Session: `WP-IDD-20260619`, `TASK-IDD-001`, `SWU-IDD-001` (`WORK-PACK.md:3–25`; `task-session/TASK-IDD-001-CONTEXT-PACK.md:3–8`; `task-session/TASK-IDD-001-RESULT.md:3–8`). É um pacote de authoring Invoke + uma execução Task Session documentada; não há manifesto de run nesse diretório.

### Matriz: obrigação → testemunho

| Método | Obrigação | Evidência no run | Limite da evidência |
|---|---|---|---|
| 1 | Nomear o seed em linguagem comum (`CYBERALCHEMY-METHOD.md:57–58`) | Intenção: endurecer `define`/`design` sem lhes dar autoridade de execução (`INVOKE-DEFINE.md:3–5`; `:26–31`). | Presente. |
| 2 | Delimitar contexto, restrições, artefatos, owner e estágio (`CYBERALCHEMY-METHOD.md:60–61`) | Escopo, superfícies e harness (`INVOKE-DEFINE.md:7–13`); fronteiras contra execução e arquivos sujos (`TASK-IDD-001-CONTEXT-PACK.md:36–41`). | O owner é especificado principalmente pela cadeia de rotas, não como campo único inicial. |
| 3 | Declarar objetivo e artefato esperado (`CYBERALCHEMY-METHOD.md:63–64`) | Objetivo do work-pack (`WORK-PACK.md:7–9`); outputs previstos e template (`RESULT.md:7–10`). | Presente. |
| 4 | Descobrir evidência, lacunas, desconhecidos e blockers (`CYBERALCHEMY-METHOD.md:66–67`) | Contratos-fonte enumerados (`INVOKE-DESIGN.md:12–21`) e contexto selecionado com razão (`TASK-IDD-001-CONTEXT-PACK.md:10–23`). | Não há diário independente de busca, resultados de pesquisa, nem registro explícito de “unknowns/blockers” desta fase. Isso é ausência de testemunho específico, não prova de que não houve descoberta. |
| 5 | Escolher rota governante mínima (`CYBERALCHEMY-METHOD.md:69–70`) | A fronteira de autoridade foi desenhada: `define`/`design` não executam; `plan` planeja; `task-session` executa (`INVOKE-DESIGN.md:5–10`). O resultado declara modo `full` e lista a rota posterior (`RESULT.md:3–15`). | Há decisão operacional, mas não um registro comparativo de alternativas que demonstre por que `full` era a menor rota responsável. |
| 6 | Criar artefato-draft (`CYBERALCHEMY-METHOD.md:72–73`) | Artefatos concretos: define, design, layering, work-pack e transport (`RESULT.md:7–10`); design descreve os componentes e mudanças propostas (`INVOKE-DESIGN.md:36–44`). | Presente. |
| 7 | Introduzir tensão estruturada (`CYBERALCHEMY-METHOD.md:75–76`) | Riscos explícitos e mitigação (`INVOKE-DESIGN.md:70–74`); Distill registra unidade, gap e split evitado (`INVOKE-DESIGN.md:86–91`). | Não há retorno separado de Balancer/premortem; riscos e Distill são o testemunho disponível. |
| 8 | Revisar rumo ao fechamento contextual (`CYBERALCHEMY-METHOD.md:78–79`) | Resultado declara mudanças implementadas em contratos, mirrors, harness e fixtures (`task-session/TASK-IDD-001-RESULT.md:14–38`); critérios do work-pack são declarados satisfeitos (`:83–86`). | A sequência draft→revisão é inferível por proposta e resultado, mas não há diff/registro de revisão no pacote. |
| 9 | Tornar o trabalho navegável (`CYBERALCHEMY-METHOD.md:81–82`) | Context pack tem entradas, obrigações, fronteiras e plano de validação (`TASK-IDD-001-CONTEXT-PACK.md:10–61`); transport nomeia rota, alvo, fontes e gates (`PLAN-TRANSPORT.md:3–44`). | Não existe teste de retomada por terceiro. |
| 10 | Preservar abertura/evolução (`CYBERALCHEMY-METHOD.md:84–85`) | Gap de mirrors e risco residual são preservados (`WORK-PACK.md:70–75`; `TASK-IDD-001-RESULT.md:76–81`). | Não há condição explícita que invalide o artefato no futuro. |
| 11 | Registrar trace: decisões, rejeições, tensões, validação, observabilidade (`CYBERALCHEMY-METHOD.md:87–88`) | Decisões e lacunas (`RESULT.md:11–14`); mudanças, comandos e resultados (`task-session/TASK-IDD-001-RESULT.md:14–65`); trace de técnicas com evidência (`:67–81`). | Há “split avoided” (`INVOKE-DESIGN.md:88–91`), mas não inventário abrangente de alternativas rejeitadas. |
| 12 | Encaminhar ao próximo owner (`CYBERALCHEMY-METHOD.md:90–91`) | Rota `define → design → plan → task-session` (`PLAN-TRANSPORT.md:3–11`); gates e autoridade de mutação delimitados (`:28–39`); resultado inicial recomenda `task-session` (`RESULT.md:14–15`). | O resultado da Task Session diz “Next route: none required” (`TASK-IDD-001-RESULT.md:83–86`), portanto encerra este SWU, não a lifecycle inteira. |
| 13 | Refletir após uso (`CYBERALCHEMY-METHOD.md:93–94`) | Nenhum testemunho de uso repetido, reflexão, proposal de melhoria ou sinal de observabilidade no diretório selecionado. | Ausência de registro, não falha inferida. O relatório cita `spells/invoke/development/runs/20260619T204106Z.md` (`TASK-IDD-001-RESULT.md:54–58`), mas esse arquivo não está presente no checkout. |

### Cinco âncoras

| Âncora | Evidência |
|---|---|
| Objective | `WORK-PACK.md:7–9`. |
| Output artifact | `RESULT.md:7–10`; `WORK-PACK.md:11–16`. |
| Discovery | Corpus de contratos e fontes selecionadas (`INVOKE-DESIGN.md:12–21`; `TASK-IDD-001-CONTEXT-PACK.md:10–23`), sem produto separado de discovery. |
| Tension | Riscos/mitigações (`INVOKE-DESIGN.md:70–74`) e Distill (`:86–91`). |
| Route | Cadeia explícita e Task Session como destino (`PLAN-TRANSPORT.md:3–11`; `RESULT.md:14–15`). |

### Route: uma âncora, duas decisões operacionais

A evidência normativa não sustenta reduzir Route a um único significado.

1. **Passo 5 — decisão governante de rota:** escolher qual forma de trabalho pode conter responsavelmente o problema: define/design/plan/validation/interrogation/lifecycle authoring/execution (`CYBERALCHEMY-METHOD.md:69–70`). No run, isto aparece na separação de responsabilidades entre `define`, `design`, `plan` e `task-session` (`INVOKE-DESIGN.md:5–10`).

2. **Passo 12 — decisão de handoff/owner seguinte:** entregar o resultado à autoridade de lifecycle correta (`CYBERALCHEMY-METHOD.md:90–91`). No run, o transport nomeia `task-session` para o SWU (`PLAN-TRANSPORT.md:3–11`).

São conectadas, mas não equivalentes: a primeira seleciona a governança e suas fronteiras; a segunda materializa a transferência após o artefato/gates. A própria regra de ownership confirma a separação: Invoke pode preparar handoff, mas os owners de lifecycle conservam suas autoridades (`CYBERALCHEMY-METHOD.md:185–187`). O contrato Invoke atual também diz que Invoke é front door de authoring, não owner de todo artefato, e que o handoff route torna-se o próximo owner (`spells/invoke/README.md:22–24`, `:116–121`).

### Resíduo verificável

O pacote histórico referencia contratos sob `arcanum/spells/invoke/...` (`INVOKE-DESIGN.md:16–21`; `WORK-PACK.md:29–34`), enquanto o checkout atual os expõe em `spells/invoke/...`. Isso é uma divergência de caminho em documentação/transport a preservar como evidência de drift; não permite concluir que a execução histórica falhou.
