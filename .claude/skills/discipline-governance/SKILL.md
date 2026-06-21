---
surface_kind: generated-native-runtime-package
runtime: claude
canonical_source: arcana/discipline-governance/SKILL.md
alias_of: null
generated_by: tools/bootstrap_arcanum.sh --profile
mutation_policy: regenerate-from-canonical-source
name: discipline-governance
description: "Use when: formalizing, routing, validating, promoting, or retiring an Arcanum discipline so a recurring cross-capability practice gets a card, catalog entry, and a hardening route without claiming sigil or spell authority."
argument-hint: "<scan|formalize|route|validate|promote|deprecate> <practice-or-discipline-id> [--status <status>] [--evidence <path>] [--dry-run]"
tier: arcana
domain: discipline-governance
version: 0.2.1
origin: created from the disciplines layer (catalog, card template, schema, catalog validator) which had no owning lifecycle sigil; promoted to 0.2.0 on 2026-06-21 after the 3-regime experiment harness (low=gitignore, medium=receipt-id-legend, complex=scan+curation), telemetry emission, and a reflection pass; 0.2.1 applied the two reflection-named iterations (public/private candidate tagging in scan/route; active-pattern cross-sigil evidence rule in validate)
allowed-tools: Read, Write, Glob, Grep, Bash, AskUserQuestion, Agent
---

# Sigil: Discipline Governance

<objective>
Turn a recurring cross-capability practice into a governed Arcanum discipline: an evidence-backed discipline card, a catalog entry, and a named hardening route, while keeping the disciplines layer a catalog authority rather than a promotion surface for sigils, spells, or knowledge.
</objective>

<logic-type>
Arcana: long-lived governance of method-level practices across context selection, evidence, routing, validation, and promotion.
</logic-type>

<modes>
- `scan`: find recurring or hidden practices that appear across multiple capabilities and propose candidate disciplines. **Each candidate is tagged `public-safe` or `private-parent` with a named target catalog** (public arcanum vs a private umbrella catalog); a practice tied to private composition must never be routed into the public catalog (v0.2.1).
- `formalize`: turn one practice into a discipline card and a catalog row, default status `candidate`, written to the target catalog named by the candidate's `public-safe | private-parent` tag.
- `route`: decide the hardening move for a discipline (catalog-only, template, validator, constitution, spell, or sigil) and hand off to the owning lifecycle. The route never moves a `private-parent` discipline into the public catalog (v0.2.1).
- `validate`: run the catalog validator and check a card against the discipline schema, returning pass, flag, or block. **An `active-pattern` (or higher) discipline must cite at least one evidence ref OUTSIDE its own owning sigil; a card whose evidence is only its own sigil README is a thin one-per-sigil pointer and stays `candidate`** (v0.2.1).
- `promote`: raise a discipline's status when the next route names owner, evidence, validation surface, and mutation boundary.
- `deprecate`: retire a discipline with rationale and a superseding route.
</modes>

<applicability>
Use this sigil when:

- a practice recurs across multiple sigils, spells, or framework documents and has no formal home,
- scattered rules for one practice are causing drift, rework, or confusion,
- a discipline card or catalog entry must be created, corrected, or kept schema-valid,
- a discipline needs a hardening decision (constitution, validator, template, spell, or sigil),
- a discipline's status should advance or retire with named evidence,
- the discipline catalog must be validated after edits.
</applicability>

<non-applicability>
Do not use this sigil when:

- the practice is a one-off task, not a durable cross-capability method,
- a capability-local note inside one sigil or spell is enough,
- the request is to mutate a sigil, spell, registry, ontology, or glossary contract (route to that owner),
- the request is to author the enforceable constitution itself (route to `constitution-governance` after the discipline names that route),
- the request is to define a canonical term (route to `definitions-governance`).
</non-applicability>

<inputs>
Expected inputs, if available:

- a candidate practice name or an existing `discipline_id`,
- evidence paths where the practice already appears,
- the current catalog `disciplines/DISCIPLINES.md`,
- the card template `disciplines/templates/discipline-card.md`,
- the schema `disciplines/discipline.schema.yml`,
- prior scan output under `disciplines/development/`,
- a desired status or hardening route.
</inputs>

<chain-boundary>
Discipline Governance owns the disciplines layer: cards, the catalog, scan evidence, routing decisions, and status changes.

- `constitution-governance` owns constitutions. When a discipline's hardening route is a constitution, this sigil names the route and hands off; it does not author the constitution itself.
- `definitions-governance` owns canonical terms a discipline depends on.
- `inventory` and `context-builder` supply source-backed evidence; their evidence stays non-authoritative until an owner promotes it.
- `decision-gate` resolves blocker-level promotion, precedence, or scope decisions.
- `sigil-development` owns this sigil's own lifecycle, observability, and reflection.

A discipline may recommend a route, but it must never directly promote registry, ontology, glossary, sigil, or spell knowledge.
</chain-boundary>

<default-output>
Prefer target-local outputs:

1. `disciplines/cards/<discipline-id>.md` for a discipline card,
2. a single row in `disciplines/DISCIPLINES.md` for the catalog entry,
3. `disciplines/development/` for scan evidence and routing notes,
4. `arcana/discipline-governance/development/` for this sigil's own development artifacts.

Do not author constitutions, validators, or sigils inline; name the route and hand off to the owning lifecycle.
</default-output>

