.DEFAULT_GOAL := help
SHELL := bash
.ONESHELL:

# Configuration variables
PROJECT_PATH := src
PYTHON_VERSION := 3.12
PORT := 8000
HOST := 0.0.0.0
ENVIRONMENT := local

export ENVIRONMENT := $(ENVIRONMENT)

# -----------------------------------------------------------------------------
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
install: ## Install all requirements to run the service
	@if ! command -v uv &> /dev/null; then \
		echo "Error: 'uv' is not installed. Please install it to continue."; \
		echo "Installation instructions: https://astral.sh/uv/install.sh"; \
		exit 1; \
	fi
	@echo "Creating virtual environment..."
	@uv venv
	@echo "Installing dependencies..."
	@uv pip install -e . --group dev
	@echo "Installing pre-commit hooks..."
	@uv run pre-commit install
	@echo "Installation complete!"
	@source .venv/bin/activate

.PHONY: update_libs
update_libs: ## Update all installed libraries
	uv lock --upgrade

.PHONY: clean_cache
clean_cache: ## Remove all temporary files like pycache
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

.PHONY: test
test: ## Run the tests
	@docker compose up --build test

.PHONY: down
down: ## Teardown of all running services
	@docker compose down

.PHONY: clean
clean: ## Teardown and removal of all containers, volumes, and images
	@docker compose down --volumes --remove-orphans --rmi all
