⸻

A1 – Finalize docs layout and align GOV-ARCH-001

Title: Finalize docs/ layout to match REF-001 and align GOV-ARCH-001

Background

The monorepo now serves as the canonical platform repository. Documentation must follow REF-001-Glossary-and-Standards-Catalog.md to avoid fragmentation and confusion. GOV-ARCH-001-Architecture-Documentation-Index.md must reflect the real file tree and document status.

Tasks
	1.	Create/verify canonical docs/ subdirectories
From repo root:
	•	Ensure these directories exist (create if missing):
	•	docs/governance/
	•	docs/product/
	•	docs/architecture/
	•	docs/data-models/
	•	docs/services/
	•	docs/ingestion/
	•	docs/security-controls/
	•	docs/ai/
	•	docs/observability/
	•	docs/runbooks/
	•	docs/strategy/
	2.	Move existing docs into correct locations
Using git mv, place each .md file in the correct folder:
	•	Governance:
	•	REF-001-Glossary-and-Standards-Catalog.md → docs/governance/
	•	GOV-ARCH-001-Architecture-Documentation-Index.md → docs/governance/
	•	Product:
	•	PRD-001-Neurocipher-Platform-Vision-and-Scope.md → docs/product/ (if file exists)
	•	PDR-002-Capabilities-and-Module-Mapping-(Neurocipher-vs-AuditHound).md → docs/product/
	•	Architecture:
	•	ARC-001-Platform-Context-and-Boundaries.md → docs/architecture/
	•	System-Architecture-Blueprint.md → docs/architecture/ (to be refactored in A2)
	•	Data models:
	•	DM-003-Physical-Schemas-and-Storage-Map.md → docs/data-models/
	•	DM-005-Governance-Versioning-and-Migrations.md → docs/data-models/
	•	DCON-001-Data-Contract-Specification.md → docs/data-models/
	•	Services:
	•	DPS-ING-001-Ingest-Service-Architecture.md → docs/services/
	•	DPS-NORM-001-Normalize-Service-Architecture.md → docs/services/
	•	DPS-API-001-API-Service-Architecture.md → docs/services/
	•	Security:
	•	SEC-001-Threat-Model-and-Mitigation-Matrix.md → docs/security-controls/
	•	SEC-002-IAM-Policy-and-Trust-Relationship-Map.md → docs/security-controls/
	•	SEC-003-Network-Policy-and-Segmentation-Model.md → docs/security-controls/
	•	Strategy:
	•	Comprehensive strategic/technical review → docs/strategy/ (rename to a clean ID if needed)
	•	Confirm that ls docs/ shows only directories, no loose .md files.
	3.	Normalize front matter according to REF-001
For each .md under docs/:
	•	Ensure front matter exists with at least:
	•	id:
	•	title:
	•	owner:
	•	status: (Draft / Reviewed / Approved)
	•	last_reviewed: (ISO date, e.g. 2025-11-28)
	•	Fix any inconsistencies (missing fields, wrong status).
	4.	Update GOV-ARCH-001 paths
In docs/governance/GOV-ARCH-001-Architecture-Documentation-Index.md:
	•	For each row, update the Path column to the new folder path.
	•	Add rows for any new docs that now exist but were not indexed.
	•	Remove or mark as deprecated any entries that no longer exist.
	5.	Set Status and Tier for each document
	•	For each indexed doc:
	•	Existing – file present with meaningful content.
	•	Draft – file present but skeletal or incomplete.
	•	Planned – no file yet.
	•	Set Tier based on impact:
	•	Tier 1: blocks implementation (core PRDs, ARCs, DM-003/005, DCON-001, DPS-ING/NORM/API, SEC-001).
	•	Tier 2: blocks integration (embed, security-actions, some data specs).
	•	Tier 3: blocks production (DR, observability, secrets, test strategy).
	•	Tier 4: nice-to-have.
	•	Ensure no Tier-1 document is left as Planned without an associated issue in Milestone 2/3.

Dependencies
	•	None. This is foundational and can run in parallel with A3–A5.

Acceptance Criteria
	•	No .md files exist directly under docs/ root; all are under the correct subfolders.
	•	Every document under docs/ has REF-001-compliant front matter.
	•	GOV-ARCH-001:
	•	Has accurate paths for all existing docs.
	•	Lists Tier and Status for each.
	•	Has no references to non-existent files.
	•	Tier-1 docs are all marked Existing or Draft (not Planned).

⸻

A2 – Re-scope System Architecture Blueprint as ARC-002

Title: Re-scope System-Architecture-Blueprint into ARC-002-Data-Pipeline-Architecture-Blueprint

Background

The original System Architecture Blueprint was created with a data-pipeline-centric view and implicitly treated that as “the platform”. ARC-001 now defines the platform context and boundaries. This issue confines the old blueprint to the nc-data-pipeline subsystem as ARC-002 and aligns it with ARC-001.

Tasks
	1.	Rename and relocate document
	•	Ensure the current blueprint is located at docs/architecture/System-Architecture-Blueprint.md.
	•	Rename it using git mv to:
docs/architecture/ARC-002-Data-Pipeline-Architecture-Blueprint.md.
	2.	Update front matter
Open the file and:
	•	Set id: ARC-002-Data-Pipeline-Architecture-Blueprint.
	•	Set title: System Architecture Blueprint – Neurocipher Data Pipeline.
	•	Set status: to Draft or Reviewed depending on confidence.
	•	Update last_reviewed: to current date.
	•	Ensure owner: is set correctly (e.g., Architecture or your name).
	3.	Clarify scope to data pipeline only
In the document body:
	•	Add a short scope section at the top:
Scope: This document describes the nc-data-pipeline subsystem of the Neurocipher platform (ingest → normalize → embed → query). Platform-level context and module boundaries are defined in ARC-001-Platform-Context-and-Boundaries.
	•	Review each section and:
	•	Replace any “platform-wide” language with “data pipeline” where appropriate.
	•	If other modules (AuditHound, Agent Forge, MCP, Core) are mentioned, label them as external consumers or producers relative to the pipeline.
	4.	Align with ARC-001 and DPS/DM/SEC docs
	•	Cross-check that references to modules and responsibilities are consistent with:
	•	ARC-001-Platform-Context-and-Boundaries.md
	•	DPS-ING-001, DPS-NORM-001, DPS-API-001
	•	DM-003, DM-005
	•	Add a “Related Documents” section listing these file IDs.
	5.	Update GOV-ARCH-001
	•	Update the row for ARC-002 with:
	•	Correct path.
	•	New title.
	•	Updated Status and Tier.

Dependencies
	•	A1 should be at least partially done so the doc is already under docs/architecture/.
	•	ARC-001 should exist to reference.

Acceptance Criteria
	•	The old System Architecture Blueprint is now ARC-002-Data-Pipeline-Architecture-Blueprint.md under docs/architecture/.
	•	ARC-002 explicitly scopes itself to nc-data-pipeline only and defers platform context to ARC-001.
	•	No section in ARC-002 implies the pipeline is the entirety of the platform.
	•	GOV-ARCH-001 is updated to reference ARC-002 with correct metadata.

⸻

A3 – Create service skeletons under services/

Title: Create service skeletons for all platform modules under services/

Background

The monorepo will host multiple services: pipeline, core, AuditHound API, Agent Forge, and MCP server. Creating clear skeletons now prevents accidental architecture drift and gives contributors defined homes for implementation.

Tasks

For each of the following services:
	•	services/nc-data-pipeline/
	•	services/nc-core/
	•	services/nc-audithound-api/
	•	services/nc-agent-forge/
	•	services/nc-mcp-server/

Perform the steps:
	1.	Create directory structure
For each service:
	•	Create:

services/<service-name>/
  README.md
  pyproject.toml (or minimal placeholder)
  src/<python_package>/__init__.py
  tests/__init__.py

Examples:
	•	services/nc-data-pipeline/src/nc_data_pipeline/__init__.py
	•	services/nc-core/src/nc_core/__init__.py
	•	etc.

	2.	Write service README
For each service README.md:
	•	Include:
	•	Purpose.
	•	Responsibilities.
	•	Explicit non-goals.
	•	Key interactions (upstream/downstream).
	•	Links to relevant docs, for example:
	•	nc-data-pipeline: ARC-002, DPS-ING-001, DPS-NORM-001, DPS-API-001, DM-003, DCON-001.
	•	nc-core: ARC-003, DM-004, DM-006.
	•	nc-audithound-api: ARC-004, PRD-003.
	•	nc-agent-forge: ARC-005, PRD-004.
	•	nc-mcp-server: ARC-006.
	3.	Minimal pyproject.toml
	•	For each service, create a minimal pyproject.toml with:
	•	name (e.g., nc-data-pipeline).
	•	version (0.0.0 is fine).
	•	dependencies (can be empty or minimal placeholder).
	•	Ensure the format does not break tooling; keep it syntactically valid.
	4.	Quick import sanity check
	•	From repo root, create a virtual environment and run:

python -c "import nc_data_pipeline, nc_core, nc_observability"

(Just confirm the packages exist where expected; adjust the import path if necessary via PYTHONPATH or editable installs.)

	5.	Link to GOV-ARCH-001
	•	Ensure GOV-ARCH-001 lists each service as a row in the “Services” section, referencing its primary architecture document.

