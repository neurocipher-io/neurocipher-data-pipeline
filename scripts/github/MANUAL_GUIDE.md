# Manual Creation Guide

If you cannot run the automated script, you can create the milestones and issues manually using this guide.

## Creating Milestones

Navigate to: `https://github.com/neurocipher-io/neurocipher-data-pipeline/milestones/new`

Create these 6 milestones:

### 1. DB-ML0 – Inventory and gap map
**Description:**
```
Single, accurate map of all entities and where they physically live (Postgres / S3 / Weaviate), plus what's implemented vs not.
```

### 2. DB-ML1 – Postgres OLTP schema finalized (nc.*)
**Description:**
```
nc schema is complete, consistent with DM-003, and safe to run in dev/stg/prod.
```

### 3. DB-ML2 – Lake / Iceberg layout (LAK-001 + physical DDL)
**Description:**
```
Define and implement the analytical/lake tables for long-term storage and heavy analytics, separate from OLTP.
```

### 4. DB-ML3 – Weaviate / vector schema and indexes
**Description:**
```
Clean, documented Weaviate schema with clear governance for class versions and index types.
```

### 5. DB-ML4 – Cross-store contracts and lineage
**Description:**
```
Every piece of data has a clear contract and lineage between Postgres, S3/Iceberg, and Weaviate.
```

### 6. DB-ML5 – DR, performance, and capacity for the DB layer
**Description:**
```
Database layer is not only designed but also operable: DR, performance targets, and capacity planning exist and are enforceable.
```

## Creating Issues

Navigate to: `https://github.com/neurocipher-io/neurocipher-data-pipeline/issues/new`

For each issue, copy the title and body from the `milestones_and_issues.json` file, assign to the appropriate milestone, and add labels.

### Quick Reference

The complete specification is in `milestones_and_issues.json`. Here's a quick checklist:

#### DB-ML0 – Inventory and gap map (3 issues)
- [ ] DB-001: Build entity → store → migration status matrix
- [ ] DB-002: Complete implementation status audit for all entities
- [ ] DB-003: Create gap list and mismatch documentation

#### DB-ML1 – Postgres OLTP schema finalized (nc.*) (5 issues)
- [ ] DB-004: Complete nc.* physical DDL for all entities
- [ ] DB-005: Complete nc.* RLS + tenant guard coverage
- [ ] DB-006: Define and implement indexes and constraints for major tables
- [ ] DB-007: Implement retention and partitioning for large tables
- [ ] DB-008: Build automated migration harness and smoke tests

#### DB-ML2 – Lake / Iceberg layout (LAK-001 + physical DDL) (4 issues)
- [ ] DB-009: Define LAK-001 lakehouse layout specification
- [ ] DB-010: Map OLTP → Lake projections for all entities
- [ ] DB-011: Create Iceberg table DDL and bootstrap process
- [ ] DB-012: Define retention and DR for lakehouse

#### DB-ML3 – Weaviate / vector schema and indexes (4 issues)
- [ ] DB-013: Lock baseline Weaviate class schema (NcChunkV1)
- [ ] DB-014: Align Weaviate documentation with reality
- [ ] DB-015: Create Weaviate dev environment setup
- [ ] DB-016: Build schema apply and smoke test scripts

#### DB-ML4 – Cross-store contracts and lineage (3 issues)
- [ ] DB-017: Create data contract specification (DCON-001)
- [ ] DB-018: Build lineage mapping documentation (LIN-001)
- [ ] DB-019: Implement consistency checks across stores

#### DB-ML5 – DR, performance, and capacity for the DB layer (3 issues)
- [ ] DB-020: Align DR-001 for all database stores
- [ ] DB-021: Establish performance baselines and SLOs
- [ ] DB-022: Create capacity model (CAP-001)

## Using the gh CLI

Alternatively, if you have the `gh` CLI installed and authenticated, run:

```bash
python scripts/github/create_milestones_and_issues.py
```

This will automatically create all milestones and issues.
