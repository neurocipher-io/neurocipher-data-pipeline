# Repository Guidelines

## Project Structure & Module Organization

- `services/` hosts Lambda, Step Functions, and Glue workloads (each service keeps `src/` plus `tests/`).  
- Shared runtime utilities live in `libs/python/`; schemas live in `schemas/openapi/` and `schemas/events/` (`*.v1.json`).  
- Docs are grouped under `docs/`, operational artifacts under `ops/{dashboards,alerts,owners.yaml}`, IaC under `iac/stacks/`, and the repo root holds `openapi.yaml` plus `.spectral.yaml`.

## Build, Test, and Development Commands

- `make init` – bootstrap Poetry, Node tooling, and pre-commit hooks.
- `make fmt` – apply Black, isort, and markdownlint.
- `make lint` – run Spectral (`npx @stoplight/spectral-cli lint`), markdownlint, and Lychee link checks.
- `make test` – execute pytest suites across `services/**/tests` and `libs/python/tests` with coverage.
- `make build` – package Lambda bundles and containers, then scan dependencies.

Use `npm run spectral` for a fast OpenAPI-only lint when editing `openapi.yaml`.

## Coding Style & Naming Conventions

- Python follows Black defaults (88-char lines, 4-space indent) plus type hints for public functions.  
- JSON/YAML use 2-space indents and kebab-case filenames (e.g., `event.security.finding.v1.json`).  
- Markdown specs require front matter (`id`, `title`, `owner`, `status`, `last_reviewed`) and sentence-case headings, and every doc must start with REF-001 metadata.  
- Directories and filenames avoid spaces, ampersands, and em dashes; enforce via `rg -n '[—&()]' docs`.

## Testing Guidelines

- Pytest drives unit and contract suites; fixtures belong in `tests/fixtures/` and files follow `test_<feature>.py`.  
- Maintain ≥80% line coverage via `pytest --junitxml=reports/junit.xml --cov=src --cov-report=xml --cov-fail-under=80`, and keep samples in `schemas/events/examples/`.  
- Run `make test` locally before pushing; rerun the full pytest command when reproducing CI failures or schema updates.

## Commit & Pull Request Guidelines

- Commits follow `type: scope` (e.g., `feat: ingestion retries`, `docs: runbook refresh`) and reference Jira IDs in the body.  
- Avoid mixing IaC with runtime changes unless the description justifies it.  
- PRs must include a summary, `make fmt && make lint && make test` evidence, linked issue, screenshots/logs for UX or dashboard work, and reviewer tags from `ops/owners.yaml`.  
- Keep PRs in draft until Spectral, markdownlint, and Lychee checks pass in CI.

## Validation & QA Flow

- Local sandbox runs `markdownlint docs AGENTS.md`, `yamllint .`, `ruff .`, `black --check .`, `isort --check-only .`, and `pytest services libs/python` via `make lint` / `make test`.  
- Skip `npx` installs and external HTTP probes in the sandbox; instead emit a status summary noting the deferral.  
- `.github/workflows/lint.yml` performs networked checks (Spectral + Lychee) on every push/PR, so confirm it stays green before requesting review.

## Security & Configuration Tips

Never commit secrets or `.env` files; rely on AWS Secrets Manager and SSM parameters.  
Enforce KMS encryption and least-privilege IAM in every template in `iac/`.  
Review `ops/owners.yaml` before editing IAM-related IaC to ensure the correct approval path.  
When editing security-engine contracts, update both schema `$id` fields and the corresponding guides in `docs/security-engine/`, then rerun Spectral plus JSON schema validation before requesting review.

See `AGENTS.md` and `agents.yaml` for automation and validation rules.
