PYTHON ?= python3
VENV_PYTHON ?= .venv/bin/python
DOCKER_COMPOSE ?= docker compose

.PHONY: setup build up down ingest seed reseed test coverage ragas load-test health lint security deploy

setup:
	$(PYTHON) -m venv .venv
	$(VENV_PYTHON) -m pip install -r requirements.txt
	@if [ ! -f .env ]; then \
		cp .env.example .env; \
		echo "[INFO] Archivo .env creado desde .env.example"; \
	fi

build:
	$(DOCKER_COMPOSE) build

up:
	$(DOCKER_COMPOSE) up -d

down:
	$(DOCKER_COMPOSE) down

ingest:
ifndef FILES
	@echo "[ERROR] Debes indicar archivos: make ingest FILES='data/sample_docs/doc1.md'"
	@exit 1
endif
	$(VENV_PYTHON) scripts/ingest_local.py $(FILES) $(if $(MODULE),--module $(MODULE),)

seed:
	$(VENV_PYTHON) scripts/seed_sample_docs.py

reseed:
	$(VENV_PYTHON) scripts/reset_vector_store.py
	$(VENV_PYTHON) scripts/seed_sample_docs.py

test:
	$(VENV_PYTHON) -m pytest -q

coverage:
	$(VENV_PYTHON) -m pytest --cov=app --cov-report=term-missing --cov-report=xml

ragas:
	$(VENV_PYTHON) scripts/ragas_eval.py

load-test:
	@if command -v k6 >/dev/null 2>&1; then \
		mkdir -p reports; \
		k6 run --summary-trend-stats='avg,min,med,max,p(90),p(95),p(99)' --summary-export reports/load_test_report.json scripts/load_test.js; \
		echo "[OK] Reporte generado: reports/load_test_report.json"; \
	else \
		echo "[ERROR] k6 no esta instalado. Instala k6 para ejecutar load-test."; \
		exit 1; \
	fi

health:
	@curl -fsS http://localhost:8000/v1/health || (echo "[ERROR] /v1/health no disponible en localhost:8000" && exit 1)

lint:
	@if ! command -v ruff >/dev/null 2>&1; then \
		echo "[ERROR] ruff no instalado. Ejecuta: pip install ruff"; \
		exit 1; \
	fi
	@if ! command -v mypy >/dev/null 2>&1; then \
		echo "[ERROR] mypy no instalado. Ejecuta: pip install mypy"; \
		exit 1; \
	fi
	ruff check app tests
	mypy app

security:
	$(VENV_PYTHON) scripts/security_scan.py

deploy:
	./scripts/deploy_cloud_run.sh