Dependencies
	•	A1 (docs layout) for correct doc paths used in READMEs.
	•	A2 is useful but not strictly required to create the skeletons.

Acceptance Criteria
	•	All five service directories exist with README.md, pyproject.toml, src/, and tests/ subdirectories.
	•	Each README clearly states purpose, responsibilities, non-goals, and links to the correct spec documents.
	•	A simple import check confirms the packages exist (even if empty).
	•	GOV-ARCH-001 references each service module.

⸻

A4 – Create libs/python skeletons

Title: Create libs/python skeleton packages (nc_models, nc_common, nc_observability, nc_security)

Background

Shared concerns (data contracts, utilities, observability, security) must be centralized to avoid duplication and divergence. These libs form the shared backbone for all services.

Tasks
	1.	Create base directories
Under libs/python/:
	•	nc_models/
	•	nc_common/
	•	nc_observability/
	•	nc_security/
	2.	Initialize each package
For each directory:
	•	Add __init__.py.
	•	Add README.md describing:
	•	Scope and responsibilities.
	•	What should and should not live here.
	•	References to relevant docs:
	•	nc_models → DCON-001, DM-003, DM-004, DM-006.
	•	nc_common → REF-001, any general engineering standards.
	•	nc_observability → OBS-LOG-001, OBS-MET-001 (C02, C03).
	•	nc_security → SEC-001..004, DM-006 (tenant isolation).
	3.	Minimal pyproject.toml (optional)
	•	Optionally create a pyproject.toml under libs/python/ if you intend to package these libs separately.
	•	Ensure internal imports between services and libs are planned (e.g., via editable installs, monorepo tooling, or PYTHONPATH settings).
	4.	Import sanity check
	•	In a dev environment, confirm:

python -c "import nc_models, nc_common, nc_observability, nc_security"


	5.	Update GOV-ARCH-001 or create a libs index
	•	Add references to these libs in GOV-ARCH-001 or a small docs/engineering/libs-index.md so contributors know where to find/put shared concerns.

Dependencies
	•	A1 (for pointer docs like DCON-001).

Acceptance Criteria
	•	Four Python packages exist, importable from a dev environment.
	•	Each package README defines scope and links to relevant specs.
	•	There is a single, documented place to put:
	•	Canonical models (nc_models).
	•	Shared utilities (nc_common).
	•	Observability helpers (nc_observability).
	•	Security primitives (nc_security).

⸻

A5 – Create infra/ skeleton

Title: Create infra/ skeleton with modules and AWS environments

Background

Infrastructure must be structured to support AWS-first deployment and future multi-cloud expansion. A clear infra/ layout avoids entangling environment-specific configuration with reusable modules.

Tasks
	1.	Create infra modules
Under infra/modules/:
	•	vpc/
	•	iam-baseline/
	•	kms/
	•	observability/
For each:
	•	Add .gitkeep or README.md describing:
	•	Intended Terraform/CloudFormation module responsibilities.
	•	Any constraints (e.g., VPC design patterns, IAM baselines).
	2.	Create AWS environment folders
Under infra/aws/environments/:
	•	dev/
	•	staging/
	•	prod/
For each:
	•	Add README.md describing:
	•	How the environment is expected to compose modules.
	•	Any environment-specific overrides (e.g., reduced scale in dev).
	3.	Multi-cloud placeholders
	•	Add infra/gcp/README.md and infra/azure/README.md stating these are reserved for future environments and must align with core module patterns.
	4.	Cross-reference in docs
	•	In SEC-002 and SEC-003, reference:
	•	infra/modules/vpc/
	•	infra/modules/iam-baseline/
	•	In any future infra or governance doc, refer to these module locations.

Dependencies
	•	None strictly, but B13/B14 (IAM, network docs) will depend on this layout.

Acceptance Criteria
	•	infra/ tree exists with modules/, aws/environments/, and placeholders for gcp/ and azure/.
	•	Each module/env directory has at least a README explaining its purpose.
	•	Security and architecture docs can refer to infra/modules/* locations unambiguously.

⸻

A6 – Update CI workflows for monorepo layout

Title: Update GitHub Actions workflows to support monorepo layout

Background

CI must understand the new directory structure so that linting, link checking, and OpenAPI validation continue to run correctly as the monorepo evolves.

Tasks
	1.	Update path filters
In all relevant workflows under .github/workflows/:
	•	Ensure on.push.paths and on.pull_request.paths include:
	•	docs/**
	•	services/**
	•	libs/**
	•	infra/**
	•	Existing paths such as migrations/**, schemas/**, tests/**.
	2.	Docs-related jobs
	•	For markdownlint and any Markdown-related checks:
	•	Change docs/*.md to docs/**/*.md.
	•	For lychee (link checker):
	•	Ensure it scans docs/**/*.md and any other necessary paths.
	3.	OpenAPI lint
	•	Confirm the OpenAPI lint job points to the current spec file(s).
For now: root openapi.yaml.
	•	Add a small comment mentioning potential future split (e.g., per-service OpenAPI files under services/*/api/openapi/).
	4.	Trial PR
	•	Create a test branch and make:
	•	A small change under docs/architecture/.
	•	A placeholder change under services/nc-core/.
	•	Open a PR and confirm:
	•	Docs changes trigger docs-related jobs.
	•	Service changes trigger appropriate lint/test jobs.

Dependencies
	•	A1, A3–A5 should have established the final directory structure.

Acceptance Criteria
	•	CI runs successfully on the current main branch with the new layout.
	•	A PR that changes nested docs triggers markdown and link checks.
	•	A PR that changes service or lib code triggers the relevant lint/test jobs.
	•	No workflows reference obsolete paths.

⸻

A7 – Align root Makefile with new layout

Title: Validate and align root Makefile with monorepo layout

Background

The root Makefile is still oriented around the earlier repo structure. It must be updated to work with the monorepo without breaking existing DB and testing workflows.

Tasks
	1.	Run all key targets
From repo root:
	•	make fmt
	•	make lint
	•	make test
	•	make db_local_up
	•	make db_local_migrate
	•	make db_local_smoke_test
	2.	Fix any broken paths
If any target fails due to path issues:
	•	Update file globs to:
	•	Use docs/**/*.md instead of docs/*.md.
	•	Handle new services/ and libs/ locations for Python sources.
	•	Ensure DB targets still use:
	•	migrations/postgres/
	•	tests/db/ as before (no structural move yet).
	3.	Clarify future direction in comments
	•	Add a comment block at the top or near the service-level targets:
	•	Explain that:
	•	Root make currently manages shared infra (lint, test, formatting, DB).
	•	In future, service-specific Makefiles (under services/*/) may be introduced.
	•	This is the single source of truth until then.
	4.	Re-run targets
	•	Re-run all targets from step 1 to confirm everything is green.

Dependencies
	•	A1, A3–A5 should be complete or nearly complete so path patterns are stable.
	•	A6 may run before or after; they are related but independent.

Acceptance Criteria
	•	All existing make targets run successfully with the monorepo structure.
	•	No hard-coded paths reference the old layout incorrectly.
	•	Comments in the Makefile clearly explain how it fits into the monorepo and the plan for future per-service Makefiles.

⸻

A8 – Update migration-plan.md to reflect current state

Title: Update migration-plan.md to reflect completed work and remaining phases

Background

migration-plan.md was originally drafted for the repository rename and initial restructuring. It must be updated so it accurately describes completed phases and remaining migration tasks, and maps to the new issue set.

Tasks
	1.	Mark completed phases
	•	For all steps already executed (rename to neurocipher-platform, initial directory creation):
	•	Mark them as DONE with completion dates.
	•	Optionally add a short note if there were deviations.
	2.	Align phases with A1–A7 work
	•	Ensure the sections describing docs layout, service skeletons, libs, infra, CI, and Makefile map directly to:
	•	A1–A7 issue IDs.
	•	Update wording to accurately match what is now in the monorepo (no references to the old repo name or structure).
	3.	Revise Phase 4 “code migration”
	•	Replace any instructions that assume migrating migrations/, schemas/, or tests/ into services/ immediately.
	•	Clarify that:
	•	The current phase focuses on structure and skeletons.
	•	Moving DB/test artifacts into service-specific modules will be a later refactor once services exist and are implemented.
	•	Add a “Future refactor” subsection summarizing this later step.
	4.	Add issue mapping
	•	At the end of migration-plan.md, add a table mapping:
	•	Phase/step → GitHub issue ID (A1–A8, B01–B14, C01–C05).
	•	Explicitly differentiate between:
	•	Monorepo structural tasks (A-series).
	•	Architecture/product docs (B-series).
	•	Production readiness docs (C-series).

Dependencies
	•	A1–A7 should be near completion so the plan can reference reality.

Acceptance Criteria
	•	migration-plan.md reads as a current, accurate description of work done and remaining.
	•	There are no instructions contradicting the current repo layout.
	•	A new contributor can read migration-plan.md and see:
	•	What was done.
	•	What remains.
	•	Which GitHub issues correspond to each phase.
	

---

B01 – PRD-001 Neurocipher Platform Vision and Scope

Title: Write PRD-001-Neurocipher-Platform-Vision-and-Scope

Background

