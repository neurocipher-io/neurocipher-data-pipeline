#!/usr/bin/env python3
"""
Script to create GitHub milestones and issues for the database roadmap.
This script uses the GitHub REST API to create milestones and issues.
"""

import os
import sys
import json
import subprocess
from typing import Dict, List, Optional

REPO_OWNER = "neurocipher-io"
REPO_NAME = "neurocipher-data-pipeline"

# Milestone definitions
MILESTONES = [
    {
        "title": "DB-ML0 – Inventory and gap map",
        "description": "Single, accurate map of all entities and where they physically live (Postgres / S3 / Weaviate), plus what's implemented vs not."
    },
    {
        "title": "DB-ML1 – Postgres OLTP schema finalized (nc.*)",
        "description": "nc schema is complete, consistent with DM-003, and safe to run in dev/stg/prod."
    },
    {
        "title": "DB-ML2 – Lake / Iceberg layout (LAK-001 + physical DDL)",
        "description": "Define and implement the analytical/lake tables for long-term storage and heavy analytics, separate from OLTP."
    },
    {
        "title": "DB-ML3 – Weaviate / vector schema and indexes",
        "description": "Clean, documented Weaviate schema with clear governance for class versions and index types."
    },
    {
        "title": "DB-ML4 – Cross-store contracts and lineage",
        "description": "Every piece of data has a clear contract and lineage between Postgres, S3/Iceberg, and Weaviate."
    },
    {
        "title": "DB-ML5 – DR, performance, and capacity for the DB layer",
        "description": "Database layer is not only designed but also operable: DR, performance targets, and capacity planning exist and are enforceable."
    }
]

