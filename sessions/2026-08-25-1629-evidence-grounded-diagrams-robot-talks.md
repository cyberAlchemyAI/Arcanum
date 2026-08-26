---
session_id: RT-EGD-20260825-1629
date: 2026-08-25
topic: evidence-grounded-diagrams design audit
status: complete
node_type: agent-dialogue
tags: [robot-talks, evidence-grounded-diagrams, skill-design, schema, artifact-lifecycle]
artifact_kind: session
layer: capability
created_at: 2026-08-25T16:29:40-03:00
updated_at: 2026-08-25T19:10:00-03:00
decisions_made: true
contradictions_found: true
---

# Evidence-Grounded Diagrams: Robot Talks Design Audit

## Investigation Scope

**Central Question:** Como projetar `evidence-grounded-diagrams` para ser a melhor skill possível — incluindo arquitetura cognitiva, prompt, schema, artefatos auxiliares, validação e experiência de uso?

**Why Now:** A implementação inicial já existe, mas o usuário quer garantir que o prompt, os contratos e o lifecycle sejam projetados como um sistema coerente antes da promoção e instalação. O usuário também tornou explícita a obrigação de que todo diagrama emitido seja salvo e tagueado.

**Layer Definitions:**

1. Prompt e arquitetura de instruções da skill.
2. Modelo semântico, schemas e invariantes verificáveis.
3. Persistência, tagging, versionamento, renderização, validação, promoção e instalação no runtime.

**Agent Roles:**

| Agent | Concern | Central Question | Out of Scope |
|---|---|---|---|
| Instruction Architect | Arquitetura cognitiva e operacional | Como organizar gatilhos, modos, decisões, progressive disclosure e handoffs para execução consistente? | Schemas campo a campo, diretório de promoção e instalação de renderer. |
| Semantic Contract Architect | Modelo semântico e schemas | Qual conjunto mínimo de contratos governa pedido, claims, bundle, tags, versão, equivalente textual e validação? | Reescrita do prompt, escolha de renderer e instalação. |
| Artifact Lifecycle Auditor | Lifecycle e encaixe no repo | Como persistir, validar, publicar, promover e instalar sem oficializar drafts nem depender de ferramentas ausentes? | Campos detalhados de schemas e reescrita do prompt. |

**Assumptions to Challenge:**

- `transmutations/` é necessariamente a fonte canônica correta.
- Todo scratch deve ser persistido.
- A obrigação de persistência pode ser garantida apenas por instrução.
- Os schemas atuais de invocation e result bastam.
- JSON Schema é formato canônico permitido para novos contratos.
- Um único manifest deve conter todo o estado.
- `textual_equivalent` é apenas uma explicação ou alt text.
- `review + correction_authorized` é um limite de mutação suficientemente claro.
- Neutralidade de renderer é suficiente sem adapters e capability detection.
- `x-ray` deve ser o owner da capability.
- Tags dispensam um índice de artefatos.
- Bootstrap e sync incremental oferecem a mesma cobertura.

**Success Criteria:** A investigação termina quando houver uma recomendação rastreável para arquitetura do prompt, contratos canônicos, bundle e lifecycle, renderer ladder, tagging/index, fonte canônica, instalação no runtime e testes negativos, com tensões explícitas submetidas ao gate humano.

**Strategy Check:** A alternativa de dividir a investigação por arquivos (`SKILL.md`, schemas e scripts) foi rejeitada porque produziria sobreposição de perguntas e esconderia contradições entre comportamento, contrato e operação. A decomposição por preocupações preserva independência, permitindo que os agentes leiam evidência comum por lentes diferentes.

## Agent Reports

### Agent 1 — Instruction Architect

#### Key Findings

