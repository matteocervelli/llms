.PHONY: help sync-global watch-sync sync-audit sync-check sync-push sync-pull sync-settings test lint format

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Available targets:'
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-20s %s\n", $$1, $$2}'

sync-global: ## Copy project .claude files to global ~/.claude
	@./scripts/copy-to-global.sh

watch-sync: ## Watch .claude for changes and auto-copy to global (for active development)
	@./scripts/watch-and-sync.sh

sync-audit: ## Audit configuration differences between project and global
	@python sync_claude_configs.py --audit

sync-check: ## Quick check sync status (audit with summary only)
	@python sync_claude_configs.py

sync-push: ## Sync project → global (with interactive conflict resolution)
	@python sync_claude_configs.py --sync

sync-pull: ## Sync global → project (with interactive conflict resolution)
	@python sync_claude_configs.py --sync --pull

sync-dry: ## Preview sync operations without making changes
	@python sync_claude_configs.py --sync --dry-run

sync-settings: ## Analyze and compare settings.json files
	@python sync_claude_configs.py --settings

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
