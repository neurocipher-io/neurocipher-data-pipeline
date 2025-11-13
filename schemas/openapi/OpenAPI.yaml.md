The authoritative specification now lives at `openapi.yaml` in the repository root.

- Endpoints include `/v1/ingest/event`, `/v1/query`, `/v1/admin/reindex`, `/v1/security/actions`, `/v1/security/actions/{id}`, and `/v1/health`.
- Mandatory headers: `Tenant-Id`, `Idempotency-Key`, and `Correlation-Id` (auto-generated if omitted).
- Security Engine contracts surface through `/v1/security/actions*`, aligning with the schemas described in `docs/integrations/Security-Engine-Integration.md`.

Use `npx @stoplight/spectral-cli lint openapi.yaml` to validate changes.
