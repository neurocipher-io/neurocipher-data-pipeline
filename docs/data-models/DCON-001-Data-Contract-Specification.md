Status: Tier-1 Stub  
Owner: Data Architecture  
Approvers: Architecture Board, Data Engineering Lead  
Last updated: 2025-11-26  
Applies to: All inter-service communication, libs/python/nc_models/  
Related: DM-003, DM-005, SRG-001, DPS-ING-001, DPS-NORM-001, REF-001, REF-002

-----

## 1. Purpose

This document defines the rules, formats, and compatibility guarantees for data
contracts across the Neurocipher platform.

It exists to:

- Establish a single source of truth for shared data structures.
- Define versioning and backward compatibility requirements.
- Specify where canonical models live (`libs/python/nc_models/`).
- Prevent services from defining conflicting schemas.

-----

## 2. Scope

This document covers:

- Canonical data contract definitions (Finding, Asset, Identity, Event).
- Versioning strategy for contracts.
- Backward and forward compatibility rules.
- Validation and enforcement mechanisms.
- Location of canonical Pydantic models.

This document does not cover:

- Physical storage schemas (see DM-003).
- Wire protocol specifics (see openapi.yaml per service).
- Schema registry implementation (see SRG-001).

-----

## 3. References

- REF-001 Glossary and Standards Catalog (§4 Naming, §8 Data Classification, §11 Events)
- REF-002 Platform Constants
- DM-003 Physical Schemas and Storage Map
- DM-005 Governance, Versioning, and Migrations

-----

## 4. Canonical model location

All shared data models must be defined in:

```
libs/python/nc_models/
  src/
    nc_models/
      __init__.py
      finding.py          # SecurityFinding, FindingSeverity
      asset.py            # CloudAsset, AssetType
      identity.py         # CloudIdentity, Principal
      event.py            # SecurityEvent, EventSource
      compliance.py       # ComplianceControl, Framework
      remediation.py      # RemediationAction, PlaybookStep
      common.py           # Shared enums, base classes
      _version.py         # Contract version metadata
```

Services must import from `nc_models`. Services must not define their own
versions of these core types.

Package naming follows REF-001 §4.2: `org_service` in snake_case.

-----

## 5. Core data contracts

|Contract           |Description                              |Key Fields                                       |Status |
|-------------------|-----------------------------------------|-------------------------------------------------|-------|
|`SecurityFinding`  |A detected security issue                |id, severity, resource_id, detection_time, source|Defined|
|`CloudAsset`       |A cloud resource being monitored         |arn_or_uri, provider, asset_type, region, tags   |Defined|
|`CloudIdentity`    |A principal (user, role, service account)|id, provider, identity_type, permissions         |Planned|
|`SecurityEvent`    |An audit or activity event               |id, timestamp, actor, action, resource           |Planned|
|`ComplianceControl`|A control from a framework               |id, framework, requirement, status               |Planned|
|`RemediationAction`|An action taken or recommended           |id, finding_id, action_type, status              |Planned|

-----

## 6. Naming conventions (per REF-001 §4)

|Element     |Convention                   |Example                               |
|------------|-----------------------------|--------------------------------------|
|JSON fields |snake_case                   |`resource_id`, `detection_time`       |
|Primary keys|UUIDv7                       |`018fa0b8-6cde-7d2a-bd7f-8d9a3f6f1d0a`|
|Timestamps  |ISO 8601 with Z suffix       |`2025-11-26T18:00:00Z`                |
|Enums       |UPPER_SNAKE_CASE             |`CRITICAL`, `AWS_GUARDDUTY`           |
|Event names |domain.service.event.v{major}|`security.finding.created.v1`         |

-----

## 7. Versioning strategy

### 7.1 Semantic versioning

Contracts follow SemVer: `MAJOR.MINOR.PATCH`

- MAJOR: Breaking changes (field removal, type change, required field added).
- MINOR: Backward compatible additions (new optional field).
- PATCH: Documentation, bug fixes, no schema change.

### 7.2 Current version

```python
# libs/python/nc_models/src/nc_models/_version.py
CONTRACT_VERSION = "0.1.0"
```

### 7.3 Version in messages

All serialized messages must include a `contract_version` field:

```json
{
  "contract_version": "0.1.0",
  "id": "018fa0b8-6cde-7d2a-bd7f-8d9a3f6f1d0a",
  "severity": "HIGH"
}
```

-----

## 8. Compatibility rules

