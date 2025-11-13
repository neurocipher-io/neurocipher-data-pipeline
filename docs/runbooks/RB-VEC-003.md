# Document ID: RB-VEC-003
**Title:** Vector Latency Investigation  
**Status:** Draft v0.1  
**Owner:** ml-platform  
**Last Reviewed:** 2025-11-09  
**References:** SVC-001, ING-003, OBS-002

---

## 1. Purpose
Diagnose elevated p95 latency for vector search endpoints (Weaviate/OpenSearch hybrid) and restore service performance.

## 2. Preconditions
- Alert `vector_latency_p95 > 400ms`.  
- Access to Weaviate admin APIs and OpenSearch dashboards.  
- Recent deployment logs available.

## 3. Response Steps
1. Check cluster health: `curl $WEAVIATE/v1/.well-known/ready` and `GET _cluster/health`.  
2. Inspect resource usage (CPU/memory/IO) via CloudWatch or Grafana.  
3. Verify index compaction schedule; run `python tools/compact_vectors.py` if overdue.  
4. Rebalance shards or scale nodes using IaC parameter (`terraform apply -target=module.vector_cluster`).  
5. Flush caches and warm embeddings through synthetic queries.  
6. Communicate status in `#query-alerts`.

## 4. Validation
- p95 latency < 250ms for 30 minutes.  
- No error spike in ingestion or query pipelines.  
- Capacity dashboard shows healthy utilization (< 70% CPU).

## 5. Escalation
If latency remains high after scaling + compaction, escalate to platform-serving and consider feature flagging heavy endpoints until fix ships.
