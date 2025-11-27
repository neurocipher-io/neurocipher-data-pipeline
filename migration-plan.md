# Neurocipher Monorepo Migration Plan

Status: Ready for execution  
Target: Rename neurocipher-data-pipeline → neurocipher-platform  
Owner: Cody Prevost  
Last updated: 2025-11-27

---

## Pre-Migration Verification

Before any migration steps, verify:

1. On `main` branch with no uncommitted changes
2. All CI workflows passing
3. No open PRs targeting main
4. Local environment matches remote

Commands to verify:

```bash
git status                    # Should show "nothing to commit, working tree clean"
git branch --show-current     # Should show "main"
git fetch origin
git diff origin/main          # Should show no diff
```

---

## Phase 1: Create docs/ Structure

Status: NOT STARTED

Create the documentation directory tree per GOV-ARCH-001:

```bash
mkdir -p docs/governance
mkdir -p docs/product
mkdir -p docs/architecture
mkdir -p docs/data-models
mkdir -p docs/ingestion
mkdir -p docs/services
mkdir -p docs/security-controls
mkdir -p docs/ai
mkdir -p docs/observability
mkdir -p docs/runbooks
```

After completion:

- Verify all directories exist
- Commit: `docs: create documentation directory structure`

---

## Phase 2: Move Existing Docs

Status: NOT STARTED

Move existing documentation to correct locations. Use `git mv` to preserve history.

Mapping table:

| Current Location Pattern | Target Location |
|--------------------------|-----------------|
| `**/REF-001*` | `docs/governance/` |
| `**/GOV-*` | `docs/governance/` |
| `**/DM-003*`, `**/DM-005*` | `docs/data-models/` |
| `**/ING-003*` | `docs/ingestion/` |
| `**/SEC-001*`, `**/SEC-002*`, `**/SEC-003*` | `docs/security-controls/` |
| `**/System-Architecture-Blueprint*` | `docs/architecture/` |
| `**/MCP-TASK-*`, `**/MCP-LEDGER-*`, `**/MCP-ARCH-*` | `docs/architecture/` |
| `**/MCP-RUN-*` | `docs/runbooks/` |
| `**/OBS-*` | `docs/observability/` |
| `**/PRD-*` | `docs/product/` |

Important notes:

- Only move files that are still "floating" in root or odd paths
- Skip files already in correct locations
- Do not re-move Tier-1 docs created in Phase 3 (they are already placed correctly)

For System-Architecture-Blueprint.md:

- Move to `docs/architecture/`
- Update its header to: `Status: Draft for review`
- Add note: "This document predates the full platform view. See ARC-001 for canonical context."

Commands:

```bash
git mv path/to/existing/doc.md docs/target-folder/doc.md
```

After completion:

- Verify no broken links in moved docs
- Commit: `docs: move existing documentation to structured layout`

---

## Phase 3: Add Tier-1 Stub Documents

Status: COMPLETE

The following Tier-1 documents have been created:

| Document | Path | Status |
|----------|------|--------|
| ARC-001-Platform-Context-and-Boundaries.md | `docs/architecture/` | Created |
| DCON-001-Data-Contract-Specification.md | `docs/data-models/` | Created |
| DPS-ING-001-Ingest-Service-Architecture.md | `docs/services/` | Created |
| DPS-API-001-API-Service-Architecture.md | `docs/services/` | Created |
| DPS-NORM-001-Normalize-Service-Architecture.md | `docs/services/` | Created |
| GOV-ARCH-001-Architecture-Documentation-Index.md | `docs/governance/` | Created |
| PRD-001-Neurocipher-Platform-Vision-and-Scope.md | `docs/product/` | Created |

Verification:

- Confirm all files exist in their specified paths
- Confirm all files have correct REF-001 header format
- Confirm GOV-ARCH-001 references all documents correctly

If any are missing, create them before proceeding to Phase 4.

---

## Phase 4: Create services/ Skeleton

Status: NOT STARTED

