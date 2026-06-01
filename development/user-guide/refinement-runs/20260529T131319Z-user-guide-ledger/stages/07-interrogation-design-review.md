# Stage 07: Interrogation Design Review

Status: `flag`

## Review Findings

| Severity | Finding | Required Repair |
| --- | --- | --- |
| P1 | `concept_state` could overclaim mastery. | Add evidence types and statuses that distinguish exposed, clarified, practiced, transferable, mastered, and stale. |
| P1 | `attempt_count` can feel judgmental. | Rename semantics to `clarification_turns` or define it as section friction, not user quality. |
| P1 | Guide receipts might store too much raw conversation. | Store short summaries and pointers, not full transcripts, unless the user explicitly opts in. |
| P2 | The install game needs a skip path. | It must produce an empty/minimal profile and allow later replay. |
| P2 | The concept library seed may privilege software too early. | Treat software concepts as one library among many; install can add domain libraries when available. |
| P2 | Cross-domain analogies need guardrails. | Every bridge pattern needs `maps_well`, `breaks_here`, and `target_definition`. |

## Mastery Rule

Do not add a definition to the user glossary as mastered unless at least one active evidence type exists:

- user teach-back,
- retrieval from memory,
- correct transfer to a new example,
- blocker resolution plus user explanation of what changed,
- successful contrast between neighboring concepts.

## Protected Context Rule

The user ledger stores learning preferences and confirmed knowledge state. It must not infer mental health, intelligence, personality type, identity categories, or hidden traits.

## Verdict

The design is viable with flags. Repair should make the ledger smaller, rename friction fields, and strengthen glossary evidence rules.
