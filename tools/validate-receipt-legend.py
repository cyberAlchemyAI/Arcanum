#!/usr/bin/env python3
"""Validate the receipt-id-legend discipline: receipts that cite a tracked id must
gloss it inline.

Deterministic check for the RECEIPT-ID-LEGEND-CONSTITUTION
(framework/RECEIPT-ID-LEGEND-CONSTITUTION.md, rule `receipt-id.gloss-on-cite`).

A "tracked id" is a token like BLK-..., GAP-..., DEC-..., ENA-..., GATE-...,
CTX-..., TASK-..., SWU-..., or R-<scope>-<n>. For each cited id the file must
EITHER gloss it on the same line (an `id - meaning`, `id — meaning`, `id (meaning)`,
or `id: meaning` form, or a markdown link `[..](..)` on the line) OR define it
elsewhere in the same file (a line that introduces the id with a gloss).

Usage:
    python3 tools/validate-receipt-legend.py <file.md> [<file.md> ...]
    python3 tools/validate-receipt-legend.py --self-test

Exit: 0 = pass (all cited ids glossed), 4 = violations, 1 = usage/error.
"""

from __future__ import annotations

import re
import sys

# Tracked-id token: a known prefix + uppercase/-digit body, or R-<word>-<n>.
ID_RE = re.compile(
    r"\b("
    r"(?:BLK|GAP|DEC|ENA|GATE|CTX|TASK|SWU)-[A-Z0-9][A-Z0-9-]*"
    r"|R-[A-Z0-9]+-\d+"
    r")\b"
)

# A gloss on the same line: id followed by ` - `, ` — `, `: `, or ` (`, OR any md link on the line.
def line_glosses(line: str, idx_after_id: int, line_has_link: bool) -> bool:
    tail = line[idx_after_id:]
    # allow a closing markdown wrapper (backtick, *, _) before the gloss separator
    if re.match(r"[\s`*_]*(?:-|—|:|\()", tail):
        return True
    return line_has_link


def check_text(text: str) -> list[str]:
    lines = text.splitlines()
    # ids that are DEFINED somewhere with a gloss become known for the whole file.
    defined: set[str] = set()
    for line in lines:
        has_link = "](" in line
        for m in ID_RE.finditer(line):
            if line_glosses(line, m.end(), has_link):
                defined.add(m.group(1))

    violations: list[str] = []
    for n, line in enumerate(lines, 1):
        has_link = "](" in line
        for m in ID_RE.finditer(line):
            tid = m.group(1)
            if tid in defined:
                continue
            if not line_glosses(line, m.end(), has_link):
                violations.append(f"line {n}: cited id `{tid}` has no inline gloss or definition")
    return violations


def run_files(paths: list[str]) -> int:
    any_bad = False
    for p in paths:
        try:
            text = open(p, encoding="utf-8").read()
        except OSError as e:
            print(f"ERROR: cannot read {p}: {e}")
            return 1
        v = check_text(text)
        if v:
            any_bad = True
            print(f"VALIDATION=block  {p}")
            for line in v:
                print(f"  BLOCK: {line}")
        else:
            print(f"VALIDATION=pass  {p}")
    return 4 if any_bad else 0


def self_test() -> int:
    ok = "Active blockers: `BLK-TDE-AUTH-001` - auth round-trip fails on dialect drift; `GAP-X-002` (emit bodies are stubs)."
    bad = "Active blockers: BLK-TDE-AUTH-001, BLK-TDE-GATE-002"
    a = check_text(ok)
    b = check_text(bad)
    passed = (a == [] and len(b) >= 2)
    print("SELF-TEST=pass" if passed else "SELF-TEST=fail")
    print(f"  glossed receipt violations: {len(a)} (expect 0)")
    print(f"  bare receipt violations: {len(b)} (expect >=2)")
    return 0 if passed else 4


def main(argv: list[str]) -> int:
    args = argv[1:]
    if not args:
        print(__doc__)
        return 1
    if args[0] == "--self-test":
        return self_test()
    return run_files(args)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