The platform currently has detailed technical architecture, schema, and service specs, but the top-level product requirements are fragmented. A single PRD for the entire Neurocipher platform is needed to anchor all module-level design decisions (Neurocipher core, AuditHound, Agent Forge, MCP) and to support board/investor conversations.

Tasks
	1.	Create and place file
	•	Create:
docs/product/PRD-001-Neurocipher-Platform-Vision-and-Scope.md
	•	Add REF-001-compliant front matter:
	•	id: PRD-001-Neurocipher-Platform-Vision-and-Scope
	•	title: Neurocipher Platform – Vision and Scope
	•	owner: Product
	•	status: Draft
	•	last_reviewed: <today>
	2.	Write Vision & Problem Statement
	•	Describe the core problem space for SMBs:
	•	Cloud security posture complexity.
	•	Compliance overhead (SOC2/ISO/PCI/GDPR).
	•	Lack of affordable, integrated tools.
	•	Articulate the vision:
	•	Neurocipher as a continuous security and posture engine.
	•	AuditHound as a compliance/reporting front-end.
	•	Agent Forge as safe auto-remediation / orchestration.
	•	MCP as an integration boundary for tools/assistants.
	3.	Define Target Customers and Personas
	•	Enumerate primary personas:
	•	SMB founder/owner.
	•	“Accidental sysadmin” or lean IT engineer.
	•	External auditor / compliance consultant.
	•	For each persona, capture:
	•	Goals and pain points.
	•	Current alternatives (manual, spreadsheets, expensive enterprise tools).
	4.	Core Capabilities & Non-Goals
	•	List core capabilities of the platform as a whole:
	•	Continuous cloud posture monitoring and threat detection.
	•	Centralized risk/finding aggregation.
	•	Compliance reporting and audit evidence mapping.
	•	Guided or automated remediation workflows.
	•	Explicitly list non-goals:
	•	Not a general-purpose SIEM.
	•	Not a ticketing system (integrates with JIRA/ServiceNow instead).
	•	Not a generic LLM platform.
	5.	Module-Level Responsibilities (High-Level)
	•	Summarize module roles (reusing PDR-002 but at product level):
	•	Neurocipher core: continuous scanning, posture, findings.
	•	AuditHound: compliance checks + reports.
	•	Agent Forge: orchestration & auto-remediation.
	•	MCP server: API boundary for external tools/agents.
	•	Keep this at PRD abstraction level; detailed boundaries belong in ARC-001/ARC-00x.
	6.	Key Use Cases / User Journeys
	•	Create 3–5 primary user journeys:
	•	“Onboard cloud account and see first findings.”
	•	“Generate SOC2 readiness report.”
	•	“Auto-remediate a risky security group.”
	•	For each, describe current pain, desired outcome, and platform behavior.
	7.	Success Metrics & Constraints
	•	Define product-level KPIs:
	•	Time-to-first-value (e.g., first findings within X minutes).
	•	Reduction in manual compliance work (hours saved per audit).
	•	Number of supported frameworks and cloud providers.
	•	Capture constraints:
	•	Must be multi-tenant and secure by design.
	•	AWS-first implementation, but multi-cloud roadmap.
	•	Strict data isolation and privacy requirements.
	8.	Cross-References
	•	Add a “Related Documents” section linking:
	•	PDR-002-Capabilities-and-Module-Mapping
	•	ARC-001-Platform-Context-and-Boundaries
	•	SEC-001-Threat-Model-and-Mitigation-Matrix
	9.	Update Index
	•	Update GOV-ARCH-001:
	•	Mark PRD-001 as Existing.
	•	Set Tier (likely Tier 1).
	•	Ensure the path is correct.

Dependencies
	•	A1 (docs/ structure and GOV-ARCH alignment) should be in place.
	•	PDR-002 and ARC-001 should exist to reference.

Acceptance Criteria
	•	docs/product/PRD-001-Neurocipher-Platform-Vision-and-Scope.md exists with complete content and valid front matter.
	•	The document can be read standalone by a PM or executive and clearly explains what Neurocipher is, for whom, and why.
	•	Responsibilities and module roles in PRD-001 are consistent with PDR-002 and ARC-001.
	•	GOV-ARCH-001 lists PRD-001 as Existing, Tier-1, with a correct path.

⸻

B02 – PRD-003 AuditHound Compliance Module Requirements

Title: Write PRD-003-AuditHound-Compliance-Module-Requirements

Background

AuditHound is defined canonically as the compliance module: on-demand or scheduled assessments, reports, and remediation guidance — not continuous scanning. It needs a focused PRD that describes requirements in auditor language, distinct from the Neurocipher platform PRD.

Tasks
	1.	Create and place file
	•	Create:
docs/product/PRD-003-AuditHound-Compliance-Module-Requirements.md
	•	Add front matter:
	•	id: PRD-003-AuditHound-Compliance-Module-Requirements
	•	title: AuditHound – Compliance Module Requirements
	•	owner: Product
	•	status: Draft
	•	last_reviewed: <today>
	2.	Define Scope & Purpose
	•	Explain:
	•	AuditHound’s purpose: compliance assessment and reporting.
	•	Scope: frameworks supported (SOC2, ISO 27001, PCI-DSS, GDPR, HIPAA, etc.).
	•	Constraints: no direct cloud scanning, no auto-remediation, no continuous monitoring.
	3.	Framework & Control Modeling
	•	Describe:
	•	How frameworks and control catalogs are represented (controls, sub-controls).
	•	How control requirements map to:
	•	Evidence types (logs, policies, configs).
	•	Neurocipher findings (optional support).
	4.	Inputs & Evidence Sources
	•	Enumerate input types:
	•	Static documents and policies (PDF, DOCX, Markdown).
	•	System-generated evidence (screenshots, exports).
	•	Structured exports from Neurocipher (findings, posture snapshots).
	•	Define basic requirements for evidence ingestion (file size limits, formats, tagging).
	5.	Assessment & Scoring Behavior
	•	Define:
	•	What it means to “run an assessment” in AuditHound.
	•	Output states for each control (e.g., Pass / Fail / Partial / Not Applicable).
	•	Optional maturity levels (if you want them now or leave as future).
	6.	Reporting Requirements
	•	Describe:
	•	Report types (readiness report, auditor-ready report, delta change report).
	•	Output formats (PDF, HTML, maybe JSON).
	•	Content expectations:
	•	Plain-English summary.
	•	Control-by-control status.
	•	Mapped evidence references.
	•	Step-by-step remediation guidance.
	7.	User Experience & Roles
	•	Capture:
	•	Who runs assessments (internal owner, external consultant).
	•	How they schedule or trigger checks (manual, scheduled).
	•	Required UI/UX behavior at a conceptual level (even if front-end is later).
	8.	Non-Goals & Dependencies
	•	Clearly state:
	•	AuditHound does not:
	•	Call cloud provider APIs directly.
	•	Run auto-remediation.
	•	Provide real-time alerts.
	•	It may depend on Neurocipher for deeper evidence, but can function with static inputs.
	9.	Cross-References & Index
	•	Add “Related Documents”:
	•	PRD-001
	•	PDR-002
	•	ARC-004-AuditHound-Service-Architecture
	•	Update GOV-ARCH-001:
	•	Mark PRD-003 as Existing, Tier-1 or Tier-2 as appropriate.

Dependencies
	•	PRD-001 and PDR-002 should be in place for platform-level and capability-level context.

Acceptance Criteria
	•	PRD-003 exists and clearly defines AuditHound’s purpose, scope, inputs, outputs, and non-goals.
	•	It is clear that AuditHound is compliance-only and consumes, but does not produce, technical scanning results.
	•	GOV-ARCH-001 shows PRD-003 as Existing with correct path and tier.

⸻

B03 – PRD-004 Agent Forge Orchestration Requirements

Title: Write PRD-004-Agent-Forge-Orchestration-Requirements

Background

Agent Forge is the orchestration and auto-remediation engine. It requires a dedicated PRD to define what workflows it supports, what safety constraints apply, and how it integrates with Neurocipher and AuditHound at a product level.

Tasks
	1.	Create and place file
	•	Create:
