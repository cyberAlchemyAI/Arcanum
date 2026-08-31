# Interactive Design Wizard Implementation Layering

## Target

Add a durable Design interview layer without replacing the existing stateless
Design producer.

The prerequisite Wizard Design and package baseline must be admitted before L0
implementation begins. That prerequisite is a lifecycle gate, not an
implementation layer.

## L0 — One durable question across terminal, chat, and restart

**After this layer, we know whether one evidence-backed Design question can
survive interruption and remain identical in both user surfaces.**

- Minimum working unit: declare a two-ref evidence boundary, compile its
  classifications, validate one agent-authored question, persist one immutable
  revision, render it in terminal and chat, accept one revision-guarded answer,
  restart, resume, and expose one frozen draft field.
- Included: minimum schemas, explicit session root, immutable revision plus
  atomic `HEAD.json`, one active question, one answer, one draft mapping, focused
  integration fixture.
- Deferred: broad evidence discovery, multiple dependent questions, direct
  chat transport, complete Design request, generated packages, retention tools.
- Visible outcome: the operator can leave and return without losing the active
  question or its evidence.
- Risk reduced: silent question loss, surface divergence, stale answer overwrite.
- Main cost: cross-process state and parity fixture.
- Exit evidence: two-run byte equality, restart/resume PASS, stale-revision
  BLOCK, identical question/coverage identities in both renderers.
- Promotion: continue only if the vertical proof closes without hidden state.

## L1 — Complete evidence and state integrity

**After this layer, we know whether selected historical evidence remains
accounted for as sources change and terminal/chat submissions race.**

- Minimum working unit: total denominator classifications, bidirectional
  traceability, staleness propagation, conflict preservation, and interrupted
  transaction recovery.
- Included: all five evidence classifications, required evidence classes,
  unused included evidence, earliest dependency reopening, conflicting-answer
  record, path and symlink confinement, state-machine mutation tests.
- Deferred: full Design authoring, package sync, automatic cleanup.
- Visible outcome: status explains what is included, missing, stale, conflicting,
  or still blocking.
- Risk reduced: partial-evidence claims, silent reuse of stale decisions,
  concurrent state corruption.
- Main cost: dependency graph and negative test matrix.
- Exit evidence: every denominator ref has one classification; every backed
  question and draft field has reverse traces; all transition mutations fail
  closed.
- Non-regression: L0 terminal/chat identity and restart behavior remain true.
- Promotion: continue only when relevant drift invalidates exactly the affected
  decisions.

## L2 — Existing Design authoring integration

**After this layer, we know whether the interview can create a complete Design
authoring request without becoming a second Design producer.**

- Minimum working unit: validated question queue, decision-to-JSON-Pointer
  mapping, finalize gates, and existing Design `check` invocation.
- Included: deterministic mechanical-gap ordering, agent-authored semantic
  questions, complete request validation, explicit optional call to `author`.
- Deferred: `produce`, `admit`, `status`, direct approval capture, runtime
  execution, direct chat transport.
- Visible outcome: a complete, reviewable draft request that the existing CLI
  accepts.
- Risk reduced: duplicate producer logic, hidden semantic inference, incomplete
  handoff.
- Main cost: mapping completeness and compatibility tests across Design stages.
- Exit evidence: complete fixture passes existing `check`; each missing, stale,
  or conflicted fixture blocks before output.
- Non-regression: L0/L1 state and evidence guarantees remain true.
- Promotion: continue only when the existing producer remains the sole machine
  authoring authority.

## L3 — Compatibility and reusable activation

**After this layer, we know whether the approved wizard is portable across the
canonical, Codex, and Claude Invoke packages without carrying unrelated bytes.**

- Minimum working unit: concrete documentation, isolated generated-package
  canaries, exact selective synchronization, and parity verification.
- Included: operator guide, native-agent chat guidance, canonical regressions,
  exact generated allowlist, two-run canary.
- Deferred: direct app integration, shared service, automatic retention purge,
  publication, deployment.
- Visible outcome: the same local workflow is available through each admitted
  package surface.
- Risk reduced: generated drift, package-only breakage, owner-byte overwrite.
- Main cost: isolated generation and broad compatibility validation.
- Exit evidence: exact allowlist parity and byte-identical canary results with
  no unrelated delta.
- Non-regression: all L0-L2 guarantees and the stateless non-wizard CLI remain
  unchanged.
- Promotion: later direct transport work requires a separate Design and cannot
  be inferred from L3.

## Recommended Start

After the Wizard Design admission prerequisite, implement L0 only. It is the
smallest slice that proves the actual user benefit; a storage-only or
terminal-only prototype would not.
