# Document ID: RB-ING-003-D
**Title:** Reference Data Refresh  
**Status:** Draft v0.1  
**Owner:** platform-data  
**Last Reviewed:** 2025-11-09  
**References:** ING-003, DCON-001, GOV-001

---

## 1. Purpose
Refresh cached reference datasets (taxonomies, customer metadata) used by enrichment workers and ensure alignment with authoritative sources.

## 2. Preconditions
- Refresh window scheduled or change request approved.  
- Source-of-truth dataset available in Lakehouse or partner S3 bucket.  
- Feature flags ready for toggling new reference set.

## 3. Response Steps
1. Capture current reference version (`cat services/enrichment/config/reference_version`).  
2. Pull new dataset via `python tools/download_reference.py --source <path>`.  
3. Validate schema and checksums (`make test` runs `pytest -k reference`).  
4. Publish to cache bucket `s3://nc-reference/<env>/` with new version tag.  
5. Update config map and redeploy enrichment workers.  
6. Monitor enrichment latency/error metrics for 30 minutes.

## 4. Validation
- Workers read new version and emit success logs.  
- Checksums stored in `ops/dashboards/reference.json`.  
- No increase in enrichment failures.

## 5. Escalation
If refresh causes regressions, roll back to previous version using stored artifact and notify data consumers of the temporary pause.
