# The Dashboard That Looked Finished

"Make me a student dashboard" can produce a polished screen in seconds.

One version arrives with statistic cards, a blue chart, a sidebar, and a table
of recent activity. Another shows assignments, colored due dates, and a filter
for classes. Both look like software. Both look finished.

Then a student asks one ordinary question:

What do I need to do before tomorrow?

The chart cannot answer. It shows activity without showing the next action. The
assignment screen gets closer, but overdue work is hidden and assignments
returned by a teacher are mixed in with completed work.

Neither screen is ugly. Neither is random. "Student dashboard" simply allowed
several plausible answers, and we never chose which answer the student needed.

The table gives us a way back.

This user is a student checking work at the end of the day. The important data
is the class, due date, submission state, and teacher return state. The useful
actions are opening an assignment, filtering by class, and finding unfinished
work. The screen succeeds when the student can see what is due next, what is
overdue, and what came back for revision without asking someone to explain it.

Those promises create a shape we can build and test. They do not describe every
future part of the portal. They describe one useful piece: an assignment
summary panel.

The whole portal is too large for one inspectable move. A single blue button is
too small to answer the student's question. The panel sits between them. It has
one clear job, enough data to do it, actions the student needs, and checks that
connect it back to the larger application.

The generated panel now shows "Due next," "Overdue," and "Returned for
revision." A student can open an assignment or filter by class. With sample
data in place, the same question runs again.

What is due next? Visible.

What is overdue? Visible and separate.

What came back from the teacher? Visible with a revision label.

The panel works on its own, and its links return to the correct place in the
portal. The smaller build recomposes into the larger one.

One mismatch remains. Assignments due at midnight appear under the wrong day
for students in another time zone. This time the boundary does not need to
change. The mismatch points to a local date-handling repair, so that is where
the work goes next.

This is the useful correction to vibe coding. The AI is not expected to read
our minds, and a fast first result is not expected to be final. We keep the
promise visible, build something reality can challenge, find the exact
mismatch, and let that mismatch choose the next move.

Sometimes the next move is a small repair. Sometimes the promise itself needs
revision. Sometimes one overloaded step must become a craft layer with its own
checks and a way back into the whole.

That way of working is **Craft**.

Craft does not make every first result correct. It makes the next responsible
move easier to see.