- **A espinha epistemológica é forte e deve permanecer no núcleo.** A skill trata o diagrama como conjunto comprimido de claims, exige decisão de admissão antes de desenhar, constrói o ledger antes do draft e compara diagrama, ledger e equivalente textual antes da entrega (`SKILL.md:8`, `SKILL.md:107`, `SKILL.md:164`). Isso é o verdadeiro comportamento distintivo da skill.
- **A progressive disclosure está invertida.** O `SKILL.md` manda ler o schema semântico inteiro antes de toda criação ou revisão, enquanto também carrega seleção de famílias, loops, auditoria, renderização e contratos de saída no prompt principal (`SKILL.md:30`, `SKILL.md:130`, `SKILL.md:150`). A orientação de criação de skills recomenda manter apenas seleção e workflow essencial no `SKILL.md`, carregando variantes e referências somente quando necessárias (`skill-creator/SKILL.md:135`, `skill-creator/SKILL.md:145`).
- **O modelo de modos não representa o comportamento prometido.** O contrato possui apenas `create` e `review`; `correction_authorized` permite modificar durante review, mas não existe processo nem resultado próprio para correção (`schema.md:14`, `schema.md:21`, `SKILL.md:180`). O resultado estruturado confirma apenas dois envelopes (`result.schema.json:259`, `result.schema.json:481`). Correção precisa ser um modo operacional próprio ou uma segunda fase explícita após review.
- **`textual_equivalent` está corretamente definido no documento semântico, mas enfraquecido no workflow.** A definição completa inclui nodes, relações tipadas, direção, escopo e distinções epistêmicas, e rejeita simples descrição visual (`schema.md:65`). O processo reduz isso a “nodes and typed relations” (`SKILL.md:171`); o resultado não separa `caption`, `rationale` e `textual_equivalent` (`result.schema.json:262`).
- **Persistência ainda não é um gate de entrega.** O processo termina após revisão e precisão; `artifact_path` é apenas opcional dentro da representação, sem receipt, tagging ou estado de falha de persistência (`SKILL.md:164`, `result.schema.json:196`). Isso conflita com a exigência do usuário e com a regra do repo de classificar todo artefato e validar após ferramentas que criam arquivos (`ARTIFACT-CONSTITUTION.md:77`).

#### Gaps or Inconsistencies

- A descrição de trigger cobre criar e revisar, mas não corrigir, versionar, persistir ou auditar equivalência fonte/render.
- Inputs formalmente obrigatórios não têm política operacional de resolução: o agente não sabe o que pode inferir, quando perguntar e quando bloquear.
- `review + correction_authorized` mistura diagnóstico read-only com mutação.
- Não existe definição operacional de “diagrama emitido”.
- Não existe estado entre “render validado” e “entregue”: persistência, tagging e receipt precisam ocorrer nesse intervalo.
- “Render when available” não diz como detectar capacidades, escolher fallback ou impedir uma troca silenciosa de renderer.
- O prompt não diferencia ausência de evidência, ausência do source, renderer indisponível e falha ao persistir.
- Não há exemplos ou fixtures para caption, rationale e equivalente textual.
- Não há prova comportamental de que diferentes agentes seguirão as invariantes.

#### Local Tensions

- Prompt conciso × regras indispensáveis.
- Neutralidade semântica × execução determinística.
- Persistência obrigatória × review read-only.
- Menor diagrama × auditabilidade completa.
- Input natural × contrato completo.
- Exemplos úteis × política implícita.
- Persistir sempre × runtime sem escrita.

#### Questions for Synthesis

1. O que conta como persistência válida?
2. Quando um diagrama passa a contar como emitido?
3. `revise` deve ser modo próprio ou composição `review → create-new-version`?
4. Que parte do lifecycle pertence à skill e qual pertence ao contrato genérico de artefatos?
5. O ledger completo deve ser exibido ou apenas persistido e resumido?
6. Como tratar pedidos com várias perguntas estruturais?
7. Um renderer default pode ser recomendado sem contaminar o modelo semântico?

#### Recommended Instruction Architecture

Manter um `SKILL.md` curto organizado como máquina de decisão: trigger e promessa; invariantes não negociáveis; normalização de intake; router de `create`, `review`, `revise` e composição `review-and-revise`; state machine `intake → evidence-boundary → admission → claim-model → source → source-validation → render → visual-inspection → semantic-parity → persist-and-tag → handoff`; branches explícitos para `no-diagram`, `needs-evidence`, `insufficient-evidence`, `render-blocked` e `persistence-blocked`; gate que proíbe `ready` sem source validado, render inspecionado quando exigido, equivalente reconciliado e receipt persistente; e resource router por modo e renderer.

