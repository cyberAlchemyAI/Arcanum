# Forward Test: revise with explicit authorization

Use the canonical `evidence-grounded-diagrams` skill in `revise` mode.
Correction is explicitly authorized. Review and revise the exact `r0001`
bundle from the forward create run; preserve it and persist `r0002` under the
same output root.

Existing permitted evidence:

- `POL-12 §3`: the reviewer receives a draft and approves or requests changes;
- `POL-12 §4`: after changes are requested, the author sends a new version to
  review;
- `OPS-7 line 18`: approval ends review for that version.

New permitted evidence:

- `POL-12 §5`: after review ends by approval, the archive service records that
  approved version as reviewed.

Reader question: "Como uma versão de documento percorre a revisão e é
registrada após aprovação?"

Add only the smallest supported post-approval step. Preserve the review receipt
and report its stable path or handle. A Mermaid source-only draft is acceptable
when no renderer is available.
