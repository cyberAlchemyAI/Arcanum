# Craft Teaching Total Refresh Review Attacks

**Dispatch ID:** `2026-07-10-craft-teaching-total-refresh-review`  
**Review evidence boundary:** `CRAFT-INITIAL-DEFINITION.md`; `CRAFT-CODING-CLASS-SLIDE-SCHEMA.md`; `CRAFT-CODING-CLASS-SLIDE-SCHEMA.yml`; `CRAFT-CODING-CLASS-PRESENTATION.html`; and `research.md`, `findings.md`, and the three Markdown essays in `craft-storytelling-essay-research-2026-07-09/`, plus the browser observations recorded inside the Shannon archive.  
**Provenance note:** The named identities below are analytical lenses, not external empirical citations. These attack returns are dispatch-local analyses of the bounded corpus and must not be represented as external research.



===== Halford, Graeme ARCHIVE =====
# INITIAL POSITION — Halford, Graeme

**Lens:** methodology / empirical beginner cognitive walkthrough  
**Verdict:** The corpus has a coherent teaching story, but it repeatedly mistakes authored sequencing for demonstrated learner sequencing. The learner is often shown the label and explanation before making the decision that supposedly earns them.

## Findings By Artifact

### `CRAFT-INITIAL-DEFINITION.md`

- **MAJOR — The source front-loads an unusable vocabulary stack.** The executive definition introduces “schema,” “data,” “translation relation,” “functor-like process,” and “residue” within ten lines, followed by SCU, PCRA, entropy, reflection tower, constitutions, and axioms. A beginner cannot yet distinguish these abstractions through action.
  **Correction:** Extract a beginner substrate containing only target, facts, chosen shape, built thing, check, and mismatch; promote formal terms after worked decisions.

- **MAJOR — The teaching claim outruns empirical evidence.** “Craft improves agentic artifact creation” is presented as an operational claim, while the document supplies conceptual grounding but no novice trial, comprehension measure, or transfer result.
  **Correction:** Label improvement as a hypothesis until beginner testing demonstrates recall, application, and transfer.

### `CRAFT-CODING-CLASS-SLIDE-SCHEMA.md`

- **MAJOR — “One new term per slide” is not actually enforced.** S14 names `Craft` while displaying “schema/data layer,” seven lifecycle verbs, “artifact,” and “residue”; its check demands mapping “intention, schema, artifact, residue, and next layer.”
  **Correction:** Split S14 into learner reconstruction, plain-language rule, and optional formal vocabulary recap.

- **MAJOR — S08 breaks the promised transfer order.** Its visual includes a “broken login” before S11 supposedly transfers the established table model into software.
  **Correction:** Keep S08 entirely within the table witness and introduce login only after learners abstract the table pattern.

- **MINOR — Several checks test parroting rather than understanding.** “Students can say that the schema narrows...” can pass through repetition without choosing or rejecting a design.
  **Correction:** Require learners to classify two candidate tables and explain why one violates the chosen shape.

### `CRAFT-CODING-CLASS-SLIDE-SCHEMA.yml`

- **MAJOR — The machine schema reproduces the overload while declaring a pass.** `draft_status: pass` and validation claiming the one-term constraint conflict with S14’s multi-term concept and check.
  **Correction:** Make validation count all learner-visible undeclared terms, not only the `new_term` field.

- **MINOR — Prompts contain the expected answer space.** S11 says “Break login into fields, button, validation, error, session, redirect,” converting a learner decision into list completion.
  **Correction:** Ask learners to inspect a failing login scenario before revealing responsibility categories.

### `CRAFT-CODING-CLASS-PRESENTATION.html`

- **MAJOR — Concrete-before-term is simultaneous, not sequential.** `renderSlides()` renders the term, title, question, concept, and visual together; only S01 has `revealMax`. The learner sees `schema`, `SCU`, and `entropy` before demonstrating the need for them.
  **Correction:** Add staged reveal states: witness first, learner choice second, term last.

- **MAJOR — Keyboard use destroys the only real pause.** The reveal stage handles Space, but the bubbling window handler also maps Space to `goToSlide(activeIndex + 1)`. A keyboard learner can reveal and leave S01 in one action.
  **Correction:** Stop propagation when Space activates a reveal, and advance only after reveal steps are exhausted.

- **MINOR — S01 leaks the instructional mechanism.** The projected text says “Do not answer yet” and “reveal the structure,” exposing speaker direction to learners.
  **Correction:** Project only the object and question; keep timing and reveal instructions in notes.

### `research.md`

- **MAJOR — Cognitive assertions are presented as findings without learner evidence.** “The presentation will break” and “15-second silent list is load-bearing” derive from expert reasoning, not observation, recall testing, or novice walkthrough data.
  **Correction:** Mark these as hypotheses and define a small test: independent response count, explanation quality, and delayed transfer.

- **MINOR — The proposed sequence is treated as proof of comprehension.** “Earn” repeatedly means “placed after,” with no evidence that learners formed the concept themselves.
  **Correction:** Define earning as a successful learner decision before terminology appears.

### `findings.md`

- **MAJOR — Its validation checklist forces every essay to carry the whole framework.** Each essay must explain schema/data translation, residue, SCU, craft layers, and recomposition, contradicting the three-essay division of cognitive labor.
  **Correction:** Give each essay one primary concept and require only the prerequisites needed for that concept.

- **MAJOR — The checklist is already falsified by the drafts.** It requires each essay to have a “learner scene, pause, visible object, and buildable witness,” but Essay 2 answers its room question immediately and Essay 3 labels a pause only after explaining the theory.
  **Correction:** Validate drafts against literal paragraph order and record failures instead of intention-level passes.

### Essay 1: `The Table Is Not The Project`

- **MAJOR — The essay names the framework before the experience earns it.** “This is the schema/data hinge” is followed immediately by schema, artifact, Craft, structure, comparison, and mismatch before the plan is executed.
  **Correction:** Complete one build-and-wobble witness before naming schema, artifact, or residue.

- **MINOR — The learner makes no consequential choice.** The narrator supplies the desk target, research questions, plan, checks, and residue routes.
  **Correction:** Present two plausible desk choices and pause for the learner to choose using discovered constraints.

### Essay 2: `When One Step Becomes Its Own Build`

- **MAJOR — The pause is fake.** “Ask the room what changed” is immediately followed by the authored answer: the step needs everything the whole table needed.
  **Correction:** Supply competing interpretations and delay the answer until the learner identifies which hidden obligations require a separate build.

- **MINOR — Lifecycle repetition becomes recital.** Define, research, design, plan, build, validate, reflect are replayed as seven explanatory blocks without a learner-controlled branch.
  **Correction:** Walk one failed leg decision through the minimum necessary loop and let its failure trigger the next reveal.

### Essay 3: `Why Vibe Coding Drifts`

- **MAJOR — The causal explanation precedes the supposed discovery pause.** Schema, artifact, validation, and residue are defined at lines 35–43; only afterward does the “bad dashboard” appear and “This is the pause.”
  **Correction:** Show two plausible but wrong dashboards first, ask why neither satisfies the request, then name ambiguity and schema.

- **MAJOR — The correction is delivered, not discovered.** The student-dashboard specification and validation questions are supplied wholesale; the beginner never chooses user, data, action, or success condition.
  **Correction:** Reveal those dimensions one at a time through learner decisions and show how each eliminates a concrete wrong output.

## Reconstructed Learning Sequence

1. Show only a plain table; learner lists missing build needs.
2. Show two incompatible table uses; learner chooses which target is intended. Reveal **define**.
3. Introduce a room constraint that invalidates one design. Reveal **research**.
4. Compare two sketches against the chosen constraints. Reveal **chosen shape**, then **schema**.
5. Ask which physical action can happen next and what proves completion. Reveal **plan**.
6. Show the built table without judgment. Reveal **artifact**.
7. Let the learner choose checks derived from the earlier sketch. Reveal **validate**.
8. Show one failed check; learner chooses repair, research, or redesign. Reveal **residue**.
9. Show an ornate leg and ask whether “make the legs” remains executable.
10. Learner identifies its independent target, tools, checks, and return fit. Reveal **craft layer**.
11. Transfer to two generated dashboards; learner identifies missing user, data, action, and done condition.
12. Compare whole app, assignment panel, and blue button. Reveal **smallest coherent unit**.
13. Only after multiple plausible outputs are visible, optionally name **entropy**.
14. Learner reconstructs the method in plain language; formal Craft wording becomes optional recap.

