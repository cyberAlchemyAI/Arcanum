---
artifact_id: craft-role-bound-handoff-model
status: candidate-development
created: 2026-06-13
source_project: adjacent-private-workspace
source_artifacts:
  - role-bound business-owner handoff
  - role-bound technical-owner handoff
  - role-bound proof-owner handoff
  - role-bound runtime-owner handoff
candidate_for: craft handoff/interface improvement
---

# Role-Bound Craft Handoff Model

## Purpose

Capture a reusable Craft handoff pattern discovered in an adjacent private
workspace: a handoff file should not only summarize work. It should be an
executable interface for a responsible person's agent.

The receiving agent should be able to read one `TO-<PERSON>.md` file, bind to
the right Craft ledgers, ask the responsible person only the questions they own,
update artifacts after each answer, and preserve cross-person ownership
boundaries.

## Model

A role-bound Craft handoff has five required sections.

### 1. Agent Execution Contract

The handoff starts with the exact steps the receiving agent must run:

1. Read the project bootstrap or orientation file by path.
2. Read the handoff and linked artifacts by path. Do not paste file contents
   into prompts.
3. Run `$craft state` for the listed ledgers before asking avoidable questions.
4. Run `$interrogation` only when the responsible person owns a decision,
   value, or judgment call.
5. Ask one evidence-backed question at a time.
6. Patch or update the target artifact immediately after each answer.
7. Route out-of-owner questions to the correct handoff instead of answering
   by proxy.
8. Return a `Craft Result` naming touched ledgers, decisions, residue, and next
   moves.

### 2. Person-Facing Craft Scope

The handoff names the exact ledgers the person owns or influences.

Each row should include:

- scope name;
- `.craft/ledger.yml` path;
- why this person owns the next move;
- relevant blockers, decisions, gaps, or recomposition gates.

This prevents agents from running repository-wide Craft status and then
guessing which node matters.

### 3. Interrogation Interface

The handoff names when `$interrogation` is appropriate and how questions should
be formed.

Each question should include:

- concise context with decision or gap ID;
- why the answer matters;
- recommended default when the artifact already supports one;
- unresolved risk if unanswered;
- target artifact or Craft ledger row to update.

The mode can be generic (`owner-decision`) or role-specific
(`technical-interface`, `measurement-proof`, `business-trigger`), but the
orchestrating behavior stays the same: one question, wait, update, repeat.

### 4. Ownership Boundary

The handoff must say what the person must not decide.

Examples:

- A technical owner can decide interface shape, but cannot ratify business
  posture or budget decisions.
- A proof owner can define measurement contracts, but cannot assign an
  independent reviewer or approve unsupported external claims.
- A runtime owner can shape AI/runtime and burn-in capture, but cannot implement
  an interactive product surface while the headless boundary is open.
- A business owner can ratify owner decisions and provide business inputs, but
  should not be asked to fill engineering implementation details when the specs
  already assign those to another owner.

### 5. Receipt And Craft Update Rule

After each answer, implementation receipt, validation run, or blocked route,
the agent updates the owning artifact.

Allowed updates:

- `decide` a Craft decision when the owner has selected an option;
- add evidence or residue to a gap;
- add receipt paths for completed work;
- update next moves;
- preserve a routed blocker for another owner;
- leave runtime handoffs as `not_run` when no runtime execution happened.

Disallowed updates:

- close child work without recomposition evidence;
- treat dispatch validation as execution evidence;
- answer for another responsible person;
- promote local definitions or runtime evidence into canonical knowledge without
  the owner route.

## Candidate Craft Contract Addition

Future Craft versions could add a lightweight `handoff_interface` method or
documented pattern:

```text
handoff_interface

Inputs:
  target_person
  role
  owned_ledgers
  interrogation_modes
  ownership_boundaries
  receipt_targets

Writes:
  TO-<PERSON>.md or equivalent handoff artifact
  optional Craft artifact row linking the handoff

Returns:
  handoff path
  owner ledgers
  pending decisions/gaps
  interrogation start points
```

Quality bar:

- handoff is executable by a future agent;
- every target ledger is explicit;
- Interrogation asks one question at a time;
- owner boundaries are explicit;
- artifact update targets are named;
- no runtime or recomposition closure is claimed without evidence.

## Source Fixture Mapping

The source fixture handoffs apply the model as follows:

| Source handoff | Interface focus |
| --- | --- |
| `TO-BUSINESS-OWNER.md` | Founder decisions, business inputs, staffing, legal, thresholds, parent blockers. |
| `TO-TECHNICAL-OWNER.md` | Backend/domain-modeler implementation surfaces, manifest boundaries, promotion-governance build tasks. |
| `TO-PROOF-OWNER.md` | QA, proof, measurement, claims register, instrumentation, validation packets. |
| `TO-RUNTIME-OWNER.md` | AI runtime lane, ingestion and drafting workflow, hardware spec and burn-in capture. |

This candidate should remain development evidence until a Craft maintenance pass
decides whether to promote it into `arcana/craft/SKILL.md`, examples, templates,
or generated runtime mirrors.
