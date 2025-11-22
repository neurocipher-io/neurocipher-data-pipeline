# Database Roadmap - Milestones and Issues Summary

This document provides a complete summary of the 6 milestones and 22 issues created for the database roadmap implementation.

## Milestones Overview

| # | Title | Description | Issues |
|---|-------|-------------|--------|
| 1 | DB-ML0 – Inventory and gap map | Single, accurate map of all entities and where they physically live (Postgres / S3 / Weaviate), plus what's implemented vs not. | 3 |
| 2 | DB-ML1 – Postgres OLTP schema finalized (nc.*) | nc schema is complete, consistent with DM-003, and safe to run in dev/stg/prod. | 5 |
| 3 | DB-ML2 – Lake / Iceberg layout (LAK-001 + physical DDL) | Define and implement the analytical/lake tables for long-term storage and heavy analytics, separate from OLTP. | 4 |
| 4 | DB-ML3 – Weaviate / vector schema and indexes | Clean, documented Weaviate schema with clear governance for class versions and index types. | 4 |
| 5 | DB-ML4 – Cross-store contracts and lineage | Every piece of data has a clear contract and lineage between Postgres, S3/Iceberg, and Weaviate. | 3 |
| 6 | DB-ML5 – DR, performance, and capacity for the DB layer | Database layer is not only designed but also operable: DR, performance targets, and capacity planning exist and are enforceable. | 3 |

**Total: 6 milestones, 22 issues**

## Issues by Milestone

### DB-ML0 – Inventory and gap map

| Issue # | Title | Labels |
|---------|-------|--------|
| DB-001 | Build entity → store → migration status matrix | area:db, type:docs, priority:high |
| DB-002 | Complete implementation status audit for all entities | area:db, type:audit, priority:high |
| DB-003 | Create gap list and mismatch documentation | area:db, type:docs, priority:high |

**Goal:** Create a comprehensive inventory of all entities, their physical stores, implementation status, and identify gaps between documentation and implementation.

---

### DB-ML1 – Postgres OLTP schema finalized (nc.*)

| Issue # | Title | Labels |
|---------|-------|--------|
| DB-004 | Complete nc.* physical DDL for all entities | area:db, type:migrations, priority:high |
| DB-005 | Complete nc.* RLS + tenant guard coverage | area:db, type:migrations, priority:critical |
| DB-006 | Define and implement indexes and constraints for major tables | area:db, type:migrations, priority:high |
| DB-007 | Implement retention and partitioning for large tables | area:db, type:migrations, priority:medium |
| DB-008 | Build automated migration harness and smoke tests | area:db, type:testing, priority:high |

**Goal:** Finalize the Postgres OLTP schema with complete DDL, RLS, indexes, partitioning, and automated testing.

---

### DB-ML2 – Lake / Iceberg layout (LAK-001 + physical DDL)

| Issue # | Title | Labels |
|---------|-------|--------|
| DB-009 | Define LAK-001 lakehouse layout specification | area:lakehouse, type:docs, priority:high |
| DB-010 | Map OLTP → Lake projections for all entities | area:lakehouse, type:docs, priority:high |
| DB-011 | Create Iceberg table DDL and bootstrap process | area:lakehouse, type:migrations, priority:medium |
| DB-012 | Define retention and DR for lakehouse | area:lakehouse, type:docs, priority:medium |

**Goal:** Design and implement the analytical lakehouse layer for long-term storage and analytics.

---

### DB-ML3 – Weaviate / vector schema and indexes

| Issue # | Title | Labels |
|---------|-------|--------|
| DB-013 | Lock baseline Weaviate class schema (NcChunkV1) | area:weaviate, type:migrations, priority:high |
| DB-014 | Align Weaviate documentation with reality | area:weaviate, type:docs, priority:high |
| DB-015 | Create Weaviate dev environment setup | area:weaviate, type:dev-environment, priority:medium |
| DB-016 | Build schema apply and smoke test scripts | area:weaviate, type:testing, priority:high |

**Goal:** Establish production-ready Weaviate schema with proper governance, documentation, and testing.

---

### DB-ML4 – Cross-store contracts and lineage

| Issue # | Title | Labels |
|---------|-------|--------|
| DB-017 | Create data contract specification (DCON-001) | area:data-contracts, type:docs, priority:high |
| DB-018 | Build lineage mapping documentation (LIN-001) | area:lineage, type:docs, priority:high |
| DB-019 | Implement consistency checks across stores | area:data-quality, type:testing, priority:medium |

**Goal:** Define clear contracts and lineage for all data across Postgres, Weaviate, and the lakehouse.

---

### DB-ML5 – DR, performance, and capacity for the DB layer

| Issue # | Title | Labels |
|---------|-------|--------|
| DB-020 | Align DR-001 for all database stores | area:dr, type:docs, priority:high |
| DB-021 | Establish performance baselines and SLOs | area:performance, type:docs, priority:medium |
| DB-022 | Create capacity model (CAP-001) | area:capacity, type:docs, priority:medium |

**Goal:** Make the database layer fully operable with DR plans, performance targets, and capacity planning.

---

## Label Reference

### Area Labels
- `area:db` - PostgreSQL database tasks
- `area:lakehouse` - Lakehouse/Iceberg tasks
- `area:weaviate` - Weaviate vector database tasks
- `area:data-contracts` - Data contract definition tasks
- `area:lineage` - Data lineage tasks
- `area:data-quality` - Data quality and consistency tasks
- `area:dr` - Disaster recovery tasks
- `area:performance` - Performance tuning and SLO tasks
- `area:capacity` - Capacity planning tasks

### Type Labels
- `type:docs` - Documentation tasks
- `type:audit` - Audit and assessment tasks
- `type:migrations` - Schema migrations and DDL tasks
- `type:testing` - Testing and validation tasks
- `type:dev-environment` - Development environment setup tasks

### Priority Labels
- `priority:critical` - Critical priority (1 issue)
- `priority:high` - High priority (14 issues)
- `priority:medium` - Medium priority (7 issues)

## Implementation Guide

### Phase 1: Inventory and Foundation (Milestone 0)
Start with DB-001, DB-002, and DB-003 to establish a baseline understanding of what exists and what needs to be built.

### Phase 2: OLTP Core (Milestone 1)
Complete the Postgres OLTP schema with DB-004 through DB-008. This is the foundation for all other work.

### Phase 3: Parallel Tracks (Milestones 2 & 3)
Work on lakehouse (DB-009 through DB-012) and Weaviate (DB-013 through DB-016) can proceed in parallel once the OLTP foundation is solid.

### Phase 4: Integration (Milestone 4)
With all stores defined, create contracts and lineage (DB-017 through DB-019) to tie everything together.

### Phase 5: Operationalization (Milestone 5)
Finally, ensure operational readiness with DR, performance, and capacity planning (DB-020 through DB-022).

## Files

- `milestones_and_issues.json` - Machine-readable specification
- `create_milestones_and_issues.py` - Script to create milestones and issues in GitHub
- `README.md` - Usage instructions
- `SUMMARY.md` - This document

## Next Steps

1. Review this summary to ensure all milestones and issues align with project goals
2. Run the creation script: `python scripts/github/create_milestones_and_issues.py`
3. Verify milestones and issues were created in GitHub
4. Begin work on Milestone 0 (Inventory and gap map)
