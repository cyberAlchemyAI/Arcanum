# Craft Coding Class Slide Schema

Status: draft teaching schema
Date: 2026-07-07
Audience: absolute beginners with some vibe-coding experience
Source anchor: `CRAFT-INITIAL-DEFINITION.md`
Whisper preset: `veritasium` for live presentation, `veritasium-formal` for handout or essay

## Teaching Promise

By the end of the first class, students should understand this practical rule:

```text
If a step needs its own plan, tools, validation, and way back into the whole,
it has become its own craft layer.
```

The class should not begin with "schema", "data", "entropy", or "residue".
It should begin with a table, then walk the table through the Craft lifecycle:

```text
Define -> Research when needed -> Design -> Plan -> Execute -> Validate -> Reflect
```

Research is not a new universal phase in the formal six-step loop. In this
beginner deck it is made visible as the grounding move between definition and
design, because the initial definition lists research as an input when domain
information is missing.

## Beginner Constraints

- One new term per slide.
- Every term must be earned by a visible example first.
- Avoid category-theory language in the first presentation.
- Keep facilitator prompts in speaker notes, not on the projected slide.
- Translate `define` as "name the target and boundary".
- Translate `research` as "find the facts that would change the design".
- Translate `schema` as "the chosen shape of valid work" before naming it.
- Translate `artifact` as "the thing that actually exists" before naming it.
- Translate `validate` as "compare the artifact back to the schema".
- Translate `residue` as "what is left over when the result does not fully match the plan".
- Translate `SCU` as "the smallest responsible piece we can build and check".
- Translate `entropy` as "too many possible meanings still competing".
- Use vibe coding examples as recognition moments after the table lifecycle is established.

## Slide Object Schema

Each slide should be drafted with these fields.

```yaml
slide:
  id: CRAFT-INTRO-S##
  title: ""
  learner_question: ""
  visual: ""
  story_beat: ""
  new_term: ""
  concept_move: ""
  activity_or_prompt: ""
  speaker_note: ""
  validation_check: ""
  next_bridge: ""
```

| Field | Purpose |
| --- | --- |
| `id` | Stable slide handle for editing, review, and later HTML generation. |
| `title` | Short slide title, preferably concrete before abstract. |
| `learner_question` | The question students should be trying to answer. |
| `visual` | The image, diagram, code snippet, or object shown first. |
| `story_beat` | Where the slide sits in the simple-table to lifecycle-to-recursion arc. |
| `new_term` | At most one Craft term introduced on this slide. |
| `concept_move` | The exact abstraction the slide earns. |
| `activity_or_prompt` | What the teacher asks students to do or say. This belongs in speaker notes. |
| `speaker_note` | The live explanation in plain language. |
| `validation_check` | How the teacher knows the slide landed. |
| `next_bridge` | The sentence that carries the class into the next slide. |

## Deck Structure

### CRAFT-INTRO-S01: Look At This Table

```yaml
id: CRAFT-INTRO-S01
title: Look At This Table
learner_question: "What would you need before anyone builds?"
visual: "Plain table with a pause badge, then click-revealed buckets and examples."
story_beat: "Start with recognition and a short silent pause before clues."
new_term: ""
concept_move: "Even a familiar object has hidden requirements before it can be built."
activity_or_prompt: "Silent list for 15 seconds; then reveal buckets and examples."
speaker_note: "Hold the answer back. Let the room notice materials, tools, measurements, and steps."
validation_check: "Students name at least materials, tools, measurements, and steps."
next_bridge: "That list is raw material. Craft starts by defining what this object is supposed to become."
```

### CRAFT-INTRO-S02: Define The Object

