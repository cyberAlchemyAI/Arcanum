# Anti-Patterns

## Owner Collapse

Bad: `verification-weaver` claims to derive tests, run browser checks, execute
experiments, map architecture, or adjudicate research claims.

Good: route to the owner lane, preserve owner status, and record gaps or
residue in the parent receipt.

## Promotion Laundering

Bad: a parent receipt marks a draft, seed, dry-run, or blocked owner output as
promoted.

Good: parent receipts use only `promotion_action: none` or
`promotion_action: candidate-request`.

## Fixture Contamination

Bad: public fixtures copy private project examples, credentials, local machine
paths, or generated reports.

Good: use synthetic fixtures that model structure, not private content.

## Oracle Guessing

Bad: a target passes because the router inferred intent from file names or
natural-language confidence alone.

Good: require a deterministic oracle, fixture runner, proof checker, browser
evidence, human review, research run data, or explicit gap.

## UX Over-Mechanization

Bad: a mechanically passing UI receipt is treated as UX-complete when human
comprehension risk is still unresolved.

Good: flag the residue and route it to `ux-evidence-validator`.

## Architecture Folder Guessing

Bad: architecture alignment is inferred from folders alone.

Good: require source-backed evidence or an explicit architecture gap.

## Generated Evidence Drift

Bad: generated reports become canonical source material.

Good: generated reports are run evidence only; durable fixtures and contracts
remain the source authority.
