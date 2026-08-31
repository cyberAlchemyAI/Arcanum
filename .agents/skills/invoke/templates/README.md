# Invoke Template Inventory

This directory contains invoke-owned template families and standalone companion templates used by the `invoke` spell.

## Ownership Model

| Path | Role |
| --- | --- |
| [domainspec-spec/](domainspec-spec/) | DomainSpec baseline bundle (define + design + plan stages). |
| [module-formulae/](module-formulae/) | Deprecated — legacy module-first bundle (retained for fixtures/mogt; see its README). |
| [implementation-layering.md](implementation-layering.md) | Standalone layering companion for plan, full, and validate flows. |
| [work-pack.md](work-pack.md) | Canonical executable planning manifest and current state for plan, full, and validate flows. |
| [generic/](generic/) | Neutral fallback family for broad lifecycle authoring requests. |
| [research/](research/) | Evidence-first discovery family. |
| [refresh/](refresh/) | Artifact refresh report and patch proposal family. |
| [architecture/](architecture/) | Architecture planning family. |
| [spell/](spell/) | Spell authoring handoff family. |
| [sigil/](sigil/) | Sigil authoring handoff family. |
| [session-handoff/](session-handoff/) | New session/thread handoff family for reflection, lifecycle splits, research directions, and continuations. |
| [ux-plan/](ux-plan/) | Experience planning family. |

## Family Scaffold Contract

Every dedicated family directory should contain:

- `README.md` with selection rules, outputs, gates, and validation commands.
- one primary template named after the family, for example `generic.md`.
- `examples/passing.md` with a minimal valid example.
- `examples/missing-input.md` with a negative example and expected block or flag result.

Every primary template should include frontmatter fields for:

- `template_id`,
- `template_type`,
- `applies_to`,
- `required_inputs`,
- `optional_inputs`,
- `output_files`,
- `status`,
- `authority_level`,
- `promotion_evidence`,
- `promotion_decision`,
- `validation_rules`,
- `validation_examples`,
- `created_at`,
- `updated_at`.

## Shared Validation Rules

1. Links in each template and example must resolve.
2. Every family must include one passing example and one missing-input negative example.
3. Template selection must record eligibility evidence and explicit user choice on ties.
4. Candidate templates remain candidate-only until validation evidence and explicit promotion approval exist.
5. Family templates must not duplicate [implementation-layering.md](implementation-layering.md) or [work-pack.md](work-pack.md); they should reference those standalone companions.
6. Wording must stay framework-neutral and Arcanum-owned.

## Promotion Gate

A family template can move from candidate to canonical only after:

- required inputs and outputs are documented,
- validation examples pass,
- at least one approved invoke stage uses the template or reviews it as equivalent to an approved-stage need,
- promotion evidence is recorded,
- explicit promotion decision is captured.
