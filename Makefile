.PHONY: test test-unit test-integration test-e2e test-fast test-coverage clean help

# 🧪 Testing Commands

test: ## Run all tests
	pytest

test-unit: ## Run only unit tests
	pytest -m unit

test-integration: ## Run only integration tests  
	pytest -m integration

test-e2e: ## Run only end-to-end tests
	pytest -m e2e

test-fast: ## Run tests excluding slow ones
	pytest -m "not slow"

test-coverage: ## Run tests with detailed coverage report
	pytest --cov=app --cov-report=html --cov-report=term-missing

# 🧹 Cleanup Commands

clean: ## Clean up generated files
	rm -rf .pytest_cache/
	rm -rf htmlcov/
	rm -rf .coverage
	rm -rf coverage.xml
	find . -type d -name __pycache__ -delete
	find . -type f -name "*.pyc" -delete

# 🚀 Development Commands

install-dev: ## Install development dependencies
	pip install -r requirements.txt
	pip install pytest pytest-asyncio httpx pytest-mock pytest-cov

format: ## Format code with black
	black app/ tests/

lint: ## Lint code with flake8
	flake8 app/ tests/

type-check: ## Type check with mypy
	mypy app/ --ignore-missing-imports

quality: format lint type-check ## Run all code quality checks

# 🐳 Docker Commands

docker-test: ## Run tests in Docker
	docker compose -f docker-compose.test.yml up --build --abort-on-container-exit

docker-clean: ## Clean Docker test environment
	docker compose -f docker-compose.test.yml down -v
	docker system prune -f

# 📊 Reporting

test-report: test-coverage ## Generate comprehensive test report
	@echo "📊 Test Coverage Report generated in htmlcov/"
	@echo "🔍 Open htmlcov/index.html in browser to view"

help: ## Show this help message
	@echo "AI Agent Farm - Testing & Development Commands"
	@echo ""
	@awk 'BEGIN {FS = ":.*##"; printf "Usage:\n  make \033[36m<target>\033[0m\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

# Default target
.DEFAULT_GOAL := help