docs/product/PRD-004-Agent-Forge-Orchestration-Requirements.md
	•	Add front matter:
	•	id: PRD-004-Agent-Forge-Orchestration-Requirements
	•	title: Agent Forge – Orchestration and Auto-Remediation Requirements
	•	owner: Product
	•	status: Draft
	•	last_reviewed: <today>
	2.	Define Scope & Purpose
	•	Describe:
	•	Agent Forge as the platform’s workflow and action engine.
	•	It takes tasks (scan, remediate, notify, ticket, etc.) and orchestrates safe execution.
	•	Call out high-level non-goals:
	•	Not a “brain” (it does not own risk logic).
	•	Not a generic low-code workflow platform for arbitrary business processes.
	3.	Workflow Types & Triggers
	•	Enumerate primary workflow types:
	•	Run a scan (trigger pipeline + core).
	•	Apply a remediation (tighten SG, rotate key, etc.).
	•	Notify/stakeholder updates (Slack, email, ticket).
	•	Define triggers:
	•	Manual trigger from UI/API.
	•	Scheduled.
	•	Event-driven (e.g., high-risk finding created).
	4.	Safety & Policy Requirements
	•	Specify:
	•	Approval requirements for destructive actions (e.g., must be “approved” by human or certain role).
	•	Scope limitations (no cross-account actions beyond tenancy).
	•	Rate limits and blast radius controls (e.g., no mass deletion, bounded automation).
	•	High-level audit requirements:
	•	Every action must have a trace log (who, what, when, why, outcome).
	5.	User Roles & UX Constraints
	•	Define:
	•	Roles (e.g., Security Engineer, Platform Owner).
	•	Permissions model (who can configure workflows, who can approve actions).
	•	Outline expected UX behavior conceptually (not UI design).
	6.	Integrations & Dependencies
	•	Identify:
	•	Dependencies on Neurocipher Core (requires findings and posture context).
	•	Dependencies on AuditHound (can be used to auto-collect evidence).
	•	External integrations (JIRA, email, Slack, etc. as future).
	•	Clarify that Agent Forge itself does not define the risk logic; it executes tasks based on policies and inputs.
	7.	Cross-References & Index
	•	Add “Related Documents”:
	•	PRD-001
	•	PDR-002
	•	ARC-005-Agent-Forge-Architecture
	•	Update GOV-ARCH-001 with PRD-004 as Existing.

Dependencies
	•	PRD-001 and PDR-002 for overall platform and module mapping.
	•	ARC-005 will lean on this PRD.

Acceptance Criteria
	•	PRD-004 clearly defines the functional and non-functional requirements for Agent Forge.
	•	It is obvious how Agent Forge interacts with Neurocipher and AuditHound without re-owning their logic.
	•	GOV-ARCH-001 references PRD-004 correctly with status and tier.

⸻

B04 – ARC-002 Data Pipeline Architecture Blueprint (content completion)

Title: Complete ARC-002-Data-Pipeline-Architecture-Blueprint for nc-data-pipeline

Background

A2 re-scoped and renamed the legacy System Architecture Blueprint to ARC-002 for the data pipeline. This issue ensures ARC-002 is complete and current, aligned with the monorepo and service architecture (DPS-ING/NORM/API).

Tasks
	1.	Review current ARC-002 content
	•	Read docs/architecture/ARC-002-Data-Pipeline-Architecture-Blueprint.md as of A2.
	•	Note any references that still assume “platform” instead of “data pipeline”.
	•	Identify missing sections vs REF-001 structural expectations (overview, components, flows, dependencies).
	2.	Define Pipeline Responsibilities
	•	Clearly describe nc-data-pipeline responsibilities:
	•	Ingest from S3/webhooks/API/schedules.
	•	Normalize/raw-to-structured transformation and PII detection.
	•	Store raw/normalized artifacts.
	•	Push embedding jobs and index into Weaviate/OpenSearch.
	•	Explicitly list non-goals (no GUI, no business-level compliance logic).
	3.	Component & Flow Diagrams (Textual)
	•	Document core components:
	•	Ingest service.
	•	Normalize service.
	•	Embed workers.
	•	Query API.
	•	Storage backends: Postgres (nc.*), S3, Weaviate, OpenSearch.
	•	Describe flows in words and/or ASCII diagrams:
	•	Ingest → Normalize → Embed → Query.
	•	Error paths and retries.
	4.	Integration Points
	•	Describe how the pipeline integrates with:
	•	Neurocipher Core (e.g., how findings are fed or consumed).
	•	Agent Forge (e.g., pipeline-triggered scans).
	•	AuditHound (e.g., evidence snapshots).
	•	Keep the responsibilities aligned with ARC-001 and PDR-002.
	5.	Operational & Non-Functional Characteristics
	•	Capture:
	•	Performance expectations (throughput, latency).
	•	Scalability considerations (SQS, Fargate workers, etc.).
	•	Reliability and failure handling (DLQs, backoff).
	•	Link to DM-003/DM-005 for schema and migration governance.
	6.	Update Cross-References & Status
	•	In ARC-002:
	•	Add a “Related Documents” section referencing ARC-001, DM-003, DM-005, DCON-001, DPS-ING/NORM/API.
	•	In GOV-ARCH-001:
	•	Mark ARC-002 as Reviewed if the content is stable enough.
	•	Confirm the tier (likely Tier-1).

Dependencies
	•	A2 must be complete (rescope + rename).
	•	DPS-ING/NORM/API specs and DM-003/DM-005/DCON-001 should exist for cross-ref.

Acceptance Criteria
	•	ARC-002:
	•	Describes the pipeline subsystem comprehensively.
	•	Contains explicit responsibilities and non-goals, component and flow descriptions, and integration points.
	•	No language suggests ARC-002 is the architecture of the entire platform.
	•	GOV-ARCH-001 lists ARC-002 as Existing and up to date.

⸻

B05 – ARC-003 Neurocipher Core Semantic Engine

Title: Write ARC-003-Neurocipher-Core-Semantic-Engine

Background

Neurocipher Core is the semantic engine: it owns canonical schemas, embeddings, security graph, and risk reasoning. Its responsibilities must be clearly defined and separated from nc-data-pipeline, AuditHound, and Agent Forge.

Tasks
	1.	Create and place file
	•	Create:
docs/architecture/ARC-003-Neurocipher-Core-Semantic-Engine.md
	•	Add front matter:
	•	id: ARC-003-Neurocipher-Core-Semantic-Engine
	•	title: Neurocipher Core – Semantic Engine Architecture
	•	owner: Architecture
	•	status: Draft
	•	last_reviewed: <today>
	2.	Define Core’s Responsibilities
	•	Describe:
	•	Ownership of canonical security entities (assets, identities, controls, findings).
	•	Ownership of embeddings / vector representations and higher-level semantic models.
	•	Ownership of security graph and relationship modeling (attack paths, posture, risk rollups).
	•	Explicitly distinguish from:
	•	nc-data-pipeline (data ingestion & pre-processing).
	•	AuditHound (compliance modeling and reports).
	•	Agent Forge (workflow execution).
	3.	Data Model & Storage
	•	Reference DM-003/DCON-001 and describe:
	•	Core’s logical data model: key entities, relationships.
	•	How embeddings are stored and retrieved.
	•	How the security graph is stored (e.g., Postgres relations, graph DB, or vector + relational hybrid).
	4.	Risk & Reasoning Layer
	•	Define:
	•	How Core computes risk (rules, heuristics, LLM-based reasoning).
	•	How prioritization is done (severity, exposure, exploitability).
	•	How explanations are generated (e.g., LLM templates or structured rule explanations).
	5.	APIs & Events
	•	Describe:
	•	Core’s northbound APIs (for AuditHound, UI, external tools).
	•	Event flows: how findings or posture changes are emitted (e.g., event.security.finding.v1).
	•	Link to relevant event schemas and OpenAPI endpoints.
	6.	Integration with Other Modules
	•	Outline:
	•	How Core consumes inputs from the pipeline (normalized documents, signals).
	•	How Core informs Agent Forge (findings that can trigger workflows).
	•	How Core provides evidence to AuditHound.
	7.	Non-Functional Characteristics
	•	Capture:
	•	Performance expectations (typical query and analysis latency).
	•	Scalability (horizontal scaling, caching).
	•	Observability needs (metrics, logs, traces).
	8.	Update Index
	•	Add to GOV-ARCH-001:
	•	Status Existing (or Draft).
	•	Tier (likely Tier-1).
	•	Correct path.

Dependencies
	•	ARC-001 and DM-003/DCON-001 for platform context and data model references.

Acceptance Criteria
	•	ARC-003 clearly defines what Neurocipher Core is responsible for and how it operates.
	•	There is no overlap/confusion with pipeline, AuditHound, or Agent Forge responsibilities.
	•	A senior engineer could begin designing Core’s schemas and APIs from this document.
	•	GOV-ARCH-001 lists ARC-003 correctly.

⸻

B06 – ARC-004 AuditHound Service Architecture

Title: Write ARC-004-AuditHound-Service-Architecture

Background

AuditHound’s product requirements (PRD-003) must be backed by a clear service architecture that aligns with its compliance-only role and its dependence on Neurocipher for technical findings.

Tasks
	1.	Create and place file
	•	Create:
docs/architecture/ARC-004-AuditHound-Service-Architecture.md
	•	Add front matter:
	•	id: ARC-004-AuditHound-Service-Architecture
	•	title: AuditHound – Service Architecture
	•	owner: Architecture
	•	status: Draft
	•	last_reviewed: <today>
	2.	Define Service Boundaries
	•	Describe:
	•	The main AuditHound service(s): API, job runner (for assessments), report generator.
	•	Infrastructure components (DB tables for assessments/runs/reports, evidence storage).
	•	Clearly state non-goals:
	•	No direct cloud API calls.
	•	No continuous monitoring.
	3.	Components & Data Flow
	•	Define components:
	•	Control catalog & framework engine.
	•	Evidence ingestion component.
	•	Assessment runner.
	•	Reporting component.
	•	Describe flows:
	•	User triggers an assessment → engine resolves required evidence and inputs → results stored → report generated.
	4.	Data Model Overview
	•	Summarize key entities:
	•	framework, control, assessment_run, control_result, evidence_reference, report.
	•	Reference DCON-001 and any planned DM-* docs for details.
	5.	Integration with Neurocipher
	•	Describe:
	•	How AuditHound optionally consumes Neurocipher findings (posture evidence).
	•	How these are mapped to controls (e.g., “Control CC6.x uses these Neurocipher finding types”).
	6.	APIs & External Integrations
	•	Outline API surface:
	•	Trigger assessment.
	•	Fetch assessment status.
	•	Fetch/generated report.
	•	Mention possible integrations:
	•	Export to PDF, send to auditors, share via MCP, etc.
	7.	Observability & Security Considerations
	•	Note:
	•	Logs and metrics patterns (defer details to OBS-LOG-001/OBS-MET-001).
	•	Tenant isolation considerations for evidence and reports.
	8.	Update Index
	•	Add ARC-004 to GOV-ARCH-001 with Existing status and Tier-1 or Tier-2.

