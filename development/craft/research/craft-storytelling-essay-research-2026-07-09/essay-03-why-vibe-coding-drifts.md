# Why Vibe Coding Drifts

Status: draft essay
Whisper transport: presentation companion essay
Deck range: `CRAFT-INTRO-S11` through `CRAFT-INTRO-S14`
Source substrate: `findings.md`

"Make me a dashboard" sounds like a request.

To an AI, it is closer to a fog bank.

A dashboard for whom? A teacher? A student? A manager? A developer? What data
does it show? Grades, sales, server errors, class attendance, project health?
What can the user do there? Filter, export, approve, comment, assign, compare?
What should happen when there is no data? What counts as done?

If those answers are missing, the model still has to continue. It will produce
something plausible because plausibility is easy when the target is loose. A
header, a few cards, a chart, a sidebar, a table. It may look good. It may even
look like the thing people expect when they hear "dashboard."

And still be wrong.

This is why vibe coding drifts. Not because the AI is bad. Not because the user
is foolish. Drift happens because a vague feature name contains too many valid
worlds. The translator has not been given a chosen shape of valid work, so many
possible meanings compete.

That is the software version of the table problem.

"Table" felt obvious until we had to build one. "Dashboard" feels obvious until
we have to decide who uses it, what data it carries, what actions it supports,
what validation proves it works, and how it fits into the larger app.

Craft does not solve this by saying "write better prompts." That is too shallow.
Prompt clarity helps, but Craft is deeper than prompt polish. Craft asks what
schema/data translation is happening.

The schema is the chosen structure that makes the intent legible enough to
produce valid work. The artifact is the thing that actually exists: the generated
screen, the component, the route, the behavior, the test result. Validation
compares the artifact back to the chosen structure. Residue is what remains when
the result does not fully match the shape we chose.

So the learner starts with the bad dashboard.

It has charts, but not the right charts. It has a table, but no useful action.
It looks complete, but nobody knows whether it helps the user. This is the pause.
The learner should feel the same recognition as the table slide: "I thought I
knew what I asked for, but now I can see the missing structure."

Now constrain the work.

This dashboard is for a student checking assignments. It shows due soon, overdue,
submitted, and graded work. The student can open an assignment, filter by class,
and see what needs action today. The empty state tells them they are caught up.
Validation means a student can answer three questions without explanation: what
is due next, what is overdue, and what did the teacher return?

That is not just a better prompt. It is a small schema.

Now the artifact can be judged. Does the screen show the right groups? Does the
filter work? Is the empty state clear? Can a student find the next action? Does
the route connect to the rest of the student portal? If not, the leftover is
residue.

Some residue is local. A label is unclear. A card is too crowded. The empty
state is missing. Repair it.

Some residue says the schema was incomplete. Maybe students need assignment
status definitions before the dashboard can be valid. Research and define.

Some residue says the unit is too large. "Student dashboard" may contain
assignment summary, grade trend, messages, class switcher, and notifications.
Trying to build all of that at once gives the translator too many relations to
preserve. Split a responsible piece.

But do not split blindly.

The smallest coherent unit is not the smallest possible task. A single blue
button may be too tiny to mean anything by itself. The whole dashboard may be too
large to build and check responsibly. The useful middle might be "assignment
summary panel": one user, one data shape, one action surface, clear validation,
and a path back into the dashboard.

That path back matters. If the assignment panel works alone but cannot connect
to the student portal, the work has recomposition residue. Craft cares about the
piece and the whole.

This is the real correction to vibe coding.

Vibe coding often jumps from intent to artifact: "make me a dashboard" becomes a
screen. Craft inserts the missing discipline:

Name the target. Find facts that would change the design. Choose the shape of
valid work. Build the smallest responsible piece. Validate the artifact. Route
the residue. Recompose the result into the whole.

The AI is still useful. In fact, it becomes more useful. A model can generate,
compare, revise, and explore quickly. But speed without a chosen structure only
multiplies plausible wrong answers. Craft turns speed into learning by giving
each output a way to be checked.

The point is not to remove uncertainty. The point is to make uncertainty visible
soon enough to route it.

That is why the final Craft rule matters:

Craft is not making the work smaller; it is finding the next smallest coherent
schema/data layer whose artifact can be validated, whose residue can be routed,
and whose result can recompose into the whole.

A vague prompt asks the model to guess the world.

Craft builds the world one responsible layer at a time.