## Explicit Zero-Finding Defenses

No artifact survives the full lens with zero findings.

Two components do survive narrower attacks:

- **Essay 2’s recomposition boundary survives:** “The layer only earns its independence if its result can recompose into the whole” successfully blocks naive endless splitting.
- **The deck’s table-to-software macro-order survives:** placing the main software transfer after the ornate-leg recursion is cognitively defensible, despite the premature login example in S08.

# FINAL POSITION — Halford, Graeme

**Lens:** methodology / empirical beginner cognitive walkthrough

The confrontation strengthens the central finding: the corpus largely confuses a well-authored explanation with a learner-earned model. Alexander identifies the missing causal continuity, Spivak specifies the proof required before recursion is justified, and Shannon shows that the presentation machinery cannot currently enact the pedagogy its schemas claim.

The clean-room replacement should therefore teach through observable decisions and consequences, not merely improved sequencing.

## Revised And Upheld Findings

- **MAJOR — Authored order is not learner-earned order.** Upheld. A term appearing after an example in the slide list does not mean the learner experienced the need for it. S02–S14 generally render witness, label, explanation, and expected conclusion simultaneously. Each abstraction needs an interaction sequence: witness, learner choice, visible consequence, then term.

- **MAJOR — The deck lacks a persistent causal history.** Alexander’s claim is accepted and strengthens mine. The simple table, completed artifact, wobble, ornate table, and software examples are adjacent exhibits rather than states of one developing problem. The learner therefore cannot attribute later changes to earlier choices.

- **MAJOR — The interaction schema cannot represent the teaching rule.** Shannon is correct. Fields such as `visual`, `new_term`, and `concept_move` describe slide contents, but not ordered states, allowed inputs, consequences, or reveal conditions. The YAML’s pass declaration is unsupported because the represented structure cannot prove example-before-term behavior.

- **MAJOR — S14 is an assessment pile-up disguised as recomposition.** Upheld. It simultaneously demands Craft, intention, schema, artifact, residue, layer, and the full lifecycle. That tests short-term vocabulary management rather than whether the learner can diagnose a build.

- **MAJOR — The lower-layer rule is under-specified.** Spivak is correct that complexity alone cannot justify a split. “Needs its own plan, tools, validation, and way back” is suggestive but insufficient. The learner also needs evidence that local repair cannot responsibly close the mismatch, that the proposed split reduces unresolved obligations, and that both local and upper checks pass.

- **MAJOR — The final model lacks return and stopping behavior.** A loop ending at “Reflect on residue” can imply endless iteration. The learner needs to see either repair within the current layer, descend into a lower layer and return, or stop when named checks pass with acceptable remaining mismatch.

- **MAJOR — The rendered controls violate the only genuine pause.** Upheld and independently confirmed by Shannon’s browser evidence. Space on focused S01 reveals and navigates; final activation resets the reveal; S02–S14 expose their contents simultaneously. These are behavioral failures, not editorial imperfections.

- **MAJOR — The essays reproduce explanation before discovery.** Essay 1 names the schema/data hinge before the build produces a mismatch. Essay 2 immediately answers “what changed?” Essay 3 defines schema, artifact, validation, and residue before showing the bad dashboard it calls “the pause.”

- **MAJOR — Qualitative constructs are presented as if operationalized.** “Entropy,” “SCU,” “acceptable residue,” and “reduces residue” lack observable classroom proxies. Without proxies, a learner cannot tell whether a unit is better or merely smaller.

- **MINOR — Mobile interaction requirements are absent.** The problem is not simply that slides exceed one viewport. It is that the implementation does not define what must remain visible together, how state persists while scrolling, or how navigation avoids replacing the learner’s current decision.

## Findings Withdrawn Or Demoted

- **Demoted from MAJOR to MINOR — The formal source document front-loads vocabulary.** The source definition is not itself necessarily beginner-facing. Its density is acceptable as an authority artifact. The failure occurs when the deck imports its terminology without a pedagogical translation boundary.

- **Demoted from MAJOR to MINOR — S08 previews login before the formal software transfer.** A short cross-domain preview can support transfer. It becomes harmful only when it introduces a second unexplained causal thread or leaks the later answer. The clean-room version may retain one brief software echo after the table mismatch.

- **Demoted from MAJOR to MINOR — The research lacks empirical learner trials.** This is acceptable for exploratory design work if hypotheses remain explicitly provisional. The unsupported `pass` language remains MAJOR because it converts expert expectation into claimed validation.

- **Qualified — Local repair need not always fail before creating a lower layer.** Spivak’s rule is right for this teaching story, but should not become universal doctrine. Safety, irreversible cost, specialist boundaries, or already-observed repeated failures may justify decomposition before another repair attempt. The deck should teach failed repair as the clearest beginner witness, not as the only legitimate trigger.

## Resolved Tensions

### 1. Persistent Story Versus Learner Choice

One persistent table does not overconstrain choice if it constrains the world rather than the answer. The room size, uneven floor, available tools, and required use remain stable. At each stage, learners choose between plausible alternatives: narrow or wide top, shim or joint repair, generic leg instruction or independent leg build.

Choices become meaningful when the deck records them and later consequences depend on them. A predetermined narrative with rhetorical questions would merely conceal the answer more theatrically.

### 2. Necessary Formal Terms

The beginner deck needs only:

- **Schema**, after learners select which constraints define an acceptable table.
- **Artifact**, after something exists that can be tested.
- **Validate**, after learners compare that thing against earlier choices.
- **Residue**, after a specific mismatch remains.
- **Craft layer**, after local repair fails and an independent sub-build is justified.
- **Craft**, only after learners reconstruct the full pattern.

`Define`, `research`, `design`, `plan`, `execute`, and `reflect` can initially remain ordinary verbs rather than term badges.

**SCU** is optional late compression after learners compare a whole app, a coherent panel, and an isolated button. **Entropy** should be omitted from the first deck unless tied to an observable proxy such as the number of materially different valid outputs still compatible with the request.

### 3. Observable Lower-Layer Condition

A failed local repair justifies a candidate lower layer when all of these are visible:

1. A named upper-level check still fails after one bounded repair.
2. The remaining cause cannot be represented or tested inside the current step without introducing an independent target, sequence, tools, or checks.
3. The candidate lower unit has explicit input, output, local validation, and return interface.
4. Moving the work downward reduces the unresolved decisions held by the upper step.
5. The result passes both its local check and the upper artifact’s integration check.

For the table: a shim does not close the wobble; inspection shows that leg geometry and attachment require independent design; the rebuilt leg passes dimension and strength checks; after reattachment, the whole table passes stability and fit checks.

### 4. Mobile Behavior

Mobile should allow vertical scrolling. Forcing every state into one screen would encourage tiny text and compressed reasoning.

Before the fold, however, each state must preserve the **witness, learner question, and primary choice or control**. The consequence and newly earned term may appear after interaction or below the fold. Scrolling must preserve state, controls must report state accessibly, and reveal input must never also navigate.

### 5. Strengths To Preserve

The clean-room package should retain:

- the familiar table as the first witness;
- research before design;
- validation as comparison rather than intuition;
- residue as actionable information rather than shame;
- Essay 2’s anti-fragmentation and recomposition boundary;
- the table-to-software transfer;
- the aspiration of one earned concept per state;
- plain, beginner-readable language;
- the distinction between a coherent unit and the smallest possible task.

## Final Clean-Room Design Rules

1. Use one persistent causal object through target, constraint, choice, failure, repair, split, return, and stop.
2. Represent every teaching beat as explicit ordered states: witness, input, consequence, term, check.
3. Never reveal the term or preferred answer before a consequential learner choice.
4. Carry learner choices forward so later evidence can confirm or challenge them.
5. Introduce no more than one formal term per state, counting all visible copy.
6. Require observable validation, not verbal repetition.
7. Create a lower layer only with a named trigger, reduced unresolved load, local check, return interface, and upper check.
8. Show repair, descent, return, and acceptable-residue stopping edges explicitly.
9. Replay the same causal grammar in software rather than starting a second lecture.
10. Define desktop, mobile, keyboard, pointer, and assistive-state parity before claiming the deck passes.
11. Treat SCU and entropy as optional compression after learners can demonstrate the underlying distinctions.
12. Replace `pass` declarations with evidence receipts from literal state inspection and beginner trials.

The final design target is not a clearer explanation of Craft. It is a sequence in which a beginner repeatedly makes a defensible choice, sees what that choice causes, and only then receives the name for the pattern they have already used.