Referências auxiliares recomendadas: `claim-model.md`, runbooks de create/review/revise, `diagram-families.md`, `artifact-handoff.md`, adapters por renderer, exemplos não normativos, templates e scripts determinísticos. Schemas não devem ser leitura cognitiva obrigatória.

### Agent 2 — Semantic Contract Architect

#### Key Findings

- **Os schemas atuais não podem permanecer canônicos no formato existente.** A constituição exige `.schema.yml`, enquanto `schema.md` se declara semantic authority e os contratos estão em `.schema.json` (`SCHEMA-CONSTITUTION.md:9-10,28-34,49-52`; `references/schema.md:3-7`).
- **`invocation` + `result` não cumprem “todo diagrama emitido deve ser salvo e tagueado”.** Não há `diagram_id`, revisão, tags, membros source/render, persistência ou lineage; `artifact_path` é opcional (`result.schema.json:196-210,259-340`).
- **O ledger não fecha a cadeia de referência.** O schema não garante que source IDs, locators, claim IDs ou `applies_to` resolvam. Invariantes importantes existem apenas em prosa; o precedente do x-ray declara corretamente que schema estrutural não prova verdade ou correção explicativa (`xray-lane-model.schema.yml:101-105`).
- **`textual_equivalent` precisa ser companion verificável.** A definição conceitual está correta (`schema.md:65-67`), mas o schema aceita string vazia e não liga o texto aos claims (`result.schema.json:325-330`). Equivalência semântica final ainda exige validação assistida ou humana.
- **A Metadata Constitution é direção, não obrigação canônica.** Ela propõe IDs, intent, owner, lifecycle e sidecars, mas permanece candidate e depende de infraestrutura futura (`ARTIFACT-METADATA-CONSTITUTION.md:30-60,104,108-114,168-176`).

#### Gaps or Inconsistencies

1. `schema.md` mistura glossário, semântica e autoridade canônica.
2. Faltam quatro objetos separados: pedido, modelo semântico, manifest do bundle e receipt.
3. Não existe identidade persistente, revision ou lineage.
4. `schema_version` está confundido com versão editorial.
5. O resultado não conserva um evidence-set identificável.
6. Referências entre fontes, locators, claims, elementos e visual semantics não são fechadas.
7. Não há modelo explícito de elemento visual.
8. O equivalente textual não declara cobertura de claims.
9. Não existem caption e rationale separados.
10. Não há vocabulário ou normalização de tags.
11. `official + ready + render NOT_RUN` continua schema-valid.
12. Review não vincula receipt ao digest da revisão auditada.
13. Status editorial, retention class, readiness e validation estão misturados.
14. Faltam fixtures negativas epistemicamente perigosas.

#### Local Tensions

- Bundle autocontido × duplicação de evidência.
- Manifest único × responsabilidades com ritmos diferentes.
- Vocabulário fechado × domínio aberto.
- Hashes sempre × hashes condicionais.
- Schema estrito × fidelidade epistemológica.
- Salvar × versionar no Git.

#### Questions for Synthesis

1. Qual é a definição operacional de emitido?
2. Quem resolve storage root e `diagram_id`?
3. Tags desconhecidas bloqueiam ou geram warning?
4. O registry será próprio, Inventory ou namespaced?
5. Evidência será snapshot, referência imutável ou ambos?
6. O equivalente textual é gerado ou editável, e quem prova não-deriva?
7. Correção sempre gera nova revisão?
8. Relation kinds fechados ou extensíveis por namespace?
9. Publicação exige todos os checks PASS ou perfis permitem N/A?
10. Metadata candidate será compatibilidade antecipada ou dependência?

#### Recommended Semantic Contract

Criar quatro schemas canônicos `.schema.yml`:

