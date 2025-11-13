# Document ID: RB-LAK-001-B
**Title:** Orphan File Remediation  
**Status:** Draft v0.1  
**Owner:** platform-data  
**Last Reviewed:** 2025-11-09  
**References:** LAK-001, OBS-003, DR-001

---

## 1. Purpose
Detect and delete Parquet files not referenced by current Iceberg manifests to reduce storage waste and prevent query inconsistency.

## 2. Preconditions
- List of orphan candidates generated via `python tools/find_orphans.py`.  
- Confirmation backups exist for the affected partitions.  
- Maintenance window scheduled.

## 3. Procedure
1. Save orphan list to `ops/artifacts/orphans/<date>.json`.  
2. Sample 5% of entries to verify they are not active snapshots.  
3. Remove files using `aws s3 rm --recursive --exclude '' --include '@orphans.txt'`.  
4. Run `CALL system.rewrite_manifests('db.table')` to purge references.  
5. Trigger Glue crawler to refresh metadata.  
6. Update observability dashboard notes with cleanup summary.

## 4. Validation
- Athena queries return expected row counts.  
- Storage metrics align with planned reduction.  
- No new errors in Iceberg commit logs.

## 5. Escalation
If deletion affects live data, immediately restore from backup and escalate to the Lakehouse owner to review detection heuristics.