Dependencies
	•	PRD-003 and PDR-002 for product and capability context.
	•	DM-006 for multi-tenant isolation patterns.

Acceptance Criteria
	•	ARC-004 provides a full service-level architecture for AuditHound consistent with its compliance-only role.
	•	It does not introduce direct cloud scanning; all such functionality is delegated to Neurocipher.
	•	A backend engineer could start designing nc-audithound-api from this document.
	•	ARC-004 is indexed and cross-referenced correctly.

⸻

B07 – ARC-005 Agent Forge Architecture

Title: Write ARC-005-Agent-Forge-Architecture

Background

Agent Forge’s PRD (PRD-004) defines its requirements. ARC-005 must define the technical architecture: components, state machine, workflow representation, policy enforcement, and integration with other modules.

Tasks
	1.	Create and place file
	•	Create:
docs/architecture/ARC-005-Agent-Forge-Architecture.md
	•	Add front matter:
	•	id: ARC-005-Agent-Forge-Architecture
	•	title: Agent Forge – Orchestration Engine Architecture
	•	owner: Architecture
	•	status: Draft
	•	last_reviewed: <today>
	2.	Conceptual Model
	•	Define:
	•	What a “workflow” is (steps, dependencies, inputs/outputs).
	•	Workflow types (scan, remediate, notify, ticket, evidence gather).
	•	Execution graph/state machine (pending, running, success, failed, cancelled).
	3.	Components
	•	Describe:
	•	Orchestration service (API/front door, scheduler).
	•	Worker/executor layer (Lambda/Fargate tasks).
	•	Policy engine (safety and authorization).
	•	Persistence (workflow and task state store).
	•	Audit log store.
	4.	Policy and Safety Model
	•	Define:
	•	How policies are defined and evaluated (e.g., policy-as-code, config).
	•	Guardrails:
	•	What actions require approval.
	•	Where approvals are logged.
	•	Maximum scope for automated actions (e.g., per account, per environment).
	5.	Integration with Other Modules
	•	Describe:
	•	How workflows are triggered by Neurocipher findings or AuditHound recommendations.
	•	How remediation actions are executed (e.g., via AWS SDK, CloudFormation, or external scripts).
	•	How Agent Forge reports back statuses to:
	•	Neurocipher.
	•	AuditHound (when evidence is collected or actions completed).
	6.	APIs & Events
	•	Outline:
	•	Orchestration APIs (create workflow, cancel workflow, get status).
	•	Event flows for action updates (ties into event.security.action_status.v1 etc.).
	7.	Observability & Failure Modes
	•	Define:
	•	Log and metric expectations.
	•	Handling of partial failures (some steps succeed, others fail).
	•	Dead-letter behavior for failed tasks.
	8.	Update Index
	•	Register ARC-005 in GOV-ARCH-001 with Existing status, correct path, and Tier.

Dependencies
	•	PRD-004 and ARC-001/ARC-003 for context and inputs.
	•	Event schemas in schemas/events/ for actions and statuses.

Acceptance Criteria
	•	ARC-005 clearly describes Agent Forge architecture, including workflows, policy, components, and integration points.
	•	The division of responsibility between Agent Forge, Neurocipher, and AuditHound is clear and consistent.
	•	GOV-ARCH-001 is updated accordingly.

⸻

B08 – ARC-006 MCP Server Integration Architecture

Title: Write ARC-006-MCP-Server-Integration-Architecture

Background

The MCP server is the boundary for tools and assistants to interact with Neurocipher. Its architecture must make clear what operations are exposed, how tenant context is passed, and how security and rate limiting are enforced.

Tasks
	1.	Create and place file
	•	Create:
docs/architecture/ARC-006-MCP-Server-Integration-Architecture.md
	•	Add front matter:
	•	id: ARC-006-MCP-Server-Integration-Architecture
	•	title: MCP Server – Integration Architecture
	•	owner: Architecture
	•	status: Draft
	•	last_reviewed: <today>
	2.	Scope & Purpose
	•	Describe:
	•	MCP server as a thin integration layer exposing safe operations.
	•	High-level capabilities (query posture, fetch compliance reports, trigger scans).
	3.	Capabilities & Tools
	•	Define:
	•	MCP “tools” or capabilities exposed to clients (e.g., “get_findings”, “run_scan”, “get_report”).
	•	For each capability:
	•	High-level description and mapping to underlying services (pipeline, core, AuditHound, Agent Forge).
	4.	Authentication & Tenant Context
	•	Describe:
	•	How the MCP server authenticates clients.
	•	How tenant/account context is carried on each request.
	•	Reference:
	•	RLS model and account_id.
	•	Security docs (SEC-001..003).
	5.	Rate Limiting & Abuse Prevention
	•	Outline:
	•	Rate limits per tenant and per client.
	•	Logging of usage.
	•	Potential abuse detection heuristics (optional but recommended).
	6.	Error Handling & Observability
	•	Define:
	•	Error response patterns.
	•	Logging of errors with correlation IDs.
	•	Metrics around tool usage.
	7.	Update Index
	•	Add ARC-006 to GOV-ARCH-001 with correct status and tier.

Dependencies
	•	ARC-001 for platform boundaries.
	•	PRD-001/PRD-003/PRD-004 for high-level operations to expose.
	•	DM-006 for tenant context strategy.

Acceptance Criteria
	•	ARC-006 describes how MCP clients interact with the platform via a defined set of capabilities.
	•	Auth, tenant isolation, rate limiting, and observability are addressed at an architectural level.
	•	There is no ambiguity about which operations are available via MCP and which are explicitly not.

⸻

B09 – DM-004 Vector and Search Index Layout

Title: Write DM-004-Vector-and-Search-Index-Layout

Background

Vector and search indices (Weaviate and OpenSearch) are currently defined via schema files but not fully documented in a single canonical data model document. DM-004 must describe all classes/indices, fields, and usage patterns.

Tasks
	1.	Create and place file
	•	Create:
docs/data-models/DM-004-Vector-and-Search-Index-Layout.md
	•	Add front matter:
	•	id: DM-004-Vector-and-Search-Index-Layout
	•	title: Vector and Search Index Layout
	•	owner: Data Engineering
	•	status: Draft
	•	last_reviewed: <today>
	2.	Summarize Roles of Weaviate and OpenSearch
	•	Describe:
	•	Weaviate as the vector store for semantic similarity.
	•	OpenSearch as the keyword and log search backend.
	•	Clarify when queries hit which system (or both via hybrid search).
	3.	Weaviate Classes
	•	For each Weaviate class defined under schemas/weaviate/:
	•	Name.
	•	Key properties (fields, types).
	•	Vectorization parameters (dimension, model).
	•	Multi-tenancy approach (per-class vs per-tenant namespaces or tenant IDs on documents).
	4.	OpenSearch Indices
	•	For each index template under schemas/opensearch/:
	•	Index name pattern.
	•	Key fields and mappings.
	•	Analyzer / tokenizer configuration.
	•	ILM policies (hot/warm/cold, retention rules).
	5.	Relationships with Core Data Model
	•	Explain:
	•	How nc.document_chunk maps into Weaviate and OpenSearch.
	•	How findings, assets, or other entities are indexed or referenced in search.
	6.	Lifecycle and Maintenance
	•	Define:
	•	Reindex strategies.
	•	How changes to schema are rolled out.
	•	How old indices are decommissioned.
	7.	Update Index
	•	Add DM-004 to GOV-ARCH-001 with correct path, status, and tier.

Dependencies
	•	DM-003 for physical schemas.
	•	schemas/weaviate/ and schemas/opensearch/ must be available.

Acceptance Criteria
	•	DM-004 describes all vector and search index structures and their relationships to the core data model.
	•	It is clear where any given type of content (e.g., document chunk, finding) is indexed and how.
	•	GOV-ARCH-001 lists DM-004 as Existing.

⸻

B10 – DM-006 Multi-Tenant Data Isolation Model

Title: Write DM-006-Multi-Tenant-Data-Isolation-Model

Background

Multi-tenancy is implemented via RLS in Postgres and enforced across storage layers. DM-006 must define the end-to-end isolation model for every state store (DB, S3, Weaviate, OpenSearch, logs).

Tasks
	1.	Create and place file
	•	Create:
