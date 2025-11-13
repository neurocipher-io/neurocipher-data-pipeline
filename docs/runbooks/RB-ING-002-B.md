# Document ID: RB-ING-002-B
**Title:** Dedup Drift Investigation  
**Status:** Draft v0.1  
**Owner:** platform-data  
**Last Reviewed:** 2025-11-09  
**References:** ING-002, OBS-002, CI/CL-003

---

## 1. Purpose
Respond when dedup false positives/negatives exceed thresholds, preventing missed or duplicated records in the Clean Zone.

## 2. Preconditions
- Alert `dedup_drift_ratio > 5%` or manual report.  
- Access to Redshift/Athena tables for duplicate sampling.  
- Recent deployment info from CI run.

## 3. Response Steps
1. Pull metrics for affected partition (`aws cloudwatch get-metric-data`).  
2. Sample duplicates via Athena query comparing hashes vs. payload IDs.  
3. Inspect dedup cache TTL and bloom filter stats in `services/normalization/logs`.  
4. If TTL misconfigured, update config map in `ops/dashboards` and redeploy service.  
5. If hash collision, adjust canonicalization code in `libs/python/dedup.py` and bump version.  
6. Reprocess affected window using `python tools/replay.py --window <start> <end>`.

## 4. Validation
- Drift ratio < 1% sustained for 1 hour.  
- Replay job outputs success metrics with zero errors.  
- Dashboards reflect expected ingest rate.

## 5. Escalation
If drift persists, escalate to Data Governance for approval to purge/rebuild affected partitions before resuming ingestion.
