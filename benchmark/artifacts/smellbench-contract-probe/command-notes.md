# SmellBench Contract Probe Command Notes

## Zenodo Artifact

Command:

```bash
curl -L --max-time 20 -sS https://zenodo.org/api/records/19247588
```

Result: pass.

Observed:

- Record ID: `19247588`
- DOI: `10.5281/zenodo.19247588`
- Title: `SmellBench: Evaluating LLM Agents on Architectural Code Smell Repair - ExperimentsReproductionPackage`
- Access: open
- Resource type: software
- License: `cc-by-4.0`
- File: `ExperimentsReproductionPackage.7z`
- Size: `6310819`
- Published checksum: `md5:87c00f711c74fc48f85b2cafb35a5cd6`

## Download And Checksum

Command:

```bash
curl -L --max-time 60 -o artifacts/smellbench-contract-probe/ExperimentsReproductionPackage.7z https://zenodo.org/api/records/19247588/files/ExperimentsReproductionPackage.7z/content
md5sum artifacts/smellbench-contract-probe/ExperimentsReproductionPackage.7z
```

Result: pass.

Observed checksum:

```text
87c00f711c74fc48f85b2cafb35a5cd6  artifacts/smellbench-contract-probe/ExperimentsReproductionPackage.7z
```

## Extraction

Local extractor setup:

```bash
python3 -m pip install --target /tmp/smellbench-probe-pydeps py7zr
```

Command:

```bash
PYTHONPATH=/tmp/smellbench-probe-pydeps python3 -m py7zr x artifacts/smellbench-contract-probe/ExperimentsReproductionPackage.7z artifacts/smellbench-contract-probe/extracted
```

Result: pass.

Extracted components:

- `python_smells_detector/`
- `Dataset Builder/`
- `Codex Mcp Container/`
- `Codex Scheduler/`
- `Code Smell Evaluator/`

## Evaluator Verification

Local dependency setup:

```bash
python3 -m pip install --target /tmp/smellbench-eval-pydeps -r 'artifacts/smellbench-contract-probe/extracted/ExperimentsReproductionPackage/Code Smell Evaluator/requirements.txt'
```

Command:

```bash
PYTHONPATH=/tmp/smellbench-eval-pydeps MPLCONFIGDIR=/tmp/smellbench-mpl-cache python3 generate_cross_comparison.py
```

Working directory:

```text
artifacts/smellbench-contract-probe/extracted/ExperimentsReproductionPackage/Code Smell Evaluator
```

Result: pass.

Generated:

```text
evaluation_reports/cross_agent_comparison_20260525_152420.xlsx
```

Top leaderboard row:

```text
#1 GPT 5.3 Spark 0.4784 (repair=0.383 fp=0.891 partial=0.353)
```

Warnings:

- `numpy` emitted `RuntimeWarning: invalid value encountered in divide` during correlation calculations. The evaluator still completed and wrote the Excel report.

## Contract Outcome

`SWU-HARNESS-007A` passes. The next blocker is not the upstream SmellBench contract; it is the missing harness-local agent candidate and smoke adapter required by `SWU-HARNESS-007B`.
