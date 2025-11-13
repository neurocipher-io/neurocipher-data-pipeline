# Agent Forge Integration

**Owner:** Platform Engineering  
**Purpose:** Capture the orchestration responsibilities that Agent Forge provides (workflow coordination, backfills, rollout control) while keeping Neurocipher services loosely coupled.

## Role of Agent Forge

- Orchestrates multi-stage jobs (ingest → normalize → embed → serve) using Step Functions and EventBridge.
- Schedules DR drills, backfills, and bulk re-index operations.
- Produces rollout decisions (pause/continue) that the pipeline services consume via lightweight contracts.

## Contracts

| Contract | Description |
| --- | --- |
| `event.orchestration.job_status.v1` | Agent Forge → Neurocipher. Broadcasts job phase updates (queued, running, halted). Stored under `schemas/events/`. |
| `cmd.orchestration.rollout.v1` | Agent Forge → Neurocipher Feature Flags service. Signals traffic ramps (10/25/50/100%). |
| `event.orchestration.health.v1` | Neurocipher → Agent Forge. Provides aggregated health snapshots used before promoting rollouts. |

Detailed schema definitions are maintained in the Schema Registry; this doc is the single reference from core specs. When Agent Forge introduces new workflows, update this file and the associated schemas instead of embedding orchestration detail in architecture.md.
