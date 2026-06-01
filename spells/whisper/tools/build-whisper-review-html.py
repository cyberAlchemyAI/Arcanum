#!/usr/bin/env python3
"""Build a commentable Whisper draft review HTML from a Markdown draft."""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
from dataclasses import dataclass
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover - environment guard
    yaml = None


@dataclass
class Paragraph:
    text: str
    source_line: int


def repo_relative(path: Path) -> str:
    try:
        root = Path(__file__).resolve().parents[3]
        return str(path.resolve().relative_to(root))
    except ValueError:
        return str(path)


def load_schema(path: Path | None) -> dict:
    if path is None:
        return {}
    if yaml is None:
        raise RuntimeError("PyYAML is required to read the Whisper schema.")
    loaded = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(loaded, dict):
        raise RuntimeError(f"Schema did not parse as a mapping: {path}")
    return loaded.get("text_intent_substrate", loaded)


def parse_markdown(path: Path) -> tuple[str, list[Paragraph]]:
    title = path.stem
    paragraphs: list[Paragraph] = []
    current: list[str] = []
    start_line = 1
    in_code = False

    def flush() -> None:
        nonlocal current, start_line
        if current:
            paragraphs.append(Paragraph(" ".join(current).strip(), start_line))
            current = []

    for line_no, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        line = raw.strip()
        if line.startswith("```"):
            flush()
            in_code = not in_code
            continue
        if in_code:
            continue
        if not line:
            flush()
            continue
        if line.startswith("# "):
            flush()
            title = line[2:].strip()
            continue
        if line.startswith("#"):
            flush()
            continue
        if not current:
            start_line = line_no
        current.append(line)

    flush()
    return title, paragraphs


def inline_markdown(text: str) -> str:
    escaped = html.escape(text)
    escaped = re.sub(r"`([^`]+)`", r"<code>\1</code>", escaped)
    escaped = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", escaped)
    escaped = re.sub(r"\*([^*]+)\*", r"<em>\1</em>", escaped)
    return escaped


def part_role(schema: dict, part_id: str) -> str:
    for part in schema.get("composition_parts", {}).get("parts", []):
        if part.get("part_id") == part_id:
            return str(part.get("role", "part"))
    return "part"


def infer_part_id(text: str, index: int, total: int) -> str:
    lower = text.lower()
    if index <= 2:
        return "reader_grounded_opening_hook"
    if "harari" in lower or "sapiens" in lower:
        return "harari_shared_fiction_bridge"
    if "generative ai changes" in lower or "workbench" in lower:
        return "research_context_generative_ai_changes_who_can_operate_on_language"
    if "new possibility" in lower or "natural language replaces engineering" in lower:
        return "core_insight_language_becomes_executable_through_ai"
    if lower.startswith("if that is true") or lower.startswith("start there") or index >= total - 1:
        return "invitation_to_name_a_workflow"
    if "danger" in lower or "private jargon" in lower or "this is the power" in lower:
        return "implications_for_personal_code"
    if "arcanum" in lower or "alias" in lower or "schema" in lower or "meta-schema" in lower:
        return "arcanum_example_aliases_sigils_schemas"
    if index < total / 2:
        return "core_insight_language_becomes_executable_through_ai"
    return "implications_for_personal_code"


def build_article(title: str, paragraphs: list[Paragraph], schema: dict) -> tuple[str, list[dict]]:
    blocks: list[dict] = []
    article_parts = [f"<h1>{inline_markdown(title)}</h1>"]

    for idx, paragraph in enumerate(paragraphs, start=1):
        block_id = f"p{idx:03d}"
        part_id = infer_part_id(paragraph.text, idx, len(paragraphs))
        role = part_role(schema, part_id)
        blocks.append(
            {
                "block_id": block_id,
                "part_id": part_id,
                "role": role,
                "paragraph_index": idx,
                "source_line": paragraph.source_line,
                "text": paragraph.text,
            }
        )
        article_parts.append(
            "\n".join(
                [
                    f'<section class="review-block" data-review-block data-block-id="{block_id}" '
                    f'data-part-id="{html.escape(part_id)}" tabindex="0">',
                    '  <div class="block-meta">',
                    f'    <span class="block-id">{block_id}</span>',
                    f'    <span class="part-id">{html.escape(part_id)}</span>',
                    f'    <span>line {paragraph.source_line}</span>',
                    "  </div>",
                    '  <div class="block-body">',
                    f"    <p>{inline_markdown(paragraph.text)}</p>",
                    '    <div class="block-actions">',
                    '      <button type="button" data-add-comment>Comment</button>',
                    f'      <span class="comment-count" data-comment-count="{block_id}">0</span>',
                    "    </div>",
                    "  </div>",
                    "</section>",
                ]
            )
        )

    return "\n".join(article_parts), blocks


def build_review_data(draft: Path, schema_path: Path | None, schema: dict, title: str, blocks: list[dict]) -> dict:
    draft_hash = hashlib.sha256(draft.read_bytes()).hexdigest()[:12]
    draft_id = draft.stem
    selected = (
        schema.get("pareto_tournament", {})
        .get("consensus", {})
        .get("selected_candidate_set", "")
    )
    return {
        "review_id": f"{draft_id}-{draft_hash}",
        "transport": schema.get("transport_schema", {}).get("transport_id", "unknown"),
        "draft": {
            "id": draft_id,
            "title": title,
            "path": repo_relative(draft),
            "sha256_12": draft_hash,
        },
        "schema": {
            "path": repo_relative(schema_path) if schema_path else None,
            "substrate_version": schema.get("metadata", {}).get("substrate_version"),
        },
        "pareto": {
            "tiering": schema.get("pareto_tournament", {}).get("tiering"),
            "selected_candidate": selected,
            "objectives": [item.get("id") for item in schema.get("pareto_tournament", {}).get("objectives", [])],
            "hard_gates": [item.get("id") for item in schema.get("pareto_tournament", {}).get("hard_gates", [])],
        },
        "blocks": blocks,
    }


def render(template: str, article_html: str, review_data: dict) -> str:
    data_json = json.dumps(review_data, ensure_ascii=True, indent=2).replace("</", "<\\/")
    return (
        template.replace("__WHISPER_REVIEW_DATA_JSON__", data_json)
        .replace("__WHISPER_REVIEW_ARTICLE_HTML__", article_html)
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--draft", required=True, type=Path)
    parser.add_argument("--schema", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument(
        "--template",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "templates" / "draft-review-base.html",
    )
    args = parser.parse_args()

    draft = args.draft
    schema_path = args.schema
    output = args.output or draft.with_suffix(".review.html")

    schema = load_schema(schema_path)
    title, paragraphs = parse_markdown(draft)
    article_html, blocks = build_article(title, paragraphs, schema)
    review_data = build_review_data(draft, schema_path, schema, title, blocks)
    html_text = render(args.template.read_text(encoding="utf-8"), article_html, review_data)

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(html_text, encoding="utf-8")
    print(f"WROTE {output}")
    print(f"BLOCKS {len(blocks)}")
    print(f"REVIEW_ID {review_data['review_id']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