===== Alexander, Christopher ARCHIVE =====
# INITIAL POSITION

**Reviewer:** Alexander, Christopher  
**Lens:** temporal-prior / historical-lineage pattern analysis

The corpus has the right objects, but not yet a consistently causal story. Too often it presents a lifecycle sequence and calls that sequence an earned transformation. The missing connective tissue is consequence: an earlier choice must produce the later pressure.

## Findings By Artifact

### `CRAFT-INITIAL-DEFINITION.md`

**MAJOR:** The operational spine is repeatedly replaced by catalogs. “Intent -> chosen schema -> functor-like translator...” is causal, but the later “Layer Families,” residue taxonomy, method-routing table, and philosophical primitive list accumulate classifications without showing one artifact changing through them.

**Proposed correction:** Add one running historical witness whose successive failures demonstrate why each formal distinction became necessary.

**MAJOR:** The “Universal Physics Of Craft” turn outruns the artifact history. “All making can be understood...” is staged as a philosophical claim, but no cross-domain transformation in the document earns that ascent.

**Proposed correction:** End at the operational honesty boundary, treating the universal claim as an explicitly unearned research question rather than the culmination.

### `CRAFT-CODING-CLASS-SLIDE-SCHEMA.md`

**MAJOR:** S02-S08 form a list-like exposition: define, research, schema, plan, artifact, validate, residue. The table is specified as “finished” before the wobble appears, so the failure is not visibly caused by a prior choice.

**Proposed correction:** Carry one concrete constraint and one mistaken assumption through every slide until they produce the wobble.

**MAJOR:** S09 substitutes an ornate table for the prior table. “Sometimes it reveals a hidden project” does not causally explain why this particular subproject emerged.

**Proposed correction:** Let validation of the same table expose a leg problem whose attempted repair requires carving, tooling, practice, and fit validation.

### `CRAFT-CODING-CLASS-SLIDE-SCHEMA.yml`

**MAJOR:** The machine-readable schema preserves the same causal gap. S08 shows “Wobbly table and broken login examples,” then S09 introduces an “Ornate table” with no inherited condition connecting them.

**Proposed correction:** Encode persistent story-state fields such as inherited constraint, attempted action, observed consequence, and next pressure.

**MINOR:** The validation claim “The final definition recomposes the whole story” checks conceptual coverage, not whether each transition was caused by the preceding scene.

**Proposed correction:** Add a check requiring every major object transformation to name its prior cause.

### `CRAFT-CODING-CLASS-PRESENTATION.html`

**CRITICAL:** The rendered deck makes the causal break concrete. S06 depicts a successful artifact with a check mark; S07 offers a generic checklist; S08 suddenly supplies a wobbly table; S09 replaces it with an ornate table. Failure, recursion, and ornament are three disconnected exhibits.

**Proposed correction:** Render one table state changing over time: chosen uneven floor constraint, inadequate joint choice, built wobble, failed repair, then earned leg sub-build.

**MAJOR:** “The word stayed small, but the work inside it got much bigger” describes complexity but does not show what made it grow.

**Proposed correction:** Reveal hidden work as the consequence of a failed upper-level instruction, not as labels in a branching diagram.

**MINOR:** S14 ends with another lifecycle card list and the formal definition, repeating what the deck already named.

**Proposed correction:** End with the repaired table and working software feature, asking learners to reconstruct the causal chain from visible evidence.

### `research.md`

**MAJOR:** Explorer 1’s “Narrative Moves” is a strong inventory but not a historical lineage. Its bullet sequence states each pedagogical move independently, while “the ornate leg reveal” is declared strongest without deriving it from the wobble.

**Proposed correction:** Recast the return as scene -> decision -> consequence -> newly necessary pattern.

**MINOR:** The risk “use [the table] to earn the pattern, then move to software” recognizes metaphor exhaustion but does not specify the invariant carried across the transfer.

**Proposed correction:** Name the transferred invariant explicitly: an underspecified upper instruction produces an artifact whose validation exposes a bounded sub-build.

### `findings.md`

**MAJOR:** The artifact correctly requests “residue pressure between S08 and S09,” but its recommended witness scene still begins with an already ornate leg. The proposed cure repeats the gap it diagnoses.

**Proposed correction:** Specify the failed upper-level build that makes the ornate-leg subproject necessary.

**MAJOR:** The validation checklist requires every essay to explain SCU, craft-layer formation, and recomposition, encouraging each essay to restate the whole theory instead of advancing one historical stage.

**Proposed correction:** Validate the trilogy as a cumulative chain, assigning one transformation and one inherited obligation to each essay.

### `essay-01-the-table-is-not-the-project.md`

**MAJOR:** The desk is built through an enumerated method, then residue arrives as hypotheticals: “Maybe one leg is slightly short. Maybe the surface flexes.” No earlier decision produces a particular failure.

**Proposed correction:** Choose one fact, one design response, one overlooked constraint, and one resulting wobble that must be inherited by Essay 2.

**MINOR:** The ending converts the story into a seven-command list and then repeats the formal definition.

**Proposed correction:** End on the unresolved physical consequence that forces the next essay’s recursion.

### `essay-02-when-one-step-becomes-its-own-build.md`

**MAJOR:** “Then the table changes” is an authorial substitution, not an earned transformation. Ornament arrives from outside the prior build rather than emerging from its residue.

**Proposed correction:** Begin with the exact failed table inherited from Essay 1 and show why local repair cannot close the wobble.

**MINOR:** The repeated “Then research. Then design. Then plan. Then build. Then validate.” passage turns recursion into another lifecycle recital.

**Proposed correction:** Let each phase answer a concrete failure produced by the preceding action.

### `essay-03-why-vibe-coding-drifts.md`

**MAJOR:** The software transfer is intellectually recognizable but historically reset. The “bad dashboard” is asserted after the prompt; the reader never sees an actual plausible choice become wrong against a prior user need.

**Proposed correction:** Show one generated dashboard, one omitted assignment obligation, the failed learner action, and the resulting schema repair.

**MINOR:** “Craft builds the world one responsible layer at a time” stops carrying the formal idea because “world” has no validation or recomposition referent.

**Proposed correction:** End with the assignment panel successfully reattached to the portal and validated by a student task.

## Causal Story Spine

1. A learner sees a plain table and volunteers materials and tools: the table is an invitation.
2. The room is narrow and the floor uneven: constraints exert pressure.
3. The learner chooses dimensions and simple corner joints, then builds.
4. The table fits, but wobbles under a laptop: the failed build is a consequence of the chosen structure.
5. A foot pad hides the wobble but does not stabilize the joint: local repair fails.
6. “Make stable legs” now requires its own geometry, material research, test piece, tools, load check, and attachment interface: the subproject earns recursion.
7. The validated legs return to the upper build; the table becomes level and load-bearing: recomposition is witnessed.
8. “Make a dashboard” repeats the same historical pattern: a plausible screen fails a concrete student task.
9. An assignment-summary layer is defined, built, validated, and reattached to the portal: software transfer becomes recognition, not analogy.
10. The ending shows both completed objects and asks what caused each new layer to become necessary.

## Explicit Zero-Finding Defenses

None. Every target yielded at least one temporal-lineage finding. Several individual elements survived attack, especially the opening pause, the dual local/upper validation in Essay 2, and recomposition residue in Essay 3, but no complete artifact sustains the causal chain from invitation through pressure, consequence, earned recursion, and recognized transfer.

# FINAL POSITION

**Reviewer:** Alexander, Christopher  
**Lens:** temporal-prior / historical-lineage pattern analysis

The confrontation strengthens the central diagnosis: the corpus repeatedly confuses ordered exposition with earned transformation. Halford identifies the learner-level symptom, Spivak specifies the formal threshold that is missing, and Shannon shows that the interaction model cannot presently enact the sequence the prose promises. These are not separate defects. They are four views of the same break: the deck says events happen in order, but neither the learner, the artifact, nor the interface carries consequential state forward.

## Revised And Upheld Findings

**CRITICAL: The presentation has no persistent causal history. Upheld and strengthened.**

S06 shows a successful artifact, S08 introduces a wobble, and S09 substitutes ornament. Nothing in the chosen room facts, schema, or build plan causes the wobble; nothing about the wobble causes ornament. Halford sharpens this: because learners make no consequential choice, even the apparent sequence is authored order rather than learner-earned order.

