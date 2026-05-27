# Artifact Authoring Memory

Status: durable repository memory
Date: 2026-05-27
Owner: Artifact Constitution

## Chart Line Breaks

When creating charts or visual artifacts, do not use literal `\n` sequences for
line breaks in labels, titles, legends, annotations, or tooltips.

Use HTML markup such as `<br>` or the renderer's structured rich-text support
instead. The goal is to make line breaks survive browser rendering, screenshots,
exports, and downstream artifact validation.

This rule is also recorded in [ARTIFACT-CONSTITUTION.md](ARTIFACT-CONSTITUTION.md).
