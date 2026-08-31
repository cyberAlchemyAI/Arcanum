# INV-QUALITY-ANTI-PATTERN-001

## Scenario

Validate that `invoke` experiment evidence uses Quality Bar and Anti-Pattern checks as behavioral gates, not just file-existence checks.

## Quality Bar pass output

- Define output includes intent, scope, missing inputs, a machine candidate definition registry, deterministic views, define transport, phase status, and next route.
- Design output includes approved source contracts, six design views, risks, dependency/interface notes, glossary consistency, handoff boundaries, phase status, and next route.
- Integration output consumes define artifacts in design without inventing upstream approval.

## Quality Bar partial output

- Output is usable but names unresolved non-blocker gaps.
- Missing optional evidence is marked explicitly and routed to follow-up.

## Quality Bar fail output

- Output claims `pass` while required inputs, source contracts, or approved define outputs are missing.
- Output is a save-summary instead of the actual artifact body.

## Anti-Pattern flag hit

- Candidate template is usable but not approved for promotion.
- Evidence ambiguity is present but does not control a required design decision.

## Anti-Pattern block hit

- Design proceeds without approved define outputs or explicit discovery approval.
- Design treats missing contracts as approved.
- Design silently implements deferred `plan` or `full` behavior.
- Design mutates downstream spell or sigil contracts instead of handing off to `spellcraft` or `sigil-development`.
- Define silently promotes a candidate definition or treats a generated glossary view as its authority source.
