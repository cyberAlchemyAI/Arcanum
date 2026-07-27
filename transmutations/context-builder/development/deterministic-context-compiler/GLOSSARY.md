# Glossary

These terms are local explanatory vocabulary for this Invoke package. They are
not promoted Arcanum definitions.

| Term | Meaning |
| --- | --- |
| Context request manifest | Typed input containing obligations, candidate evidence mappings, policies, and output requirements. |
| Obligation | Stable requirement that must be covered, explicitly resolved, or block compilation. |
| Evidence candidate | Source path, selector, obligation refs, authority rank, ambiguity marker, and cost metadata proposed before deterministic selection. |
| Source snapshot | Exact source and selector binding with current content digest. |
| Excerpt object | Normalized selector-level bytes stored by content hash. |
| Content-addressed cache | Non-authority generated store whose object identity derives from admitted inputs and excerpt bytes. |
| Covering-set policy | Deterministic rule that chooses candidates until every obligation is covered or compilation blocks. |
| Compiled payload | Single runtime-facing representation selected from the persisted pack outputs. |
| Pack receipt | Machine record of inputs, selected objects, blockers, rendered hashes, counts, and compiler version. |
| Base-pack proof | Runtime receipt establishing that a referenced full pack is already available for a delta payload. |
| Token measurement | Count produced for one declared tokenizer and exact payload bytes. |
| Actual prompt usage | Runtime/provider receipt for prompt tokens actually processed; never inferred from file size. |
| Cache hit | Reuse of an exact validated excerpt object; not proof that the runtime already knows the excerpt. |
| Session evidence | Run-specific handoff artifacts that remain audit evidence rather than reusable source of truth. |

## Consistency Rules

- “Deterministic” always names the exact bounded inputs and outputs.
- “Cache” never implies authority, freshness, or runtime visibility.
- “Token reduction” is a measured comparison, not a design assertion.
- “Exact token count” requires a named tokenizer.
- “Runtime usage” requires a runtime receipt.