|Change Type         |Allowed      |Migration Required  |
|--------------------|-------------|--------------------|
|Add optional field  |Yes          |No                  |
|Add required field  |No (breaking)|Yes, MAJOR bump     |
|Remove field        |No (breaking)|Yes, MAJOR bump     |
|Rename field        |No (breaking)|Yes, MAJOR bump     |
|Change field type   |No (breaking)|Yes, MAJOR bump     |
|Add enum value      |Yes          |No                  |
|Remove enum value   |No (breaking)|Yes, MAJOR bump     |
|Change default value|Careful      |Depends on consumers|

Per REF-001 §5: Support N and N-1 versions at minimum.

-----

## 9. Event envelope (per REF-001 §11)

All events use CloudEvents 1.0:

```json
{
  "id": "018fa0b8-6cde-7d2a-bd7f-8d9a3f6f1d0a",
  "source": "svc.security.finding",
  "type": "security.finding.created.v1",
  "specversion": "1.0",
  "time": "2025-11-26T18:00:00Z",
  "datacontenttype": "application/json",
  "data": {
    "finding_id": "018fa0b8-6cde-7d2a-bd7f-8d9a3f6f1d0a",
    "tenant_id": "tenant_abc123",
    "severity": "HIGH",
    "resource_id": "arn:aws:s3:::my-bucket"
  }
}
```

-----

## 10. Example: SecurityFinding contract

```python
# libs/python/nc_models/src/nc_models/finding.py

from datetime import datetime
from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, Field
import uuid

class FindingSeverity(str, Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    INFO = "INFO"

class FindingSource(str, Enum):
    AWS_CONFIG = "AWS_CONFIG"
    AWS_GUARDDUTY = "AWS_GUARDDUTY"
    AWS_SECURITY_HUB = "AWS_SECURITY_HUB"
    GCP_SCC = "GCP_SCC"
    AZURE_DEFENDER = "AZURE_DEFENDER"
    NEUROCIPHER_DETECTION = "NEUROCIPHER_DETECTION"

class SecurityFinding(BaseModel):
    """Canonical security finding contract."""
    
    contract_version: str = "0.1.0"
    
    id: str = Field(
        default_factory=lambda: str(uuid.uuid7()),
        description="UUIDv7 finding identifier"
    )
    tenant_id: str = Field(..., description="Tenant this finding belongs to")
    severity: FindingSeverity
    source: FindingSource
    resource_id: str = Field(..., description="ARN or URI of affected resource")
    resource_type: str
    region: Optional[str] = None
    detection_time: datetime = Field(..., description="ISO 8601 with Z suffix")
    title: str
    description: str
    recommendation: Optional[str] = None
    compliance_mappings: List[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        use_enum_values = True
        json_encoders = {
            datetime: lambda v: v.strftime("%Y-%m-%dT%H:%M:%SZ")
        }
```

-----

## 11. PII handling (per REF-001 §8.1)

Contracts must respect PII tiers:

|Field Type         |PII Level|Handling                       |
|-------------------|---------|-------------------------------|
|`resource_id` (ARN)|P3       |Allowed raw                    |
|`user_email`       |P2       |Pseudonymize or hash           |
|`credentials`      |P0       |Never persist, reject ingestion|

Detection and redaction automation per REF-001 §8.2 applies to all payloads.

-----

## 12. Validation and enforcement

### 12.1 Build time validation

- All services importing `nc_models` get Pydantic validation automatically.
- CI pipeline runs schema compatibility checks on PR.

### 12.2 Runtime validation

- Ingest service validates incoming data against contracts.
- Invalid payloads route to dead letter queue with validation errors.
- Errors follow RFC 7807 Problem Details (REF-001 §10.2).

### 12.3 Contract testing

- Each service that produces or consumes a contract must have contract tests.
- Tests verify serialization and deserialization round trips.

-----

## 13. Acceptance criteria

This document is complete when:

- [ ] All core contracts are defined with field level documentation.
- [ ] Versioning strategy is approved by Architecture Board.
- [ ] `libs/python/nc_models/` structure is created.
- [ ] SecurityFinding and CloudAsset are fully implemented.
- [ ] Contract tests exist for all defined contracts.
- [ ] CI enforces backward compatibility checks.
- [ ] Event envelope matches CloudEvents 1.0 (REF-001 §11).
- [ ] PII handling aligns with REF-001 §8.1.

-----

## 14. Open questions

- [ ] Use Avro or Protobuf for wire format, or keep JSON only (per REF-001 §10.1)?
- [ ] Define contract deprecation sunset period.
- [ ] Confirm schema registry service (SRG-001) scope for runtime validation.

-----

## 15. Revision history

|Date      |Author           |Change             |
|----------|-----------------|-------------------|
|2025-11-26|Data Architecture|Initial Tier-1 stub|