<process>
1. Resolve the target: a candidate practice (for `scan`/`formalize`) or an existing `discipline_id` (for `route`/`validate`/`promote`/`deprecate`).
2. Classify the mode. If no mode is given, infer the smallest mode that satisfies the request and state the inference.
3. Gather evidence. A discipline needs at least one concrete repository reference. Confirm the maintenance signal: the practice appears across multiple capabilities, already has scattered rules, or has caused drift, rework, or confusion. Tag the candidate `public-safe` or `private-parent` and name its target catalog (v0.2.1).
4. For `formalize`, write a card from `disciplines/templates/discipline-card.md` with: status, steward, purpose, boundary, evidence refs, quality bar, and promotion guardrail. Add one catalog row to the target catalog (public `disciplines/DISCIPLINES.md`, or the private umbrella catalog for a `private-parent` discipline) matching the required columns. Default status is `candidate`.
5. For `route`, choose the smallest sufficient hardening move and name its owner:
   - catalog-only when the card is enough,
   - template when the practice needs a reusable shape,
   - validator when the practice can be checked deterministically,
   - constitution when the practice enforces structure or form (hand off to `constitution-governance`),
   - spell or sigil only when the practice needs executable lifecycle behavior.
6. For `validate`, run the catalog validator and check the card against the schema. Report pass, flag, or block with the failing rule. Additionally flag any `active-pattern`-or-higher discipline whose evidence is only its own owning sigil (a thin one-per-sigil pointer): it must cite cross-capability evidence outside that sigil or be downgraded to `candidate` (v0.2.1).
7. For `promote`, apply the Growth Rule: raise status only when the next route names owner, evidence, validation surface, and mutation boundary. Route blocker-level decisions through `decision-gate`.
8. For `deprecate`, mark the discipline `deprecated`, cite the rationale, and name the superseding route.
9. Preserve the layer boundary in every mode: do not mutate capability-local contracts and do not treat discipline evidence as canonical knowledge.
10. Validate the result (catalog validator, schema, local Markdown links, product-neutral wording) and return paths changed, status, route, and next step.
</process>

<discipline-model>
A discipline has a named purpose, a boundary, evidence, a steward, a maturity status, and a next hardening move.

Status ladder:

- `candidate`: useful practice exists, authority and validation still being proven,
- `active-pattern`: already used by active capabilities, but the discipline-level contract is not canonical,
- `implemented`: working repository support exists, may still need discipline-level rules,
- `canonical`: accepted framework authority with validator or constitution support,
- `deprecated`: superseded or withdrawn.

Growth Rule: promote a discipline only when the next route names its owner, evidence, validation surface, and mutation boundary.
</discipline-model>

<routing-model>
Map each discipline to the smallest sufficient hardening route:

| Route | Use when | Owner |
| --- | --- | --- |
| catalog-only | the card captures the practice and no enforcement is needed yet | Discipline Governance |
| template | the practice needs a reusable shape | the template's host capability |
| validator | the practice can be checked deterministically | `tools/` plus the rule's owner |
| constitution | the practice enforces structure or form across artifacts | `constitution-governance` |
| spell or sigil | the practice needs executable lifecycle behavior | `spellcraft` or `sigil-development` |

A discipline can hold more than one route over time, but each route names a separate owner.
</routing-model>

<validation-model>
Every discipline card declares one validation mode, matching the schema:

- `prose-review`: human or model review only,
- `validator`: a deterministic script or check enforces it,
- `fixture`: example-backed checks enforce it,
- `observability`: usage signals confirm it,
- `mixed`: a combination.

Run `python3 disciplines/scripts/validate-discipline-catalog.py` after any catalog edit. A card that claims a `validator` mode must cite an existing validator or be blocked until one exists.
</validation-model>

<quality-bar>
A successful execution must:

- produce or update an evidence-backed discipline card and a schema-valid catalog row,
- cite at least one concrete repository reference for the practice,
- name the steward and the next hardening move,
- choose the smallest sufficient route and hand off enforcement to the owning lifecycle,
- keep discipline guidance separate from capability-local authority,
- pass the catalog validator and resolve all local Markdown links,
- route blocker-level promotion or scope decisions through `decision-gate`,
- return paths changed, status, route, and next step.
</quality-bar>

<anti-patterns>
Avoid:

- cataloging a one-off task as a durable discipline,
- formalizing a practice with no concrete evidence,
- letting a discipline promote a sigil, spell, registry, ontology, or glossary entry,
- authoring a constitution, validator, or sigil inline instead of naming the route,
- claiming a `validator` mode with no validator behind it,
- raising status without owner, evidence, validation surface, and mutation boundary,
- editing the catalog without running the catalog validator.
</anti-patterns>

<observability>
For meaningful executions, emit or prepare telemetry with:

- mode,
- target discipline id,
- card created or updated,
- catalog row added or changed,
- route chosen and owner,
- status before and after,
- validator result,
- decision gates required,
- pass, flag, or block result.
</observability>

<output-contract>
Return:

```markdown
## Discipline Governance Result

- Mode: <scan | formalize | route | validate | promote | deprecate>
- Target discipline: <id or candidate>
- Status: pass | flag | block
- Card: <path or none>
- Catalog row: <added | changed | none>
- Route: <catalog-only | template | validator | constitution | spell | sigil>
- Status change: <none or before -> after>
- Validator result: <pass | flag | block | not-run>
- Decisions needed: <none or list>
- Validation: <checks and result>
- Next route: constitution-governance | decision-gate | sigil-development | task-session | deferred
```
</output-contract>

<origin>
Created from the existing `disciplines/` layer (catalog, card template, schema, and catalog validator), which had no owning lifecycle sigil. Generalized into an Arcana governance sigil that formalizes, routes, validates, promotes, and retires disciplines without claiming sigil or spell authority.
</origin>
</content>
</invoke>
