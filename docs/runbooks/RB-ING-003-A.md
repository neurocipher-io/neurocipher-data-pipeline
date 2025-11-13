# Document ID: RB-ING-003-A
**Title:** Sink Failure Recovery  
**Status:** Draft v0.1  
**Owner:** platform-data  
**Last Reviewed:** 2025-11-09  
**References:** ING-003, OBS-003, LAK-001

---

## 1. Purpose
Recover enrichment sinks (Lakehouse, Vector store, Search) when writes fail or retries exhaust, ensuring data parity across destinations.

## 2. Preconditions
- Alert on sink error rate > 1% or backlog > 10 minutes.  
- DLQ messages captured for failed sink operations.  
- Access to sink credentials and replay tooling.

## 3. Response Steps
1. Identify failing sink via metrics tags (`sink=lake`, `sink=vector`, etc.).  
2. For Lakehouse: inspect Iceberg commit logs; for Vector: check Weaviate health `/v1/.well-known/ready`.  
3. Pause failing sink worker using deployment toggle (`make deploy-dev WORKER=<name> DISABLE=true`).  
4. Apply fix (e.g., schema update, index rebuild).  
5. Replay messages from DLQ with `python tools/replay_sink.py --sink <name> --from-dlq`.  
6. Re-enable worker and monitor throughput.

## 4. Validation
- Sink success rate back to ≥ 99.5%.  
- DLQ drained.  
- Cross-sink parity check via `python tools/parity_check.py --window 1h` passes.

## 5. Escalation
If failure persists > 30 minutes or parity check fails twice, escalate to Platform SRE and consider invoking RB-ING-003-B or DR-001 for deeper recovery.