# Issue definitions for each milestone
ISSUES = {
    "DB-ML0 – Inventory and gap map": [
        {
            "title": "DB-001: Build entity → store → migration status matrix",
            "body": """Complete an entity inventory and implementation status mapping.

**Tasks:**
- [ ] List all entities from DM-001/DM-003 (account, user, scan, finding, evidence, remediation, ticket, integration, notification, asset, control, policy, audit_log, event, ingestion/embedding chain, etc.)
- [ ] For each entity, record:
  - [ ] Logical name
  - [ ] Physical store(s): postgres.nc.*, s3://..., Weaviate NcChunkV1, future Iceberg tables
  - [ ] Multi-tenant or global classification
- [ ] Document findings in a structured table format

**Done when:**
- Single table listing "logical entity → physical store(s) → migration file → status" exists
- No entities are "mystery" anymore (everything is classified: done / partial / missing)
""",
            "labels": ["area:db", "type:docs", "priority:high"]
        },
        {
            "title": "DB-002: Complete implementation status audit for all entities",
            "body": """Audit implementation status for all entities and tables.

**Tasks:**
- [ ] For each entity/table, verify:
  - [ ] Is it fully covered in migrations 0001 + 0002?
  - [ ] Are RLS + trg_tenant_guard in place (for tenant tables)?
  - [ ] Are indexes defined for the main query patterns?
- [ ] Document coverage gaps
- [ ] Create tracking table for implementation completeness

**Done when:**
- Complete audit of all entities exists
- Implementation status is documented for each entity
""",
            "labels": ["area:db", "type:audit", "priority:high"]
        },
        {
            "title": "DB-003: Create gap list and mismatch documentation",
            "body": """Document all gaps and mismatches between design and implementation.

**Tasks:**
- [ ] Create a gap list document (DM-003-Gaps.md or add section to DM-003)
- [ ] List entities defined in DM-003 but not yet implemented
- [ ] List entities implemented but not yet fully documented (indexes, retention, partitioning)
- [ ] Document any mismatch between docs and live schema
- [ ] Prioritize gaps for resolution

**Done when:**
- Gap list document exists and is comprehensive
- All mismatches between documentation and implementation are identified
""",
            "labels": ["area:db", "type:docs", "priority:high"]
        }
    ],
    "DB-ML1 – Postgres OLTP schema finalized (nc.*)": [
        {
            "title": "DB-004: Complete nc.* physical DDL for all entities",
            "body": """Ensure all nc.* tables are fully defined in migrations.

**Tasks:**
- [ ] For every nc.* table in DM-003:
  - [ ] Confirm presence in migrations (0001, 0002 or future 0003+)
  - [ ] Add missing tables or columns via new migration(s)
  - [ ] Ensure all reserved words are properly handled (e.g., "references" in nc.control)
- [ ] Review and validate DDL consistency
- [ ] Test migrations on clean database

**Done when:**
- All nc.* tables from DM-003 exist in migrations
- No missing tables or columns remain
- All reserved words are properly handled
""",
            "labels": ["area:db", "type:migrations", "priority:high"]
        },
        {
            "title": "DB-005: Complete nc.* RLS + tenant guard coverage",
            "body": """Ensure RLS and tenant guard are properly configured for all tenant tables.

**Tasks:**
- [ ] Confirm trg_tenant_guard + RLS:
  - [ ] Exist on all tenant tables (account-scoped)
  - [ ] Do not exist on global tables (where appropriate)
- [ ] Add smoke-test SQL blocks for critical flows:
  - [ ] ingestion→chunk→embedding_ref
  - [ ] scan→finding→ticket
  - [ ] Other critical multi-tenant data flows
- [ ] Test tenant isolation thoroughly

**Done when:**
- All tenant tables have proper RLS and tenant guards
- Smoke tests validate tenant isolation
- No cross-tenant data leaks possible
""",
            "labels": ["area:db", "type:migrations", "priority:critical"]
        },
        {
            "title": "DB-006: Define and implement indexes and constraints for major tables",
            "body": """Add necessary indexes and constraints for performance and data integrity.

**Tasks:**
- [ ] For each major table (scan, finding, ticket, asset, audit_log, event):
  - [ ] Define primary keys (composite where needed, e.g. (id, occurred_at))
  - [ ] Add necessary secondary indexes:
    - [ ] scan(status, account_id, started_at)
    - [ ] finding(account_id, status, severity)
    - [ ] ticket(account_id, status, priority)
    - [ ] audit_log(account_id, timestamp, action)
    - [ ] event(account_id, occurred_at, event_type)
- [ ] Document indexes in DM-003 under each table's section
- [ ] Test query performance with indexes

**Done when:**
- All major tables have proper primary keys and indexes
- Index strategy is documented in DM-003
- Query performance is validated
""",
            "labels": ["area:db", "type:migrations", "priority:high"]
        },
        {
            "title": "DB-007: Implement retention and partitioning for large tables",
            "body": """Define and implement partitioning strategy and retention policies.

**Tasks:**
- [ ] Confirm partitioning strategy for big tables:
  - [ ] audit_log: partition by time (e.g., monthly) or by account_id + time
  - [ ] event: partition by time or account_id + time
  - [ ] finding: evaluate need for partitioning
- [ ] Ensure retention procedures exist in migrations
- [ ] Document retention policies in DM-003:
  - [ ] How many days/months data is kept
  - [ ] What happens on purge
  - [ ] Archival strategy
- [ ] Test partition creation and retention procedures

**Done when:**
- Partitioning is implemented for large tables
- Retention procedures are in place and tested
- All policies are documented in DM-003
""",
            "labels": ["area:db", "type:migrations", "priority:medium"]
        },
        {
            "title": "DB-008: Build automated migration harness and smoke tests",
            "body": """Create comprehensive testing harness for database migrations and schema.

**Tasks:**
- [ ] Lock in Makefile targets:
  - [ ] db_local_up
  - [ ] db_local_migrate
  - [ ] db_local_down
- [ ] Add minimal test script that:
  - [ ] Runs db_local_up, db_local_migrate
  - [ ] Executes smoke-test SQL for:
    - [ ] Ingestion path
    - [ ] scan→finding→ticket path
    - [ ] RLS isolation verification
  - [ ] Exits non-zero on failure
- [ ] Integrate into CI/CD pipeline

**Done when:**
- make db_local_up && make db_local_migrate gives fully functional nc_dev
- Smoke-test SQL covers all critical flows and passes
- Tests run successfully in CI
""",
            "labels": ["area:db", "type:testing", "priority:high"]
        }
    ],
    "DB-ML2 – Lake / Iceberg layout (LAK-001 + physical DDL)": [
        {
            "title": "DB-009: Define LAK-001 lakehouse layout specification",
            "body": """Create comprehensive lakehouse layout specification.

**Tasks:**
- [ ] Write LAK-001-Lakehouse-Layout.md describing:
  - [ ] Which entities are mirrored to the lake (finding, asset, scan, ticket, audit_log, event)
  - [ ] Table naming conventions (e.g., nc_lake.finding_v1)
  - [ ] Partitioning scheme (e.g., by account_id and date)
  - [ ] Storage format (Iceberg/Parquet, compression, encryption)
- [ ] Align with existing docs (DM-003, DM-005)
- [ ] Review and validate with team

**Done when:**
- LAK-001 exists and is consistent with DM-003/DM-005 naming
- Storage format and partitioning strategy is clearly defined
""",
            "labels": ["area:lakehouse", "type:docs", "priority:high"]
        },
        {
            "title": "DB-010: Map OLTP → Lake projections for all entities",
            "body": """Define transformation and projection logic from OLTP to lake tables.

**Tasks:**
- [ ] For each lake table:
  - [ ] Define projection from nc.* tables (which columns, denormalization strategy)
  - [ ] Include soft-deletion / is_current semantics where relevant
  - [ ] Document transformation logic
- [ ] Create mapping documentation
- [ ] Define data quality checks

**Done when:**
- Clear mapping exists from every nc.* table to its lake equivalent
- Transformation logic is documented
- For every major entity, lake table schema is defined
""",
            "labels": ["area:lakehouse", "type:docs", "priority:high"]
        },
        {
            "title": "DB-011: Create Iceberg table DDL and bootstrap process",
            "body": """Implement initial Iceberg table definitions and bootstrap procedures.

**Tasks:**
- [ ] Create initial Iceberg table DDL for dev environment
- [ ] Decide orchestration approach (pipeline, not DB)
- [ ] Document target schema and layout clearly
- [ ] Create bootstrap scripts or procedures
- [ ] Test table creation and basic operations

**Done when:**
- Initial Iceberg DDL exists for all planned lake tables
- Bootstrap process is documented
- Tables can be created in dev environment
""",
            "labels": ["area:lakehouse", "type:migrations", "priority:medium"]
        },
        {
            "title": "DB-012: Define retention and DR for lakehouse",
            "body": """Establish retention policies and disaster recovery procedures for lakehouse.

**Tasks:**
- [ ] Define retention policies:
  - [ ] How long lake data is kept
  - [ ] Archival strategy
  - [ ] Compaction and cleanup procedures
- [ ] Document recovery procedures:
  - [ ] Can OLTP be rehydrated from lake snapshots?
  - [ ] Analytics-only recovery?
  - [ ] Point-in-time recovery capabilities
- [ ] Integrate with DR-001 document

**Done when:**
- Retention policies are defined and documented
- Recovery procedures are documented in LAK-001 or DR-001
- Backup and restore strategy is clear
""",
            "labels": ["area:lakehouse", "type:docs", "priority:medium"]
        }
    ],
    "DB-ML3 – Weaviate / vector schema and indexes": [
        {
            "title": "DB-013: Lock baseline Weaviate class schema (NcChunkV1)",
            "body": """Finalize and lock the baseline Weaviate schema.

**Tasks:**
- [ ] Confirm NcChunkV1 Weaviate schema:
  - [ ] Class name, properties, multi-tenant config (tenant = account_id)
  - [ ] vectorIndexType: "hnsw" as baseline
- [ ] Ensure repo has:
  - [ ] JSON schema file
  - [ ] "Apply schema" script (curl or Python)
- [ ] Test schema application
- [ ] Document schema versioning strategy

**Done when:**
- NcChunkV1 schema is locked and versioned
- Schema file exists in repo
- Apply script exists and is tested
""",
            "labels": ["area:weaviate", "type:migrations", "priority:high"]
        },
        {
            "title": "DB-014: Align Weaviate documentation with reality",
            "body": """Update DM-003 and DM-005 to accurately reflect Weaviate implementation.

**Tasks:**
- [ ] Update DM-003:
  - [ ] Scope updated to "Weaviate 1.34+ multi-tenant"
  - [ ] "Index types supported" section present and accurate
  - [ ] Multi-tenant configuration documented
- [ ] Update DM-005:
  - [ ] §8.10 spells out class versioning
  - [ ] Index-type change process documented (NcChunkV{n+1} dual-write, benchmarks, DR updates)
- [ ] Review for consistency

**Done when:**
- DM-003 and DM-005 fully describe how Weaviate is used and governed
- Documentation matches implementation
""",
            "labels": ["area:weaviate", "type:docs", "priority:high"]
        },
        {
            "title": "DB-015: Create Weaviate dev environment setup",
            "body": """Build local development environment for Weaviate.

**Tasks:**
- [ ] Add docker-compose.weaviate.dev.yml to the repo:
  - [ ] Weaviate 1.34 container
  - [ ] Persistent volume configuration
  - [ ] Basic config
- [ ] Add Makefile helpers:
  - [ ] make weaviate_up
  - [ ] make weaviate_down
- [ ] Document setup in README or dev docs
- [ ] Test environment setup

**Done when:**
- New developer can run make weaviate_up successfully
- Weaviate container runs with correct version and config
- Setup is documented
""",
            "labels": ["area:weaviate", "type:dev-environment", "priority:medium"]
        },
        {
            "title": "DB-016: Build schema apply and smoke test scripts",
            "body": """Create automation for schema application and basic validation.

**Tasks:**
- [ ] Create script to:
  - [ ] Start Weaviate dev container
  - [ ] Apply NcChunkV1 schema
  - [ ] Insert a few chunks for account_id = test_account
  - [ ] Query back to ensure multi-tenant isolation works
- [ ] Document script usage
- [ ] Integrate into smoke test suite
- [ ] Add to CI if appropriate

**Done when:**
- Script exists and is documented (scripts/apply_weaviate_schema.sh or similar)
- Smoke test validates multi-tenant isolation
- New developer can run full test successfully
""",
            "labels": ["area:weaviate", "type:testing", "priority:high"]
        }
    ],
    "DB-ML4 – Cross-store contracts and lineage": [
        {
            "title": "DB-017: Create data contract specification (DCON-001)",
            "body": """Define comprehensive data contracts for all major entities and events.

**Tasks:**
- [ ] For each major entity and event:
  - [ ] Define field types and constraints
  - [ ] Define how it appears in:
    - [ ] nc.* (OLTP)
    - [ ] Lake/Iceberg (analytics)
    - [ ] Weaviate (if applicable)
- [ ] Document contract specifications
- [ ] Create validation rules
- [ ] Align with existing DCON-001 if it exists

**Done when:**
- DCON-001 exists and covers all major entities
- Each entity has clear contract definition across all stores
""",
            "labels": ["area:data-contracts", "type:docs", "priority:high"]
        },
        {
            "title": "DB-018: Build lineage mapping documentation (LIN-001)",
            "body": """Create comprehensive data lineage documentation.

**Tasks:**
- [ ] Draw lineage per domain:
  - [ ] Ingestion → nc.raw_* → nc.chunk → NcChunkV1 → analytics tables
  - [ ] Scan → nc.scan → nc.finding → nc.ticket / nc.remediation → lake
- [ ] Create lineage diagrams
- [ ] Document lineage in LIN-001 or similar document
- [ ] Link to related documents (DM-003, DM-005, LAK-001)

**Done when:**
- LIN-001 exists with clear lineage for all major data flows
- Diagrams are created and documented
- Lineage is traceable from source to all destinations
""",
            "labels": ["area:lineage", "type:docs", "priority:high"]
        },
        {
            "title": "DB-019: Implement consistency checks across stores",
            "body": """Build automated consistency validation across data stores.

**Tasks:**
- [ ] Create script-level sanity checks:
  - [ ] For a test account, count of findings in OLTP vs lake vs Weaviate should align
  - [ ] Validate data freshness across stores
  - [ ] Check referential integrity where applicable
- [ ] Document consistency rules and SLAs
- [ ] Add to smoke test suite
- [ ] Create alerting for consistency violations

**Done when:**
- For any entity (e.g., finding), can answer:
  - Where is source of truth?
  - Where are copies/derivatives stored?
  - How do we know they're in sync?
- Automated checks exist and run regularly
""",
            "labels": ["area:data-quality", "type:testing", "priority:medium"]
        }
    ],
    "DB-ML5 – DR, performance, and capacity for the DB layer": [
        {
            "title": "DB-020: Align DR-001 for all database stores",
            "body": """Extend DR-001 to cover all database and storage systems.

**Tasks:**
- [ ] Document backup strategy for:
  - [ ] Postgres (nc_dev equivalent in prod)
  - [ ] Weaviate (snapshots, export)
  - [ ] Lake / Iceberg catalog
- [ ] Define RPO/RTO for each store
- [ ] Document restore procedures
- [ ] Create backup automation or procedures
- [ ] Test backup and restore procedures

**Done when:**
- DR-001 mentions Postgres, Weaviate, and lake explicitly
- Backup/restore mechanics are documented
- RPO/RTO targets are defined
""",
            "labels": ["area:dr", "type:docs", "priority:high"]
        },
        {
            "title": "DB-021: Establish performance baselines and SLOs",
            "body": """Define and measure performance baselines for database operations.

**Tasks:**
- [ ] Define key queries:
  - [ ] Dashboard queries for findings, scans, tickets
  - [ ] Search queries in Weaviate
  - [ ] Analytics queries in lake
- [ ] On dev environment:
  - [ ] Run simple load tests or query timing at small scale
  - [ ] Measure baseline performance
- [ ] Set preliminary SLOs:
  - [ ] P95 response times for critical queries
  - [ ] Throughput targets
  - [ ] Concurrent user capacity
- [ ] Document in performance docs

**Done when:**
- Key queries are identified and documented
- Performance baselines are measured and documented
- SLOs are defined
""",
            "labels": ["area:performance", "type:docs", "priority:medium"]
        },
        {
            "title": "DB-022: Create capacity model (CAP-001)",
            "body": """Build capacity planning model for database layer.

**Tasks:**
- [ ] Very rough sizing:
  - [ ] Expected rows/day for each big table (finding, audit_log, event)
  - [ ] Expected GB/day in lake
  - [ ] Expected vectors/day in Weaviate
- [ ] Growth assumptions and projections
- [ ] Define what triggers scaling changes
- [ ] Document in CAP-001 or equivalent
- [ ] Create monitoring dashboards for capacity metrics

**Done when:**
- CAP-001 (or equivalent sections) mentions all stores explicitly
- Rough understanding of:
  - Growth rates
  - Scaling triggers
  - Capacity limits
""",
            "labels": ["area:capacity", "type:docs", "priority:medium"]
        }
    ]
}


