# Document ID: RB-ING-003-B
**Title:** Iceberg Commit Rollback  
**Status:** Draft v0.1  
**Owner:** platform-data  
**Last Reviewed:** 2025-11-09  
**References:** ING-003, LAK-001, DR-001

---

## 1. Purpose
Rollback a failed Iceberg commit that corrupted a table snapshot or introduced bad data.

## 2. Preconditions
- Confirmed bad commit ID from Glue/Athena query.  
- Access to S3 versioned data and Iceberg CLI or Spark job runner.  
- Change freeze communicated to stakeholders.

## 3. Response Steps
1. Locate problematic snapshot via `CALL system.history('db.table') ORDER BY made_current_at DESC`.  
2. Disable downstream consumers (set `vector_sync_enabled=false`).  
3. Execute rollback: `CALL system.rollback_to_snapshot('db.table', <snapshot_id>)`.  
4. Validate with targeted queries (row counts, checksums).  
5. Rebuild metadata caches and rerun compaction job if needed.  
6. Re-enable consumers and document snapshot IDs in incident log.

## 4. Validation
- Checksums match pre-incident baseline.  
- No lingering write errors for 30 minutes.  
- Dashboards show normalized latency.

## 5. Escalation
If rollback fails or data loss exceeds RPO, invoke DR-001 for table restore from backups and notify leadership.
