# Two-Lane Representation Discipline

Status: candidate
Steward: Craft development package and Inventory

## Purpose

Govern artifacts that carry the same content in two synchronized, separately-authoritative lanes: a **human prose lane** authored for people, and a **machine-structured lane** (YAML/JSON) authored for agents and validators. Each lane is the source of truth for its own consumer — prose for human reading and judgment, structure for deterministic filtering, validation, and reuse without reparsing prose — and the two are kept in sync so neither silently drifts from the other.

## Boundary

This discipline names the dual-lane representation invariant only: that a governed artifact has a human lane and a synchronized machine lane, each authoritative for its consumer. It does not own the method that produces either lane, the machine lane's schema contract (that is the `schema` discipline), or any single capability's ledger, inventory, or view content. Craft (`CRAFT.md` prose × `.craft/ledger.yml`) and Inventory (Markdown view × JSON view) are instances of this discipline, not owned by it. This is the human/machine-representation sense of "two-lane"; the opposed-lanes adjudication sense is the sibling [`two-lane-dialectic`](two-lane-dialectic.md) discipline.

## Evidence

- [Inventory](../../arcana/inventory/README.md) - states the invariant directly: "the human view stays Markdown; the machine view is JSON so agents can filter without reparsing prose."
- [Craft README](../../development/craft/README.md) - the recursive ledger pairs human prose with a schema-backed machine ledger (`.craft/ledger.yml`) kept in sync.
- [Craft discipline](craft.md) - records Craft as a candidate instance that keeps prose and a machine ledger together.
- [Discipline Catalog](../DISCIPLINES.md) - records `two-lane-representation` as a candidate discipline.

## Validation

- Mode: prose-review
- Check: `python3 disciplines/scripts/validate-discipline-catalog.py` for catalog row shape, plus card review that a claimed instance genuinely carries BOTH lanes and names how they stay in sync (not a single artifact with an incidental schema).
- Latest result: pass

## Quality Bar

A useful two-lane representation entry must:

- identify both lanes explicitly — which artifact is the human prose lane and which is the machine-structured lane,
- name each lane's consumer and why that consumer needs its own lane (human judgment versus deterministic filtering and validation),
- name the synchronization obligation and how drift between the lanes is detected or prevented,
- keep the machine lane's schema validity with the `schema` discipline, not here,
- distinguish a true dual-lane artifact from a single artifact that merely has a schema or incidental metadata.

## Promotion Guardrail

Discipline evidence can recommend a route, but it cannot directly promote registry, ontology, glossary, sigil, or spell knowledge. Pairing two lanes does not make either lane canonical; canonical status for the machine lane routes through the `schema` discipline and its owner.
