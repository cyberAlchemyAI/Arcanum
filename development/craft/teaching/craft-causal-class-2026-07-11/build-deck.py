#!/usr/bin/env python3
import hashlib
import json
from html import escape
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
    output_html = TEMPLATE.read_text(encoding="utf-8")
    output_html = output_html.replace("__DECK_DATA__", payload)
    output_html = output_html.replace("__DECK_SHA__", digest)
    output_html = output_html.replace("__DECK_TITLE__", escape(deck["title"]))
    output_html = output_html.replace("__DECK_SUBTITLE__", escape(deck["subtitle"]))
    output_html = output_html.replace("__SLIDE_COUNT__", str(len(deck["slides"])))
    if any(marker in output_html for marker in (
        "__DECK_DATA__",
        "__DECK_SHA__",
        "__DECK_TITLE__",
        "__DECK_SUBTITLE__",
        "__SLIDE_COUNT__",
    )):
        raise SystemExit("template placeholders were not replaced")
    OUTPUT.write_text(output_html, encoding="utf-8")
    print(f"built {OUTPUT.name}: {len(deck['slides'])} slides, sha256 {digest}")


if __name__ == "__main__":
    main()
