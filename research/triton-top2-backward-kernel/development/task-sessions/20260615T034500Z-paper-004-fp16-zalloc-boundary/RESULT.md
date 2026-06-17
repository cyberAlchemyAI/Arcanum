# Result - SWU-PAPER-004 FP16 And CAP2 Zero-Allocation Boundary

Status: `complete`

Changed:

- Added `NC-012` for FP16 empirical tolerance versus formal FP16 proof.
- Added `NC-013` for CAP2 zero-allocation acceptance remaining open.
- Added `FP16 And Allocation Boundary` to `DATA-APPENDIX.md`.
- Added matching boundary prose to the paper implementation and limitations sections.

Validation:

- Marker search confirmed `NC-012`, `NC-013`, `FP16 And Allocation Boundary`, `formal FP16 numerical equivalence`, and `full-CAP2 zero-allocation proof` are present.
- Task evidence JSON validates with `python3 -m json.tool`.