def run_gh_command(args: List[str]) -> Dict:
    """Run a gh CLI command and return the result."""
    try:
        result = subprocess.run(
            ["gh"] + args,
            capture_output=True,
            text=True,
            check=True
        )
        if result.stdout:
            try:
                return json.loads(result.stdout)
            except json.JSONDecodeError:
                return {"output": result.stdout}
        return {"success": True}
    except subprocess.CalledProcessError as e:
        print(f"Error running gh command: {e.stderr}", file=sys.stderr)
        return {"error": e.stderr, "stdout": e.stdout}


def get_existing_milestones() -> List[Dict]:
    """Get list of existing milestones."""
    result = run_gh_command([
        "api",
        f"/repos/{REPO_OWNER}/{REPO_NAME}/milestones",
        "--jq", "."
    ])
    if "error" in result:
        return []
    return result if isinstance(result, list) else []


def create_milestone(title: str, description: str) -> Optional[Dict]:
    """Create a GitHub milestone."""
    print(f"Creating milestone: {title}")
    result = run_gh_command([
        "api",
        f"/repos/{REPO_OWNER}/{REPO_NAME}/milestones",
        "-f", f"title={title}",
        "-f", f"description={description}",
        "-X", "POST"
    ])
    
    if "error" in result:
        # Check if milestone already exists
        if "already exists" in result.get("error", "").lower():
            print(f"  Milestone already exists: {title}")
            existing = get_existing_milestones()
            for m in existing:
                if m.get("title") == title:
                    return m
        else:
            print(f"  Error creating milestone: {result.get('error')}")
        return None
    
    print(f"  Created milestone: {title} (number: {result.get('number')})")
    return result


