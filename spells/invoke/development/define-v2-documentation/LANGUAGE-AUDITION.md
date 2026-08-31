# Invoke Define v2 Language Audition

- Transport: `agent_operational_reference`
- Transport status: `candidate`
- Intent state: `frozen`
- Human gate: `pending`
- Scope: three representative public-guide moments only
- Machine validation: `not_evaluated`; this audition is prose, not a source or
  compiler receipt

## Moment 1 — Opening: What Invoke Define Does

Invoke Define turns a bounded development intent into one source-bound,
candidate definition package. You author a single
`invoke.define-source.v2` document. The compiler validates that source and
generates the complete bundle, including `SPEC.md`, `DEFINITIONS.json`, the two
Markdown views, supporting evidence files, and the stage receipt.

The distinction matters: `DEFINITIONS.json` is an output, not the document you
fill in. The stage receipt is evidence that the producer completed the declared
transformation; it is not the definition artifact. Start with the source,
inspect the generated definitions, and read the receipt last.

```text
intent + exact repository evidence
                |
                v
       DEFINE-SOURCE-v2.json      <- you author this
                |
                v
     Invoke Define v2 compiler
                |
                +--> DEFINITIONS.json            <- machine artifact
                +--> DEFINITIONS.md / GLOSSARY.md <- derived views
                +--> SPEC.md + evidence files
                `--> stage receipt                <- production evidence
```

Everything emitted by this producer remains candidate-only. A passing receipt
can establish that the artifact was authored by the installed v2 producer. It
does not promote a definition, release a registry, authorize mutation, or prove
that the definition is true.

## Moment 2 — The Ownership Distinction

A trustworthy Define source contains several kinds of values, but you do not
own all of them in the same way.

**Author semantic decisions.** Choose the bounded objective, declarations,
terms, voices, boundaries, consumers, relations, warnings, and next route from
the available evidence. These fields express what you mean, so a schema cannot
choose them for you.

**Compute evidence bindings.** Repository-relative paths, SHA-256 digests, byte
sizes, and selector bounds describe bytes that already exist. Observe them with
tools. Never type a plausible value or preserve an old value after the source
changes.

**Copy contract constants exactly.** The v2 schema version, selected profile,
candidate status, output filenames, and no-effect transport policy are fixed by
the producer contract. They are not customization points.

**Let the compiler derive outputs.** Output hashes, `DEFINITIONS.json`, both
Markdown views, producer identity, receipt ID, receipt digest, and
`authority_effect` belong to the compiler. If they appear as authored claims in
your source, the source is wrong even when the values happen to match.

This gives a practical rule: exercise judgment over meaning, use tools for
evidence, copy constants from the active contract, and never impersonate the
producer.

## Moment 3 — The Five Voices

The five voices are five responsibilities for one meaning. They are not five
opportunities to improvise related descriptions.

Suppose the term is **staged candidate**.

- **Normative voice — what the term means.** “A staged candidate is validated
  proposed content awaiting an explicit accept or discard decision.”
- **Formal voice — the precise representation, when one exists.**
  “`status = staged` and `accepted_revision_id` is unchanged.” Use `null` when
  the evidence does not support a stable formalization.
- **Operational voice — how a consumer recognizes or uses it.** “Treat content
  as a staged candidate only after candidate validation passes and before an
  acceptance receipt advances the head.” Use `null` only when no responsible
  operational test can be stated.
- **Plain-language voice — the same meaning without specialist machinery.**
  “A proposed change that has passed its checks but has not been accepted yet.”
- **Domain-context voice — where this meaning applies here.** “In the UI
  prototyping studio, a staged candidate may be previewed or discarded, but it
  does not replace the current accepted revision.”

Review the five voices together. If one changes the status boundary, adds a new
permission, or refers to a different object, repair the semantic disagreement
before compilation. A polished sentence cannot compensate for five voices that
do not define the same thing.

## Human Gate

Review these three moments for:

1. whether the opening makes the source/output/receipt distinction immediate;
2. whether the ownership categories are precise without feeling ceremonial;
3. whether the five-voice example makes the responsibilities genuinely
   different while preserving one meaning; and
4. whether the tone should be more concise, more formal, or more conversational.

Full public-guide drafting remains blocked until this language is approved or
revised.
