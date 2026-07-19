#!/usr/bin/env python3

import json
import re
import subprocess
from pathlib import Path


PACKAGE = Path(__file__).resolve().parent
REPO = PACKAGE.parents[4]
BUILDER = REPO / "arcanum/spells/whisper/tools/build-whisper-review-html.py"
DRAFT = PACKAGE / "VOICE-AUDITION.md"
SCHEMA = PACKAGE / "whisper-review-substrate.yml"
OUTPUT = PACKAGE / "audition-review.html"

PARTS = {
    "p001": ("opening", "curiosity gap and concrete contradiction"),
    "p002": ("opening", "curiosity gap and concrete contradiction"),
    "p003": ("opening", "curiosity gap and concrete contradiction"),
    "p004": ("tension", "local correctness versus failed intent"),
    "p005": ("tension", "local correctness versus failed intent"),
    "p006": ("tension", "local correctness versus failed intent"),
    "p007": ("tension", "local correctness versus failed intent"),
    "p008": ("reveal", "making as testable learning and governed recursion"),
    "p009": ("reveal", "making as testable learning and governed recursion"),
    "p010": ("reveal", "making as testable learning and governed recursion"),
}


def main() -> None:
    subprocess.run(
        [
            "python3",
            str(BUILDER),
            "--schema",
            str(SCHEMA),
            "--draft",
            str(DRAFT),
            "--output",
            str(OUTPUT),
        ],
        cwd=REPO,
        check=True,
    )

    document = OUTPUT.read_text()
    data_match = re.search(
        r'(<script id="whisper-review-data" type="application/json">)(.*?)(</script>)',
        document,
        flags=re.DOTALL,
    )
    if not data_match:
        raise RuntimeError("Whisper review data block was not found")

    data = json.loads(data_match.group(2))
    block_ids = {block["block_id"] for block in data["blocks"]}
    if block_ids != set(PARTS):
        raise RuntimeError(f"Unexpected review blocks: {sorted(block_ids)}")

    for block in data["blocks"]:
        block["part_id"], block["role"] = PARTS[block["block_id"]]

    encoded = json.dumps(data, indent=2, ensure_ascii=True)
    document = (
        document[: data_match.start(2)]
        + encoded
        + document[data_match.end(2) :]
    )

    for block_id, (part_id, _) in PARTS.items():
        section_pattern = re.compile(
            rf'(<section class="review-block"[^>]*data-block-id="{block_id}".*?</section>)',
            flags=re.DOTALL,
        )
        section_match = section_pattern.search(document)
        if not section_match:
            raise RuntimeError(f"Review section {block_id} was not found")
        section = section_match.group(1)
        section = re.sub(r'data-part-id="[^"]+"', f'data-part-id="{part_id}"', section, count=1)
        section = re.sub(
            r'<span class="part-id">[^<]+</span>',
            f'<span class="part-id">{part_id}</span>',
            section,
            count=1,
        )
        document = document[: section_match.start()] + section + document[section_match.end() :]

    document = document.replace(
        "<head>",
        '<head>\n  <link rel="icon" href="data:,">',
        1,
    )
    OUTPUT.write_text(document)
    print(f"WROTE {OUTPUT.relative_to(REPO)}")
    print("PARTS opening=3 tension=4 reveal=3")


if __name__ == "__main__":
    main()
