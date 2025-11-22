# Database Roadmap Implementation Guide

## Overview

This document provides a complete guide for implementing the database roadmap through GitHub milestones and issues. The roadmap covers all aspects of database design, implementation, and operations for the neurocipher-data-pipeline project.

## Files Delivered

### 1. `milestones_and_issues.json`
Complete machine-readable specification of all milestones and issues in JSON format. This file can be used programmatically to create milestones and issues.

### 2. `create_milestones_and_issues.py`
Python script that uses the GitHub CLI (`gh`) to automatically create all milestones and issues from the JSON specification. The script:
- Validates authentication
- Creates 6 milestones
- Creates 22 issues with proper milestone assignment and labels
- Handles existing milestones/issues gracefully
- Provides progress feedback

### 3. `README.md`
Comprehensive usage guide including:
- Prerequisites and setup instructions
- How to run the automated creation script
- Manual creation fallback instructions
- Troubleshooting guide
- Label reference

### 4. `SUMMARY.md`
Human-readable summary of all milestones and issues organized by:
- Milestone overview table
- Detailed issues by milestone
- Label reference
- Implementation phase guide

### 5. `MANUAL_GUIDE.md`
Step-by-step manual creation guide for users who cannot use the automated script. Includes:
- Exact milestone titles and descriptions
- Complete issue checklist
- Links to GitHub UI for creation
- Quick reference guide

## Milestones Created

| # | Milestone | Issues | Priority Distribution |
|---|-----------|--------|-----------------------|
| 0 | DB-ML0 – Inventory and gap map | 3 | 3 high |
| 1 | DB-ML1 – Postgres OLTP schema finalized | 5 | 1 critical, 3 high, 1 medium |
| 2 | DB-ML2 – Lake / Iceberg layout | 4 | 2 high, 2 medium |
| 3 | DB-ML3 – Weaviate / vector schema | 4 | 3 high, 1 medium |
| 4 | DB-ML4 – Cross-store contracts | 3 | 2 high, 1 medium |
| 5 | DB-ML5 – DR, performance, capacity | 3 | 1 high, 2 medium |

**Total: 6 milestones, 22 issues (1 critical, 14 high, 7 medium)**

## Issues Summary

### Milestone 0: Inventory and Gap Map
Foundation phase - understand current state before building.

1. **DB-001**: Build entity → store → migration status matrix
   - Complete inventory of all entities
   - Document physical stores and multi-tenant classification
   
2. **DB-002**: Complete implementation status audit
   - Verify migration coverage
   - Check RLS and tenant guards
   - Validate indexes
   
3. **DB-003**: Create gap list and mismatch documentation
   - Document entities not yet implemented
   - Identify doc/implementation mismatches
   - Prioritize gaps

### Milestone 1: Postgres OLTP Schema Finalized
Core OLTP database foundation.

4. **DB-004**: Complete nc.* physical DDL
   - Ensure all tables from DM-003 exist
   - Handle reserved words
   - Test migrations
   
5. **DB-005**: Complete RLS + tenant guard coverage ⚠️ CRITICAL
   - Confirm guards on all tenant tables
   - Add smoke tests for critical flows
   - Test tenant isolation
   
6. **DB-006**: Define indexes and constraints
   - Primary keys for all major tables
   - Secondary indexes for query patterns
   - Document in DM-003
   
7. **DB-007**: Implement retention and partitioning
   - Partition large tables (audit_log, event)
   - Define retention procedures
   - Test partition creation
   
8. **DB-008**: Build automated migration harness
   - Lock in Makefile targets
   - Create smoke test script
   - Integrate into CI/CD

### Milestone 2: Lake / Iceberg Layout
Analytical lakehouse layer.

9. **DB-009**: Define LAK-001 specification
   - Document entities mirrored to lake
   - Define naming conventions
   - Specify storage format
   
10. **DB-010**: Map OLTP → Lake projections
    - Define transformations
    - Document denormalization strategy
    - Include soft-deletion semantics
    
11. **DB-011**: Create Iceberg DDL and bootstrap
    - Initial table definitions
    - Bootstrap procedures
    - Test table creation
    
12. **DB-012**: Define retention and DR for lakehouse
    - Retention policies
    - Recovery procedures
    - Integrate with DR-001

### Milestone 3: Weaviate / Vector Schema
Vector search and embedding storage.

13. **DB-013**: Lock baseline Weaviate schema
    - Finalize NcChunkV1 schema
    - JSON schema file
    - Apply script
    