**Important**: This phase creates only the directory skeleton. We do NOT move existing `migrations/`, `schemas/`, `tests/db/`, or `openapi.yaml` yet.

Rationale:

- Current `make db_local_*` targets assume root-level paths
- Moving these now would break CI and local development
- We defer the bulk move until actual service code exists

Create skeleton only:

```bash
mkdir -p services/nc-data-pipeline/src/nc_data_pipeline
mkdir -p services/nc-data-pipeline/tests
touch services/nc-data-pipeline/src/nc_data_pipeline/__init__.py
touch services/nc-data-pipeline/tests/__init__.py
```

Create placeholder README:

```bash
cat > services/nc-data-pipeline/README.md << 'EOF'
# nc-data-pipeline

Neurocipher Data Pipeline service.

## Services

- `svc-ingest-api` - Raw data ingestion from cloud providers
- `svc-normalize` - Transformation and enrichment
- `svc-embed` - Vector embedding workers
- `svc-query-api` - Query and analytics API

## Structure

```
nc-data-pipeline/
├── src/nc_data_pipeline/   # Service code (to be implemented)
├── tests/                  # Service-specific tests
└── README.md
```

## Note

Database migrations and schemas remain at repository root until
service implementation begins. See MIGRATION-PLAN.md Phase 4 notes.
EOF
```

What stays at root for now:

- `migrations/` - Used by `make db_local_*`
- `schemas/` - Referenced by current tests
- `tests/db/` - Integration tests for DB
- `openapi.yaml` - Will be split later into per-domain specs
- `Makefile` - Current DB and test targets

After completion:

- Verify skeleton directories exist
- Verify existing `make db_local_smoke_test` still works
- Commit: `feat: create services/nc-data-pipeline skeleton`

---

## Phase 5: Create libs/ Structure

Status: NOT STARTED

Create shared libraries directory structure:

```bash
mkdir -p libs/python/nc_models/src/nc_models
mkdir -p libs/python/nc_common/src/nc_common
mkdir -p libs/python/nc_observability/src/nc_observability
```

Create placeholder files:

```bash
touch libs/python/nc_models/src/nc_models/__init__.py
touch libs/python/nc_common/src/nc_common/__init__.py
touch libs/python/nc_observability/src/nc_observability/__init__.py
```

Create libs README:

```bash
cat > libs/README.md << 'EOF'
# Shared Libraries

Shared Python packages for the Neurocipher platform.

## Packages

| Package | Purpose | Status |
|---------|---------|--------|
| `nc_models` | Canonical Pydantic models per DCON-001 | Placeholder |
| `nc_common` | Shared utilities, config, env handling | Placeholder |
| `nc_observability` | Logging, metrics, tracing per REF-001 §12 | Placeholder |

## Usage

Services import from these packages:

```python
from nc_models.finding import SecurityFinding
from nc_common.config import get_settings
from nc_observability.logging import get_logger
```

## Standards

- Package names use snake_case per REF-001 §4.2
- All models follow DCON-001 contracts
- Logging follows REF-001 §12.1 required keys
EOF
```

After completion:

- Commit: `feat: create libs/ structure for shared Python packages`

---

## Phase 6: Create infra/ Structure

Status: NOT STARTED

Create infrastructure directory structure:

```bash
mkdir -p infra/modules
mkdir -p infra/aws/environments/dev
mkdir -p infra/aws/environments/stg
mkdir -p infra/aws/environments/prod
mkdir -p infra/gcp
mkdir -p infra/azure
```

Create infra README:

```bash
cat > infra/README.md << 'EOF'
# Infrastructure

Infrastructure as Code for Neurocipher platform.

## Structure

```
infra/
├── modules/          # Cloud-agnostic Terraform modules
├── aws/
│   └── environments/
│       ├── dev/      # Development environment
│       ├── stg/      # Staging environment
│       └── prod/     # Production environment
├── gcp/              # GCP-specific (placeholder)
└── azure/            # Azure-specific (placeholder)
```

## Standards

- Environment names: `dev`, `stg`, `prod` per REF-002
- Resource tags per REF-001 §6.1
- KMS aliases per REF-002: `alias/nc-dp-data-{env}`
- S3 buckets per REF-002: `s3://nc-dp-{env}-raw`, `s3://nc-dp-{env}-norm`

