# Invoke Validation Experiment

This experiment applies the framework [Validation Experiment Protocol](../../../framework/VALIDATION-EXPERIMENT-PROTOCOL.md) to the `invoke` spell.

## Artifact

- Canonical ID: `invoke`
- Source path: [../README.md](../README.md)
- Promotion target: preserve implemented-mode evidence and proceed toward library spell registry release only after `full` and `validate` evidence
- Current status: L0 `define`, L1 `design`, L2 `plan`, L2H `handoff`, and L2R `refresh` implemented; `full` and `validate` deferred

## Hypothesis

`invoke` can reliably turn vague development intent into governed define outputs, turn approved define outputs into governed design and plan artifacts, and refresh existing workflow artifacts without confusing completion of the current Refresh artifact with permission or readiness for later lifecycle work.

If this passes, the implemented modes retain their evidence-backed status and the targeted Refresh repair is usable. `full`, `validate`, and registry release remain separately gated.

## Fixtures

| Fixture ID | Scenario | Input Shape | Expected Result |
| --- | --- | --- | --- |
| [TEMPLATE-TASK-MATRIX](TEMPLATE-VALIDATION-TASKS.md) | Template validation task inventory. | Every invoke-owned template family or standalone companion. | `pass`; each template target has low, medium, and complex realistic tasks. |
| [INV-DEFINE-PASS-001](fixtures/INV-DEFINE-PASS-001.md) | Define from vague but usable development intent. | Core goal, scope hints, template inventory, concept sources. | `pass`; spec, glossary, and define transport outputs are produced. |
| [INV-DEFINE-BLOCK-001](fixtures/INV-DEFINE-BLOCK-001.md) | Missing core goal. | No actionable goal or scope boundary. | `block`; result records missing goal and keeps next route deferred. |
| [INV-DEFINE-FLAG-001](fixtures/INV-DEFINE-FLAG-001.md) | No exact eligible template and candidate creation is unapproved. | Core goal with unsupported template fit. | `flag`; candidate-template gap is recorded without promotion. |
| [INV-DEFINE-GLOSSARY-001](fixtures/INV-DEFINE-GLOSSARY-001.md) | New glossary term has no Necronomicon match. | Core goal with a local term, `sol-thread`. | `pass`; no-match term is recorded with rationale and promotion gate. |
| [INV-DESIGN-PASS-001](fixtures/INV-DESIGN-PASS-001.md) | Design from approved define outputs. | Approved spec, approved glossary, source contracts, design constraints. | `pass`; architecture bundle includes all six views, glossary consistency report, design transport report, and next route `plan`. |
| [INV-DESIGN-BLOCK-001](fixtures/INV-DESIGN-BLOCK-001.md) | Missing source contracts without discovery approval. | User asks for design, but approved source contracts are absent and discovery mode is not approved. | `block`; result records missing inputs and routes back to `define` or discovery approval. |
| [INV-DESIGN-FLAG-001](fixtures/INV-DESIGN-FLAG-001.md) | Evidence ambiguity. | Approved spec exists, but architecture evidence is contradictory or incomplete. | `flag` or `block` depending on decision impact; research companion is selected and claim status is carried into design decisions. |
| [INV-DESIGN-HANDOFF-001](fixtures/INV-DESIGN-HANDOFF-001.md) | Spell or sigil target. | Approved define outputs target a spell or sigil. | `pass` or `flag`; `invoke` emits handoff context and routes execution to `spellcraft` or `sigil-development`. |
| [INV-INTEGRATION-DEFINE-DESIGN-001](fixtures/INV-INTEGRATION-DEFINE-DESIGN-001.md) | Define-to-design integration chain. | Realistic request, define expected output, concrete spec/glossary/transport artifacts, and design expected output. | `pass`; design consumes define artifacts, preserves glossary terms, emits six views, records transport, and routes to `plan`. |
| [INV-REFRESH-PASS-001](fixtures/INV-REFRESH-PASS-001.md) | Complete proposal with later gates. | Exact proposal, no apply approval, and pending target work. | `pass`; current proposal is complete, handoff is gated, and mutation remains unauthorized. |
| [INV-REFRESH-FLAG-001](fixtures/INV-REFRESH-FLAG-001.md) | Refresh-authoring ambiguity. | Conflicting artifacts with no known authority winner. | `flag`; exact safe proposal remains incomplete and the blocker is scoped to refresh authoring. |
| [INV-REFRESH-BLOCK-001](fixtures/INV-REFRESH-BLOCK-001.md) | Missing current-mode inputs. | Target artifact inventory and exact scope are missing. | `block`; no safe Refresh artifact is produced. |
| [INV-REFRESH-NOOP-001](fixtures/INV-REFRESH-NOOP-001.md) | Evidence already represented. | No delta or drift. | `no-op`; handoff is not needed. |
| [INV-REFRESH-APPLY-PASS-001](fixtures/INV-REFRESH-APPLY-PASS-001.md) | Approved application. | Exact scope, explicit approval, and validation command. | `pass`; delta is applied and validated with ready handoff. |

## Execution Method

Use the contract dry-run runner:

```bash
arcanum/spells/invoke/development/run-validation-fixtures.sh
```

The runner does not invoke a live Codex command process. It replays fixture expectations against the canonical `invoke define` and `invoke design` contract gates. This keeps the experiment reproducible until a live Codex command execution harness exists.

Each fixture also includes a realistic user request and an expected user-facing `Invoke Validation Fixture Result` file. The runner checks both the fixture and expected output.

Each run writes a timestamped report under `arcanum/spells/invoke/development/runs/`.