```yaml
id: CRAFT-INTRO-S02
title: Define The Object
learner_question: "Which table are we actually talking about?"
visual: "Target card for a small work table with use, place, not-this, and next artifact."
story_beat: "Raw intent becomes a bounded target."
new_term: "define"
concept_move: "Define turns a wish into a named target with a boundary."
activity_or_prompt: "Ask what must be named before the table can be discussed responsibly."
speaker_note: "Use the initial definition closure condition: what, why, for whom, in what bounded space, and what artifact should exist next."
validation_check: "Students distinguish dining table, desk, coffee table, and work table."
next_bridge: "Now that the target is named, we still need facts before choosing the shape."
```

### CRAFT-INTRO-S03: Research Before Design

```yaml
id: CRAFT-INTRO-S03
title: Research Before Design
learner_question: "What do we need to learn before choosing?"
visual: "Research cards: room facts, material facts, example facts."
story_beat: "The target is grounded before the design hardens."
new_term: "research"
concept_move: "Research gathers evidence so the design is not just a guess."
activity_or_prompt: "Ask which facts would change the table design."
speaker_note: "Research here means grounding. It is the route when missing domain information would change the schema."
validation_check: "Students name at least two facts that would change the table design."
next_bridge: "Now the evidence can become a structure."
```

### CRAFT-INTRO-S04: Design The Schema

```yaml
id: CRAFT-INTRO-S04
title: Design The Schema
learner_question: "What structure will hold the target?"
visual: "Annotated table plan with material, size, joinery, and finish."
story_beat: "Research and definition become a chosen structure."
new_term: "schema"
concept_move: "The design becomes a schema: the chosen shape of valid work."
activity_or_prompt: "Point to one design choice the schema now fixes."
speaker_note: "Schema should feel practical: it is the chosen structure that makes the target buildable and checkable."
validation_check: "Students can say that the schema narrows which tables count as valid."
next_bridge: "A design is still not a build order. We need a plan."
```

### CRAFT-INTRO-S05: Plan The Build

```yaml
id: CRAFT-INTRO-S05
title: Plan The Build
learner_question: "What is the next executable piece?"
visual: "Plan card broken into measure, cut, join, finish, and check."
story_beat: "Design becomes staged work."
new_term: "plan"
concept_move: "Plan turns the design into ordered work with done checks."
activity_or_prompt: "Ask which step should happen first and what would prove it is done."
speaker_note: "Introduce the planning ladder gently: plan becomes waves, tasks, and smallest work units."
validation_check: "Students name a next step, input, output, and done check."
next_bridge: "Once a step is clear enough, someone can build."
```

### CRAFT-INTRO-S06: Build The Artifact

```yaml
id: CRAFT-INTRO-S06
title: Build The Artifact
learner_question: "What exists after the work runs?"
visual: "Plan compared with a finished simple table."
story_beat: "The schema/data relation becomes concrete."
new_term: "artifact"
concept_move: "The artifact is the thing produced from the schema and plan."
activity_or_prompt: "Ask what changed when the drawing became a physical table."
speaker_note: "The sketch cannot hold coffee. The artifact can, and now it can be inspected."
validation_check: "Students can distinguish the plan from the produced object."
next_bridge: "Now we compare the thing back to the shape that produced it."
```

### CRAFT-INTRO-S07: Validate The Match

```yaml
id: CRAFT-INTRO-S07
title: Validate The Match
learner_question: "Does the table match the design?"
visual: "Validation checklist: height, level, stable, fit."
story_beat: "The artifact is compared back to the schema."
new_term: "validate"
concept_move: "Validate means compare the artifact back to the schema."
activity_or_prompt: "Ask which check should run first."
speaker_note: "Validation is not a vibe. It is a comparison between the thing made and the structure chosen."
validation_check: "Students name concrete checks such as height, stability, level surface, and material match."
next_bridge: "Anything left over is not shame. It is information."
```

### CRAFT-INTRO-S08: Reflect On The Leftover

