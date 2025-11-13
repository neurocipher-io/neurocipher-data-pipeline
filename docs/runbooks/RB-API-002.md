# Document ID: RB-API-002
**Title:** Elevated API 5xx Response Runbook  
**Status:** Draft v0.1  
**Owner:** platform-serving  
**Last Reviewed:** 2025-11-09  
**References:** SVC-001, OBS-002, OPS-001

---

## 1. Purpose
Contain and resolve spikes in 5xx responses for public serving APIs (REST + GraphQL) while maintaining customer-facing SLAs.

## 2. Preconditions
- Alert from `api_5xx_rate` > 1% for 5 minutes.  
- Access to query-api logs and AWS ALB metrics.  
- Feature flag control for rate limiting.

## 3. Response Steps
1. Confirm scope via `aws cloudwatch get-metric-statistics --metric-name HTTPCode_ELB_5XX_Count`.  
2. Inspect recent deploys (`git log -5 services/query-api`). If new release, consider rollback.  
3. Check dependency health (Weaviate, OpenSearch, RDS) via existing dashboards.  
4. If saturation, enable surge queue or reduce concurrency via `aws appmesh update-virtual-node`.  
5. Capture failing requests with `sls logs -f query-api`.  
6. Apply fix (config change or hotfix), redeploy via `make deploy-dev && make deploy-stg`, then promote.

## 4. Validation
- 5xx rate < 0.1% for 30 minutes.  
- Latency remains within SLO.  
- Synthetic probes succeed.

## 5. Escalation
If customer impact persists > 15 minutes, escalate to platform-serving on-call and comms channel; coordinate with Security if issue is abuse-related.
