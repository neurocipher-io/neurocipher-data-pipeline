# GitHub Milestones and Issues Management

This directory contains scripts and data files for managing GitHub milestones and issues for the neurocipher-data-pipeline project.

## Files

- `milestones_and_issues.json` - Complete specification of all milestones and issues for the database roadmap
- `create_milestones_and_issues.py` - Python script to create the milestones and issues in GitHub

## Database Roadmap Milestones

The database roadmap is organized into 6 milestones with a total of 22 issues:

### DB-ML0 – Inventory and gap map (3 issues)
Single, accurate map of all entities and where they physically live (Postgres / S3 / Weaviate), plus what's implemented vs not.

### DB-ML1 – Postgres OLTP schema finalized (nc.*) (5 issues)
nc schema is complete, consistent with DM-003, and safe to run in dev/stg/prod.

### DB-ML2 – Lake / Iceberg layout (LAK-001 + physical DDL) (4 issues)
Define and implement the analytical/lake tables for long-term storage and heavy analytics, separate from OLTP.

### DB-ML3 – Weaviate / vector schema and indexes (4 issues)
Clean, documented Weaviate schema with clear governance for class versions and index types.

### DB-ML4 – Cross-store contracts and lineage (3 issues)
Every piece of data has a clear contract and lineage between Postgres, S3/Iceberg, and Weaviate.

### DB-ML5 – DR, performance, and capacity for the DB layer (3 issues)
Database layer is not only designed but also operable: DR, performance targets, and capacity planning exist and are enforceable.

## Usage

### Prerequisites

1. Install the GitHub CLI (`gh`):
   ```bash
   # macOS
   brew install gh
   
   # Linux
   # See https://github.com/cli/cli/blob/trunk/docs/install_linux.md
   ```

2. Authenticate with GitHub:
   ```bash
   gh auth login
   ```

### Creating Milestones and Issues

Run the Python script to create all milestones and issues:

```bash
python scripts/github/create_milestones_and_issues.py
```

The script will:
1. Check if you're authenticated with GitHub
2. Create all 6 milestones (or skip if they already exist)
3. Create all 22 issues and assign them to their respective milestones
4. Apply labels to issues (only if the labels already exist in the repository)
5. Print a summary of created milestones and issues

### Manual Creation

If you prefer to create milestones and issues manually, refer to the `milestones_and_issues.json` file for the complete specification including:
- Milestone titles and descriptions
- Issue titles, bodies (with task checklists), and labels
- Milestone assignments for each issue

### Issue Naming Convention

All issues follow the naming pattern: `DB-XXX: <clear action>`

Examples:
- DB-001: Build entity → store → migration status matrix
- DB-002: Complete implementation status audit for all entities
- DB-003: Create gap list and mismatch documentation

### Labels

The following labels are expected to exist in the repository:
- `area:db` - Database-related tasks
- `area:lakehouse` - Lakehouse/lake-related tasks
- `area:weaviate` - Weaviate vector database tasks
- `area:data-contracts` - Data contract tasks
- `area:lineage` - Data lineage tasks
- `area:data-quality` - Data quality tasks
- `area:dr` - Disaster recovery tasks
- `area:performance` - Performance-related tasks
- `area:capacity` - Capacity planning tasks
- `type:docs` - Documentation tasks
- `type:audit` - Audit tasks
- `type:migrations` - Migration tasks
- `type:testing` - Testing tasks
- `type:dev-environment` - Development environment tasks
- `priority:critical` - Critical priority
- `priority:high` - High priority
- `priority:medium` - Medium priority

## Troubleshooting

### Authentication Issues

If you see "gh CLI is not authenticated", run:
```bash
gh auth status
gh auth login
```

### Missing Labels

If labels don't exist in the repository, the script will skip them but still create the issues. You can:
1. Create the missing labels manually in GitHub
2. Run the script again (it will skip existing issues/milestones)
3. Or manually add labels to the created issues

### Permission Issues

Ensure you have write access to the `neurocipher-io/neurocipher-data-pipeline` repository.

## Reference

For the complete database roadmap specification that this implementation is based on, see the original specification document provided in the project issue.
