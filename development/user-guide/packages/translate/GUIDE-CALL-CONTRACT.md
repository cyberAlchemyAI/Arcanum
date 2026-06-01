# Guide Call Contract For Translate

## Purpose

Define how Guide may call Translate without absorbing translation responsibility into Guide.

## Call Boundary

Guide may call Translate when:

- user needs source-domain vocabulary,
- an analogy or metaphor would help,
- a target concept needs a bridge from a familiar domain,
- explanation sections need terms aligned to User preferences,
- Guide needs to know whether a bridge failed and should become residue.

Guide should not call Translate when:

- missing facts require research,
- target structure must be inspected,
- canonical definitions are uncertain,
- the user asks for task execution rather than understanding.

## Request Shape

```yaml
translate_request:
  target_concept: <concept or artifact focus>
  source_domain: <known user domain>
  target_domain: <target domain>
  requested_style: <concrete-first | contrast | metaphor | plain-language>
  user_handle_refs:
    - <domain anchor or vocabulary preference>
  target_context_ref: <artifact or section>
```

## Response Shape

```yaml
translate_response:
  translated_explanation: <user-facing bridge>
  term_map: <source-to-target terms>
  bridge_map: <what maps and where it breaks>
  target_domain_definition: <truth-preserving definition>
  research_need: none | missing_fact | missing_source_domain | missing_target_definition | unsafe_mapping
  receipt_ref: <translate receipt>
```

## Research Boundary

Translate returns `research_need`. Guide decides whether to dispatch research or subagents.

## User Boundary

Translate returns `ledger_update_proposal`. User ledger decides whether to accept, reject, or defer it.

## Validation

Guide-call contract passes when:

- Guide can call Translate through the request shape,
- Translate response preserves target definition,
- Translate does not dispatch research,
- Translate does not write User ledger rows directly.
