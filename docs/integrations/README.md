# Integrations Catalog

This folder centralizes cross-product integrations so core Neurocipher documentation stays focused on the pipeline itself.

| Module | Doc | Summary |
| --- | --- | --- |
| AuditHound compliance suite | [AuditHound-Integration.md](AuditHound-Integration.md) | Describes how AuditHound consumes Neurocipher ingest/query surfaces, throughput limits, IAM roles, and monitoring expectations. |
| Agent Forge orchestrator | [Agent-Forge-Integration.md](Agent-Forge-Integration.md) | Covers workflow coordination, rollout signaling, and the event/command contracts shared with Agent Forge. |
| Security Engine remediation loop | [Security-Engine-Integration.md](Security-Engine-Integration.md) | Defines the contract between the Neurocipher pipeline and the Security Engine module (events, commands, callbacks, SLAs). |

If a spec needs to mention a particular partner module, reference this catalog instead of embedding details inline.