1. `diagram-request.schema.yml`: request, modo, reader question, resolution, evidence-set, publication intent, formato/renderer e alvo exato em review.
2. `diagram-semantic-model.schema.yml`: identidade/revisão, purpose, scope, sources/locators, claims, elements, encodings, visual semantics e cobertura do equivalente textual.
3. `diagram-bundle-manifest.schema.yml`: identity, lifecycle, retention class, owner, lineage, members, paths/digests, tags, destinations e persistência.
4. `diagram-validation-receipt.schema.yml`: identidade/digests observados e checks de schema, integridade referencial, evidência, reconciliação semântica, render, acessibilidade e persistência.

Bundle recomendado:

```text
<diagram-id>/<revision>/
  diagram.<source>
  diagram.<render>
  diagram.meta.yml
  diagram.claims.yml
  textual-equivalent.md
  validation.receipt.yml
```

Invariantes fora do schema devem resolver referências, calcular aggregate status, validar suficiência e conflitos, conferir cobertura do equivalente, vincular receipts aos bytes auditados e impedir publicação oficial sem persistência, render inspecionado e ausência de blockers. Persistência não implica promoção Git.

### Agent 3 — Artifact Lifecycle Auditor

#### Key Findings

- A fonte canônica deve permanecer em `transmutations/evidence-grounded-diagrams/`: o Arcanum define `transmutations/` como bounded cognitive synthesis e expõe tiers canônicos ao Codex por links ou packages em `.agents/skills/` (`README.md:115,128,138,181ff`).
- A skill já possui o owner semântico correto, mas não garante persistência, tagging nem paths obrigatórios; ao mesmo tempo, exige render inspecionado para publicação oficial (`SKILL.md:17,214-225`).
- A política de artefatos suporta lifecycle em estágios: output gerado permanece não durável e ignorado até promoção deliberada, e ferramentas que escrevem exigem validação (`ARTIFACT-CONSTITUTION.md`).
- Sidecars são adequados como direção, mas a Metadata Constitution ainda não é canônica. Novos contratos canônicos precisam usar `.schema.yml`.
- `x-ray` oferece precedente de renderer/validator, mas é seed, mais amplo e não comprovado como owner deste contrato.

#### Gaps or Inconsistencies

- Resultado pode omitir `artifact_path`.
- O ambiente não tem `mmdc`, Graphviz `dot` ou PlantUML, apesar do gate de publicação exigir render.
- Não há distinção explícita entre working, saved draft, validated, published e promoted.
- Não há contrato fechado de tags, versões, evidência ou índice.
- Bootstrap copia pacotes completos; sync incremental cobre apenas `orchestrate`.

#### Local Tensions

- Todo diagrama emitido é salvo × todo scratch é salvo.
- Instruction-only × completion gates machine-checkable.
- Draft válido × render obrigatório.
- Tags × índice autoritativo.
- Reuso de x-ray × transferência de ownership.

#### Questions for Synthesis

1. Que evento define emissão?
2. Onde drafts persistentes não promovidos devem viver?
3. Render externo inspecionado pode satisfazer publicação?
4. Que metadata candidate pode ser adotada localmente?
5. Sync genérico deve ser criado ou bootstrap permanece o único mecanismo?

#### Recommended Artifact Lifecycle

Estados: `working → saved draft → validated draft → published → promoted`. Falhas só são preservadas quando produziram entrega visível ou evidência útil. Promoção permanece explícita.

Cada entrega emitida torna-se bundle versionado com source, render quando disponível, metadata provisória, evidence refs e validation results. Scratch pode ser efêmero; qualquer estado salvo exige localização não opcional. Generated bundles continuam não canônicos até promoção.

Renderer ladder: renderer nativo quando disponível; renderer repo/browser suportado; source-only com validação estrutural e `render unavailable`. Ausência ou falha de render não impede salvar draft, mas bloqueia publicação oficial.

Tags controladas classificam; um índice resolve inventário, versões e estado atual. A fonte permanece em `transmutations/`; `.agents/skills/` e Codex home são derivados. Bootstrap transporta todos os support dirs exceto `development/`; o sync incremental atual não deve ser anunciado como compatível.

## Synthesis

### Tension T1 — Autoridade semântica atual viola a constituição de schema