```yaml
id: CRAFT-INTRO-S08
title: Reflect On The Leftover
learner_question: "What does the leftover teach us?"
visual: "Wobbly table and broken login examples."
story_beat: "Validation creates a reflection moment."
new_term: "residue"
concept_move: "Residue is the mismatch or missing detail that tells us the next responsible move."
activity_or_prompt: "Name the leftover and route it: repair, research again, redesign, re-plan, or split a new layer."
speaker_note: "Residue is signal that the current layer may be missing information, structure, a check, a smaller unit, or a path back into the whole."
validation_check: "Students distinguish residue from total failure and name one next move."
next_bridge: "Sometimes the leftover is small. Sometimes it reveals a hidden project."
```

### CRAFT-INTRO-S09: Same Word, New Problem

```yaml
id: CRAFT-INTRO-S09
title: Same Word, New Problem
learner_question: "Would the same plan still be enough?"
visual: "Ornate table with intricate patterned legs."
story_beat: "A familiar word hides a new lifecycle."
new_term: ""
concept_move: "Complex objects hide smaller projects inside familiar words."
activity_or_prompt: "List the new hidden work."
speaker_note: "Let students feel that the ornate leg may need its own define, research, design, plan, build, validate, and reflect cycle."
validation_check: "Students identify that the leg design may need its own drawing, tools, practice, and checks."
next_bridge: "The leg is part of the table, but it may also need its own layer."
```

### CRAFT-INTRO-S10: A Step Becomes a Build

```yaml
id: CRAFT-INTRO-S10
title: A Step Becomes a Build
learner_question: "When does one step need its own cycle?"
visual: "Table plan branching into leg plan, carving plan, assembly plan, finish plan."
story_beat: "The lifecycle becomes recursive."
new_term: "craft layer"
concept_move: "If a part needs its own lifecycle and way back into the whole, it has become a craft layer."
activity_or_prompt: "Choose one hidden subproject and say what its own lifecycle would need."
speaker_note: "The layer is separate because the current step can no longer be responsibly handled as a single step inside the upper plan."
validation_check: "Students can say why 'make the legs' is too broad."
next_bridge: "Software hides the same kind of work inside feature names."
```

### CRAFT-INTRO-S11: Software Does This Too

```yaml
id: CRAFT-INTRO-S11
title: Software Does This Too
learner_question: "What is hiding inside 'login'?"
visual: "Student portal branching into login, profile, dashboard, assignments."
story_beat: "Transfer the recursive table model into software."
new_term: ""
concept_move: "A feature name can hide its own target, evidence, design, plan, checks, and residue."
activity_or_prompt: "Break login into fields, button, validation, error, session, redirect."
speaker_note: "Keep this grounded in what beginners have seen."
validation_check: "Students produce at least three smaller responsibilities under one feature."
next_bridge: "Now we need a way to choose how much work belongs in one responsible piece."
```

### CRAFT-INTRO-S12: Small Enough To Hold

```yaml
id: CRAFT-INTRO-S12
title: Small Enough To Hold
learner_question: "Which piece can we build and check?"
visual: "Too big / useful middle / too tiny diagram."
story_beat: "Introduce the balance point after recursion is visible."
new_term: "SCU"
concept_move: "An SCU is the smallest coherent unit that still carries responsibility."
activity_or_prompt: "Pick the responsible unit: whole app, login form, or one blue button."
speaker_note: "The useful middle is small enough to build and check, but large enough to fit back into the whole."
validation_check: "Students can reject both too-large and too-tiny units."
next_bridge: "When the unit is too loose, too many paths compete."
```

### CRAFT-INTRO-S13: Too Many Good Answers

```yaml
id: CRAFT-INTRO-S13
title: Too Many Good Answers
learner_question: "Why does the result drift?"
visual: "Vague dashboard prompt splitting into many plausible outputs."
story_beat: "Connect lifecycle discipline to vibe-coding drift."
new_term: "entropy"
concept_move: "Entropy is the uncertainty pressure created when too many meanings are still possible."
activity_or_prompt: "Make 'dashboard' less slippery: who uses it, what data, what actions, what done means."
speaker_note: "The AI has many plausible continuations; vague tasks let those continuations compete."
validation_check: "Students suggest constraints such as user, data, layout, actions, and success criteria."
next_bridge: "Craft is the method for routing that pressure instead of letting it drift."
```