def get_existing_labels() -> List[str]:
    """Get list of existing labels."""
    result = run_gh_command([
        "api",
        f"/repos/{REPO_OWNER}/{REPO_NAME}/labels",
        "--jq", ".[].name"
    ])
    if "error" in result:
        return []
    if "output" in result:
        return [label.strip() for label in result["output"].split("\n") if label.strip()]
    return []


def create_issue(title: str, body: str, milestone_number: int, labels: List[str]) -> Optional[Dict]:
    """Create a GitHub issue."""
    print(f"  Creating issue: {title}")
    
    # Filter labels to only include those that exist
    existing_labels = get_existing_labels()
    valid_labels = [label for label in labels if label in existing_labels]
    
    if len(valid_labels) < len(labels):
        print(f"    Note: Some labels don't exist and will be skipped: {set(labels) - set(valid_labels)}")
    
    args = [
        "api",
        f"/repos/{REPO_OWNER}/{REPO_NAME}/issues",
        "-f", f"title={title}",
        "-f", f"body={body}",
        "-f", f"milestone={milestone_number}",
        "-X", "POST"
    ]
    
    # Add labels if any are valid
    if valid_labels:
        for label in valid_labels:
            args.extend(["-f", f"labels[]={label}"])
    
    result = run_gh_command(args)
    
    if "error" in result:
        print(f"    Error creating issue: {result.get('error')}")
        return None
    
    print(f"    Created issue #{result.get('number')}: {title}")
    return result