**Correction:** Use one persistent table whose state records the learner’s constraint-sensitive choice, resulting build, observed mismatch, attempted repair, and justified lower-layer extraction.

**CRITICAL: The schema cannot represent the pedagogy it claims. New finding from Shannon, incorporated.**

The rule “Every term must be earned by a visible example first” requires ordered states, but each slide object contains only one `visual`, one `concept_move`, and one `validation_check`. Except for S01, the term, explanation, and answer appear simultaneously. A causal story cannot exist only in speaker notes; its prior states must be representable and testable.

**Correction:** Replace each static slide object with ordered interaction states: witness, learner input, committed choice, consequence, term reveal, and comprehension check.

**MAJOR: The lower-layer threshold is formally under-specified. Upheld and sharpened by Spivak.**

The current rule says a step becomes a craft layer when it needs “its own plan, tools, validation, and way back into the whole.” This identifies attributes of a possible sub-build, but not the observable event that justifies splitting. An ornate part or complicated feature is not sufficient.

**Correction:** A lower layer is justified only when a named upper-layer mismatch survives a bounded local repair, a candidate split predicts lower residue, the sub-build has independent local validation, and its output has an explicit upper-level recomposition check.

**MAJOR: S04 collapses distinct historical objects. New formal finding, accepted.**

The visual called `planShape` says “the plan decides what counts as the right table,” although S04 is supposed to earn schema/design and S05 separately earns plan. This collapses the chosen validity structure into execution order before learners can experience their different consequences.

**Correction:** S04 must show a constraint-bearing design/schema; S05 must transform that schema into ordered executable work without changing what counts as valid.

**MAJOR: The software transfer is analogy rather than recognition. Upheld.**

The dashboard sequence begins again from a vague prompt. It does not replay the same causal structure with a visible generated artifact, failed user action, attempted repair, bounded extraction, and reintegration. The learner is told that software “does this too” instead of recognizing an already-lived pattern.

**Correction:** Replay the table invariant exactly: underspecified instruction -> plausible choice -> produced artifact -> failed obligation -> failed local repair -> lower layer -> local and upper validation.

**MAJOR: The final loop is not a loop. New formal finding, accepted.**

S14 lists stages but shows neither a return edge nor the acceptable-residue condition that ends iteration. As an ending, it restates definitions instead of showing closure.

**Correction:** End with the repaired artifact, a visible validation comparison, acceptable remaining residue, and an explicit return from reflection to the responsible earlier stage when residue is not acceptable.

**MAJOR: The interface violates the narrative contract. New empirical finding, accepted.**

Space on focused S01 both reveals and advances; the final reveal cycles back to the hidden state; S02-S14 expose answer and term together; and notes have no visible or programmatic state feedback. These behaviors make the historical sequence unstable even where one exists.

**Correction:** Give reveal controls exclusive event handling, make terminal states monotonic unless explicitly reset, expose state through visible and ARIA feedback, and validate every state transition independently.

**MAJOR: Mobile should preserve causal units, not force desktop pagination. Revised finding.**

A strict one-screen rule would overconstrain legibility and interaction on small screens. Unbounded scrolling, however, can place the consequence or term outside the learner’s current causal frame.

**Correction:** Allow vertical scrolling within a slide, but keep the witness, active question, and current learner action before the fold. Consequence and term may follow after interaction, while navigation and progress remain stable and visible.

**MINOR: Entropy should remain qualitative. Accepted from Shannon.**

“Too many possible meanings still competing” is suitable beginner language. Claims about minimizing or measuring entropy are not warranted in this deck without observable proxies.

**Correction:** Tie uncertainty pressure to visible proxies such as divergent outputs, omitted obligations, relation count, or repeated validation mismatch.

## Withdrawn Or Demoted Findings

I withdraw my earlier implication that every lifecycle recital is inherently defective. A concise recap can be useful after learners have enacted the transformations. The defect is premature recital, not lists themselves.

I demote the ornate-table metaphor from a fundamental narrative failure to a replaceable implementation choice. Ornament can remain if it is caused by a real requirement, such as matching an existing room or restoration pattern, and if a failed local repair exposes the carving sub-build. Uncaused ornament remains defective.

I also demote my criticism of Essay 2’s repeated “Then research. Then design...” sequence. Spivak is right that this essay already preserves two major strengths: anti-fragmentation and recomposition. Its sequence becomes acceptable if each phase answers evidence produced by the previous phase rather than operating as an independent definition.

## Resolved Tensions

A persistent story need not overconstrain learner choice. The story should fix the objective and available evidence, not the learner’s decision. Learners can choose among plausible joints, materials, dimensions, or repair strategies. The package must be prepared to show distinct consequences for those choices, then reconverge when evidence demonstrates the same formal threshold. Choice becomes more meaningful because it changes the artifact’s history.

The necessary beginner terms are: **define**, **schema**, **artifact**, **validate**, **residue**, **craft layer**, and **smallest coherent unit**. “Research,” “plan,” and “execute” can remain ordinary verbs rather than formal badges. “Entropy” is optional and should appear only after learners see multiple plausible software outputs from one loose instruction. “Craft” is earned only after the learner can reconstruct the entire causal chain.

Failed local repair becomes a justified lower layer under one observable condition: after a bounded repair attempt, the same named upper-level validation obligation still fails, and resolving it requires a separately specifiable object with its own inputs, artifact, local check, and recomposition check. The split remains provisional until it reduces the original residue and passes both validation surfaces.

On mobile, vertical scrolling is acceptable. The first viewport must contain the persistent object state, the current question, and the available action. Definitions, explanation, and consequences should not precede the learner’s action. No causal pair should be separated without a persistent state summary.

## Clean-Room Design Rules

1. Maintain one stateful table history through constraint, choice, build, mismatch, repair, split, and recomposition.
2. Give every scene the sequence: witness -> learner choice -> committed state -> consequence -> term -> check.
3. Never use complexity alone to justify a layer.
4. Require failed bounded local repair before proposing extraction.
5. Validate lower-layer artifacts locally and again inside the upper artifact.
6. Preserve explicit recomposition and acceptable-residue stop conditions.
7. Separate schema validity from plan execution.
8. Transfer to software by replaying the causal invariant, not by asserting similarity.
9. Represent interaction states, inputs, transitions, terminal behavior, viewport expectations, and validation checks in the schema.
10. Preserve S01’s pause, the concrete table doorway, “validation is not a vibe,” residue as operational information, Essay 2’s anti-fragmentation rule, and the smallest-coherent-unit balance.
11. End on witnessed closure, not a definition recital.

The clean-room package should therefore teach Craft as a history of responsible transformations. A learner should not merely remember the order of terms. They should be able to say which observed consequence made each next concept necessary.

===== Spivak, David ARCHIVE =====
Declared identity: Spivak, David  
Declared lens: source-corpus/existing Craft teaching definition traceability

## INITIAL POSITION

# INITIAL POSITION

The refresh preserves Craft’s vocabulary, but its central teaching rule is not yet fully traceable to the source definition. The corpus repeatedly says a layer needs “a way back into the whole,” while often validating only recognition of that phrase, not demonstrated recomposition. This leaves a real risk of teaching Craft as responsible decomposition rather than governed schema/data translation with residue-driven recursion and closure.

## Findings By Artifact

### `CRAFT-INITIAL-DEFINITION.md`

**MAJOR** — The teaching-critical term “craft layer” lacks a stable source definition. The document defines reflection-tower promotion when residue “cannot be closed by local repair” and requires the next layer’s “validation, and recomposition path” (lines 433-443), but “craft layer” is absent from Initial Vocabulary and the capability’s form remains an open question (lines 700-708).  
**Correction:** Define a craft layer explicitly, including necessary trigger, residue-reduction test, recomposition obligation, and stop condition.

**MINOR** — “At least five residue types” introduces a table containing seven types (lines 419-431).  
**Correction:** Say “at least seven” or remove the count.

### `CRAFT-CODING-CLASS-SLIDE-SCHEMA.md`

**MAJOR** — The teaching promise says a step becomes a layer when it needs “its own plan, tools, validation, and way back into the whole” (lines 13-16). That is weaker than the source trigger: local repair must be insufficient, the missing schema must be identified, and splitting must reduce residue (definition lines 433-449). Complexity alone can therefore appear sufficient.  
**Correction:** Add: “and cannot be responsibly closed in the current layer; splitting must reduce residue.”

