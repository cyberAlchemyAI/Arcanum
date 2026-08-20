#!/usr/bin/env python3
"""Validate the Invoke ontology package with the canonical Ontology Vault validator."""

from pathlib import Path
import subprocess
import sys


ARCANUM_ROOT = Path(__file__).resolve().parents[3]
VALIDATOR = ARCANUM_ROOT / "arcana/ontology-vault/scripts/ontology_package.py"


raise SystemExit(
    subprocess.call(
        [
            sys.executable,
            str(VALIDATOR),
            "validate-package",
            "--package-root",
            str(Path(__file__).resolve().parents[1]),
            "--repository-root",
            str(ARCANUM_ROOT),
            *sys.argv[1:],
        ]
    )
)
