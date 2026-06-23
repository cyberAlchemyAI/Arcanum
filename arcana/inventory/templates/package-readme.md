# Inventory Package

This package is the repository-local compiled knowledge layer.

Raw sources are read-only inputs. Generated inventory pages are maintained by the agent according to [schema.md](schema.md). [index.md](index.md) is the human content catalog, [index.json](index.json) is the machine catalog, and the log is the chronological operation record.

## Layout

```text
.arcanum/inventory/
  README.md
  schema.md
  index.md
  index.json
  log.md
  tags.md
  indexes/
  raw/
  wiki/
  entries/
  queries/
  lint/
```

## Rules

- Do not edit raw sources during ingest.
- Update [index.md](index.md) and [index.json](index.json) whenever generated pages are created, renamed, retired, or materially changed.
- Append [log.md](log.md) after install, ingest, query, lint, validate, backfill, or sync operations.
- Register new tags in [tags.md](tags.md) before using them repeatedly.
- Mark generated claims as evidence-backed, inference, synthesis, contradiction, or open question.
- Keep optional CSV projections under `projections/` secondary to `index.json` and record their source and freshness.
