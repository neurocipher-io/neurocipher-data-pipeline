# Document ID: RB-LAK-001-A
**Title:** Snapshot Expiration Procedure  
**Status:** Draft v0.1  
**Owner:** platform-data  
**Last Reviewed:** 2025-11-09  
**References:** LAK-001, DR-001, GOV-002

---

## 1. Purpose
Retire obsolete Iceberg snapshots to control storage costs while preserving recovery points mandated by DR-001.

## 2. Preconditions
- Snapshot inventory exported from Glue/Athena.  
- Approval from Data Governance for snapshot range removal.  
- Backups verified in `s3://nc-backups-<env>/`.

## 3. Procedure
1. List snapshots: `CALL system.snapshots('db.table')`.  
2. Identify candidates older than retention policy (e.g., > 45 days) excluding compliance-hold IDs.  
3. Export metadata to `ops/artifacts/snapshot-expiration/<date>.csv`.  
4. Run `CALL system.expire_snapshots('db.table', older_than => TIMESTAMP '...')`.  
5. Trigger compaction/manifest cleanup job via `make lakehouse-maint`.  
6. Update records in governance tracker and notify stakeholders.

## 4. Validation
- `system.snapshots` output excludes expired IDs.  
- Storage metrics drop as expected without impacting queries.  
- DR-001 RPO still achievable (retain required number of snapshots).

## 5. Escalation
If expiration fails or removes required snapshots, halt process and escalate to Platform SRE + Governance; prepare restore via DR-001 before resuming.
