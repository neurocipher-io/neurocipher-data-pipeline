# Document ID: RB-LAK-001-D
**Title:** Lifecycle Policy Verification  
**Status:** Draft v0.1  
**Owner:** platform-data  
**Last Reviewed:** 2025-11-09  
**References:** LAK-001, GOV-002, DR-001

---

## 1. Purpose
Verify S3 lifecycle policies (transition, expiration, replication) remain aligned with governance requirements after infra changes.

## 2. Preconditions
- Recent IaC change touching storage buckets.  
- Access to `iac/stacks/core` and AWS CLI.  
- Policy definitions documented in GOV-002.

## 3. Procedure
1. List lifecycle rules: `aws s3api get-bucket-lifecycle-configuration --bucket <name>`.  
2. Compare results to IaC templates and governance spreadsheet.  
3. Run sample object tests: upload tagged object and confirm transition events (Glacier, deletion) via CloudTrail.  
4. Validate replication configuration if multi-region.  
5. Document verification in `docs/governance` and attach evidence.

## 4. Validation
- Policy output matches expected filters/actions.  
- Sample objects transition/expire per schedule.  
- Auditors supplied with evidence pack.

## 5. Escalation
If policies drift or violate retention requirements, halt related deployments, open Sev-2 incident, and engage Governance plus Security to remediate.
