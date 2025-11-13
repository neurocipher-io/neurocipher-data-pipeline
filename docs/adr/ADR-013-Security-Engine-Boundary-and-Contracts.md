# ADR-013 Security Engine Boundary and Contracts

## Status
Accepted — 2025-11-10

## Context
The Neurocipher pipeline requires a remediation loop that evaluates findings, issues commands, and records outcomes. The Security Engine handles remediation logic but must remain decoupled so that pipeline services do not depend on its runtime internals. Previous drafts mixed Security Engine details into ingestion and serving specs, creating unclear ownership and governance.

## Decision

1. **Boundary ownership:** Neurocipher core owns the Security Engine contracts (schemas, APIs, IAM roles) and exposes them via the pipeline repository. Implementation of the Security Engine runtime may reside in a separate repository managed by Security Engineering.
2. **Contracts:** All communication uses the event/command schemas registered in `schemas/events/` and the `/v1/security/actions*` API surface described in `openapi.yaml`.
3. **Observability:** Metrics/logs/traces for the integration are required (see OBS-001/OBS-003); action IDs and status IDs must appear in every signal.
4. **Governance:** Changes to the contracts follow DM-005 and SRG-001 processes and require review from both Platform Architecture and Security Engineering.

## Consequences

- Core documentation references the Security Engine only through the defined contracts (architecture diagrams, DCON-001, SRG-001, OBS-00x, openapi.yaml).
- Implementation guides, remediation playbooks, and control catalogs remain under `docs/security-engine/` (or the dedicated repo) and may evolve independently without modifying pipeline internals.
- Partner integrations consume Security Engine functionality exclusively through the documented contracts, eliminating cross-product bleed.
