.DEFAULT_GOAL := help
SHELL := bash
.ONESHELL:

# Configuration variables
PROJECT_PATH := src
PYTHON_VERSION := 3.12
PORT := 8000
HOST := 0.0.0.0
ENVIRONMENT := local


.PHONY: help
help: ## Show help
	@echo "Usage: make <target>"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "%-20s %s\n", $$1, $$2}'

.PHONY: virtualenv
virtualenv: ## Create a virtual environment
	@echo "Creating virtual environment using UV..."
	@uv venv
	@source .venv/bin/activate

.PHONY: lint
lint: ## Run linters
	uv run pre-commit run --all-files

.PHONY: install
install: ## Install and configure the project dependencies
	uv pip install --upgrade pip wheel
	uv sync
	uv pip install --group dev
	uv run pre-commit install

.PHONY: update_libs
update_libs: ## Update all installed libraries
	uv pip install --upgrade $(shell uv run uv pip list --format freeze | cut -d= -f1)

.PHONY: clean
clean: ## Remove all temporary files like pycache
	find . -type f -name "*.rdb" -delete
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +


# -----------------------------------------------------------------------------
.PHONY: start
start: install ## Start the development server
	cd ${PROJECT_PATH} && uv run uvicorn main:app --reload --host ${HOST} --port ${PORT}

.PHONY: app
app: ## Run the application
	@COMPOSE_BAKE=true docker compose up --build app
