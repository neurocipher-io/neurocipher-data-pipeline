# Document ID: RB-ING-001
**Title:** Ingest Backlog Remediation Runbook  
**Status:** Draft v0.1  
**Owner:** platform-ingest (see `ops/owners.yaml`)  
**Last Reviewed:** 2025-11-09  
**References:** ING-001, OBS-002, CI/CL-003

---

## 1. Purpose
Restore steady-state ingestion when SQS backlog or DLQ depth breaches alert thresholds, ensuring no loss or duplication of customer events.

## 2. Preconditions
- PagerDuty alert or dashboard shows backlog > 15 minutes or DLQ > 1,000 messages.
- Access to AWS console/CLI for `sqs`, `cloudwatch`, and `lambda`.
- Latest schema bundle pulled (`schemas/events/`).

## 3. Response Steps
1. Confirm alert scope via `aws sqs get-queue-attributes --queue-url $QUEUE --attribute-names ApproximateNumberOfMessages`.  
2. Pause downstream consumers by setting Lambda reserved concurrency to 0 (`aws lambda put-function-concurrency`).  
3. Inspect DLQ samples with `aws sqs receive-message` and validate against schema (`npm run spectral` or `make test`).  
4. Apply fixes (schema roll forward/back, config) and redeploy via `make deploy-dev` → promote to `stg`.  
5. Redrive DLQ using `aws sqs start-message-move-task` once fix validated.  
6. Restore consumer concurrency gradually (25%, 50%, 100%) while monitoring p95 ingest latency.

## 4. Validation
- Backlog returns to < 5 minutes sustained for 15 minutes.  
- DLQ drain complete (`ApproximateNumberOfMessages` = 0).  
- No new errors in `platform-ingest` log stream for 30 minutes.  
- `make test` green, Spectral + markdownlint pass.

## 5. Escalation
If backlog grows after fix or replay exceeds 2 hours, escalate to Platform On-Call (`pagerduty:ingest-api`) and file incident with timeline, commands run, and data samples.