docs/data-models/DM-006-Multi-Tenant-Data-Isolation-Model.md
	•	Add front matter:
	•	id: DM-006-Multi-Tenant-Data-Isolation-Model
	•	title: Multi-Tenant Data Isolation Model
	•	owner: Data Engineering
	•	status: Draft
	•	last_reviewed: <today>
	2.	Postgres Isolation
	•	Describe:
	•	account_id pattern on all tenant-scoped tables.
	•	RLS policies enforcing account_id = nc.current_account_id().
	•	The session variable and helper functions:
	•	SET SESSION app.account_id = 'acct_xxx'
	•	nc.current_account_id()
	•	nc.require_tenant_context()
	3.	Object Storage Isolation
	•	Define S3 prefix layout:
	•	Buckets and prefix patterns per account.
	•	How raw vs normalized data is separated per tenant.
	•	Describe any encryption or KMS key strategy relevant to per-tenant separation (link to SEC-004 later).
	4.	Vector and Search Isolation
	•	Explain how tenant context is encoded in:
	•	Weaviate classes (namespaces, multi-tenancy flags, or tenant IDs).
	•	OpenSearch indices (per-tenant index vs shared index with tenant field).
	•	Ensure the model is consistent with DM-004.
	5.	Logs, Metrics, Traces
	•	Define:
	•	How tenant context is propagated into logs and metrics (e.g., tenant_id field).
	•	Any constraints to prevent cross-tenant leakage via observability backends.
	6.	Cross-Tenant Operations Constraints
	•	Clearly specify:
	•	That any cross-tenant operation must be explicitly designed and is not allowed by default.
	•	How internal admin operations (if any) are separated from tenant-context flows.
	7.	Update Index
	•	Add DM-006 to GOV-ARCH-001 with correct path and tier (likely Tier-1 or Tier-2).

Dependencies
	•	DM-003/DM-005 for existing schema.
	•	SEC-001..003 and future SEC-004 for security alignment.
	•	DM-004 for index-level behavior.

Acceptance Criteria
	•	DM-006 describes a consistent multi-tenant isolation strategy across Postgres, S3, vector/search, and observability.
	•	It is obvious how a given tenant’s data is separated and how context is set/enforced in each layer.
	•	GOV-ARCH-001 lists DM-006 correctly.

⸻

B11 – DPS-EMBED-001 Embed Service Architecture

Title: Write DPS-EMBED-001-Embed-Service-Architecture

Background

The embedding service turns normalized chunks into vector/search documents. Its architecture must define input queues, batching, model selection, failure modes, and index writes.

Tasks
	1.	Create and place file
	•	Create:
docs/services/DPS-EMBED-001-Embed-Service-Architecture.md
	•	Add front matter:
	•	id: DPS-EMBED-001-Embed-Service-Architecture
	•	title: Embed Service Architecture
	•	owner: Architecture
	•	status: Draft
	•	last_reviewed: <today>
	2.	Service Scope
	•	Describe:
	•	Inputs (normalized document chunks).
	•	Outputs (vectors in Weaviate, docs in OpenSearch, metadata updates in Postgres).
	•	Non-goals (no business logic beyond embedding; no decision-making).
	3.	Component Overview
	•	Define components:
	•	Input queue (e.g., SQS).
	•	Worker pool (ECS/Fargate, Lambda).
	•	Embedding model client (OpenAI, other LLM).
	•	Index writers (Weaviate/OpenSearch clients).
	•	Tie these components back to infra modules where relevant.
	4.	Batching & Concurrency
	•	Document:
	•	Batch sizes for embedding calls.
	•	Concurrency strategy and rate limiting.
	•	How backpressure is handled (e.g., queue depth thresholds).
	5.	Error Handling
	•	Define:
	•	Retry strategy (retries, exponential backoff).
	•	DLQ handling for permanent failures.
	•	Idempotency strategy to avoid duplicate vectors.
	6.	Observability & Metrics
	•	Specify key metrics:
	•	Embedding throughput.
	•	Error rate.
	•	Latency per batch.
	•	Reference OBS-LOG-001/OBS-MET-001 (once available).
	7.	Update Index
	•	Add DPS-EMBED-001 to GOV-ARCH-001 with status and tier.

Dependencies
	•	DM-003 and DM-004 for data/indices.
	•	SEC-001 for threat model; SEC-004 for secrets (embedding API keys).

Acceptance Criteria
	•	DPS-EMBED-001 provides a clear and detailed architecture for the embedding service.
	•	Engineers can implement nc-data-pipeline embedding workers without ambiguity.
	•	GOV-ARCH-001 references this doc correctly.

⸻

B12 – DPS-SEC-ACTIONS-001 Security Actions Service Architecture

Title: Write DPS-SEC-ACTIONS-001-Security-Actions-Service-Architecture

Background

The security actions service handles POST /v1/security/actions and GET /v1/security/actions/{id} and maps them into Agent Forge workflows. This doc defines its architecture and safety behavior.

Tasks
	1.	Create and place file
	•	Create:
docs/services/DPS-SEC-ACTIONS-001-Security-Actions-Service-Architecture.md
	•	Add front matter:
	•	id: DPS-SEC-ACTIONS-001-Security-Actions-Service-Architecture
	•	title: Security Actions Service Architecture
	•	owner: Architecture
	•	status: Draft
	•	last_reviewed: <today>
	2.	Scope & Responsibilities
	•	Describe:
	•	The service’s role as the API endpoint owner for security actions.
	•	That it does not directly manipulate cloud resources; instead it delegates to Agent Forge.
	3.	Input & Output Contracts
	•	Map:
	•	REST endpoints (/v1/security/actions, /v1/security/actions/{id}) to:
	•	JSON payloads.
	•	Event schemas: cmd.security.quarantine.v1, cmd.security.ticket.create.v1, cmd.security.notify.v1, etc.
	•	Include Idempotency-Key behavior.
	4.	Internal Flow
	•	Describe:
	•	Request validation and authentication.
	•	Conversion to internal command/event.
	•	Submission to Agent Forge (or queue).
	•	How status is tracked and returned on status checks.
	5.	Safety & Idempotency
	•	Define:
	•	Use of Idempotency-Key to ensure duplicate requests don’t trigger duplicate workflows.
	•	How invalid or unauthorized actions are handled.
	6.	Observability
	•	List:
	•	Key logs and metrics (action accepted, action failed, action completed).
	7.	Update Index
	•	Add DPS-SEC-ACTIONS-001 to GOV-ARCH-001.

Dependencies
	•	ARC-005 for Agent Forge architecture.
	•	Event schemas in schemas/events/.

Acceptance Criteria
	•	The document fully describes how the security actions service receives, validates, and forwards action requests, and how it tracks status.
	•	It aligns with the OpenAPI and schemas/events definitions.
	•	GOV-ARCH-001 is updated.

⸻

B13 – SEC-002 IAM Policy and Trust Relationship Map (Finalize)

Title: Finalize SEC-002-IAM-Policy-and-Trust-Relationship-Map

Background

SEC-002 exists but may be incomplete or misaligned with the new services/ and infra/ layout. This issue brings it to a “Reviewed/Approved” state.

Tasks
	1.	Review Existing SEC-002
	•	Read docs/security-controls/SEC-002-IAM-Policy-and-Trust-Relationship-Map.md.
	•	Identify:
	•	Missing roles or services.
	•	Any reference to old repo or naming.
	2.	Enumerate All Roles
	•	Create or update a table of IAM roles including:
	•	Service name.
	•	Role name.
	•	Environment (dev/staging/prod).
	•	Include:
	•	Roles for nc-data-pipeline, nc-core, nc-audithound-api, nc-agent-forge, nc-mcp-server.
	•	Any DB migration / maintenance roles.
	•	CI/CD roles, if applicable.
	3.	Trust Relationships
	•	For each role:
	•	Define which identities can assume it (ECS task, Lambda, CI, human admin).
	•	Note any cross-account assumptions if relevant.
	4.	Permissions & Least Privilege
	•	Summarize:
	•	Key permissions per role.
	•	Any policies shared via infra/modules/iam-baseline.
	•	Capture guidelines on how new permissions must be added (PR review, threat model reference).
	5.	Update to infra/ References
	•	Reference infra/modules/iam-baseline/ and any env-specific policy templates.
	6.	Update Status & Index
	•	Adjust status: in SEC-002 to Reviewed (or Approved when you are comfortable).
	•	Update last_reviewed: date.
	•	Update GOV-ARCH-001 to reflect new status.

Dependencies
	•	A5 for infra module layout.
	•	ARC-002..006 to know all services that require roles.

Acceptance Criteria
	•	SEC-002 lists all IAM roles relevant to the platform with clear trust relationships and permission summaries.
	•	It is consistent with current service naming and infra layout.
	•	Status is Reviewed or higher, and GOV-ARCH-001 reflects this.

⸻

B14 – SEC-003 Network Policy and Segmentation Model (Finalize)

Title: Finalize SEC-003-Network-Policy-and-Segmentation-Model

Background

SEC-003 exists but must be aligned with the new infra/ layout and the clarified service boundaries. This doc defines the network-level security posture.

