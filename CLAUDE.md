# Neurocipher Platform

This is the monorepo for the Neurocipher cloud security platform.

## Structure

```
neurocipher-platform/
├── docs/           # All architecture and product documentation
├── services/       # Backend services (nc-data-pipeline, future modules)
├── libs/           # Shared Python packages
├── infra/          # Infrastructure as Code
├── migrations/     # Database migrations (root, will move later)
├── schemas/        # Data schemas (root, will move later)
└── tests/          # Tests (root, will move later)
```

## Key Documents

Before making changes, read:

- `docs/governance/REF-001-Glossary-and-Standards-Catalog.md` - Naming and formatting
- `docs/governance/GOV-ARCH-001-Architecture-Documentation-Index.md` - Doc inventory
- `docs/architecture/ARC-001-Platform-Context-and-Boundaries.md` - System context

## Standards (from REF-001 and REF-002)

### Naming

- Service names: `svc-{domain}-{function}` (e.g., `svc-ingest-api`)
- Python packages: `snake_case` (e.g., `nc_models`)
- JSON fields: `snake_case`
- API paths: `/v1/`, kebab-case nouns

### Identifiers

- Use UUIDv7 for all IDs
- Format: `018fa0b8-6cde-7d2a-bd7f-8d9a3f6f1d0a`

### Events

- CloudEvents 1.0 envelope
- Type naming: `domain.service.event.v{major}`
- Example: `security.finding.created.v1`

### Errors

- RFC 7807 Problem Details
- Content-Type: `application/problem+json`

### Timestamps

- ISO 8601 with Z suffix
- Example: `2025-11-26T18:00:00Z`

### Storage (per REF-002)

- S3 raw: `s3://nc-dp-{env}-raw`
- S3 normalized: `s3://nc-dp-{env}-norm`
- DynamoDB: `nc-dp-{env}-documents`
- KMS: `alias/nc-dp-data-{env}`

### Environments

- `dev`, `stg`, `prod` (not "staging" or "production")

## Database

Local development uses Docker Compose:

```bash
make db_local_up           # Start Postgres + Weaviate
make db_local_smoke_test   # Run smoke tests
make db_local_down         # Stop containers
```

Migrations are in `migrations/postgres/` (will move to services/ later).

## Documentation Format

All docs follow REF-001 §13:

- Mermaid for diagrams (not ASCII)
- Active voice, present tense
- No em dashes
- Required header: Status, Owner, Approvers, Last updated, Applies to, Related
