PYTHON_SOURCES=services libs/python

.PHONY: fmt lint test

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
