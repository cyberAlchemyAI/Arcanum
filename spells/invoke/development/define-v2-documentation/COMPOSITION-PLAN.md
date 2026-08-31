# Invoke Define v2 Authoring Guide Composition Plan

## Transport Contract

- Transport ID: `agent_operational_reference`
- Status: `candidate`
- Primary job: help an agent construct a trustworthy v2 source on the first
  bounded attempt.
- Secondary job: give a human reviewer a compact semantic and authority audit
  surface.
- Expected length: 2,500-4,000 words plus one complete JSON example.
- Introduction policy: establish the artifact transformation before naming
  nested fields.
- Evidence policy: every mandatory instruction must trace to the schema,
  compiler, semantic validator, or an explicitly marked authoring convention.
- Ending policy: finish with the validation sequence and exact claim ceiling,
  not a summary slogan.
- CTA policy: validate and compile locally; no promotion CTA.
- Interaction prompts: none; discriminative prompt safety is not applicable.

## Candidate Tournament

### Candidate A: Schema-Order Reference

Follow the JSON Schema property order and explain every field in sequence.

- Resonance: precise but dry.
- Relevance: complete lookup surface.
- Trajectory: weak; the reader meets details before understanding ownership.
- Cost: low authoring cost, high cognitive load.
- Disposition: rejected as the primary structure; retain its field inventory as
  a later reference section.

### Candidate B: Tutorial-First Walkthrough

Build one example from top to bottom and explain each decision as it appears.

- Resonance: approachable.
- Relevance: strong for a first run.
- Trajectory: clear.
- Cost: field lookup and edge-case discovery become difficult; example choices
  can look normative when they are only illustrative.
- Disposition: retained as the quickstart and annotated example, not the whole
  document.

### Candidate C: Ownership-First Progressive Reference

Begin with the source/output distinction, teach the bounded authoring workflow,
then provide decision-oriented field guidance, a complete example, and a
schema-order lookup section.

- Resonance: confident and practical.
- Relevance: addresses the observed category error directly.
- Trajectory: need before name; workflow before exhaustive detail.
- Cost: more editorial work, but better first-run and later-reference utility.
- Disposition: selected.

## Pareto Selection

Candidate C is non-dominated across first-run clarity, reference completeness,
authority safety, and maintenance cost. It incorporates Candidate B as a
quickstart and Candidate A as a compact lookup appendix without letting either
control the whole reading sequence.

## Narrative Anchor

**Author one trustworthy source; let the compiler earn every output.**

This sentence guides the sequence but should appear at most once in the public
guide. The documentation must demonstrate the distinction rather than repeat
the slogan.

## Public Guide Architecture

### Part 1 — What Invoke Define Does

One definition, one transformation diagram, and one explicit authority
boundary. Establish that the source is input and `DEFINITIONS.json` is output.

### Part 2 — Know What You Own

Classify the complete surface:

| Class | Responsibility | Examples |
| --- | --- | --- |
| Authored | semantic judgment supported by evidence | objective, declarations, terms, voices, boundaries |
| Computed | exact observations from repository bytes | SHA-256, size, selector bounds |
| Fixed | profile and producer contract constants | schema version, candidate status, output names |
| Derived | compiler-owned output | `DEFINITIONS.json`, Markdown views, receipt digests |
| Prohibited | values the source must never assert | active status, authority effect, receipt metadata |

### Part 3 — Sixty-Second Workflow

1. Select the bounded target and exact discovery evidence.
2. Identify only the terms needed to make that target unambiguous.
3. Write declarations and definition semantics.
4. Compute exact evidence bindings.
5. Complete fixed governance classifications without inventing authority.
6. Validate the source.
7. Compile atomically and inspect the machine artifact before the receipt.

### Part 4 — Build the Source

Explain top-level fields in decision order rather than raw schema order:

1. target and discovery;
2. declarations;
3. registry ownership and visibility;
4. definitions;
5. layering, Distill, and identity denominator;
6. fixed output and transport contracts;
7. next route.

Each field group must state:

