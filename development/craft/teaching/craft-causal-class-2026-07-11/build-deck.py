#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parent
SCHEMA = ROOT / "CRAFT-CAUSAL-CLASS-SLIDE-SCHEMA.yml"
TEMPLATE = ROOT / "presentation.template.html"
OUTPUT = ROOT / "CRAFT-CAUSAL-CLASS-PRESENTATION.html"


def main():
    source = yaml.safe_load(SCHEMA.read_text(encoding="utf-8"))
    deck = source["deck"]
    payload = json.dumps(deck, ensure_ascii=True, separators=(",", ":"))
    digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()
    html = TEMPLATE.read_text(encoding="utf-8")
    html = html.replace("__DECK_DATA__", payload)
    html = html.replace("__DECK_SHA__", digest)
    if "__DECK_DATA__" in html or "__DECK_SHA__" in html:
        raise SystemExit("template placeholders were not replaced")
    OUTPUT.write_text(html, encoding="utf-8")
    print(f"built {OUTPUT.name}: {len(deck['slides'])} slides, sha256 {digest}")


if __name__ == "__main__":
    main()

