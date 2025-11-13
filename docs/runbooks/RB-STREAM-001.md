# Document ID: RB-STREAM-001
**Title:** Stream Processing Rollback  
**Status:** Draft v0.1  
**Owner:** platform-data  
**Last Reviewed:** 2025-11-09  
**References:** PROC-002, OBS-002, CI/CL-003

---

## 1. Purpose
Rollback stream processing deployments (Kinesis, Kafka, Flink) when regressions or SLO breaches occur, minimizing downstream impact.

## 2. Preconditions
- Elevated error rate or latency triggered alerts.  
- Knowledge of last good artifact (Git SHA).  
- Replay buffers/SQS DLQs healthy.

## 3. Response Steps
1. Pause consumer via `aws lambda put-function-concurrency --reserved-concurrent-executions 0` or Flink stop command.  
2. Tag current checkpoint offset for potential forward recovery.  
3. Redeploy previous version (`make deploy --service stream --artifact <sha>`).  
4. Validate health metrics; if good, replay backlog from checkpoints using `python tools/replay_stream.py --offset <value>`.  
5. Record incident notes and root-cause owners.

## 4. Validation
- Error/latency metrics return to baseline.  
- Replay completes and throughput normalizes.  
- No data loss per checkpoint comparison.

## 5. Escalation
If rollback fails, escalate to platform-serving + SRE, evaluate DR-001 or blue/green cutover, and coordinate stakeholder communications.
