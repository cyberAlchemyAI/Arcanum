---
stage: 3
name: Interrogation (refine-review)
capability: interrogation
mode: refine-review
status: flag
verdict: proceed-with-repairs
dispatch_id: refine-coherence-metric-20260608
---

# Interrogation refine-review

## Q1. Is DCI gameable by emitting fewer gaps? (Goodhart)

Yes — the central risk. A sigil that reports `workflow_gaps: []` and `quality_bar: pass`
scores 100 regardless of reality. **Repair:** DCI cannot rest on self-reported gaps alone;
it must cross-check against *objective* signals (`execution.status`, `output_contract_drift`,
and downstream reopen/retry of the same target) that are harder to suppress, and
workflow-reflect must flag *suspiciously clean* sigils (zero variance) as a separate signal.

## Q2. Does DCI conflate unit difficulty with decomposition quality?

Risk: a hard unit fails more regardless of coherence. **Repair:** normalize per obligation
(files_changed / validation count), and read DCI as a *relative* trend per sigil over time,
not an absolute cross-sigil ranking.

## Q3. Is the SCU redefinition just renaming, or a real correction?

Real correction: it changes an **unfalsifiable** claim ("minimum of entropy") into a
**measurable** one ("minimum of residue density, located post-hoc"). But it must not
overclaim — DCI measures the *trace*, so the redefinition must keep "proxy for the
unreachable entropy," not "equals entropy." **Repair:** carry the residue-not-entropy
boundary into the redline verbatim.

## Q4. Does the redefinition lose the philosophical horizon?

The guardian role exists to prevent that. The operational correction lives in §"Entropy, SCU,
And PCRA Translation" and the formal model; the universal-physics §600+ can stay as a
*horizon* with the honesty boundary intact. **Repair:** redline scopes changes to named
sections; horizon prose is annotated, not deleted.

## Verdict

**flag — proceed with four repairs** (objective-signal anti-gaming; per-obligation
normalization; keep "proxy not equals"; scope the redline to named sections). Carried into
distill-select and design.
