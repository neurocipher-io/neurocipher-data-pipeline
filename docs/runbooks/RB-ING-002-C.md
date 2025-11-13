# Document ID: RB-ING-002-C
**Title:** PII Redaction Audit  
**Status:** Draft v0.1  
**Owner:** security-engineering  
**Last Reviewed:** 2025-11-09  
**References:** ING-002, GOV-001, REF-001

---

## 1. Purpose
Validate that PII redaction rules remain effective and documented whenever new fields or partners are onboarded.

## 2. Preconditions
- Audit request from Security or scheduled quarterly review.  
- Access to masked sample set in `s3://nc-clean-zone-samples/`.  
- Latest redaction config in `services/normalization/config/redaction.yaml`.

## 3. Response Steps
1. Generate fresh sample export: `python tools/sample_exports.py --size 500`.  
2. Run redaction unit tests `pytest -k redaction`.  
3. Compare masked output vs. REF-001 glossary to ensure required fields removed/hashed.  
4. Update `redaction.yaml` for any missing fields; rerun `make fmt && make test`.  
5. Document findings in `docs/security-controls` with before/after evidence.  
6. Obtain approval from Security Engineering lead before closing audit.

## 4. Validation
- Sample set passes automated checks (no plaintext PII).  
- Audit log stored in `ops/` evidence folder with reviewer sign-off.  
- Dashboards show zero PII rule violations.

## 5. Escalation
If critical PII leaks detected, trigger incident per SEC-001, rotate downstream data, and notify Legal immediately.