14. **DB-014**: Align Weaviate documentation
    - Update DM-003 for Weaviate 1.34+
    - Update DM-005 with versioning process
    - Review for consistency
    
15. **DB-015**: Create Weaviate dev environment
    - docker-compose.weaviate.dev.yml
    - Makefile helpers
    - Documentation
    
16. **DB-016**: Build schema apply and smoke tests
    - Apply schema script
    - Multi-tenant isolation test
    - Integration into test suite

### Milestone 4: Cross-Store Contracts and Lineage
Data governance and lineage.

17. **DB-017**: Create data contract spec (DCON-001)
    - Field types and constraints
    - Cross-store definitions
    - Validation rules
    
18. **DB-018**: Build lineage mapping (LIN-001)
    - Lineage per domain
    - Diagrams
    - Documentation
    
19. **DB-019**: Implement consistency checks
    - Cross-store sanity checks
    - Data freshness validation
    - Alerting for violations

### Milestone 5: DR, Performance, and Capacity
Operational readiness.

20. **DB-020**: Align DR-001 for all stores
    - Backup strategies (Postgres, Weaviate, Lake)
    - RPO/RTO definitions
    - Test procedures
    
21. **DB-021**: Establish performance baselines
    - Define key queries
    - Measure baseline performance
    - Set SLOs
    
22. **DB-022**: Create capacity model (CAP-001)
    - Size projections
    - Growth assumptions
    - Scaling triggers

## Implementation Sequence

### Phase 1: Foundation (Weeks 1-2)
- Complete Milestone 0 (DB-001, DB-002, DB-003)
- Establish baseline understanding
- Identify gaps and priorities

### Phase 2: OLTP Core (Weeks 3-6)
- Complete Milestone 1 (DB-004 through DB-008)
- Focus on DB-005 (RLS) as critical priority
- Establish automated testing harness

### Phase 3: Parallel Development (Weeks 7-10)
- Lakehouse: Milestone 2 (DB-009 through DB-012)
- Weaviate: Milestone 3 (DB-013 through DB-016)
- Can work in parallel with separate teams

### Phase 4: Integration (Weeks 11-12)
- Complete Milestone 4 (DB-017 through DB-019)
- Tie all stores together
- Validate consistency

### Phase 5: Operationalization (Weeks 13-14)
- Complete Milestone 5 (DB-020 through DB-022)
- DR, performance, capacity
- Production readiness

## How to Use This Deliverable

### For Project Managers
1. Review `SUMMARY.md` for overview
2. Run `create_milestones_and_issues.py` to create in GitHub
3. Use milestones to track progress
4. Assign issues to team members

### For Developers
1. Read `SUMMARY.md` to understand scope
2. Pick issues from current milestone
3. Follow task checklists in each issue
4. Reference docs (DM-001, DM-003, DM-005, LAK-001, etc.)

### For DevOps/Platform Engineers
1. Focus on automation issues (DB-008, DB-015, DB-016, DB-019)
2. Ensure CI/CD integration
3. Set up monitoring for consistency checks

### For Documentation Team
1. Many issues have documentation deliverables
2. Use issue checklists to track doc status
3. Ensure alignment between docs and implementation

## Next Steps

1. **Immediate**: Run the creation script
   ```bash
   python scripts/github/create_milestones_and_issues.py
   ```

2. **Week 1**: Begin Milestone 0
   - Assign DB-001, DB-002, DB-003 to team members
   - Set up project board if needed
   - Establish review process

3. **Week 2**: Review Milestone 0 results
   - Use gap analysis to prioritize Milestone 1 work
   - Adjust timeline if needed based on findings

4. **Ongoing**: Track progress
   - Weekly milestone review
   - Update issue status
   - Adjust priorities as needed

## Support and Questions

For questions or issues with:
- **Script execution**: See `README.md` troubleshooting section
- **Manual creation**: Use `MANUAL_GUIDE.md`
- **Content questions**: Reference original specification in project issue
- **Label management**: See `README.md` label reference

## Related Documentation

- `docs/data-models/DM-001-Canonical-Data-Model.md`
- `docs/data-models/DM-003-Physical-Schemas-and-Storage-Map.md`
- `docs/data-models/DM-005-Governance-Versioning-and-Migrations.md`
- `docs/lakehouse/LAK-001-Lakehouse-Layout-Iceberg-S3.md`
- `docs/dr/DR-001-Disaster-Recovery-Plan.md`
- `docs/capacity-performance/CAP-001-Capacity-Model.md`