**MAJOR** — S04 calls an “annotated table plan” the schema (lines 129-142), immediately before S05 distinguishes planning from design (lines 145-158). This visually collapses schema/design into plan.  
**Correction:** Show a requirements/design schema at S04 and reserve ordered build steps for S05.

### `CRAFT-CODING-CLASS-SLIDE-SCHEMA.yml`

**MAJOR** — The same under-specified layer trigger is canonicalized in `teaching_promise` (lines 10-12) and S10 (lines 171-180), without the source’s local-repair or residue-decrease gate.  
**Correction:** Encode the full trigger and add it to S10’s `validation_check`.

### `CRAFT-CODING-CLASS-PRESENTATION.html`

**MAJOR** — The rendered S04 visual literally says “the plan decides what counts as the right table” (line 903), although S04 teaches schema and S05 teaches plan.  
**Correction:** Replace “plan” with “schema/design” and visually distinguish constraints from execution order.

**MAJOR** — S14 is labeled a “Craft loop,” but its visual is a branch-grid ending at “Reflect on residue” (lines 1056-1067). It provides no return edge from a lower artifact into the upper schema and no visible closure.  
**Correction:** Render an actual cycle with local/upper validation, recomposition, and an acceptable-residue stop.

### `research.md`

**MAJOR** — The “craft layer” rule is traced back to the teaching schema itself (lines 242-245), making the corpus’s central derived rule partially circular. The source definition supports recursion through residue promotion, not that exact sufficient-condition formula.  
**Correction:** Label the classroom rule as a derived heuristic and trace each condition to reflection-tower, SCU, recomposition, and stop-criteria passages.

### `findings.md`

**MAJOR** — The validation checklist requires **each essay** to explain schema/data translation, residue routing, SCU, craft-layer formation, and recomposition (lines 135-151), but the verdict matrix assigns Essay 1 only through residue and Essay 2 only recursion (lines 153-159). The declared validation contract and designed division of labor disagree.  
**Correction:** Separate per-essay obligations from series-level obligations, then validate each draft against the correct row.

### `essay-01-the-table-is-not-the-project.md`

**MAJOR** — The essay ends by claiming the result “can recompose into the whole” (lines 112-116), but its witness stops at residue routing (lines 90-110). No repaired artifact is revalidated or reattached.  
**Correction:** Carry one residue through repair or redesign, revalidation, and closure in the table’s upper context.

### `essay-02-when-one-step-becomes-its-own-build.md`

No finding. See zero-finding defense below.

### `essay-03-why-vibe-coding-drifts.md`

**MINOR** — The closing “builds the world one responsible layer at a time” (line 115) reintroduces endless-layer rhetoric after the essay carefully rejects blind splitting (lines 78-88).  
**Correction:** Close on stopping at acceptable residue, with new layers created only when local repair cannot close the mismatch.

## Concept-Trace Matrix

| Concept or transition | Initial definition | Schema corpus | Presentation | Essays | Position |
|---|---|---|---|---|---|
| Intent → schema → artifact | Explicit, lines 8-19 | S02-S06 | Present | Strong in 01/03 | Pass |
| Design → plan distinction | Explicit, lines 302-344 | Textually distinct | S04 visual says “plan” | Strong in 01/02 | **Fail** |
| Validation → classified residue | Explicit, lines 346-373, 419-431 | S07-S08 simplifies routes | Recognition-level only | Strongest in 03 | Partial |
| Residue → new layer | Requires failed local closure, lines 433-443 | Reduced to own lifecycle | Complexity-led ornate leg | Strong in 02 | **Fail traceability** |
| SCU balance | Explicit, lines 173-244 | S12 | Preserved | Strong in 02/03 | Pass |
| No endless smallness | Explicit, lines 445-463 | Mentioned, weakly checked | Speaker-note only | Strong in 02/03 | Partial |
| Recomposition | Required, lines 430, 442, 578 | Repeated verbally | Not visually demonstrated | Demonstrated only in 02 | **Fail corpus-wide** |
| Stop at acceptable residue | Explicit, lines 511-529 | Absent from lesson checks | Absent from final slide | Closing drift in 03 | **Fail** |

## Explicit Zero-Finding Defense

**`essay-02-when-one-step-becomes-its-own-build.md` survives this lens.** I attacked it for complexity-driven splitting, generic decomposition, local-only validation, endless smallness, and missing recomposition. It explicitly rejects reflexive breakdown (lines 42-51), validates both local and upper surfaces (lines 74-77), routes residue back into the upper design (lines 79-82), and makes recomposition the condition of independence (lines 99-112).

The Markdown and YAML schemas also survive a synchronization attack: their 14-slide order, fields, concept moves, and validation checklist materially agree. Their shared problem is semantic under-specification, not representation drift.

No files were modified.

## FINAL POSITION

# FINAL POSITION

The confrontation strengthens the original traceability finding and changes its practical consequence: the next package should not merely correct terminology or add a recomposition arrow. It needs a stateful causal witness in which learners make choices, observe consequences, attempt local repair, and earn recursion from evidence.

The four lenses converge. Halford identifies the missing learner action, Alexander the missing causal continuity, Shannon the missing interaction model, and my lens identifies the missing formal criterion. These are not separate defects. Together they explain why the current corpus can recite Craft accurately while still teaching decomposition.

## Revised And Upheld Findings

**CRITICAL — The deck does not demonstrate the event that justifies a lower layer.**  
The current rule, “If a step needs its own plan, tools, validation, and way back into the whole,” identifies complexity but not necessity. Alexander is right that the simple table, wobble, ornament, and lower-leg build are disconnected exhibits. Halford is right that learners do not make the consequential choice. Shannon is right that the schema cannot encode the states needed to show the event.

A justified lower layer requires observable evidence:

1. An artifact fails a named validation against the current schema.
2. A local repair is attempted without changing the layer boundary.
3. The repaired artifact still fails because the current schema cannot represent or govern the necessary relation.
4. A candidate lower layer names its own schema, artifact, local validation, and upper interface.
5. Executing that layer reduces the original residue.
6. The lower artifact passes both local validation and upper-context validation.
7. Recomposition closes the original mismatch with acceptable residue.

Before step 5, the split is a hypothesis. Before steps 6 and 7, it is not a successful craft layer.

**MAJOR — Authored sequence is being mistaken for earned understanding.**  
The schema’s ordered slides do not prove that learners experienced the order. S02-S14 generally present visual, label, explanation, and answer together. S14 then asks learners to recompose terms they were shown rather than decisions they made. The required teaching sequence is:

```text
witness -> learner choice -> consequence -> comparison -> term -> next decision
```

A persistent story need not overconstrain choice. The stable object and upper objective remain fixed, while learners choose among plausible materials, repairs, checks, boundaries, and layer candidates. The lesson may branch locally and reconverge on the same formal criterion. Meaningful choice requires that at least two options have visibly different consequences, not that every classroom produce a different final table.

**MAJOR — The artifact model cannot encode the pedagogy it claims to validate.**  
A slide object with one `visual`, one `concept_move`, and one `validation_check` cannot represent example-before-term when the example, decision, consequence, and term occur at different times. Shannon’s browser evidence makes this concrete: S01 has reveal states, but Space both reveals and navigates; the final click resets; later slides are simultaneous; note visibility lacks state feedback.

The clean-room schema must model ordered states, accepted inputs, state transitions, reveal ownership, focus behavior, and per-state validation. A deck-level “pass” is unsupported until those states are exercised across keyboard, pointer, and mobile layouts.

**MAJOR — Schema and plan remain visually conflated.**  
S04’s visual statement that “the plan decides what counts as the right table” contradicts the intended transition. Schema/design defines valid structure and constraints; a plan orders executable work. This distinction is load-bearing because Craft cannot be reduced to better planning.

**MAJOR — Recomposition is asserted more often than demonstrated.**  
Essay 2 remains the strongest artifact because it validates the leg locally and as part of the table. Essay 1 names recomposition only in its final definition. The deck’s final “loop” is a list without a return edge or closure state. A new package must show the lower artifact changing the upper artifact and resolving the residue that caused recursion.

**MAJOR — Entropy is not earned in the beginner deck.**  
“Too many possible meanings” is a useful qualitative explanation, but calling it entropy introduces a formal-sounding quantity without an observable proxy. Unless the lesson measures something such as competing interpretations, unresolved relations, or validation divergence, the term adds authority without evidence.

## Demoted Or Withdrawn Findings

**Demoted to MINOR — The findings artifact’s per-essay validation mismatch.**  
The checklist says each essay should carry every concept, while the verdict matrix distributes concepts across the series. This is an editorial contract ambiguity, but the deeper failure is that the series lacks one causal witness connecting those concepts.