def main():
    """Main function to create milestones and issues."""
    print(f"Creating milestones and issues for {REPO_OWNER}/{REPO_NAME}")
    print("=" * 80)
    
    # Check authentication
    auth_check = subprocess.run(
        ["gh", "auth", "status"],
        capture_output=True,
        text=True
    )
    if auth_check.returncode != 0:
        print("ERROR: gh CLI is not authenticated. Please run 'gh auth login' first.")
        sys.exit(1)
    
    # Get existing milestones
    existing_milestones = get_existing_milestones()
    existing_milestone_titles = {m.get("title"): m for m in existing_milestones}
    
    # Track created milestones and issues
    created_milestones = []
    created_issues = []
    
    # Create milestones
    print("\n" + "=" * 80)
    print("CREATING MILESTONES")
    print("=" * 80)
    
    milestone_map = {}
    for milestone_def in MILESTONES:
        title = milestone_def["title"]
        description = milestone_def["description"]
        
        if title in existing_milestone_titles:
            print(f"Milestone already exists: {title}")
            milestone = existing_milestone_titles[title]
        else:
            milestone = create_milestone(title, description)
        
        if milestone:
            milestone_map[title] = milestone
            created_milestones.append({
                "number": milestone.get("number"),
                "title": title,
                "description": description
            })
    
    # Create issues for each milestone
    print("\n" + "=" * 80)
    print("CREATING ISSUES")
    print("=" * 80)
    
    for milestone_title, issues_list in ISSUES.items():
        if milestone_title not in milestone_map:
            print(f"Warning: Milestone '{milestone_title}' not found, skipping issues")
            continue
        
        milestone_number = milestone_map[milestone_title].get("number")
        print(f"\nCreating issues for milestone: {milestone_title} (#{milestone_number})")
        
        for issue_def in issues_list:
            issue = create_issue(
                title=issue_def["title"],
                body=issue_def["body"],
                milestone_number=milestone_number,
                labels=issue_def.get("labels", [])
            )
            
            if issue:
                created_issues.append({
                    "number": issue.get("number"),
                    "title": issue_def["title"],
                    "milestone": milestone_title
                })
    
    # Print summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    
    print(f"\nMilestones created/verified: {len(created_milestones)}")
    for m in created_milestones:
        print(f"  - #{m['number']}: {m['title']}")
    
    print(f"\nIssues created: {len(created_issues)}")
    for i in created_issues:
        print(f"  - #{i['number']}: {i['title']} (Milestone: {i['milestone']})")
    
    print("\n" + "=" * 80)
    print("DONE")
    print("=" * 80)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
