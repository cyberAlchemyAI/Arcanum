# Evidence And Inventory Discipline

Status: active-pattern
Steward: Inventory

## Purpose

Govern reusable repository evidence capture, indexing, and handoff so agents can retrieve what the repository already knows without treating selected evidence as downstream authority.

## Boundary

This discipline names inventory and evidence handoff practice. It does not decide ontology meaning, define glossary terms, or promote capability-local evidence beyond its owner.

## Evidence

- [Inventory](../../arcana/inventory/README.md) - defines evidence selection, indexes, cards, and non-authoritative handoff behavior.
- [Hidden Discipline Scan](../development/HIDDEN-DISCIPLINE-SCAN.md) - identifies evidence discipline as a recurring practice.
- [Discipline Catalog](../DISCIPLINES.md) - records `evidence-inventory` as an active-pattern discipline.

## Validation

- Mode: mixed
- Check: inventory card/index validators where applicable, plus `python3 disciplines/scripts/validate-discipline-catalog.py`.
- Latest result: pass

## Quality Bar

A useful evidence and inventory discipline entry must:

- preserve the distinction between source evidence and downstream authority,
- cite inventory-owned retrieval or handoff artifacts,
- keep selectors and cards traceable to local files,
- route ontology and definition claims to their owners,
- name the next hardening move for evidence handoffs.

## Promotion Guardrail

Inventory evidence can support later owner review, but it cannot directly promote ontology, glossary, registry, sigil, spell, or discipline knowledge.
