# Document ID: RB-ING-002-A
**Title:** Validation Failure Remediation  
**Status:** Draft v0.1  
**Owner:** platform-data  
**Last Reviewed:** 2025-11-09  
**References:** ING-002, SRG-001, OBS-001

---

## 1. Purpose
Provide a rapid checklist for reprocessing invalid normalization messages immediately after schema updates.

## 2. Preconditions
- Normalization service deployed with new schema version.  
- Invalid payloads accumulating in DLQ or quarantine bucket.  
- Access to latest schema bundle and release notes.

## 3. Response Steps
1. Compare deployed schema version vs. repo tag (`git describe --tags`).  
2. Run `python scripts/validate_payloads.py --input dlq.json --schema <file>` to confirm failure reason.  
3. Patch transformation mappings if required; rerun `make fmt && make test`.  
4. Deploy fix to `dev` via CI, run smoke test (`pytest -k normalization`).  
5. Redrive invalid payloads using `aws sqs start-message-move-task` or `kinesis firehose start-delivery`.  
6. Monitor normalization error dashboard for 30 minutes.

## 4. Validation
- Error rate < 0.5% with steady throughput.  
- All DLQ messages processed successfully.  
- Change log captured in release notes.

## 5. Escalation
If invalid payloads persist after two fixes, revert to previous schema version and schedule working session with upstream publisher.