**Held by the current skill contract:** `references/schema.md` se declara autoridade semântica e os arquivos `.schema.json` são tratados como contratos machine-validatable.

**Reality in repository governance:** novos schemas canônicos devem usar `.schema.yml`; Markdown descritivo deve ser explicitamente não canônico ou ter counterpart YAML.

**Impact:** critical — a skill nasce com autoridade dividida e contratos formalmente incompatíveis com o repo; instalação propagaria esse erro.

**Evidence:** Agent 2 finding 1; `framework/SCHEMA-CONSTITUTION.md:9-10,28-34,49-52`; `references/schema.md:3-7`.

### Tension T2 — Entrega prometida não implica artefato persistido

**Held by the requested behavior:** todo diagrama emitido deve ser salvo, tagueado, versionado e rastreável.

**Reality in the current implementation:** persistência não é um estado do workflow; `artifact_path` é opcional; não há identity, tags, lineage, receipt ou failure state de persistência.

**Impact:** critical — uma resposta pode parecer concluída e depois não existir como artefato auditável.

**Evidence:** Agent 1 finding 5; Agent 2 findings 2-3; Agent 3 findings 2-3.

### Tension T3 — Review read-only está misturado com mutação

**Held by the instruction layer:** review é read-only sem autorização separada.

**Reality in the mode contract:** só há create/review, e `correction_authorized` é um boolean dentro de review sem processo, envelope ou lineage próprio de revisão.

**Impact:** high — um agente pode sobrescrever ou reemitir o alvo auditado sem preservar a revisão anterior e sem receipt vinculado aos bytes revisados.

**Evidence:** Agent 1 finding 3; Agent 2 gaps 3, 11-12.

### Tension T4 — Equivalência textual forte é armazenada como string fraca

**Held by the semantic definition:** `textual_equivalent` deve preservar nós, relações tipadas, direção, escopo e distinções epistêmicas.

**Reality in workflow and schema:** o workflow reduz a obrigação a nodes/relations; o result permite string vazia e não registra cobertura dos claims.

**Impact:** high — caption, rationale, descrição visual e equivalente semântico podem ser confundidos; acessibilidade e auditabilidade ficam falsas.

**Evidence:** Agent 1 finding 4; Agent 2 finding 4.

### Tension T5 — Neutralidade de renderer não fornece execução determinística

**Held by the publication contract:** publicação oficial requer render inspecionado, e a skill permanece renderer-neutral.

**Reality in the environment:** `node`/`npx` estão disponíveis, mas `mmdc`, `dot` e PlantUML não; não há adapter contract ou capability detection na skill. `x-ray` é apenas seed/precedent.

**Impact:** high — a skill pode validar source, mas não pode honestamente declarar publicação oficial pronta no ambiente atual.

**Evidence:** Agent 1 gaps 5-7; Agent 3 findings 4-5 and gaps 2.

### Tension T6 — Tags individuais não produzem inventário confiável

**Held by the requested behavior:** tagging deve tornar os diagramas preservados reconhecíveis e recuperáveis.

**Reality in the repository/package:** não há vocabulário controlado nem índice da coleção; tags livres não resolvem current revision, lineage ou localização.

**Impact:** medium — bundles podem existir e ainda assim ficar órfãos, duplicados ou impossíveis de resolver por versão corrente.

**Evidence:** Agent 2 gaps 9-10 and local tension 3; Agent 3 gaps 4 and local tension 4.

### Tension T7 — Fonte canônica instalável, mas ainda não exposta

**Held by the runtime model:** tier canônico deve gerar superfícies em `.agents/skills/` e Codex home com support dirs intactos.

**Reality in tooling:** bootstrap copia support dirs exceto `development/` e o
sync incremental aceita qualquer sigil por `--sigil`; a skill, porém, ainda não
está registrada ou exposta como runtime desta working tree.

**Impact:** medium — o source tier e o fluxo incremental são viáveis, mas a
capability ainda não pode ser anunciada como instalada antes dos gates de
lifecycle e da geração da superfície derivada.

