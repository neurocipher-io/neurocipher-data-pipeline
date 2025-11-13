# AuditHound Integration

**Owner:** Platform SRE (shared)  
**Purpose:** Describe how the Neurocipher pipeline exchanges telemetry and search capabilities with the AuditHound compliance module without coupling their runtimes.

## Scope

- Neurocipher provides normalized assets, embeddings, and query APIs that AuditHound consumes via the standard `/v1/query` and `/v1/ingest/event` endpoints.
- AuditHound publishes posture and compliance events back through the same data-contract framework (see DCON-001) using tenants scoped to `audithound`.
- Dedicated queues, IAM roles, and rate limits shield the core pipeline from AuditHound spikes. Detailed throttling logic lives here; pipeline docs simply reference this file.

## Interfaces

| Interface | Direction | Notes |
| --- | --- | --- |
| Ingest webhook | AuditHound → Neurocipher `/v1/ingest/event` | Signed payloads, `Tenant-Id=audithound`. |
| Search API | AuditHound UI → Neurocipher `/v1/query` | Standard auth scopes `search:read`. |
| Compliance events | AuditHound → Neurocipher S3 drops (`s3://nc-dp-raw/audithound/...`) | Uses same schemas defined in DCON-001. |
| Security Engine callbacks | AuditHound → Security Engine | Routed via security contracts, not directly to pipeline. |

## Operational considerations

- Burst protection: API Gateway usage plans cap AuditHound traffic at 200 RPS sustained, 500 RPS burst.
- Isolation: Dedicated S3 prefixes and DynamoDB partition keys (`tenant=audit_hound`).
- Observability: Custom dashboards overlay AuditHound traffic on ingest/query SLOs.

For change management, link AuditHound-specific ADRs or RFCs here instead of scattering them through core docs.
