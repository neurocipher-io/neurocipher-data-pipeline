# Document ID: RB-OPS-004
**Title:** Cardinality Spike Mitigation  
**Status:** Draft v0.1  
**Owner:** platform-serving  
**Last Reviewed:** 2025-11-09  
**References:** OBS-002, OBS-003, OPS-001

---

## 1. Purpose
Reduce metrics/log cardinality explosions that threaten observability billing and system stability.

## 2. Preconditions
- Alert for `cardinality_spike_ratio > 1.5`.  
- Access to Grafana, Prometheus, and logging pipelines.  
- Recent deployment details.

## 3. Response Steps
1. Identify source metric/log label via Grafana `cardinality-exporter`.  
2. If tied to new release, roll back offending service.  
3. Apply relabel/drop rules in Prometheus (`ops/dashboards/prometheus-rules.yaml`) or update OpenSearch pipeline filters.  
4. Purge high-cardinality logs via retention override if required.  
5. Recalculate ingestion volume using `promtool tsdb analyze`.  
6. Document mitigation and open follow-up issue for long-term fix.

## 4. Validation
- Cardinality ratio < 1.1 for 1 hour.  
- Metrics pipeline ingest < capacity threshold.  
- Billing alerts cleared.

## 5. Escalation
If cardinality spike continues or impacts monitoring coverage, escalate to Observability lead and consider sampling or temporary alert suppression.
