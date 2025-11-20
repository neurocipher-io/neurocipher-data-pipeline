PYTHON_SOURCES=services libs/python

PG_CONTAINER_NAME ?= nc-pg-local
PG_IMAGE ?= postgres:15
PG_PORT ?= 5432
PG_USER ?= postgres
PG_PASSWORD ?= postgres
PG_DB ?= nc_dev

.PHONY: fmt lint test db_local_up db_local_migrate db_local_down

fmt:
	ruff --fix .
	isort .
	black .

lint:
	markdownlint docs AGENTS.md
	yamllint .
	ruff .
	isort --check-only .
	black --check .

test:
	mkdir -p reports
	pytest $(PYTHON_SOURCES) --cov=src --cov-report=xml:reports/coverage.xml --junitxml=reports/junit.xml

# Local Postgres for schema and migration validation
# Starts a Postgres 15 container, creates $(PG_DB), and applies migrations under migrations/postgres/.
db_local_up:
	@docker ps -a --format '{{.Names}}' | grep -q '^$(PG_CONTAINER_NAME)$$' || \
	  docker run -d --name $(PG_CONTAINER_NAME) \
	    -e POSTGRES_USER=$(PG_USER) \
	    -e POSTGRES_PASSWORD=$(PG_PASSWORD) \
	    -e POSTGRES_DB=$(PG_DB) \
	    -p $(PG_PORT):5432 \
	    -v $(PWD):/workspace \
	    $(PG_IMAGE)

# Apply all Postgres migrations in order to the local container database.
db_local_migrate:
	@docker exec -i $(PG_CONTAINER_NAME) sh -lc 'set -e; \
	  for f in /workspace/migrations/postgres/*.sql; do \
	    echo "Applying $$f"; \
	    psql -U $(PG_USER) -d $(PG_DB) -v ON_ERROR_STOP=1 -f "$$f"; \
	  done'

# Stop the local Postgres container if it is running.
db_local_down:
	@docker stop $(PG_CONTAINER_NAME) >/dev/null 2>&1 || true
