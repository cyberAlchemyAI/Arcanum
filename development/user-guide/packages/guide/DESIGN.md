# Guide Design

## Invoke Result

- Mode: full authoring package, design slice
- Spell: invoke
- Canonical ID: invoke
- Scope: `development/user-guide/packages/guide/`
- Phase status: `flag`
- Mode contract: `spells/invoke/design.md`
- Design views: context, high-level structure, low-level components, workflow process, decision flow, dependency interface
- Next route: `spellcraft` after User and Translate L0 evidence exists

## View 1: Context

Guide is the top-level orchestration candidate.

```text
Guide
  -> User ledger handles
  -> target/context inspection
  -> optional research/subagents
  -> optional Translate
  -> explanation sequence
  -> understanding validation
  -> User ledger update proposal
```

## View 2: High-Level Structure

| Component | Responsibility |
| --- | --- |
| Request frame | Captures what the user wants guided. |
| Route planner | Chooses inspect, research, translate, x-ray, inventory, or direct explanation. |
| Dispatch gate | Bounds subagent/research work. |
| Explanation assembler | Produces ordered guide sections. |
| Understanding validator | Asks active evidence prompts. |
| Guide receipt | Summarizes route, evidence, and User update proposal. |

## View 3: Low-Level Components

Candidate route fields:

- `guide_request_id`
- `target_ref`
- `target_type`
- `user_goal`
- `known_user_handles`
- `needed_context`
- `dispatch_steps`
- `translate_request_ref`
- `explanation_sections`
- `active_evidence_prompt`
- `receipt`

## View 4: Workflow Process

```text
/guide target
  -> frame target and user goal
  -> inspect available context
  -> decide whether research/subagents are needed
  -> call x-ray/inventory/context-builder if needed
  -> call Translate if vocabulary bridge is needed
  -> assemble guide sections
  -> ask active evidence prompt
  -> emit guide receipt and User update proposal
```

## View 5: Decision Flow

| Condition | Decision |
| --- | --- |
| Target structure is hidden. | Call x-ray or architecture-pattern inventory. |
| Missing facts block explanation. | Dispatch bounded research/subagent. |
| User needs vocabulary bridge. | Call Translate. |
| User confirms clarity passively. | Mark clarified, not mastered. |
| User gives teach-back/transfer. | Propose mastery update. |

## View 6: Dependency Interface

| Dependency | Direction | Contract |
| --- | --- | --- |
| User ledger | read/write via receipts | Guide reads concept state and proposes updates. |
| Translate | call | Guide requests translation and receives mapped explanation. |
| X-ray/Inventory/Research/Subagents | optional dispatch | Guide frames bounded tasks and consumes summaries. |

## Design Flags

- Guide should wait until User L0 and Translate L0 fixture evidence exists.
- Subagent dispatch gates need a later spellcraft design.