To run every template task through Codex, generate prompts with [generate-template-example-prompts.sh](generate-template-example-prompts.sh) and follow [TEMPLATE-EXAMPLE-RUNBOOK.md](TEMPLATE-EXAMPLE-RUNBOOK.md).

## Required Checks

| Check | Command Or Method | Pass Criteria |
| --- | --- | --- |
| Markdown links | `find arcanum/spells/invoke -name '*.md' -print0 \| xargs -0 -n1 ./tools/check_markdown_links.sh` | Every invoke markdown file reports passing links. |
| Spell contract structure | Review against [../../../arcana/spellcraft/SKILL.md](../../../arcana/spellcraft/SKILL.md) validate criteria. | Identity, modes, phases, gates, handoffs, failure policy, observability, and output contract are present. |
| Template scaffold coverage | Inspect [../templates/README.md](../templates/README.md) and family folders. | Required family README, primary template, passing example, and missing-input example exist. |
| Template task matrix coverage | Inspect [TEMPLATE-VALIDATION-TASKS.md](TEMPLATE-VALIDATION-TASKS.md). | Module Formulae, standalone companions, and each dedicated family have low, medium, and complex tasks. |
| Template prompt coverage | Inspect `example-prompts/`. | Every template task has a generated Codex invocation prompt and output capture path. |
| Prompt selector coverage | Run [select-template-example-prompt.sh](select-template-example-prompt.sh). | Exact task ID, template+complexity, and `next` selection return prompt and output paths. |
| Define gate coverage | Review [../define.md](../define.md). | Missing goal blocks, candidate-template gaps flag, glossary promotion is gated, and define transport behavior is defined. |
| Design gate coverage | Review [../design.md](../design.md). | Six views, glossary consistency, source-contract gate, no-silent-upstream-mutation, and transport behavior are defined. |
| Refresh gate coverage | Review [../refresh.md](../refresh.md) and refresh fixtures. | Phase status is current-artifact-local, blockers have lifecycle scope, handoff readiness is separate, and proposal-only pass never authorizes mutation. |
| Refresh machine evidence | Run `run-distill-active-mode-evidence-fixtures.sh`. | Valid apply and proposal evidence pass; proposal mutation stays unauthorized; downstream-only flag misclassification blocks. |
| Codex adapter readiness | Inspect `.agents/skills/invoke/SKILL.md`, `.arcanum/runtime/config.json`, and `.codex/commands/arcanum-spell-invoke.md` when legacy commands are installed. | Codex can discover the native `invoke` skill package, and the optional legacy command routes to canonical `arcanum/spells/invoke` contracts. |
| Fixture replay | `arcanum/spells/invoke/development/run-validation-fixtures.sh` | Every fixture and expected output reports `PASS`, the final result is `RESULT: pass`, and a timestamped run report is written. |
| Integration replay | `arcanum/spells/invoke/development/run-validation-fixtures.sh` | Define-to-design fixture proves spec, glossary, and transport artifacts feed the design output. |
| Registry gate | Inspect [../../../registry/SPELLS.md](../../../registry/SPELLS.md). | `invoke` is not registered until validation passes. |

## Dry-Run Output Contract

Each fixture dry-run should return:

```markdown
## Invoke Validation Fixture Result

- Fixture: <fixture-id>
- Mode: define | design | plan | handoff | refresh
- Phase status: pass | flag | block
- Phase status basis: <current artifact completeness when mode is refresh>
- Handoff readiness: <ready | gated | deferred | blocked | not-needed when mode is refresh>
- Inputs present: <summary>
- Template/profile selection: <summary>
- Design views: <coverage summary | n/a>
- Glossary consistency: pass | flag | block | n/a
- Transport report: <path | simulated>
- Decisions: <summary>
- Unresolved gaps: <summary>
- Expected next route: plan | define | spellcraft | sigil-development | deferred
- Verdict: pass | flag | block
```

## Promotion Gates

The implemented Invoke modes retain their validation status when:

- `TEMPLATE-TASK-MATRIX` passes,
- `PROMPT-SELECTOR` passes,
- `INV-DEFINE-PASS-001` passes,
- `INV-DEFINE-BLOCK-001` blocks for the expected reason,
- `INV-DEFINE-FLAG-001` flags for the expected candidate-template reason,
- `INV-DEFINE-GLOSSARY-001` records a no-match glossary term without silent promotion,
- `INV-DESIGN-PASS-001` passes,
- `INV-DESIGN-BLOCK-001` blocks for the expected reason,
- `INV-INTEGRATION-DEFINE-DESIGN-001` passes,
- all five Refresh classification fixtures pass,
- Refresh machine evidence rejects downstream-only proposal flags and proposal-only mutation authority,
- companion selection works for research, UX, spell, and sigil design cases,
- glossary conflicts are recorded instead of silently promoted,
- Codex adapter files exist and point to canonical `invoke` contracts,
- validation findings are recorded in a follow-up `VALIDATION.md` report.

Registry release remains blocked until L2/L3 plan, full, validate, examples, and registry gates pass.

## Current Verdict

`pass`.

The contract and template scaffolds are present, markdown links pass, runtime mirrors exist, and deterministic controls cover the implemented define, design, plan, handoff, and Refresh surfaces. Live Refresh stability evidence remains deferred and no `full`, `validate`, or registry-promotion claim is made.

## Next Actions

1. Add a live Refresh stability regime before using this repair as promotion evidence.
2. Implement and validate `full` mode.
3. Implement and validate `validate` mode.
4. Keep registry release blocked until the remaining lifecycle evidence passes.