**Evidence:** Agent 3 findings 1 and gap 5; `tools/bootstrap_arcanum.sh:821-874,1215,1312,1318`; `tools/sync-generated-skill-package.sh:107,117`.

### Tension T8 — Metadata desejada ainda não é governança canônica

**Held by the proposed bundle:** identity, owner, lifecycle, selectors e validation profile são necessários.

**Reality in governance:** a Artifact Metadata Constitution contém esses campos, mas está em status candidate e depende de validação futura.

**Impact:** medium — a skill deve adotar compatibilidade prospectiva local, sem alegar conformidade constitucional nem depender de parser inexistente.

**Evidence:** Agent 2 finding 5; Agent 3 finding 4.

## Consolidated Recommendation

1. Manter a fonte canônica em `transmutations/evidence-grounded-diagrams/`. A operação é bounded synthesis; `x-ray` pode fornecer adapters e padrões, não ownership.
2. Reescrever `SKILL.md` como router/state machine curto, preservando no núcleo `claim <= evidence`, review read-only, equivalência textual e o gate `persist-and-tag` antes do handoff.
3. Tornar `create`, `review` e `revise` modos explícitos. `review-and-revise` deve ser composição sequencial; revise sempre cria nova revisão e preserva o original.
4. Substituir os JSON atuais por quatro contratos `.schema.yml`: request, semantic model, bundle manifest e validation receipt. Manter glossário Markdown como companion explicitamente não canônico.
5. Persistir cada diagrama emitido como bundle versionado; definir emitido como representação entregue ao usuário ou incorporada a outro artefato. Scratch interno não emitido pode ser efêmero.
6. Separar `caption`, `rationale` e `textual_equivalent`; o equivalente deve declarar cobertura dos claims load-bearing e ser reconciliado contra model/source/render.
7. Usar renderer ladder e capability detection. Source-only é draft válido; publicação oficial exige render inspecionado, inclusive quando produzido externamente e vinculado por receipt.
8. Usar tags controladas para classificação e um índice para inventário, lineage e current revision.
9. Tratar persistência, publicação e promoção como estados distintos. Persistir não significa commitar; publicar não significa promover a canonical/durable evidence.
10. Instalar superfícies derivadas pelo bootstrap completo ou pelo sync
incremental `--sigil evidence-grounded-diagrams`. Nunca editar
`.agents/skills/` como fonte.
11. Criar validador semântico além do shape validator e fixtures negativas para referências quebradas, status agregados inconsistentes, equivalência incompleta, render ausente em publicação, receipt obsoleto, persistência ausente e sobrescrita de revisão.

## Decisions Requested at Human Gate

1. Validar T1-T8 como tensões reais, misinterpretations ou itens a deferir.
2. Aprovar ou rejeitar a recomendação consolidada.
3. Escolher o storage root padrão para bundles persistidos; a auditoria não encontrou um owner canônico já consolidado para esse path.
4. Confirmar que `emitido` significa qualquer diagrama entregue ao usuário ou incorporado a outro artefato, excluindo scratch interno.
5. Confirmar que publicação oficial exige render inspecionado; source-only pode ser salvo como draft, mas não publicado.
6. Autorizar, em sessão separada, a implementação da skill, schemas, validators, templates, index e integração de runtime.

## Human Gate Notes

Approved by the user on 2026-08-25. The user confirmed that the design question
concerns the best possible prompt, schemas, bundled resources, persistence, and
tagging behavior; authorized implementation through the canonical Arcanum
`sigil-development` lifecycle; and requested a second adversarial review after
the changes without another confirmation gate.

One factual correction was accepted from the skeptic pass: the incremental
tool `tools/sync-generated-skill-package.sh` supports any sigil selected with
`--sigil`; only its `--runtime` selector is restricted to `orchestrate`.
Therefore T7 is narrowed to promotion and runtime exposure, not missing sync
capability.

## Follow-up Actions

- Canonical package: `transmutations/evidence-grounded-diagrams/`.
- Lifecycle harness and validation evidence: package-local `development/`.
- Registry and derived runtime exposure: after validation and review gates.
- Final promotion decision: owned by `sigil-development`, informed by the
  user-authorized second `review`.
