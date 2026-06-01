# Stage 01: Context Builder Evidence Baseline

Status: `pass`

## Evidence Baseline

| Evidence | Role |
| --- | --- |
| `REFINE-SEED-PROPOSAL.md` | Captures the raw operator intent and write boundary. |
| `development/craft/CRAFT-RECURSIVE-LEDGER-DEFINE.md` | Establishes that a ledger can model a context, not just tasks. |
| `development/craft/CRAFT-MVP-DESIGN.md` | Provides the local pattern: define first, design second, schema authority, human-readable fixture, validation before promotion. |
| `development/craft/CRAFT-LEDGER-SCHEMA.yml` | Shows candidate schema authority with row families, enums, validation, and lifecycle gates. |
| `development/craft/LEDGER.md` | Demonstrates a Markdown ledger fixture with contexts, artifacts, relations, typed items, and decisions. |
| `formulae/dispatch-spec/TECHNIQUE-CATALOG.md` | Supplies route techniques used in the dispatch. |

## Local Pattern Extracted From Craft

Craft's recursive ledger is the nearest local model. It tracks nested contexts, artifacts, relations, typed items, decisions, gates, and side threads.

The User ledger should reuse the *shape discipline* without copying Craft's domain:

- Craft ledger tracks project/context state.
- User ledger tracks learning/profile state.
- Craft blockers/enablers map to User confusion/bridge/mastery evidence only at the schema-pattern level.
- Craft's source-of-truth split maps to User's split between candidate ledger, human-readable glossary, and future generated indexes.

## Hidden Structure

The User/Guide system has six hidden components:

1. User profile seed: prior domains, preferred vocabulary, known primitives, avoided metaphors, accessibility/preferences.
2. Concept library: domain-neutral primitives and optional domain-specific libraries.
3. Guide move: explanation, analogy, example, contrast, self-explanation prompt, retrieval prompt, or transfer prompt.
4. Interaction receipt: what was attempted, what changed, how many turns, what worked, what failed.
5. Ledger update: preference, partial mastery, blocker, bridge, or glossary entry.
6. Review boundary: user-local learning memory is not canonical Arcanum knowledge.

## Baseline Verdict

The target is refinement-ready. It needs a new development area because no `User` or `Guide` package exists yet, and the request is too broad for immediate implementation.
