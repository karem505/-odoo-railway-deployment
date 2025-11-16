# Makefile for Odoo Docker Deployment
# Simplifies common Docker operations
#
# Usage: make <target>
# Example: make dev-up

.PHONY: help dev-up dev-down dev-logs dev-restart prod-up prod-down prod-logs prod-restart build clean backup restore test

# Default target
.DEFAULT_GOAL := help

# Colors for output
BLUE := \033[0;34m
GREEN := \033[0;32m
YELLOW := \033[0;33m
RED := \033[0;31m
NC := \033[0m # No Color

##@ General

help: ## Display this help message
	@echo "$(BLUE)Odoo Docker Deployment - Available Commands$(NC)"
	@echo ""
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make $(GREEN)<target>$(NC)\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  $(GREEN)%-20s$(NC) %s\n", $$1, $$2 } /^##@/ { printf "\n$(BLUE)%s$(NC)\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

##@ Development (Local Testing)

dev-up: ## Start development environment
	@echo "$(GREEN)Starting development environment...$(NC)"
	docker-compose up -d
	@echo "$(GREEN)✓ Development environment started$(NC)"
	@echo "Access Odoo at: $(BLUE)http://localhost:8069$(NC)"

dev-down: ## Stop development environment
	@echo "$(YELLOW)Stopping development environment...$(NC)"
	docker-compose down
	@echo "$(GREEN)✓ Development environment stopped$(NC)"

dev-logs: ## View development logs (all services)
	docker-compose logs -f

dev-logs-odoo: ## View Odoo logs only
	docker-compose logs -f odoo

dev-logs-agent: ## View LiveKit agent logs only
	docker-compose logs -f livekit-agent

dev-restart: ## Restart development environment
	@echo "$(YELLOW)Restarting development environment...$(NC)"
	docker-compose restart
	@echo "$(GREEN)✓ Development environment restarted$(NC)"

dev-restart-odoo: ## Restart Odoo service only
	docker-compose restart odoo

dev-clean: ## Stop and remove all containers, networks, and volumes
	@echo "$(RED)WARNING: This will delete all data!$(NC)"
	@read -p "Are you sure? [y/N] " -n 1 -r; \
	echo; \
	if [[ $$REPLY =~ ^[Yy]$$ ]]; then \
		docker-compose down -v; \
		echo "$(GREEN)✓ Development environment cleaned$(NC)"; \
	fi

##@ Production

prod-up: ## Start production environment
	@echo "$(GREEN)Starting production environment...$(NC)"
	@if [ ! -f .env ]; then \
		echo "$(RED)ERROR: .env file not found!$(NC)"; \
		echo "Copy .env.example to .env and configure it first."; \
		exit 1; \
	fi
	docker-compose -f docker-compose.prod.yml up -d
	@echo "$(GREEN)✓ Production environment started$(NC)"

prod-down: ## Stop production environment
	@echo "$(YELLOW)Stopping production environment...$(NC)"
	docker-compose -f docker-compose.prod.yml down
	@echo "$(GREEN)✓ Production environment stopped$(NC)"

prod-logs: ## View production logs (all services)
	docker-compose -f docker-compose.prod.yml logs -f

prod-restart: ## Restart production environment
	@echo "$(YELLOW)Restarting production environment...$(NC)"
	docker-compose -f docker-compose.prod.yml restart
	@echo "$(GREEN)✓ Production environment restarted$(NC)"

prod-status: ## Check production services status
	docker-compose -f docker-compose.prod.yml ps

##@ Build & Deploy

build: ## Build Docker images
	@echo "$(GREEN)Building Docker images...$(NC)"
	docker-compose build --no-cache
	@echo "$(GREEN)✓ Images built successfully$(NC)"

build-prod: ## Build production Docker images
	@echo "$(GREEN)Building production Docker images...$(NC)"
	docker-compose -f docker-compose.prod.yml build --no-cache
	@echo "$(GREEN)✓ Production images built successfully$(NC)"

push: ## Push images to registry (set DOCKER_REGISTRY in .env)
	@if [ -z "$$DOCKER_REGISTRY" ]; then \
		echo "$(RED)ERROR: DOCKER_REGISTRY not set in .env$(NC)"; \
		exit 1; \
	fi
	@echo "$(GREEN)Pushing images to registry...$(NC)"
	docker-compose -f docker-compose.prod.yml push
	@echo "$(GREEN)✓ Images pushed successfully$(NC)"

pull: ## Pull latest images from registry
	@echo "$(GREEN)Pulling latest images...$(NC)"
	docker-compose -f docker-compose.prod.yml pull
	@echo "$(GREEN)✓ Images pulled successfully$(NC)"

##@ Database Operations

backup: ## Backup PostgreSQL database
	@echo "$(GREEN)Creating database backup...$(NC)"
	@mkdir -p ./backups
	@TIMESTAMP=$$(date +%Y%m%d_%H%M%S); \
	docker exec odoo-postgres-prod pg_dump -U odoo postgres > ./backups/odoo_backup_$$TIMESTAMP.sql && \
	echo "$(GREEN)✓ Backup created: ./backups/odoo_backup_$$TIMESTAMP.sql$(NC)"

restore: ## Restore PostgreSQL database (Usage: make restore FILE=backup.sql)
	@if [ -z "$(FILE)" ]; then \
		echo "$(RED)ERROR: Specify backup file$(NC)"; \
		echo "Usage: make restore FILE=./backups/odoo_backup_20240101_120000.sql"; \
		exit 1; \
	fi
	@echo "$(YELLOW)WARNING: This will restore database from $(FILE)$(NC)"
	@read -p "Are you sure? [y/N] " -n 1 -r; \
	echo; \
	if [[ $$REPLY =~ ^[Yy]$$ ]]; then \
		docker exec -i odoo-postgres-prod psql -U odoo postgres < $(FILE) && \
		echo "$(GREEN)✓ Database restored from $(FILE)$(NC)"; \
	fi

db-shell: ## Open PostgreSQL shell
	docker exec -it odoo-postgres-prod psql -U odoo postgres

##@ Maintenance

clean: ## Remove unused Docker resources
	@echo "$(YELLOW)Cleaning up Docker resources...$(NC)"
	docker system prune -f
	@echo "$(GREEN)✓ Cleanup complete$(NC)"

clean-all: ## Remove ALL Docker resources (including images)
	@echo "$(RED)WARNING: This will remove all Docker images!$(NC)"
	@read -p "Are you sure? [y/N] " -n 1 -r; \
	echo; \
	if [[ $$REPLY =~ ^[Yy]$$ ]]; then \
		docker system prune -af --volumes; \
		echo "$(GREEN)✓ All Docker resources cleaned$(NC)"; \
	fi

logs-export: ## Export logs to file
	@echo "$(GREEN)Exporting logs...$(NC)"
	@mkdir -p ./logs
	@TIMESTAMP=$$(date +%Y%m%d_%H%M%S); \
	docker-compose -f docker-compose.prod.yml logs > ./logs/odoo_logs_$$TIMESTAMP.log && \
	echo "$(GREEN)✓ Logs exported to ./logs/odoo_logs_$$TIMESTAMP.log$(NC)"

##@ Testing

test: ## Run basic health checks
	@echo "$(GREEN)Running health checks...$(NC)"
	@echo "Checking Odoo..."
	@curl -f http://localhost:8069/web/health > /dev/null 2>&1 && \
		echo "$(GREEN)✓ Odoo is healthy$(NC)" || \
		echo "$(RED)✗ Odoo is not responding$(NC)"
	@echo "Checking PostgreSQL..."
	@docker exec odoo-postgres pg_isready -U odoo > /dev/null 2>&1 && \
		echo "$(GREEN)✓ PostgreSQL is healthy$(NC)" || \
		echo "$(RED)✗ PostgreSQL is not responding$(NC)"
	@echo "Checking Redis..."
	@docker exec odoo-redis redis-cli ping > /dev/null 2>&1 && \
		echo "$(GREEN)✓ Redis is healthy$(NC)" || \
		echo "$(RED)✗ Redis is not responding$(NC)"

shell-odoo: ## Open shell in Odoo container
	docker exec -it odoo-web bash

shell-agent: ## Open shell in LiveKit agent container
	docker exec -it odoo-livekit-agent bash

shell-db: ## Open shell in PostgreSQL container
	docker exec -it odoo-postgres bash

##@ Quick Actions

quick-start: dev-up ## Quick start development environment (alias for dev-up)

quick-stop: dev-down ## Quick stop development environment (alias for dev-down)

quick-restart: dev-restart ## Quick restart development (alias for dev-restart)

status: ## Show status of all containers
	@echo "$(BLUE)Container Status:$(NC)"
	@docker ps -a --filter "name=odoo" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

watch: ## Watch logs in real-time (development)
	@echo "$(GREEN)Watching logs... (Press Ctrl+C to stop)$(NC)"
	docker-compose logs -f --tail=100

##@ Documentation

env-template: ## Create .env from template
	@if [ -f .env ]; then \
		echo "$(YELLOW).env already exists. Backup created as .env.backup$(NC)"; \
		cp .env .env.backup; \
	fi
	cp .env.example .env
	@echo "$(GREEN)✓ .env created from template$(NC)"
	@echo "$(YELLOW)⚠ Please edit .env and add your credentials$(NC)"

check-env: ## Verify .env configuration
	@echo "$(GREEN)Checking .env configuration...$(NC)"
	@if [ ! -f .env ]; then \
		echo "$(RED)✗ .env file not found$(NC)"; \
		exit 1; \
	fi
	@echo "$(GREEN)✓ .env file exists$(NC)"
	@grep -q "OPENAI_API_KEY=sk-" .env && echo "$(GREEN)✓ OpenAI API key set$(NC)" || echo "$(YELLOW)⚠ OpenAI API key not set$(NC)"
	@grep -q "ODOO_MASTER_PASSWORD=" .env && echo "$(GREEN)✓ Odoo master password set$(NC)" || echo "$(YELLOW)⚠ Odoo master password not set$(NC)"

info: ## Display environment information
	@echo "$(BLUE)Environment Information:$(NC)"
	@echo "Docker version: $$(docker --version)"
	@echo "Docker Compose version: $$(docker-compose --version)"
	@echo ""
	@echo "$(BLUE)Local URLs:$(NC)"
	@echo "  Odoo:          http://localhost:8069"
	@echo "  PostgreSQL:    localhost:5432"
	@echo "  Redis:         localhost:6379"
	@echo ""
	@echo "$(BLUE)Default Credentials:$(NC)"
	@echo "  Odoo:      admin / admin (first setup)"
	@echo "  Postgres:  odoo / odoo_local_password"
	@echo "  Redis:     - / redis_local_password"
