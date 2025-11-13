# Document ID: RB-ING-002
**Title:** Schema Violation Handling Runbook  
**Status:** Draft v0.1  
**Owner:** platform-ingest  
**Last Reviewed:** 2025-11-09  
**References:** ING-001, SRG-001, DCON-001

---

## 1. Purpose
Resolve schema validation failures in the raw ingestion pipeline and restore contracts with upstream publishers.

## 2. Preconditions
- Alert from OBS-002 dashboard (`schema_validation_error_rate > 2%`).  
- Recent payload sample captured in DLQ or CloudWatch Logs.  
- Access to schema registry repo (`schemas/events/`).

## 3. Response Steps
1. Pull failing message from DLQ and save to `/tmp/failing-payload.json`.  
2. Validate locally: `spectral lint failing-payload.json -r schemas/events/<event>.json`.  
3. Identify root cause (publisher regression vs. schema drift).  
4. If publisher regression, coordinate rollback; if schema drift, update schema + version (e.g., `event.foo.bar.v2.json`).  
5. Run `make fmt && make test` and open PR referencing incident/Jira.  
6. Deploy fix through CI/CD; once deployed, redrive DLQ with `aws sqs start-message-move-task`.

## 4. Validation
- Error rate < 0.2% for 30 minutes.  
- New schema published with `$id` and examples.  
- DLQ cleared and no new validation alarms.

## 5. Escalation
If fix requires contract negotiation or results in data loss, escalate to Data Governance plus Platform On-Call; capture decision in ADR or SRG appendix.
