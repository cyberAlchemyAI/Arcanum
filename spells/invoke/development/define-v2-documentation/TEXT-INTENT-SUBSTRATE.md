# Invoke Define v2 Documentation Intent

## Intent State

- State: `frozen`
- Transport: `agent_operational_reference`
- Transport proof status: `candidate`
- Human language gate: `pending`
- Target artifact: `spells/invoke/define-v2-authoring.md`
- Machine authority sources:
  - `spells/invoke/schemas/define-source-v2.schema.json`
  - `spells/invoke/schemas/definitions.schema.json`
  - `spells/invoke/scripts/compile_define_source_v2.py`
  - `spells/invoke/scripts/validate_definitions_artifact.py`

The transport is candidate because Whisper does not yet have a proven reusable
agent-operational-reference profile. Whisper may improve explanation and
sequence, but only Invoke schemas, compiler behavior, and executable tests can
establish machine-contract correctness.

## Author Intent

Create a polished operational guide that enables an agent to author one correct
`invoke.define-source.v2` input without confusing it with the generated
`DEFINITIONS.json`, the generated Markdown views, or the stage receipt.

The guide begins with the meaning and boundary of Invoke Define. It then teaches
the authoring decision process before presenting the complete schema surface.

## Target Public

### Primary

An agent that has repository evidence and a Define objective but has not yet
constructed the v2 machine source.

### Secondary

A human reviewer checking whether the source meaning, evidence bindings, and
candidate-only authority boundary are trustworthy.

## Reader State

The reader may know JSON Schema and still make one of four category errors:

1. author the desired `DEFINITIONS.json` directly;
2. treat the stage receipt as the main result;
3. guess mechanically verifiable evidence fields;
4. fill every string without understanding the semantic responsibility of the
   five voices, boundaries, relations, or promotion route.

The documentation succeeds when those category errors are difficult to make.

## Smallest Coherent Unit Cores

### Resonance Core

- Tone: precise, calm, operational, candid.
- Voice: a senior maintainer guiding another capable agent.
- Style register: concise technical prose supported by examples and compact
  reference tables.
- Desired residue: “I know what I am responsible for authoring, what must be
  computed, and what the compiler owns.”
- Forbidden feels: bureaucratic ceremony, schema recital, vague inspiration,
  or false certainty.

### Relevance Core

- Domain: governed semantic authoring for Invoke Define.
- Immediate problem: the schema validates shape but does not teach judgment.
- Authority mode: explanatory only; no prose may weaken or extend the machine
  contract.
- Assumptions: repository root and exact evidence files are available.
- Objections to answer:
  - “Why not write `DEFINITIONS.json` directly?”
  - “Which fields are authored versus computed?”
  - “How do the five voices differ?”
  - “What makes a source reference exact?”
  - “What does a passing receipt actually authorize?”

### Trajectory Core

- Entry: define Invoke Define through the artifact transformation it owns.
- Tension: distinguish semantic judgment from mechanical evidence and derived
  output.
- Movement: mental model -> quickstart -> field decisions -> complete example
  -> validation -> diagnostics -> authority ceiling.
- Ending: the agent can construct and compile one valid source while knowing
  that the result remains candidate-only.
- Call to action: author and validate the source, then inspect the generated
  machine artifact before handoff.

## Non-Negotiable Meaning

- The agent authors `invoke.define-source.v2`.
- The compiler generates `DEFINITIONS.json`, `DEFINITIONS.md`, `GLOSSARY.md`,
  and the stage receipt.
- `DEFINITIONS.json` is the machine definition artifact.
- The Markdown files are deterministic views, not independent authority.
- Exact paths, SHA-256 values, sizes, and selectors are observed or computed;
  they are never invented.
- Every newly emitted definition remains `candidate`.
- A passing v2 receipt opens only `artifact_authored`.
- Define grants no promotion, registry release, mutation-runtime, publication,
  deployment, or production authority.
- A documentation rule that cannot be derived from a schema, compiler,
  validator, or explicit owner decision must be recorded as a contract gap,
  not smoothed over in prose.

## Surface Boundary

### Public Guide Surface

- operational explanation;
- exact commands;
- field decision rules;
- positive and negative examples;
- error-to-remediation mapping;
- explicit authority ceiling.

### Authoring-Only Surface

- Whisper substrate and candidate comparison;
- editorial rationale;
- language-audition scoring;
- unresolved transport-proof status.

Authoring-only language must not be copied into the generated
`DEFINITIONS.json` example unless it independently satisfies the definition
schema and source-evidence contract.

## Success Signals

- A new agent can explain the source-to-output flow after the opening section.
- Every source field is classified as authored, computed, fixed, derived, or
  prohibited.
- The five voices have distinct responsibilities and aligned examples.
- One stable complete example validates and compiles atomically.
- Negative examples fail for the intended reason without output publication.
- Canonical and generated Invoke packages remain exact for the documented
  surface.
- Human review approves the opening, artifact distinction, and voice guidance
  before the full guide is drafted.

## Recomposition Proof

The smallest coherent documentation unit is the chain:

`meaning -> ownership -> authoring decisions -> exact evidence -> compilation -> authority ceiling`

Removing meaning recreates the source/output confusion. Removing ownership
invites authored hashes and receipts. Removing decision guidance reduces the
guide to a schema listing. Removing compilation and the authority ceiling makes
the workflow operationally incomplete. The complete chain therefore
recomposes into the intended guide without requiring Design, Plan, or execution
documentation.
