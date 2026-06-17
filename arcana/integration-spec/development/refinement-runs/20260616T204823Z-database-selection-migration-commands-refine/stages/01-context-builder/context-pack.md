# Context Pack: Database Selection And Migration Commands

Status: pass
Owner capability: context-builder

## Objective

Model database/data-store selection and migration commands as IntegrationSpec-local boundary machinery while preserving DomainSpec as the host application semantic layer.

## Evidence Baseline

- Prior IntegrationSpec gap review identified database/cache/resource handling as a critical gap.
- DomainSpec can name the application behavior around data access, but it does not currently own provider/resource topology, source-of-truth, store-family selection, migration history, drift, or evidence relations.
- Official cloud architecture guidance frames data-store selection around workload requirements, access patterns, consistency, scale, governance, and operations.
- Official migration-tool docs separate command families such as generate, diff, validate, status, apply, rollback, repair, baseline/stamp/resolve, reset/clean, and dry-run SQL.

## Problem Statement

How should a host system record database choices and migration commands so application-layer work is guided, dangerous operations are gated, and runtime migration facts do not become canonical DomainSpec truth?

## Context Handles

- Host meaning: DomainSpec `Operation`, `Query`, `Interface`, `Mapping`, `Policy`, `Workflow`, `Saga`, `Event`.
- Data-resource machinery: resource family, source-of-truth role, access profile, consistency model, lifecycle, governance, migration/backfill plan, evidence anchors.
- Migration-command machinery: command class, environment policy, artifact authority, schema history, checksum, lock, drift, dry-run, apply, rollback/roll-forward, repair, destructive gate.

## Boundary

No live database commands were run.
No credentials, connection strings, schema dumps, or migration logs are included.
No `arcanum/definitions/*` mutation is part of this run.
