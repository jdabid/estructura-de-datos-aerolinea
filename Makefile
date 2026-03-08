.PHONY: help up down dev logs logs-api logs-worker ps restart clean test test-cov lint format security flower grafana jaeger fe-install fe-build fe-dev fe-lint db-shell migrate migrate-gen helm-install helm-uninstall helm-template helm-lint kustomize-build-dev kustomize-build-staging kustomize-build-prod kustomize-validate kustomize-diff deploy-dev deploy-staging deploy-prod healthcheck status

help: ## Mostrar ayuda
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

# === Docker ===
up: ## Levantar todos los servicios
	docker compose up --build -d

down: ## Detener todos los servicios
	docker compose down

dev: ## Levantar en modo desarrollo con hot-reload
	docker compose -f docker-compose.yml -f docker-compose.dev.yml up --build

logs: ## Ver logs de todos los servicios
	docker compose logs -f

logs-api: ## Ver logs del API
	docker compose logs -f api

logs-worker: ## Ver logs del worker
	docker compose logs -f worker

ps: ## Ver estado de servicios
	docker compose ps

restart: ## Reiniciar todos los servicios
	docker compose restart

clean: ## Detener y eliminar volumenes
	docker compose down -v

# === Backend ===
test: ## Ejecutar tests
	docker compose exec api pytest tests/ -v --tb=short

test-cov: ## Ejecutar tests con coverage
	docker compose exec api pytest tests/ -v --tb=short --cov=src --cov-report=html

lint: ## Ejecutar linters (ruff + mypy)
	cd backend && ruff check src/ && mypy src/

format: ## Formatear codigo con ruff
	cd backend && ruff format src/

security: ## Ejecutar bandit
	cd backend && bandit -r src/ -ll -ii

# === Monitoring ===
flower: ## Open Flower dashboard
	@echo "Flower: http://localhost:5555"
	@open http://localhost:5555 2>/dev/null || echo "Open http://localhost:5555 in browser"

grafana: ## Open Grafana dashboard
	@echo "Grafana: http://localhost:3001 (admin/admin123)"
	@open http://localhost:3001 2>/dev/null || echo "Open http://localhost:3001 in browser"

jaeger: ## Open Jaeger UI
	@echo "Jaeger: http://localhost:16686"
	@open http://localhost:16686 2>/dev/null || echo "Open http://localhost:16686 in browser"

# === Frontend ===
fe-install: ## Instalar dependencias frontend
	cd frontend && npm install

fe-build: ## Build frontend
	cd frontend && npm run build

fe-dev: ## Dev server frontend (sin Docker)
	cd frontend && npm run dev

fe-lint: ## Lint frontend
	cd frontend && npm run lint

# === Database ===
db-shell: ## Abrir shell PostgreSQL
	docker compose exec db psql -U user -d flights

migrate: ## Ejecutar migraciones Alembic
	docker compose exec api alembic upgrade head

migrate-gen: ## Generar nueva migracion
	@read -p "Mensaje: " msg; docker compose exec api alembic revision --autogenerate -m "$$msg"

# === Helm / K8s ===
helm-install: ## Instalar/actualizar Helm chart
	helm upgrade --install flight-system ./infra/helm/flight-app

helm-uninstall: ## Desinstalar Helm chart
	helm uninstall flight-system

helm-template: ## Renderizar templates Helm
	helm template flight-system ./infra/helm/flight-app

helm-lint: ## Validar Helm chart
	helm lint ./infra/helm/flight-app

# === Kustomize ===
kustomize-build-dev: ## Build kustomize for dev
	kubectl kustomize infra/kustomize/overlays/dev/

kustomize-build-staging: ## Build kustomize for staging
	kubectl kustomize infra/kustomize/overlays/staging/

kustomize-build-prod: ## Build kustomize for prod
	kubectl kustomize infra/kustomize/overlays/prod/

kustomize-validate: ## Validate all kustomize builds
	@bash scripts/validate-kustomize.sh

kustomize-diff: ## Show diff between staging and prod
	@diff <(kubectl kustomize infra/kustomize/overlays/staging/) <(kubectl kustomize infra/kustomize/overlays/prod/) || true

# === Deploy ===
deploy-dev: ## Desplegar en modo desarrollo
	@bash scripts/deploy.sh --env dev --build

deploy-staging: ## Desplegar en modo staging
	@bash scripts/deploy.sh --env staging --build --migrate

deploy-prod: ## Desplegar en modo produccion
	@bash scripts/deploy.sh --env prod --build --migrate

healthcheck: ## Verificar salud de todos los servicios
	@bash scripts/healthcheck.sh

status: ## Mostrar estado de servicios y health check
	@docker compose ps
	@echo ""
	@bash scripts/healthcheck.sh
