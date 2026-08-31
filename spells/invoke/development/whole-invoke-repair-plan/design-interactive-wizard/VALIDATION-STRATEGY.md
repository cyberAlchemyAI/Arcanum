# Interactive Design Wizard Validation Strategy

## Present Planning Validation

The current turn validates only this seven-file planning package:

1. Strict JSON parsing for every JSON artifact.
2. Exact changed-path inventory.
3. Trailing-whitespace and public-boundary scans.
4. Cross-file marker checks for the prerequisite, four layers, seven SWUs,
   transport-neutral chat bridge, immutable revisions, and authority ceiling.

No runtime, schema, CLI, generated-package, or product test is claimed by the
planning validation.

## W0 — Baseline And Design Admission

- Recompute current canonical and generated Invoke package inventories,
  digests, and sizes.
- Run the selective Invoke package preview without `--apply`; classify every
  delta by owner and lifecycle.
- Author the Wizard Design through current Design stages and require exact
  stage/admission PASS.
- Re-read the CLI catalog, Design contracts, and seed from that exact baseline.
- Convert the candidate into a Plan v2 authoring request and run `check`,
  `author`, `produce`, and `admit` only after the Design pair exists.

Failure: preserve all bytes and remain at `invoke design`.

## W1 — Vertical Proof

Positive fixture:

1. Start an absent explicit session root.
2. Declare two local evidence refs.
3. Classify one `included` and one `unavailable`.
4. Add one agent-authored question bound to coverage digests.
5. Render it in terminal and through the native-agent chat projection.
6. Answer with the expected revision.
7. terminate the process, resume, and inspect the frozen draft field.
8. Repeat in an independent root and compare canonical revision bytes.

Negative fixtures:

- hidden or default session roots;
- existing output roots;
- duplicate JSON keys or non-finite values;
- traversal, symlink escape, or out-of-bound evidence refs;
- question rendered before its revision is durable;
- stale expected revision;
- a second active question;
- answer for the wrong question or question revision;
- partial revision directory or invalid `HEAD.json` target;
- terminal/chat question or coverage identity mismatch.

## W2 — Evidence And State Integrity

Exercise every evidence classification and require exactly one classification
per denominator ref. Mutate boundary selectors, denominator membership,
classification, traceability, and source bytes independently.

Required properties:

- relevant drift marks dependent questions and decisions stale;
- unrelated drift leaves independent decisions current;
- included-but-unused evidence remains visible;
- source-to-question and source-to-draft mappings have complete reverse edges;
- unavailable thread or compacted context remains a blocking evidence gap when
  its evidence class is required;
- competing terminal/chat answers preserve conflict evidence and do not change
  the canonical decision;
- interrupted writes leave the previous revision readable and resumable;
- a failed command cannot advance `HEAD.json`.

Use table-driven state-transition tests plus mutation tests over every legal
and illegal edge.

## W3 — Design Authoring Bridge

- Validate exact decision-to-JSON-Pointer mappings.
- Require deterministic mechanical-gap ordering and explicit priority for
  agent-authored semantic questions.
- Block finalize on active/unanswered questions, stale/conflicted decisions,
  missing or unclassified required evidence, incomplete traceability, changed
  coverage digests, or incomplete request fields.
- Compare finalized request bytes across two runs.
- Invoke the installed `tools/arcanum invoke design check <stage>` command and
  require PASS for a complete fixture.
- Confirm that finalize never calls `produce`, `admit`, `status`, owner-request,
  network, telemetry append, publication, or execution paths.

## W4 — Compatibility And Package Closure

- Run focused wizard and shared CLI suites.
- Run existing Define, Design, Plan, capability-status, and routing regressions.
- Generate Invoke packages in isolated targets.
- Review an exact dependency-closed allowlist before any apply.
- Run the full canary from each canonical/Codex/Claude surface twice.
- Require byte-equal session revisions, finalized request, and CLI results.
- Scan exact public targets for private-boundary tokens and strict JSON/Python
  syntax.
- Run scoped `git diff --check` including untracked create targets.

## Exit Codes And Diagnostics

- `0`: evaluated PASS; requested transition committed as one complete revision.
- `1`: evaluated BLOCK; structured diagnostics emitted and canonical state not
  advanced, except a separately identified immutable conflict-evidence record.
- `2`: invocation/interface failure; no revision or conflict record written.

Every diagnostic names a stable code, record or JSON Pointer, causal blockers,
and repair route.

## Evidence Ceiling

Passing these future checks would prove deterministic wizard behavior and
compatibility only. It would not prove architectural truth, owner approval,
Design admission beyond the exact checked bundle, Plan execution, publication,
deployment, or external effect.