**Withdrawn from the blocking case — The isolated closing line in Essay 3.**  
“Builds the world one responsible layer at a time” risks endless-layer rhetoric, but the surrounding essay explicitly rejects blind splitting and preserves SCU and recomposition. The line should be sharpened, but it is not independently dangerous.

**Withdrawn from the clean-room decision — The residue-type count discrepancy.**  
“At least five” followed by seven rows is a real copy defect, but it does not determine the beginner package’s design.

## Formal Terms

The beginner deck needs only terms that change what learners can decide:

- **Schema:** earned after learners compare plausible table constraints and choose what counts as valid.
- **Artifact:** earned when the built object can be inspected in ways the drawing cannot.
- **Validation:** earned when learners choose a check and observe pass or failure.
- **Residue:** earned after a concrete mismatch survives comparison.
- **Craft layer:** earned only after failed local repair and a successful lower-build hypothesis.
- **SCU:** earned when learners compare a too-large unit, a coherent unit, and a too-small unit using validation and recomposition.
- **Craft:** earned at the end as the name for the demonstrated method.

Define, research, design, plan, execute, and reflect can initially remain ordinary verbs. “Recomposition” may be introduced late, after “fits back into the whole” is demonstrated. “Entropy” should leave the first deck unless observable proxies are added. “Data” and “functor-like translator” belong in later formal material.

## Mobile Decision

Mobile should allow vertical scrolling. Forcing every complete slide into one viewport would make causal interactions illegible and encourage text compression.

Each state must nevertheless place the essential teaching unit before the fold:

- persistent witness;
- current learner question;
- available choice or action;
- immediate consequence;
- visible progress/state indication.

Explanatory notes, formal naming, secondary checks, and the next bridge may follow below. Navigation must not share an input with reveal behavior, and visible state must remain stable while scrolling.

## Clean-Room Design Rules

1. Use one persistent table and one persistent upper objective.
2. Preserve learner choice inside bounded, consequential branches.
3. Do not display a term before its witness and consequence.
4. Model every lesson as explicit interaction states and transitions.
5. Keep schema constraints visually distinct from plan order.
6. Require an actual local repair before proposing a lower layer.
7. Treat a split as provisional until residue demonstrably decreases.
8. Validate every lower artifact locally and against its upper interface.
9. Show recomposition changing the persistent upper artifact.
10. End at acceptable residue; do not imply recursive completeness.
11. Replay the same causal structure in software, not merely the same labels.
12. Validate pointer, keyboard, focus, notes state, mobile scrolling, and schema/HTML parity before declaring pass.

Preserve the current corpus’s strongest choices: the familiar table witness, define/research before design, schema/artifact distinction, “validation is not a vibe,” residue as information rather than shame, SCU’s rejection of both bigness and meaningless smallness, the rejection of prompt polish as the whole answer, and Essay 2’s local-plus-upper validation. These are the right bones. The clean-room package must make learners enact them.

===== Shannon, Claude ARCHIVE =====
**INITIAL POSITION — Shannon, Claude**

Lens: methodology/computational-adversarial information-state audit. No files were changed. Browser and local server were stopped.

**Findings By Artifact**

`CRAFT-INITIAL-DEFINITION.md`

- **MAJOR** — The formal model introduces measurable-looking quantities without measurement semantics: “non-linear fidelity curve” and “local minimum” (`198`), then `E = entropy(...)` (`531-579`) without scale, estimator, observations, or falsification threshold. This makes SCU selection non-computable despite the formal notation.  
  **Correction:** Define observable proxies and decision thresholds, or explicitly label entropy/local minimum as qualitative heuristics.

`CRAFT-CODING-CLASS-SLIDE-SCHEMA.md`

- **MAJOR** — “Every term must be earned by a visible example first” (`32-33`) is a temporal constraint, but the slide object has no interaction, reveal-order, or state-transition fields (`46-63`). The schema cannot represent or validate its own teaching rule.  
  **Correction:** Add ordered states such as `initial_state`, `reveals`, `term_activation`, and per-state validation.

`CRAFT-CODING-CLASS-SLIDE-SCHEMA.yml`

- **MAJOR** — The machine view declares `draft_status: pass` and says the deck “passes” five constraints (`283-285`), but supplies neither executable rules nor validation results. Its required fields (`36-48`) also omit interaction state.  
  **Correction:** Replace the unsupported pass with `unverified`, then attach machine-checkable rules and evidence per slide/state.

`CRAFT-CODING-CLASS-PRESENTATION.html`

- **CRITICAL** — Keyboard state corruption: the focused reveal handles Space (`1151-1155`), then the bubbling global handler also advances the slide (`1236-1240`). Observed result: one Space changed reveal `0→1` while moving to `2 / 14` at scrollTop `720`.  
  **Correction:** Stop propagation for reveal keys or make the global handler ignore interactive descendants.

- **MAJOR** — S01 projects facilitator direction: “Do not answer yet” (`621`) even though prompts must remain in notes. This changes the learner-facing concept from hidden requirements to presenter choreography.  
  **Correction:** Restore the schema’s concept move as projected copy and keep timing instructions exclusively in notes.

- **MAJOR** — S02-S14 render term, example, question, and abstraction simultaneously (`1113-1119`); only S01 has reveal states. Therefore “example before term” is not implemented as an observable sequence.  
  **Correction:** Give each formal-term slide an example-first state followed by an explicit term reveal.

- **MINOR** — S01’s third click silently cycles reveal `2→0` (`1136-1143`), allowing an accidental click to erase the teaching state.  
  **Correction:** Make the final reveal terminal or provide a separately labeled reset command.

`research.md`

- **MAJOR** — The evidence boundary contains only the definition and two schemas (`6-9`), yet explorer headings invoke named methodological/cognition/formal authorities (`14-17`, `96-99`, `185-188`). The resulting advice is internally circular, not independent expert or empirical evidence.  
  **Correction:** Label these as analytical lenses, or cite and distinguish actual external evidence from local interpretation.

`findings.md`

- **MAJOR** — The checklist requires every essay to explain schema/data translation, residue routing, SCU, craft-layer criteria, and recomposition (`135-151`), but no essay-by-criterion adjudication is recorded before the verdict matrix (`153-159`). “Pass condition” is being used as a requirement, not evidence of passage.  
  **Correction:** Add a literal evidence matrix with essay line references and PASS/FAIL/NOT-TESTED outcomes.

`essay-01-the-table-is-not-the-project.md`

- **MINOR** — “Before design, we need facts” (`43`) makes research sound mandatory, while the declared lifecycle says “Research when needed.”  
  **Correction:** Say research is required when missing facts could materially change the design.

`essay-02-when-one-step-becomes-its-own-build.md`

- **MAJOR** — The operational rule is plan/tools/validation/recomposition (`99-106`), but it never gives an observable test that the split actually reduces residue. “Small enough” remains judgment without comparison.  
  **Correction:** Require before/after residue evidence and reject the new layer when ambiguity or integration cost increases.

`essay-03-why-vibe-coding-drifts.md`

- **MAJOR** — “This is why vibe coding drifts” attributes drift to vague feature names (`24-27`). That excludes drift from stochastic translation, missing context, tool failure, incorrect evidence, and relation loss even under a specific request.  
  **Correction:** Present ambiguity as one major cause and preserve the broader translator/context/tool failure model.

**Browser Evidence**

At `1280×720`, S01 fit exactly one viewport. Mouse reveal worked `0→1→2`, then reset to `0`. Arrow navigation and PageDown worked. Notes mode expanded slides to `831–951 px`, breaking one-viewport presentation state.

At `390×844`, there was no horizontal overflow and the fixed chrome did not overlap S01. However, every slide after S01 exceeded the viewport (`856–1446 px`); 11 exceeded `1000 px`. Notes mode expanded states to `1323–1983 px`. The counter therefore identifies a current slide while substantial content remains unseen below the fold. The notes control exposes only `i`, has no `aria-pressed`, and gives no visible state feedback.

**Proposed Validation Set**

1. Validate Markdown/YAML/HTML parity for every slide field and visual identifier.
2. Model and test each ordered reveal state, including terminal behavior.
3. Assert Space on a focused reveal changes only reveal state.
4. Test click, Enter, Space, arrows, PageUp/Down, boundaries, notes, and hash navigation.
5. Require each rendered state to express one concept before introducing its term.
6. At `1280×720`, `1366×768`, `390×844`, and `360×800`, assert no overlap, clipping, horizontal overflow, or hidden essential copy.
7. Require notes mode to preserve active slide identity and expose toggle state.
8. Replace self-declared pedagogical passes with criterion-by-criterion evidence and learner-response thresholds.
9. Operationalize SCU/residue decisions with before/after evidence.

