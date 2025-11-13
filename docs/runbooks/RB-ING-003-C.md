# Document ID: RB-ING-003-C
**Title:** Vector Store Sync Audit  
**Status:** Draft v0.1  
**Owner:** ml-platform  
**Last Reviewed:** 2025-11-09  
**References:** ING-003, SVC-001, OBS-002

---

## 1. Purpose
Ensure the vector store remains in sync with the Lakehouse canonical dataset by periodically auditing counts and sample payloads.

## 2. Preconditions
- Scheduled audit window or alert `vector_parity_gap > 0.5%`.  
- Access to Weaviate/OpenSearch clusters and Athena tables.  
- Tools repo checked out with `python tools/vector_diff.py`.

## 3. Response Steps
1. Run parity script: `python tools/vector_diff.py --window 1h --output /tmp/parity.json`.  
2. Investigate mismatched IDs; confirm whether embeddings failed or TTL expired.  
3. For missing vectors, requeue payloads via `python tools/requeue_vectors.py --ids file`.  
4. For stale vectors, trigger compaction/index rebuild using `make vector-compact`.  
5. Update dashboards with audit results and log ticket with remediation steps.

## 4. Validation
- Parity gap < 0.1%.  
- Index rebuild completes successfully and search latency stays within SLO.  
- Audit artifacts stored in `s3://nc-audit-artifacts/<date>/vector-sync/`.

## 5. Escalation
Escalate to platform-serving if parity gap persists after two requeues or if latency SLO breach occurs during remediation.
