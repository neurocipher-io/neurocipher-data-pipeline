# Security Engine Integration

**Owner:** Security Engineering (platform)  
**Interfaces owned by:** Neurocipher Core Architecture team  
**Related docs:** docs/security-engine/SEG-001-Security-Engine-Production-Ready.md, docs/data-contracts/DCON-001-Data-Contract-Specification.md, docs/schema-registry/SRG-001-Schema-Registry.md, openapi.yaml

## Purpose

Define the contract surface between the Neurocipher data pipeline and the Security Engine remediation loop. The core pipeline detects issues, emits security events, and consumes action callbacks without embedding Security Engine runtime logic. Implementation details (policy evaluation, remediation tactics, attestation) remain in the Security Engine module.

## Deployment boundary

- Security Engine runs in its own AWS account and VPC, with Read/Write access granted only via the contracts below.
- Neurocipher owns the schemas, APIs, IAM roles, and observability hooks for the integration.
- Security Engine implementation may live in another repository provided it honors these contracts.

## Event → Action → Callback flow

| Stage | Schema/Endpoint | Source → Target | Notes |
| --- | --- | --- | --- |
| Finding event | `schemas/events/event.security.finding.v1.json` | Neurocipher pipeline → Security Engine | Triggered when policy-grade issues are detected (PII violation, data exfil, etc.). Must include `finding_id`, `severity`, `evidence`. |
| Anomaly event | `schemas/events/event.security.anomaly.v1.json` | Neurocipher pipeline → Security Engine | Used for heuristic/anomaly signals; Security Engine can enrich or discard. |
| Command dispatch | `/v1/security/actions` (POST) with `cmd.security.quarantine.v1`, `cmd.security.ticket.create.v1`, `cmd.security.notify.v1` payloads | Security Engine → Neurocipher command bus | Commands are persisted and executed asynchronously with idempotent semantics. |
| Action status | `schemas/events/event.security.action_status.v1.json` | Neurocipher pipeline → Security Engine (and optionally SOC tools) | Reports progress/outcome for each command (`queued`, `running`, `succeeded`, `failed`). Supports retries with `status_id` and exponential backoff guidance. |
| Status fetch | `/v1/security/actions/{id}` (GET) | Security Engine or ops tools → Neurocipher | Read-only view of command lifecycle, including error traces and timestamps. |

### Example payloads

**Finding event (`event.security.finding.v1`)**

```json
{
  "schema_urn": "urn:nc:schema:security:finding:event.security.finding.v1",
  "finding_id": "fin_01J0ABC7Z9M5P6Q7R8S9",
  "severity": "high",
  "classification": ["pii", "exfil-risk"],
  "detected_at": "2025-01-20T12:45:13Z",
  "resource": {
    "type": "s3_object",
    "arn": "arn:aws:s3:::nc-dp-raw/sourceA/2025/01/20/doc-123.bin"
  },
  "evidence": {
    "checksum": "sha256:abc...",
    "pii_types": ["ssn", "dob"]
  },
  "policy_id": "POL-PII-007",
  "tenant_id": "tn_01HZY3",
  "trace_id": "01J0AEH4M4Z9N3QX7TB6",
  "metadata": {
    "pipeline_stage": "normalize",
    "source": "ingest.webhook"
  }
}
```

**Command dispatch (`cmd.security.quarantine.v1`)**

```json
{
  "schema_urn": "urn:nc:schema:security:command:cmd.security.quarantine.v1",
  "action_id": "act_01J0AH1VB5M2R4S6T8",
  "target": {
    "type": "document",
    "doc_id": "doc_01HXYT"
  },
  "requested_by": "seg_automation",
  "requested_at": "2025-01-20T12:46:02Z",
  "reason": "PII policy POL-PII-007 violation",
  "ttl_seconds": 3600,
  "notify": ["sec-ops@neurocipher.io"]
}
```

**Action status (`event.security.action_status.v1`)**

```json
{
  "schema_urn": "urn:nc:schema:security:status:event.security.action_status.v1",
  "action_id": "act_01J0AH1VB5M2R4S6T8",
  "status_id": "ast_01J0AHGDX5R3S6T9",
  "status": "succeeded",
  "observed_at": "2025-01-20T12:46:20Z",
  "details": {
    "message": "Document quarantined and downstream copies flagged",
    "duration_ms": 18000
  },
  "retriable": false,
  "trace_id": "01J0AEH4M4Z9N3QX7TB6"
}
```

## Failure modes and SLAs

- **Decision latency:** p95 ≤ 90s from finding event to command dispatch. Measure via `security_engine.decision_latency_ms`.
- **Queue age:** Security event queues must stay < 120s average age; alert at 60s.
- **Delivery guarantees:** Commands are at-least-once, deduplicated via `action_id`. Callbacks must be idempotent (`status_id` + `action_id` pair).
- **Failure handling:** If `/v1/security/actions` responds ≥ 429 twice consecutively, Security Engine must back off (retry with jitter). Neurocipher emits DLQ metrics and notifies Security Engineering.

## Acceptance criteria

- Security Engine interface references appear in core docs only through the contracts listed above.
- Event schemas live under `schemas/events/` and are registered in SRG-001.
- OpenAPI contains `/v1/security/actions` and `/v1/security/actions/{id}` with examples.
- Observability dashboards include Security Engine metrics/logs/traces hooks as defined in OBS-001/OBS-003.
- ADR-013 records the ownership boundary.