### CRAFT-INTRO-S14: The Craft Rule

```yaml
id: CRAFT-INTRO-S14
title: The Craft Rule
learner_question: "What did we actually do?"
visual: "Craft loop cards: Define, Research, Design, Plan, Execute, Validate, Reflect on residue."
story_beat: "Recompose the table story into the Craft definition."
new_term: "Craft"
concept_move: "Craft searches for the next responsible schema/data layer: define, research when needed, design, plan, execute, validate, reflect."
activity_or_prompt: "Ask students to explain the loop using the simple table, ornate leg, or login example."
speaker_note: "Now the formal spine should feel earned: Craft is the recursive search for the next smallest coherent schema/data layer needed to translate intent into artifact with acceptable residue."
validation_check: "Students map intention, schema, artifact, residue, and next layer onto at least one example."
next_bridge: "Next class, we use this loop to build a small app without letting the plan disappear."
```

## Image Requirements

Required visuals:

1. Plain table with click-revealed requirements.
2. Defined table target.
3. Research board before design.
4. Table schema/design annotations.
5. Plan steps.
6. Artifact comparison.
7. Validation checklist.
8. Residue examples.
9. Ornate table.
10. Branching hidden subprojects.
11. Software feature breakdown.
12. SCU size comparison.
13. Vague prompt branching into multiple outputs.
14. Craft lifecycle recomposition.

The simple table and ornate table are still load-bearing. The lifecycle steps
between them are also load-bearing now; they prevent the deck from skipping
from object intuition directly into formal recursion.

## Essay Companion Schema

The essay should use the same sequence but fewer beats:

```text
1. The table is easy only after we define what table we mean.
2. Before design, we research the facts that would change the object.
3. A schema is the chosen shape of valid work.
4. A plan turns the schema into executable steps.
5. The artifact is the thing that exists.
6. Validation compares the artifact back to the schema.
7. Residue is the leftover that tells us the next move.
8. The ornate leg reveals when one step becomes its own craft layer.
9. Software features hide the same recursive lifecycle.
10. Craft is the loop that finds the next responsible schema/data layer.
```

Working title:

```text
The Table Is Not The Project
```

## Validation Checklist

- The first slide contains no formal Craft jargon.
- The first half of the deck walks the table through define, research, design/schema, plan, artifact, validate, and reflect/residue.
- Research appears before design, so the deck does not jump from wish to answer.
- Every formal term is preceded by a concrete example.
- No slide introduces more than one new term.
- Presenter prompts stay in speaker notes, not projected student-facing slide content.
- The ornate table appears only after the simple table lifecycle has created residue/reflection pressure.
- Vibe coding appears after the lifecycle and recursion pattern are established.
- Residue is framed as information, not failure.
- The final definition recomposes the whole story rather than appearing as a cold definition.

## Whisper Result

- Spell: whisper
- Transport: `explanatory_deep_dive_slide_schema`
- Objective: prepare the first coding-class presentation schema for Craft using a table-building story
- Target public: absolute beginners with some vibe-coding experience
- SCU cores: warm concrete teaching voice | beginner coding relevance | table lifecycle -> ornate recursion -> coding task -> Craft rule
- Candidate selected: `veritasium` for presentation, `veritasium-formal` for essay companion
- Composition plan: fourteen-slide schema plus essay companion schema
- Draft status: pass
- Validation: passes beginner constraint, concrete-before-abstract constraint, lifecycle-before-recursion constraint, one-term-per-slide constraint, and source-aligned Craft vocabulary constraint
- Learning residue: the deck must not skip Define/Research/Design before showing plan, artifact, validation, and residue; otherwise the table metaphor becomes a reveal trick instead of Craft.
- Next route: keep HTML presentation and YAML schema synchronized with this structure