- what decision it records;
- where the value comes from;
- how to know the value is sufficient;
- what not to put there;
- the validator that catches mechanical errors.

### Part 5 — Write One Definition Well

Use one aligned term across every subsection. Cover:

- stable identity, term, aliases, and candidate status;
- source-kind classification;
- five voices;
- notation and boundary;
- exact source references and selector choice;
- primary consumers and in-bundle relations;
- warnings, challenge contract, promotion boundary, drift route, version, and
  structural schema.

The five voices must describe the same meaning from different responsibilities;
they must not become five loosely related definitions.

### Part 6 — Exact Evidence Cookbook

Provide commands and selection rules for:

- repository-relative paths;
- SHA-256 and byte size;
- headings and anchors;
- line spans;
- symbols;
- JSON pointers;
- YAML paths;
- public/private source compatibility.

The commands compute evidence. The guide must never show placeholder hashes in
a purportedly compilable example.

### Part 7 — Complete Reference Example

Pair a stable discovery fixture with one complete v2 source and its generated
bundle inventory. Annotate decisions outside the JSON so the example remains a
real compiler input.

### Part 8 — Diagnose Failure

Map common errors to the responsible repair:

- source schema invalid -> repair authored shape or fixed constant;
- stale SHA/size -> recompute against intended bytes;
- selector unresolved -> select an exact locator that exists;
- term/alias collision -> resolve semantic identity;
- unresolved/self relation -> repair the in-bundle graph;
- generated view drift -> discard output and rerun the compiler;
- v1 receipt -> historical/read-only, not a new PASS;
- missing identity-denominator evidence -> stop downstream activation.

### Part 9 — Read the Result Correctly

Inspect `DEFINITIONS.json` first, human views second, and the receipt last. State
exactly what `artifact_authored=pass` proves and what remains false or
separately owned.

### Appendix — Complete Field Lookup

Provide a compact schema-order table with allowed values and cross-field
conditions. Link to the JSON Schemas as the final shape authority.

## Surface Map

| Surface | Owner | Content |
| --- | --- | --- |
| Public operational guide | Invoke | instructions, examples, commands, authority boundaries |
| Machine schemas | Invoke | allowed shape and cross-field constraints |
| Compiler and validator | Invoke | mechanical derivation and executable semantics |
| Whisper development pack | Whisper-assisted Invoke development | substrate, candidate comparison, language audition, editorial validation |
| Generated Codex/Claude packages | mechanical sync | exact canonical guide and support files |

Whisper does not own machine semantics. If editorial clarity conflicts with the
schema or validator, the executable contract wins and the prose must be
repaired.

## Language Audition

Before drafting the public guide, audition exactly three representative
moments:

1. opening definition and source-to-output transformation;
2. authored/computed/fixed/derived/prohibited distinction;
3. five-voice explanation with aligned examples.

Approval applies only to voice, sequence, and explanatory clarity. It does not
validate the schema or promote the candidate transport.

## Validation Checklist For The Later Draft

### Editorial

- The opening cannot be reused for an unrelated tool by replacing nouns.
- Specialized names follow the practical distinction they solve.
- Each section changes what the reader can do next.
- Tables serve lookup; prose explains load-bearing relationships.
- No repeated thesis, schema recital, or receipt-first framing.
- The ending produces an actionable validation sequence.

### Semantic

- No prose extends accepted enums or relaxes required fields.
- Every authoring convention is labeled as a convention.
- Every definition remains candidate-only.
- The same concept is preserved across all five voices.
- Public/private and source-evidence rules match the validator.
- No generated view is described as an authority source.

### Executable

- The complete example validates against `define-source-v2.schema.json`.
- The example compiles to the exact 11-file bundle.
- The generated definition artifact passes semantic and view-parity validation.
- Stale evidence, alias collision, active status, authored receipt metadata,
  and output-view drift all block without output publication.
- v1 compatibility tests remain green.
- Canonical, Codex, and Claude documented surfaces are byte-equivalent after
  selective sync.

## Draft Gate

Full public drafting is blocked until the operator approves or revises the
three excerpts in `LANGUAGE-AUDITION.md`.
