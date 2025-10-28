.PHONY: help sync-global watch-sync test lint format

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Available targets:'
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-20s %s\n", $$1, $$2}'

sync-global: ## Copy project .claude files to global ~/.claude
	@./scripts/copy-to-global.sh

watch-sync: ## Watch .claude for changes and auto-copy to global (for active development)
	@./scripts/watch-and-sync.sh

test: ## Run pytest tests
	@pytest tests/ -v

lint: ## Run linting checks
	@flake8 src/ tests/
	@mypy src/

format: ## Format code with black
	@black src/ tests/

install: ## Install dependencies with uv
	@uv pip install -r requirements.txt
	@uv pip install -e ".[dev]"
