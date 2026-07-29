# Experiment Prompt: sigil-new-low

Run the target sigil through the sigil-development experiment profile.

## Target Artifact

arcanum/formulae/html-preview-server

## Contract

arcanum/formulae/html-preview-server/SKILL.md

## Lifecycle Owner

sigil-development

## User Request

Use Sigil Development to review a new Formulae sigil for the request “open this
exact local HTML file in the server.” Require direct loopback startup, exact URL
verification, browser handoff, a fixed receipt, and no repository-wide inspection.
Return the full user-facing Sigil Development result body. Do not summarize that
you saved an output file.

## Required Capture

Save only the final artifact result body to `development/example-outputs/sigil-new-low.output.md`.
