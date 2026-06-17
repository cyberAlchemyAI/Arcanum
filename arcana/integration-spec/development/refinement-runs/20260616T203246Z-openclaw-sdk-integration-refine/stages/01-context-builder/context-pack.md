# Context Pack: OpenClaw Integration Modeling

Status: pass
Owner capability: context-builder

## Objective

Model how a host system should integrate OpenClaw without leaking OpenClaw runtime details into DomainSpec canon.

## Evidence Baseline

- Prior IntegrationSpec refinement selected Integration Boundary Discipline first.
- The current gap is not HTTP shape, event envelope, or payload mapping alone; it is the application-layer decision surface around external resources, connectors, trust, runtime state, failure behavior, and proof obligations.
- OpenClaw official docs distinguish external app integration through Gateway/RPC from plugin SDK code that runs inside OpenClaw.
- Operator-supplied local bridge evidence shows practical CLI/gateway wrapping patterns, but private paths and local content are withheld from the public artifact.

## Problem Statement

How should an application describe a dependency on OpenClaw so that the application layer owns the port and policy while OpenClaw remains an external agent-runtime resource?

## Useful Context Handles

- Host meaning: DomainSpec `Operation`, `Query`, `Interface`, `Mapping`, `Policy`, `Workflow`, `Saga`, `Event`.
- Integration-local machinery: `Integration Boundary`, `Integration Port`, `Connector`, `ExternalResource`, `AgentRuntimeResource`, `Session Policy`, `Trust Boundary`, `Integration Decision Record`, `Evidence Anchor`.
- OpenClaw surfaces: Gateway/RPC for external apps; CLI for one-shot automation or probes; plugin SDK only for code loaded by OpenClaw.

## Boundary

No mutation of `arcanum/definitions/*`.
No public copy of OpenClaw config, credentials, runtime transcripts, or local private bridge paths.
No claim that a validator proves runtime success.