## Strategy

AWS-first implementation with abstraction layer for future
GCP and Azure support.
EOF
```

After completion:

- Commit: `infra: create infrastructure directory structure`

---

## Phase 7: Root Makefile (Deferred)

Status: DEFERRED

**Note**: We defer root Makefile delegation until service code exists in `services/nc-data-pipeline/src/`.

Current state:

- Existing root Makefile has `db_local_*` targets that work
- No service code exists yet to delegate to
- Premature delegation would break existing workflows

Future action (after service code is implemented):

- Create `services/nc-data-pipeline/Makefile` with service-specific targets
- Update root Makefile to delegate `fmt`, `lint`, `test`, `build`
- Retain `db_local_*` targets at root (or move with path updates)

For now:

- Leave existing Makefile unchanged
- Mark this phase as deferred in execution

---

## Phase 8: Update README.md

Status: NOT STARTED

Replace root README.md with monorepo overview:

```bash
cat > README.md << 'EOF'
# Neurocipher Platform

Enterprise cloud security platform for SMBs.

## Repository Structure

```
neurocipher-platform/
├── docs/                     # Architecture and product documentation
│   ├── governance/           # Standards, glossary, decision governance
│   ├── product/              # PRDs, vision, module mapping
│   ├── architecture/         # Platform and module architecture
│   ├── data-models/          # Schemas, contracts, data governance
│   ├── services/             # Service-level architecture (DPS-*)
│   ├── security-controls/    # Threat models, IAM, network policies
│   ├── ai/                   # Model architecture, guardrails
│   └── observability/        # Logging, metrics, DR, release strategy
├── services/                 # Backend services
│   └── nc-data-pipeline/     # Data ingestion and processing
├── libs/                     # Shared Python libraries
│   └── python/
│       ├── nc_models/        # Canonical Pydantic models
│       ├── nc_common/        # Shared utilities
│       └── nc_observability/ # Logging, metrics, tracing
├── infra/                    # Infrastructure as Code
│   ├── modules/              # Shared Terraform modules
│   └── aws/                  # AWS environments
├── migrations/               # Database migrations (temporary location)
├── schemas/                  # JSON/Avro schemas (temporary location)
└── .github/                  # CI/CD workflows
```

## Modules

| Module | Purpose | Status |
|--------|---------|--------|
| **Neurocipher Core** | Continuous cloud security scanning | Planned |
| **AuditHound** | Compliance assessment and reporting | Planned |
| **Agent Forge** | Auto-remediation orchestration | Planned |
| **MCP Server** | Model Context Protocol integration | Planned |
| **Data Pipeline** | Ingestion, normalization, embedding, query | In progress |

## Quick Start

```bash
make help                    # Show available commands
make db_local_up             # Start local Postgres + Weaviate
make db_local_smoke_test     # Run database smoke tests
```

## Documentation

Start here:

- [Architecture Index](docs/governance/GOV-ARCH-001-Architecture-Documentation-Index.md)
- [Standards Catalog](docs/governance/REF-001-Glossary-and-Standards-Catalog.md)
- [Platform Context](docs/architecture/ARC-001-Platform-Context-and-Boundaries.md)

## Standards

