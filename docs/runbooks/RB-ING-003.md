# Document ID: RB-ING-003
**Title:** S3 Event Loss Recovery Runbook  
**Status:** Draft v0.1  
**Owner:** platform-ingest  
**Last Reviewed:** 2025-11-09  
**References:** ING-001, ING-003, OBS-002

---

## 1. Purpose
Reconstruct and replay missing S3 events when EventBridge notifications are lost or delayed, safeguarding downstream enrichment SLAs.

## 2. Preconditions
- Alert triggered (missing partitions or ingest gap > 15 minutes).  
- Dynamo state index (`state_ingestion`) available.  
- Access to AWS CLI with permissions to list S3 objects and publish events.

## 3. Response Steps
1. Determine affected time window using Glue catalog and Athena (`SELECT max(event_time) FROM raw_table`).  
2. Query Dynamo index for object keys in the gap (`aws dynamodb query --table state_ingestion --key-condition-expression ...`).  
3. Export key list to `/tmp/replay.txt`.  
4. For each key, emit synthetic event via `aws events put-events --entries file://replay.json` or push to SQS ingest queue.  
5. Monitor `services/ingestion` metrics (ingest rate, DLQ) while replay proceeds.  
6. After replay, compact state index if necessary and document objects processed.

## 4. Validation
- Glue/Athena record counts match expected volumes.  
- Observability dashboards show no gap for the replayed interval.  
- DLQ remains empty; no duplicate detections > 0.1%.

## 5. Escalation
If >10% of data for the interval remains missing, escalate to Data Platform leadership and consider invoking DR-001 data restoration steps.
