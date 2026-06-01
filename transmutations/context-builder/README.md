# Context Builder

Context Builder is a Transmutation sigil for creating a compact task-ready context pack from existing project evidence.

It selects only the source excerpts needed to execute a task, maps each excerpt to a concrete obligation, and rejects context that is merely interesting. The result is a smaller, more useful bundle for agents, reviewers, or implementation sessions.

For runtime delegation, Context Builder can emit a handoff pack. A handoff pack is a context pack prepared for a runtime adapter. It is stored as session evidence, emitted as Markdown plus JSON/index, and blocks when strict obligation coverage is not satisfied.

## Problem It Solves

Large repositories often bury the relevant facts under too much background material. Agents can waste time reading whole files, miss the exact obligation, or carry unrelated context into the task.

Context Builder solves this by using link-first retrieval, selector-level evidence, obligation coverage, and noise limits.

For runtime handoff, it also prevents weak runtime prompts by requiring every obligation to be covered or explicitly resolved before delegation.

## Use When

- a task needs a focused evidence pack before execution,
- requirements, architecture notes, code snippets, tests, and decisions are scattered,
- a later agent or reviewer should not reread the whole repository,
- the task has explicit obligations or completion criteria,
- context size must stay bounded.
- a runtime adapter needs selected context without doing broad repository exploration.

## Do Not Use When

- the task is simple enough to execute directly,
- no source material exists,
- the user wants a broad codebase map rather than task context,
- the work requires autonomous orchestration rather than bounded synthesis,
- selected excerpts cannot be linked to concrete obligations.
- a runtime handoff would need to proceed with uncovered, contradictory, stale, unsafe, missing write-scope, or missing validation obligations.

## Output

The sigil produces a context pack with:

- target task,
- obligation matrix,
- selected excerpts,
- selectors or anchors,
- obligation coverage,
- excluded candidates,
- unresolved gaps,
- optional machine-readable index.

When `--handoff runtime` is used, the sigil produces both:

- a Markdown handoff pack for human review and task-session reporting,
- a JSON or structured index for adapters and runtime handoff.

The canonical output shapes live in:

- `templates/runtime-handoff-pack.md`
- `templates/runtime-handoff-index.json`

Persisted handoff packs should live under a run/session evidence path. They are audit evidence for a specific execution, not canonical planning documents.

## Handoff Pack Schema

A handoff pack includes:

- identity: task/SWU, source task/work-pack, and run/session id when available,
- obligation matrix with `covered`, `resolved`, or `block` status,
- selected source paths, selectors, excerpts, and obligation refs,
- architecture guidance and related feature context,
- constraints, non-goals, write scope, done criteria, and validation surface,
- gaps, blockers, contradictions, and explicit resolutions,
- authority precedence,
- fallback exploration rule,
- provenance such as timestamp, source refs, and content hash or git SHA when available,
- Markdown and JSON/index output paths.

Strict coverage is required for runtime handoff: every obligation must be covered by selected evidence or explicitly resolved as not applicable/deferred. Otherwise Context Builder returns `BLOCK`.

## Why This Is A Transmutation

Context Builder transforms scattered project material into a bounded, evidence-linked artifact. It requires judgment, but the output is a concrete context package rather than a long-running orchestration loop.