Tasks
	1.	Review Existing SEC-003
	•	Read docs/security-controls/SEC-003-Network-Policy-and-Segmentation-Model.md.
	•	Identify:
	•	Outdated assumptions.
	•	Missing services or paths.
	2.	Define VPC & Subnet Layout
	•	Clarify:
	•	Number of VPCs and their purpose (single shared VPC vs per-env).
	•	Public vs private subnets and their assignments.
	•	Tie to infra/modules/vpc/.
	3.	Security Groups & Traffic Flows
	•	For each service:
	•	Which ports are open.
	•	Which other services it can talk to.
	•	Record:
	•	Ingress rules (from where).
	•	Egress rules (to where, including external APIs such as LLM providers).
	4.	Ingress & Egress Policies
	•	Document:
	•	How external access is provided to APIs (ALBs, API Gateway, etc.).
	•	Which resources are internet-facing and which are internal only.
	5.	Network-Level Tenant Isolation & Safety
	•	Describe:
	•	Any per-tenant concerns that affect network design (if any).
	•	Use of VPC endpoints for cloud provider APIs.
	6.	Update Status & Index
	•	Update status: to Reviewed when stable.
	•	Update last_reviewed: date.
	•	Update GOV-ARCH-001 to reflect SEC-003 status.

Dependencies
	•	A5 infra modules.
	•	ARC-002..006 for service placement.

Acceptance Criteria
	•	SEC-003 provides a coherent network topology and segmentation strategy that references the infra/ layout.
	•	For any given service, its network exposure and allowed peers are clearly documented.
	•	Status is Reviewed or Approved and GOV-ARCH-001 is updated.


---


C01 – SEC-004 Secrets and Key Management Strategy

Title: Write SEC-004-Secrets-and-Key-Management-Strategy

Background

The platform touches multiple sensitive systems: Postgres, S3, Weaviate, OpenSearch, LLM APIs, authentication tokens, and auto-remediation credentials. You already have SEC-001 (threat model), SEC-002 (IAM), and SEC-003 (network). What is missing is a canonical secrets and key management strategy that:
	•	Ties into the infra layout (infra/modules/kms/),
	•	Defines how secrets are stored, accessed, and rotated,
	•	Clarifies how different environments (dev/staging/prod) differ.

This document will be the single source of truth for all secrets and key management decisions.

Tasks
	1.	Create and place file
	•	Create:
docs/security-controls/SEC-004-Secrets-and-Key-Management-Strategy.md
	•	Add REF-001-compliant front matter:
	•	id: SEC-004-Secrets-and-Key-Management-Strategy
	•	title: Secrets and Key Management Strategy
	•	owner: Security
	•	status: Draft
	•	last_reviewed: <today>
	2.	Enumerate All Secrets and Keys
	•	Make a table listing categories of secrets/keys:
	•	Application secrets (API keys: LLM providers, email, integrations).
	•	Database credentials (Postgres app roles, admin users).
	•	Object store credentials (if applicable).
	•	Search/vector backends (Weaviate, OpenSearch).
	•	MCP server secrets (if any).
	•	Agent Forge cloud API credentials for remediation.
	•	For each, capture:
	•	Purpose.
	•	Owning service.
	•	Environment scope (dev/staging/prod).
	3.	Define Storage Mechanisms
	•	Specify where secrets live:
	•	Primary: AWS Secrets Manager and/or SSM Parameter Store.
	•	For each category of secret, define:
	•	Storage location (Secrets Manager vs SSM).
	•	Naming convention (e.g., /neurocipher/<env>/<service>/<secret_name>).
	•	Whether they are environment-specific or shared.
	4.	KMS Key Strategy
	•	Describe:
	•	Which KMS keys exist per environment (e.g., nc-app-secrets-kms-<env>, nc-data-kms-<env>).
	•	What each key is used for:
	•	Encrypting Secrets Manager values.
	•	Encrypting S3 buckets.
	•	Encrypting volumes for stateful components (e.g., Postgres, search).
	•	Link this to:
	•	infra/modules/kms/ (defined in A5).
	5.	Access Control & IAM Integration
	•	Define:
	•	Which IAM roles may read which secrets.
	•	Principle: least privilege, service-specific access.
	•	Reference SEC-002:
	•	Map secrets access to specific roles in the IAM role table.
	6.	Rotation Policies
	•	For each secret type, specify:
	•	Rotation interval (e.g., 90 days for DB passwords, shorter for API keys if feasible).
	•	Rotation mechanism:
	•	Manual rotation vs automated rotation (Secrets Manager rotation Lambdas).
	•	How dependent services are updated (deployment, config refresh).
	•	Include high-level process for emergency rotation (key compromise).
	7.	Local Development Strategy
	•	Define:
	•	How secrets are managed in local/dev:
	•	Use of .env files strictly on local machine, not committed to Git.
	•	How they differ from cloud-hosted secrets.
	•	Provide clear guidance for developers:
	•	Where to get dev secrets.
	•	How to configure their environment consistently.
	8.	Auditing & Compliance
	•	Capture:
	•	How access to secrets is logged and auditable (CloudTrail, Secrets Manager logs).
	•	Any reporting or periodic review process (e.g., quarterly review of who can read production secrets).
	9.	Related Documents & Index Update
	•	Add a “Related Documents” section referencing:
	•	SEC-001-Threat-Model-and-Mitigation-Matrix
	•	SEC-002-IAM-Policy-and-Trust-Relationship-Map
	•	SEC-003-Network-Policy-and-Segmentation-Model
	•	Update GOV-ARCH-001:
	•	Add SEC-004 with path, status Draft, and tier (likely Tier-3: production readiness).

Dependencies
	•	A5 (infra/ skeleton with modules/kms/).
	•	SEC-001..003 should exist to align threat model, IAM, and network assumptions.

Acceptance Criteria
	•	SEC-004-Secrets-and-Key-Management-Strategy.md exists with full content and valid front matter.
	•	Every category of secret and key has:
	•	A storage location,
	•	Access path,
	•	Rotation policy.
	•	The document references IAM roles and KMS modules consistently with SEC-002 and infra/.
	•	GOV-ARCH-001 lists SEC-004 as Existing with a clear tier and path.

⸻

C02 – OBS-LOG-001 Logging Strategy

Title: Write OBS-LOG-001-Logging-Strategy

Background

You have multiple services (nc-data-pipeline, nc-core, nc-audithound-api, nc-agent-forge, nc-mcp-server) and shared libs (nc_observability). To make logs useful and safe, you need a standardized logging strategy covering:
	•	Log schema,
	•	Required fields (tenant, correlation IDs, severity),
	•	Redaction of secrets/PII,
	•	Retention and sinks.

This doc will drive implementation of libs/python/nc_observability and configure logging-related infra.

Tasks
	1.	Create and place file
	•	Create:
docs/observability/OBS-LOG-001-Logging-Strategy.md
	•	Add front matter:
	•	id: OBS-LOG-001-Logging-Strategy
	•	title: Logging Strategy
	•	owner: Platform Engineering
	•	status: Draft
	•	last_reviewed: <today>
	2.	Define Logging Objectives
	•	Capture:
	•	Primary goals (debugging, audit trails, security investigation).
	•	Constraints (avoid leaking PII/secrets, ensure tenant isolation in logs).
	3.	Canonical Log Schema
	•	Define the JSON log schema fields, e.g.:
	•	timestamp (ISO 8601).
	•	level (DEBUG/INFO/WARN/ERROR).
	•	service (e.g., nc-data-pipeline, nc-core, etc.).
	•	environment (dev/staging/prod).
	•	tenant_id (ULID, or null for non-tenant operations).
	•	correlation_id / request_id.
	•	message.
	•	context (structured key-value map).
	•	Clarify:
	•	Which fields are mandatory for all log entries.
	•	Which are optional but recommended.
	4.	PII and Secret Redaction Rules
	•	Enumerate:
	•	Types of sensitive data that must never appear in logs:
	•	Secrets (tokens, passwords, API keys).
	•	Raw PII (emails, full names, addresses, etc.), unless explicitly allowed and necessary.
	•	Define:
	•	Redaction strategy (e.g., mask values, hash where necessary).
	•	Responsibility (library vs service-level).
	•	Provide examples of correct vs incorrect logging patterns.
	5.	Logging Levels & Usage Guidelines
	•	Define:
	•	How DEBUG/INFO/WARN/ERROR should be used.
	•	Provide:
	•	Examples of typical messages at each level for each service class:
	•	Pipeline ingestion events.
	•	Core risk evaluations.
	•	Agent Forge actions.
	•	AuditHound assessment runs.
	6.	Log Routing & Sinks (High-Level)
	•	Describe:
	•	Where logs are shipped (e.g., CloudWatch logs groups, OpenSearch for log search, third-party log management if any).
	•	Per-environment differences (dev vs prod retention).
	•	Define retention targets at a high level (exact ILM in DM/infra, but policy here).
	7.	Integration with nc_observability
	•	Define:
	•	How libraries will standardize log creation:
	•	One logger factory function or class used across services.
	•	Outline:
	•	Required API of nc_observability for logs (e.g., get_logger(service_name) that auto-injects fields).
	8.	Update Index
	•	Add OBS-LOG-001 to GOV-ARCH-001 with status Draft and tier (Tier-3).

Dependencies
	•	A4 (libs/python/nc_observability structure).
	•	DM-006 for tenant ID propagation.
	•	SEC-001/SEC-004 for privacy and secrets handling constraints.