- Documentation format: REF-001
- Service names: REF-002 (`svc-ingest-api`, `svc-normalize`, etc.)
- Identifiers: UUIDv7
- Events: CloudEvents 1.0
- Errors: RFC 7807 Problem Details
EOF
```

After completion:

- Commit: `docs: update README for monorepo structure`

---

## Phase 9: Update CI Workflows

Status: NOT STARTED

Update `.github/workflows/*.yml` to reflect new documentation paths.

Changes needed:

1. Update path filters for docs:

```yaml
# Before
paths:
  - 'docs/**'
  - '*.md'

# After  
paths:
  - 'docs/**'
```

2. Update any hardcoded documentation paths in CI jobs.

3. Do NOT update paths for `migrations/`, `tests/`, `schemas/` yet (they remain at root).

Verification:

```bash
# Check workflow syntax
cat .github/workflows/*.yml | grep -E "^\s+paths:" -A 5
```

After completion:

- Verify workflows parse correctly
- Commit: `ci: update workflow paths for docs/ restructure`

---

## Phase 10: Update CLAUDE.md

Status: NOT STARTED

Create or update CLAUDE.md:

```bash
cat > CLAUDE.md << 'EOF'
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
EOF
```

After completion:

- Commit: `docs: update CLAUDE.md for monorepo structure`

---

## Phase 11: Final Verification

Status: NOT STARTED

Run full verification:

```bash
# Verify docs structure
echo "=== Documentation structure ==="
find docs -type f -name "*.md" | sort

# Verify services skeleton
echo "=== Services structure ==="
find services -type f | sort

# Verify libs skeleton
echo "=== Libs structure ==="
find libs -type f | sort

# Verify infra skeleton
echo "=== Infra structure ==="
find infra -type d | sort

# Verify git status is clean
echo "=== Git status ==="
git status

# Verify existing targets still work
echo "=== Testing existing make targets ==="
make db_local_up
make db_local_smoke_test
make db_local_down
```

After all phases complete:

```bash
git tag -a v0.2.0-monorepo -m "Monorepo migration complete"
git push origin main --tags
```

---

## Post-Migration: Rename Repository

After all code changes are merged and verified:

1. Go to GitHub repository settings
2. Rename `neurocipher-data-pipeline` → `neurocipher-platform`
3. Update local remote:

```bash
git remote set-url origin git@github.com:neurocipher-io/neurocipher-platform.git
```

4. Update any external references (CI badges, documentation links)

---

## Future Work (Not Part of This Migration)

These items are deferred to after the migration is complete:

1. **Move migrations/ to services/**
   - Requires updating all `make db_local_*` targets
   - Requires updating CI workflow paths
   - Do when implementing actual service code

2. **Move tests/ to services/**
   - Move `tests/db/` to `services/nc-data-pipeline/tests/`
   - Update pytest paths in CI
   - Do when implementing actual service code

3. **Split openapi.yaml**
   - Create `services/nc-data-pipeline/api/openapi/ingest.yaml`
   - Create `services/nc-data-pipeline/api/openapi/query.yaml`
   - Do when implementing API services

4. **Implement root Makefile delegation**
   - Create service-local Makefiles first
   - Update root Makefile to delegate
   - Do when service code exists

5. **Rewrite System-Architecture-Blueprint.md**
   - Align with ARC-001 platform view
   - Show all modules (Core, AuditHound, Agent Forge, MCP)
   - Reference monorepo layout

---

## Rollback Plan

If migration fails at any phase:

```bash
git reset --hard origin/main
git clean -fd
```

Each phase is a separate commit, so you can also selectively revert:

```bash
git revert <commit-hash>
```

---

## Phase Summary

| Phase | Description | Status | Blocking |
|-------|-------------|--------|----------|
| Pre | Verify clean state | NOT STARTED | Yes |
| 1 | Create docs/ structure | NOT STARTED | Yes |
| 2 | Move existing docs | NOT STARTED | Yes |
| 3 | Add Tier-1 stubs | COMPLETE | No |
| 4 | Create services/ skeleton | NOT STARTED | Yes |
| 5 | Create libs/ structure | NOT STARTED | No |
| 6 | Create infra/ structure | NOT STARTED | No |
| 7 | Root Makefile delegation | DEFERRED | No |
| 8 | Update README.md | NOT STARTED | No |
| 9 | Update CI workflows | NOT STARTED | Yes |
| 10 | Update CLAUDE.md | NOT STARTED | No |
| 11 | Final verification | NOT STARTED | Yes |
| Post | Rename repository | NOT STARTED | No |
