---
tags: [craft-method, formal-foundations, category-theory, variational-inference, residue, schema-translation]
node_type: discovery
is_session: true
layer: theory
nature: synthesis
status: active
created: 2026-06-10
timestamp: 2026-06-10T15:42:00-03:00
expires: 2026-08-09
conversation_id: craft-formal-foundations
decisions_made: true
contradictions_found: false
specs_updated: [development/craft/CRAFT-FORMAL-FOUNDATIONS.md]
promoted_candidates: []
expected_importance: 8
importance_rationale: "Grounds Craft's core operations (residue, reflection tower, stopping criteria) in proven categorical theorems and a peer-reviewed probabilistic framework, constraining future implementation."
---

# Craft Formal Foundations

## Summary

Connected the AutoBayes paper (compositional variational inference) and the sibling `domainspec-theorem` repo (Lean 4 categorical formalization of schema→data translation and residue) to Arcanum's Craft feature, establishing domainspec-theorem as the machine-checked formalization of Craft's method and AutoBayes as its probabilistic cousin. Authored `development/craft/CRAFT-FORMAL-FOUNDATIONS.md` mapping each Craft term to proven theorems and deriving three design constraints: validate schema- and instance-fidelity separately (M6 counterexample), stop by economic decision since the tower never finitely closes (transfinite persistence), and a finite residue plateau makes stopping safe. Decided not to adopt domainspec's fractal taxonomy. Clarified that Craft today types residue by ownership (ledger `base_type`) while domainspec types it by where the loss occurred (V/H/D axes), flagging that wiring as the top next step.

## Files touched

- development/craft/CRAFT-FORMAL-FOUNDATIONS.md
