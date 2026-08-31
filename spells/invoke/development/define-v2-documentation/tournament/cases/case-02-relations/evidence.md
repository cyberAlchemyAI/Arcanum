# Validation Gate

A definition validation gate is a bounded check that must pass before a
candidate definition bundle can be handed to its next route.

# Candidate Bundle

A candidate definition bundle is the complete generated set of machine and
human views produced from one valid Define source. It depends on the validation
gate and remains authority-free.

# Layering Decision

The minimum coherent implementation unit is one source, one atomic compiler
run, and one complete output bundle.
