# Document ID: RB-LAK-001-C
**Title:** Catalog Rebuild Runbook  
**Status:** Draft v0.1  
**Owner:** platform-data  
**Last Reviewed:** 2025-11-09  
**References:** LAK-001, SRG-001, DR-001

---

## 1. Purpose
Restore Glue/Athena catalog metadata from backups when corruption or accidental deletion occurs.

## 2. Preconditions
- Confirmed catalog outage (queries failing with `EntityNotFoundException`).  
- Backup manifest available in `s3://nc-backups-<env>/glue/`.  
- Change freeze initiated for Lakehouse writes.

## 3. Procedure
1. Export current catalog state with `aws glue get-databases` for audit.  
2. Stop ingestion jobs targeting affected tables.  
3. Restore metadata by running `python tools/glue_restore.py --manifest <path>`.  
4. Re-register Iceberg tables using `spark-submit tools/register_iceberg.py --table <name>`.  
5. Validate via Athena queries and `CALL system.tables()` output.  
6. Resume ingestion jobs and note rebuild in incident log.

## 4. Validation
- Queries succeed with expected schemas.  
- Observability dashboard for catalog health green.  
- Backup manifest archived with timestamp post-restore.

## 5. Escalation
If restore fails or data drift detected, escalate to Infra team and consider cross-region recovery steps defined in DR-001.
