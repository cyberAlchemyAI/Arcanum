#!/usr/bin/env python3
import hashlib
import json
from html.parser import HTMLParser
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parent
SCHEMA = ROOT / "CRAFT-CAUSAL-CLASS-SLIDE-SCHEMA.yml"
HTML = ROOT / "CRAFT-CAUSAL-CLASS-PRESENTATION.html"
FORBIDDEN_PROJECTED_PHRASES = {
    "start with the table",
    "generic object becomes a bounded target",
    "candidate responsibility",
    "upper validation",
    "story state",
    "consequence",
}
EXPECTED_SLIDE_IDS = [f"CRAFT-CAUSAL-S{index:02d}" for index in range(1, 6)]
LATER_LESSON_TERMS = {
    "artifact",
    "validation",
    "residue",
    "craft layer",
    "recomposition",
}


class DeckParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_data = False
        self.data_chunks = []
        self.digest = None

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if tag == "script" and values.get("id") == "deck-data":
            self.in_data = True
        if tag == "meta" and values.get("name") == "deck-data-sha256":
            self.digest = values.get("content")

    def handle_endtag(self, tag):
        if tag == "script" and self.in_data:
            self.in_data = False

    def handle_data(self, data):
        if self.in_data:
            self.data_chunks.append(data)


def main():
    source = yaml.safe_load(SCHEMA.read_text(encoding="utf-8"))
    deck = source["deck"]
    parser = DeckParser()
    parser.feed(HTML.read_text(encoding="utf-8"))
    embedded = json.loads("".join(parser.data_chunks))
    if embedded != deck:
        raise SystemExit("HTML deck data differs from YAML authority")

    canonical = json.dumps(deck, ensure_ascii=True, separators=(",", ":"))
    digest = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    if parser.digest != digest:
        raise SystemExit("HTML deck digest differs from YAML authority")

    slide_ids = [slide["id"] for slide in deck["slides"]]
    if slide_ids != EXPECTED_SLIDE_IDS:
        raise SystemExit("first presentation must contain exactly slides S01 through S05")
    if len(slide_ids) != len(set(slide_ids)):
        raise SystemExit("duplicate slide id")

    if deck.get("formal_terms") != ["schema"]:
        raise SystemExit("first presentation must earn only schema")

    earned_terms = [
        (slide["id"], state["id"], state.get("earned_term"))
        for slide in deck["slides"]
        for state in slide["states"]
        if state.get("earned_term") is not None
    ]
    expected_earned_terms = [("CRAFT-CAUSAL-S03", "S03-SCHEMA", "schema")]
    if earned_terms != expected_earned_terms:
        raise SystemExit("schema must be earned once, in the final state of slide S03")

    opening = deck["slides"][0]
    opening_states = [state["visual_state"] for state in opening["states"]]
    if opening["visual"] != "table-question":
        raise SystemExit("the first slide must frame the table-building question")
    if opening_states != ["table", "cloud", "gathered"]:
        raise SystemExit("opening interaction must follow table -> cloud -> gathered")

    cloud_states = [
        (slide["id"], state["id"])
        for slide in deck["slides"]
        for state in slide["states"]
        if state["visual_state"] == "cloud"
    ]
    if cloud_states != [("CRAFT-CAUSAL-S01", "S01-CLOUD")]:
        raise SystemExit("the Mentimeter word cloud must appear once, on slide S01")

    surfaces = deck.get("surface_contract", {})
    if surfaces.get("authoring_metadata_may_be_projected") is not False:
        raise SystemExit("surface contract must forbid projecting authoring metadata")

    state_count = 0
    for slide in deck["slides"]:
        projected_slide = slide["title"].lower()
        if len(slide["title"].split()) > 10:
            raise SystemExit(f"projected title is too long in {slide['id']}")
        states = slide["states"]
        state_ids = [state["id"] for state in states]
        if len(state_ids) != len(set(state_ids)):
            raise SystemExit(f"duplicate state id in {slide['id']}")
        for index, state in enumerate(states):
            state_count += 1
            projected_state = " ".join(
                [state["learner_prompt"], *[str(item) for item in state["visible"]]]
            ).lower()
            projected = f"{projected_slide} {projected_state}"
            leaked_later_terms = sorted(term for term in LATER_LESSON_TERMS if term in projected)
            if leaked_later_terms:
                raise SystemExit(
                    f"later-lesson term leaked into {state['id']}: {', '.join(leaked_later_terms)}"
                )
            leaked = [phrase for phrase in FORBIDDEN_PROJECTED_PHRASES if phrase in projected]
            if leaked:
                raise SystemExit(f"authoring language leaked into {state['id']}: {', '.join(leaked)}")
            target = state["transition_to"]
            expected = states[index + 1]["id"] if index + 1 < len(states) else None
            if target != expected:
                raise SystemExit(f"non-linear or broken transition in {state['id']}")
            term = state.get("earned_term")
            if term is not None and term not in deck["formal_terms"]:
                raise SystemExit(f"undeclared formal term {term}")

    print(f"package OK: {len(slide_ids)} slides, {state_count} states, sha256 {digest}")


if __name__ == "__main__":
    main()