**Zero-Finding Defenses**

The essays survived attempted collapse into generic planning: Essay 1 preserves artifact comparison and routing; Essay 2 preserves local plus upper validation (`74-77`); Essay 3 explicitly rejects “better prompts” as the whole method (`35-43`). The browser also survived horizontal-overflow and first-slide chrome-overlap checks at both tested viewports.

**FINAL POSITION — Shannon, Claude**

Lens: methodology/computational-adversarial information-state audit.

My final judgment is that the existing corpus contains a sound conceptual spine but does not yet instantiate a valid teaching state machine. The central defect is now sharper after confrontation: authored sequence, visual sequence, causal sequence, and learner-earned sequence are treated as equivalent. They are not. A clean-room replacement should preserve the concepts while rebuilding the instructional computation from explicit states, choices, consequences, and closure conditions.

**Revised And Upheld Findings**

- **CRITICAL — Interaction state is corruptible.** The S01 Space event both advances the reveal and navigates because the local and global handlers consume the same input. This is not merely accessibility polish; it destroys the correspondence between learner action and rendered state. Each input must cause exactly one declared transition.

- **MAJOR — The deck mistakes authored order for learner-earned order.** I uphold Halford’s claim. S02-S14 may be ordered correctly in the source, but each renders witness, answer, term, and explanation simultaneously. A term is earned only when the learner has first inspected evidence, made or predicted a consequential choice, and observed the result.

- **MAJOR — The deck lacks a persistent causal history.** Alexander’s criticism explains why S02-S08 feel procedural despite their correct order. The successful artifact, later wobble, and ornate table do not visibly descend from prior learner decisions. The replacement needs one persistent table whose state changes across slides.

  This does not require fake freedom or an unbounded classroom branch. Learner choice can remain meaningful inside a controlled causal story: present two or three plausible choices, ask for a prediction, record the choice, then reveal the consequence. The target and constraints remain stable while decisions vary. The story becomes a small experiment rather than a recitation.

- **MAJOR — “Complex enough” does not justify a lower layer.** I uphold Spivak’s stronger predicate. Failed local repair permits investigation; it does not by itself earn decomposition. A proposed lower layer becomes justified only after it defines its own responsibility and proves that the separation reduces residue while preserving recomposition.

- **MAJOR — S04 collapses schema into plan.** The slide intends to teach schema, but its annotated visual calls itself a plan and says the plan decides validity. This removes the distinction S05 is supposed to teach. Schema should constrain valid outcomes; plan should order work that realizes those constraints.

- **MAJOR — The final loop is not computationally closed.** A list of lifecycle nodes is not a loop. The final model needs a return edge from validation/residue to local repair, lower-layer trial, schema revision, or stop. It also needs the explicit stop condition: residue is acceptable for the current objective.

- **MAJOR — The schemas cannot encode required teaching behavior.** The Markdown and YAML represent slides as static records. They lack state identifiers, allowed inputs, transitions, visible information, expected learner action, consequence, and per-state checks. The YAML’s unsupported `pass` status is therefore still invalid.

- **MAJOR — Mobile presentation state is ambiguous.** Vertical scrolling is not inherently wrong, but the current deck calls a slide active while essential content may remain hundreds of pixels below the viewport. That breaks the observable meaning of the counter and navigation controls.

- **MAJOR — Entropy and SCU currently look more measurable than they are.** Terms such as “local minimum” and the formal entropy function imply a decision procedure that the corpus does not provide. Either define observable proxies or keep the beginner language qualitative.

**Withdrawals And Demotions**

- I **withdraw** my earlier complaint that Essay 1 makes research universally mandatory. Its surrounding language already limits research to facts capable of changing the design. The wording could be tightened, but it is not a substantive defect.

- I **demote to MINOR** the causal overstatement in Essay 3. “Vague feature names” is too narrow as a complete explanation of drift, but the essay remains an effective beginner bridge. The clean-room deck should add context loss, relation loss, and tool/runtime mismatch only after ambiguity has been demonstrated.

- I **demote to MINOR** the research packet’s named-lens provenance problem. The labels can suggest external authority unsupported by the local evidence boundary, but this does not invalidate the extracted teaching risks. Rename them as analytical lenses or provide independent citations.

- I retain the final-click reset and missing notes-toggle state as **MINOR** interaction defects. They matter, but they are downstream of the larger state-model failure.

- I agree that Essay 2 is the strongest existing anti-fragmentation substrate. Its local/upper validation and recomposition language should be preserved, while adding an observable residue-reduction test.

**Exact Lower-Layer Condition**

A failed local repair should transition to a **candidate lower-layer trial** only when all preconditions hold:

```text
residue is reproducible
AND a local repair failed the same declared acceptance check
AND the unresolved work has a bounded input, output, and responsibility
AND a local validation surface can be declared
AND an upper recomposition interface can be declared
```

The candidate earns lower-layer status only after:

```text
local validation passes
AND upper-context validation passes
AND recomposition passes
AND measured residue is lower than before the split
```

“Measured residue” need not be a universal number. It can be a declared vector: failed checks, unresolved obligations, ambiguity count, integration failures, or learner-visible mismatches. The metric must be selected before the split, not invented afterward.

**Necessary Beginner Terms**

The first class needs only:

1. **Schema**, earned after constraints and a learner choice determine what counts as a valid table.
2. **Artifact**, earned when a real result exists and can be inspected.
3. **Validation**, earned through comparison against the prior schema.
4. **Residue**, earned after a concrete mismatch survives that comparison.
5. **Craft layer**, earned only after local repair fails and a bounded sub-build proves local and upper validity.
6. **Recomposition**, earned when the repaired leg returns to the table and the whole passes.
7. **Craft**, used at the end to name the already experienced method.

Define, research, design, plan, and execute can remain ordinary verbs. SCU is optional late compression after learners reject both an entire application and a meaningless fragment. Entropy should be omitted from the first deck; “too many plausible meanings” teaches the needed idea without unsupported formal weight. S14 must introduce no new vocabulary.

**Mobile Rule**

Live presentation states should fit one viewport on supported presentation screens. Mobile may use vertical reading only as a distinct responsive mode. Before the first fold, mobile must show the persistent object state, current learner question or choice, immediate consequence or earned term, progress, and navigation. Speaker notes, extended explanation, and secondary checks belong in a drawer or below-fold reading section. If within-slide scrolling is retained, it needs an explicit continuation cue and must not let navigation conceal unread essential content.

**Final Clean-Room Rules**

1. Use one persistent table and one stable target across the physical story.
2. Structure every concept as `witness → learner choice/prediction → consequence → term`.
3. Give every rendered state a stable ID, visible information set, accepted inputs, single transition, and validation check.
4. Keep schema, plan, artifact, and validation visually distinct.
5. Attempt and display local repair before proposing decomposition.
6. Treat a lower layer as provisional until residue reduction, local validity, upper validity, and recomposition are demonstrated.
7. Replay the same causal pattern in software; do not merely substitute software nouns.
8. End with a real return edge and acceptable-residue stop.
9. Generate or mechanically compare HTML against one authoritative structured schema.
10. Validate keyboard exclusivity, reveal order, viewport fit, notes state, parity, and one-idea-per-state.
11. Preserve the familiar table opening, silent pause, facts-that-change-design research rule, residue-as-information framing, anti-fragmentation discipline, local/upper validation, recomposition, and delayed software transfer.

The clean-room objective is therefore not a prettier fourteen-slide deck. It is a small, inspectable teaching machine in which every concept is causally earned and every transition can be tested.


## Verifier Returns

### Schön, Donald

**VERIFICATION POSITION**

**UPHELD:** Findings **1, 3, 4, 5, 7, 8, 9, 10, 11, 14, 17, 18, 19, 20, 21**  
**REFUTED AND DROPPED:** Findings **6, 16, 22**

### Upheld Findings

- **#1:** The authority source permits a new layer only when residue cannot be explained or closed locally and requires validation plus recomposition (`CRAFT-INITIAL-DEFINITION.md:252-262, 344-365, 558-579`). The current teaching rule requires only plan, tools, validation, and return (`CRAFT-CODING-CLASS-SLIDE-SCHEMA.md:11-16`). A beginner otherwise learns to split whenever work looks complicated.

