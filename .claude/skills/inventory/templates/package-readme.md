# Inventory Package

This package is the repository-local compiled knowledge layer.

Raw sources are read-only inputs. Generated inventory pages are maintained by the agent according to [schema.md](schema.md). The index is the content catalog, and the log is the chronological operation record.

## Layout

```text
.arcanum/inventory/
  README.md
  schema.md
  index.md
  log.md
  tags.md
  raw/
  wiki/
  entries/
  queries/
  lint/
```

## Rules

- Do not edit raw sources during ingest.
- Update [index.md](index.md) whenever generated pages are created, renamed, retired, or materially changed.
- Append [log.md](log.md) after install, ingest, query, lint, validate, backfill, or sync operations.
- Register new tags in [tags.md](tags.md) before using them repeatedly.
- Mark generated claims as evidence-backed, inference, synthesis, contradiction, or open question.