Acceptance Criteria
	•	OBS-LOG-001-Logging-Strategy.md exists with a defined log schema, redaction rules, and usage guidelines.
	•	It is clear how logs must look platform-wide and how tenant context/correlation IDs are handled.
	•	The document directly informs nc_observability implementation.
	•	GOV-ARCH-001 lists OBS-LOG-001 correctly.

⸻

C03 – OBS-MET-001 Metrics and SLOs

Title: Write OBS-MET-001-Metrics-and-SLOs

Background

You need consistent platform-level metrics and explicit SLOs to ensure operational health and guide alerting. This includes ingestion freshness, query latency, error rates, and key workflow performance.

Tasks
	1.	Create and place file
	•	Create:
docs/observability/OBS-MET-001-Metrics-and-SLOs.md
	•	Add front matter:
	•	id: OBS-MET-001-Metrics-and-SLOs
	•	title: Metrics and SLOs
	•	owner: Platform Engineering
	•	status: Draft
	•	last_reviewed: <today>
	2.	Define Observability Goals
	•	Document:
	•	Why metrics exist (early anomaly detection, capacity planning, SLA enforcement).
	•	Scope: all services and critical workflows (ingest, normalize, embed, query, compliance assessment, remediation).
	3.	Core Metrics Per Service
	•	For each major service (nc-data-pipeline, nc-core, nc-audithound-api, nc-agent-forge, nc-mcp-server), define:
	•	Throughput metrics (requests/sec, messages processed/sec).
	•	Latency metrics (p95/p99 per endpoint or workflow).
	•	Error metrics (error rate per operation).
	•	Resource-related metrics (queue depth, backlog, CPU/memory if relevant).
	•	Use consistent naming conventions.
	4.	Platform-Level SLOs
	•	Define SLOs for key user-facing behaviors, for example:
	•	Query endpoint:
	•	99% of GET /v1/query requests complete in < X ms.
	•	Ingest-to-available-latency:
	•	95% of ingested documents are searchable (embedded + indexed) within Y minutes.
	•	Compliance assessments:
	•	99% complete within Z minutes under normal load.
	•	Add error budget concepts where useful.
	5.	Metric Collection & Export
	•	Describe:
	•	How metrics are exported (e.g., CloudWatch metrics, Prometheus if applicable).
	•	How labels/tags are applied (service, env, tenant_id where appropriate but safe).
	•	Tie this to nc_observability metrics helpers (planned).
	6.	Alerting Principles
	•	Outline:
	•	High-level alerting strategy:
	•	Which SLO violations should trigger alerts.
	•	Basic thresholds for initial implementation (you can refine later).
	•	Defer the exact alert rules to ops/alerts/ configs, but define intent here.
	7.	Update Index
	•	Add OBS-MET-001 to GOV-ARCH-001 with status and tier (Tier-3).

Dependencies
	•	A4 (nc_observability).
	•	ARC-002..006 for understanding workflows.
	•	OBS-LOG-001 as a sibling observability document.

Acceptance Criteria
	•	OBS-MET-001-Metrics-and-SLOs.md defines a clear metric taxonomy and platform-level SLOs.
	•	Each core service has a defined set of metrics.
	•	At least 3–5 critical SLOs are specified with intended targets.
	•	GOV-ARCH-001 includes OBS-MET-001 with path and tier.

⸻

C04 – DR-001 Disaster Recovery and Backup Plan

Title: Write DR-001-Disaster-Recovery-and-Backup-Plan

Background

You are building a security and compliance platform; disaster recovery is not optional. DR-001 must define:
	•	RTO/RPO per critical component,
	•	Backup strategies,
	•	Restore procedures, and
	•	How DR drills are conducted and validated.

Tasks
	1.	Create and place file
	•	Create:
docs/security-controls/DR-001-Disaster-Recovery-and-Backup-Plan.md
	•	Add front matter:
	•	id: DR-001-Disaster-Recovery-and-Backup-Plan
	•	title: Disaster Recovery and Backup Plan
	•	owner: Security
	•	status: Draft
	•	last_reviewed: <today>
	2.	Define RTO and RPO
	•	For each critical component:
	•	Postgres (nc_dev / prod equivalent).
	•	S3 buckets (raw and normalized data).
	•	Weaviate vector store.
	•	OpenSearch indices.
	•	MCP server and other APIs.
	•	Specify:
	•	RTO (Recovery Time Objective).
	•	RPO (Recovery Point Objective).
	3.	Backup Strategies
	•	For each component, describe:
	•	How backups are taken:
	•	Postgres: automated snapshots and/or PITR.
	•	S3: versioning and replication, if applicable.
	•	OpenSearch: snapshots.
	•	Weaviate: snapshot/export strategy.
	•	Backup frequency.
	•	Storage location/region (e.g., cross-AZ or cross-region replication).
	4.	Restore Procedures
	•	Define step-by-step high-level procedures for:
	•	Postgres restore.
	•	S3 data restore (specific prefixes, if needed).
	•	OpenSearch snapshot restore.
	•	Weaviate restore.
	•	Note:
	•	Preconditions (IAM permissions, KMS requirements).
	•	Expected downtime and impact.
	5.	DR Scenarios
	•	Enumerate key failure scenarios:
	•	Single component failure (DB down).
	•	Data corruption.
	•	Region-wide outage (if planned for).
	•	For each, describe:
	•	Which backup and restore procedures apply.
	•	Expected RTO/RPO behavior.
	6.	Testing and Drills
	•	Specify:
	•	How often DR tests should be conducted (e.g., annually, semi-annually).
	•	Minimum scope of each test:
	•	At least 1 full restore simulation from backup.
	•	Verification that recovered system is functional and consistent.
	7.	Update Index
	•	Add DR-001 to GOV-ARCH-001 with status and tier (Tier-3: production readiness).

Dependencies
	•	DM-003, DM-004, DM-006 for understanding where critical data lives.
	•	SEC-004 for KMS dependencies and secrets.

Acceptance Criteria
	•	DR-001-Disaster-Recovery-and-Backup-Plan.md clearly defines RTO/RPO, backup strategies, and restore procedures for each critical component.
	•	It includes a DR testing cadence and minimum test requirements.
	•	GOV-ARCH-001 includes DR-001 correctly.

⸻

C05 – TEST-001 Test Strategy and Coverage Requirements

Title: Write TEST-001-Test-Strategy-and-Coverage-Requirements

Background

You already use pytest, DB integration tests, and CI workflows. As the platform grows into multiple services, you need a formal test strategy that defines:
	•	Test types (unit, integration, contract, e2e, load),
	•	Directory layout,
	•	Coverage expectations, and
	•	CI gates per stage.

Tasks
	1.	Create and place file
	•	Create:
docs/engineering/TEST-001-Test-Strategy-and-Coverage-Requirements.md
	•	If docs/engineering/ does not exist, create it and register in GOV-ARCH.
	•	Add front matter:
	•	id: TEST-001-Test-Strategy-and-Coverage-Requirements
	•	title: Test Strategy and Coverage Requirements
	•	owner: Engineering
	•	status: Draft
	•	last_reviewed: <today>
	2.	Define Test Taxonomy
	•	Describe each test type:
	•	Unit tests.
	•	Integration tests (e.g., DB integration, service-to-service).
	•	Contract tests (API contracts, event schemas, data contracts).
	•	End-to-end tests (vertical slices across services).
	•	Load/performance tests.
	•	Provide 1–2 examples per type relevant to Neurocipher.
	3.	Directory Layout
	•	Define the expected layout at repo root (and per service), e.g.:

tests/
  unit/
  integration/
  contracts/
  e2e/
  load/


	•	Clarify:
	•	For service-specific tests, subdirectories under services/<service>/tests/ may mirror this structure.

	4.	Coverage Requirements
	•	Define:
	•	Minimum unit test coverage for critical modules (e.g., 80%+).
	•	What integration/e2e coverage is expected for core flows (not percentage-only; also scenario coverage).
	•	List:
	•	Which parts of the codebase are considered “critical” (e.g., security actions, RLS enforcement, tenant isolation paths).
	5.	CI Integration and Gates
	•	Specify:
	•	Which test suites run on:
	•	Every PR (fast subset: unit + key integration).
	•	Nightly or scheduled (full integration, e2e, load).
	•	Coverage thresholds enforced in CI (e.g., fail PR if unit coverage < 80%).
	•	Define:
	•	How failures are to be interpreted (e.g., load test failures do not block PRs but block staging promotion).
	6.	Link to Existing Infrastructure
	•	Reference:
	•	.github/workflows/*.yml for test jobs.
	•	Makefile targets like make test, make db_local_smoke_test.
	•	Clarify how to run the key test suites locally.
	7.	Update Index
	•	Add TEST-001 to GOV-ARCH-001 with path, status Draft, and Tier-3.

Dependencies
	•	A6/A7 CI and Makefile should be in place.
	•	Existing tests under tests/ and tests/db/ to serve as concrete examples.

Acceptance Criteria
	•	TEST-001-Test-Strategy-and-Coverage-Requirements.md defines:
	•	Test types,
	•	Directory layout,
	•	Coverage expectations,
	•	CI integration rules.
	•	There is a clear description of which tests must pass on PRs versus nightly runs.
	•	GOV-ARCH-001 lists TEST-001 with correct path and tier.

⸻