- **#3:** “Example first” is explicitly promised (`CRAFT-CODING-CLASS-SLIDE-SCHEMA.md:30-44`), but the record has only simultaneous content fields (`46-63`). Ordered witness, input, consequence, and term states are observable if each accepted input produces one visible transition.

- **#4:** The ornate leg is introduced because it contains “hidden work,” not because a named table check resisted local repair (`CRAFT-CODING-CLASS-SLIDE-SCHEMA.md:209-229`). A beginner cannot choose between repair and decomposition from complexity alone.

- **#5:** S14 ends with lifecycle recital (`CRAFT-CODING-CLASS-SLIDE-SCHEMA.yml:219-229`), while the authority distinguishes repair, promotion, and stopping at acceptable residue (`CRAFT-INITIAL-DEFINITION.md:511-529, 558-568`). Explicit repair, descend, return, and stop choices change what the learner can do.

- **#7:** The YAML repeats the complexity trigger and static final loop (`CRAFT-CODING-CLASS-SLIDE-SCHEMA.yml:171-229`). Encoding named failed checks, local and upper results, return, and stop makes decomposition acceptance observable.

- **#8:** The focused control handles Space (`CRAFT-CODING-CLASS-PRESENTATION.html:1151-1155`), then the window handler also navigates on Space (`1236-1240`). Archived observation records reveal and navigation occurring together (`attacks.md:665-666`). Exclusive input ownership is directly testable.

- **#9:** `renderSlides()` emits term, question, and conclusion together (`CRAFT-CODING-CLASS-PRESENTATION.html:1109-1129`). The learner cannot predict or choose before seeing the answer.

- **#10:** The built table appears as successful (`CRAFT-CODING-CLASS-PRESENTATION.html:678-699`), the wobble arrives later (`1029-1054`), and the ornate table replaces it (`714-735`). No earlier learner decision causes either change.

- **#11:** S04 correctly calls schema the validity structure (`CRAFT-CODING-CLASS-PRESENTATION.html:653-663`), but its visual says “the plan decides what counts as the right table” (`903-904`). This prevents a beginner from distinguishing “what is valid?” from “what happens next?”

- **#14:** Research calls concepts “earned” merely because slides are sequenced (`research.md:101-131`) and asserts failure conditions without novice evidence (`143-153`). Prediction, consequence, and delayed term reveal establish an observable criterion.

- **#17:** Essay 1 names schema and artifact before any artifact exists (`essay-01-the-table-is-not-the-project.md:55-68`); its later mismatch is a list of hypothetical possibilities (`90-102`). A caused failure is required.

- **#18:** The narrator selects the target, research, design, plan, checks, and routes (`essay-01-the-table-is-not-the-project.md:26-53, 70-102`). Bounded alternatives would let the learner make and later inspect a consequential choice.

- **#19:** Essay 2 changes the table arbitrarily, asks what changed, then immediately answers (`essay-02-when-one-step-becomes-its-own-build.md:16-31`). It needs to inherit Essay 1’s exact failed check.

- **#20:** Essay 2 names local and upper validation (`essay-02-when-one-step-becomes-its-own-build.md:74-82`) but never compares named mismatches before and after extraction. “Lower residue” is observable only as fewer or less severe failed checks, declared in advance.

- **#21:** Essay 3 defines schema, artifact, validation, and residue before presenting the purported discovery pause (`essay-03-why-vibe-coding-drifts.md:35-50`). The learner receives the diagnosis before inspecting the failure.

### Refuted Findings

- **#6 — DROP.** Changing `draft_status: pass` (`CRAFT-CODING-CLASS-SLIDE-SCHEMA.yml:275-286`) to `unverified` does not alter any learner-visible state.  
  **Novice witness:** A beginner sees the same simultaneous term and answer whether an unseen metadata field says `pass` or `unverified`.

- **#16 — DROP.** An evidence matrix may discipline reviewers, but it does not itself change the essays’ literal order or learner interaction (`findings.md:83-96, 135-151`).  
  **Novice witness:** A beginner reading the unchanged essay still receives the authored answer immediately, regardless of whether a separate matrix marks that paragraph `FAIL`.

- **#22 — DROP.** The claimed reset is contradicted by the essay. It explicitly identifies the dashboard as the software version of the table problem (`essay-03-why-vibe-coding-drifts.md:29-33`), then applies failed obligation, repair, candidate sub-build, local fit, upper fit, and recomposition (`45-88`). Finding #21 captures the real defect: those moves are delivered rather than discovered.  
  **Novice witness:** A beginner can already reuse the table questions to reject a generic dashboard and select the assignment-summary panel; repeating the entire table history would add recital, not a new inference or choice.

No files were modified.

### Popper, Karl

**VERIFICATION POSITION**

**Lens:** Popper, Karl  
**Attack vector:** definitional and scope  
**Result:** 18 upheld; 4 refuted and dropped.

**Upheld**
- **1** — Source requires unresolved local residue, validation, and recomposition (`CRAFT-INITIAL-DEFINITION.md:435-449`); the teaching rule uses lifecycle complexity alone (`CRAFT-CODING-CLASS-SLIDE-SCHEMA.md:11-16`).
- **2** — Quantitative-looking entropy language lacks metrics; the source itself leaves measurement open (`CRAFT-INITIAL-DEFINITION.md:185-198, 544-555, 704-705`).
- **3** — “Example first” is temporal (`SLIDE-SCHEMA.md:32-35`), but the record contains only static content fields (`SLIDE-SCHEMA.yml:36-60`).
- **5** — S14 ends with lifecycle cards and reflection, without return or stopping behavior (`SLIDE-SCHEMA.md:289-302`).
- **6** — `draft_status: pass` and asserted validation have no executable receipts (`SLIDE-SCHEMA.yml:263-285`).
- **7** — YAML repeats both the complexity-only trigger and unsupported static-loop closure (`SLIDE-SCHEMA.yml:10-19, 250-284`).
- **8** — Focused Space advances reveal, then bubbles into slide navigation (`PRESENTATION.html:1151-1155, 1236-1240`); archive records reveal `0→1` plus navigation to slide 2 (`attacks.md:663-666`). **CRITICAL is sustained.**
- **9** — S02-S14 render term, question, and conclusion together; only S01 declares reveal states (`PRESENTATION.html:627, 1109-1129`).
- **10** — The finished table, later wobble, and substituted ornate table are not one caused history (`PRESENTATION.html:677-710, 713-735, 918-973`).
- **11** — The schema visual literally says the plan determines the valid table, contradicting the following plan slide (`PRESENTATION.html:654-675, 885-914`).
- **12** — Archived mobile evidence supports below-viewport content and missing notes state, while explicitly recording no horizontal overflow (`attacks.md:702-706`). **MINOR only.**
- **13** — “Will break” and “load-bearing” are interpretive assertions without novice evidence (`research.md:101-115, 141-151`).
- **14** — The research equates earlier placement with “earning” (`research.md:117-131`), without an observed learner decision.
- **15** — Every essay is assigned every framework obligation despite distinct trilogy roles (`findings.md:135-159`). **MINOR sustained.**
- **17–18** — Essay 1 names schema/artifact before a built mismatch and supplies the complete route; its later failures are hypothetical (`essay-01…md:55-75, 77-102`).
- **19–20** — Essay 2 immediately answers its pause and provides no before/after residue comparison (`essay-02…md:23-31, 74-82, 99-106`).
- **21** — Essay 3 defines schema, artifact, validation, and residue before presenting the bad dashboard pause (`essay-03…md:35-50`).

**Refuted And Dropped**
- **4** — The authority says repair locally **if local repair is enough** and otherwise promote missing schema (`CRAFT-INITIAL-DEFINITION.md:435-443`). It does not entail a mandatory failed repair attempt before every lower-layer trial.
- **16** — The prior artifact labels requirements and “Pass Condition,” but never claims the essays passed (`findings.md:135-159`). Missing adjudication is real; implied passage is not.
- **22** — Essay 3 explicitly identifies the dashboard as the software version of the table problem (`essay-03…md:29-33`). Requiring it to replay the entire physical history is a preferred redesign, not an evidenced defect.
- **Ordered request 4, insofar as it mandates failed local repair universally** — unsupported for the same reason as finding 4. Residue reduction, validation, and recomposition remain supported; universal repair-first sequencing does not.

No files were modified.
