# Whisper Draft Review HTML

Whisper draft review pages turn a Markdown draft into paragraph-level review blocks with stable IDs, part bindings, local comments, and an agent payload that can be extracted by Playwright.

## Build

```bash
python3 spells/whisper/tools/build-whisper-review-html.py \
  --schema spells/whisper/development/refinement-runs/20260526T204134Z-language-ai-substack/text-intent-substrate.yaml \
  --draft spells/whisper/development/refinement-runs/20260526T204134Z-language-ai-substack/DRAFT-SUBSTACK-002.md \
  --output spells/whisper/development/refinement-runs/20260526T204134Z-language-ai-substack/DRAFT-SUBSTACK-002.review.html
```

## Review Loop

1. Open the generated `.review.html`.
2. Select a paragraph or text span and add comments.
3. Export the agent payload through the page or with Playwright.
4. Use the payload as the next Whisper revision input.

## Playwright Extraction

```bash
python3 -m http.server 8765
CODEX_HOME=/mnt/c/Users/vlad_/.codex \
  spells/whisper/tools/extract-whisper-review-payload.sh \
  http://127.0.0.1:8765/spells/whisper/development/refinement-runs/20260526T204134Z-language-ai-substack/DRAFT-SUBSTACK-002.review.html \
  /tmp/whisper-review-payload.json
```

The extracted payload contains `block_id`, `part_id`, selected text, issue type, request type, priority, comment text, and the original block text.
