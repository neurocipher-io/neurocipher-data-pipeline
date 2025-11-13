# Document ID: RB-PROC-001
**Title:** Batch Pipeline Rollback  
**Status:** Draft v0.1  
**Owner:** platform-data  
**Last Reviewed:** 2025-11-09  
**References:** PROC-001, DR-001, OBS-002

---

## 1. Purpose
Restore batch job outputs when deployment introduces regressions, leveraging S3 versioning or RDS PITR as defined in PROC-001.

## 2. Preconditions
- Failed batch release identified (CI build ID + timestamp).  
- S3 versioning enabled on target buckets; RDS PITR snapshots available.  
- Change freeze approved.

## 3. Response Steps
1. Stop batch scheduler (`aws stepfunctions update-state-machine --logging-configuration ... disabled`).  
2. Determine corrupted window (e.g., last successful run).  
3. For S3 outputs: use `aws s3api list-object-versions` and restore previous version via `copy-object`.  
4. For RDS: initiate PITR to new instance, validate data, then promote.  
5. Redeploy previous application artifact (`make deploy --artifact <sha>`).  
6. Resume scheduler and monitor first run closely.

## 4. Validation
- Data parity confirmed against baseline metrics.  
- Observability alerts cleared.  
- Incident ticket updated with restored snapshot/version IDs.

## 5. Escalation
If rollback fails or data loss exceeds RPO, escalate to DR lead and execute relevant sections of DR-001.
