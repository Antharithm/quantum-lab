# Quantum Lab — common commands.  Run `make help` for the list.
PY := /opt/homebrew/bin/python3.13
VENV := .venv
BIN := $(VENV)/bin

.DEFAULT_GOAL := help

.PHONY: help
help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
	  sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-16s\033[0m %s\n", $$1, $$2}'

$(VENV): ## Create the main virtual environment (Python 3.13)
	$(PY) -m venv $(VENV)
	$(BIN)/python -m pip install --upgrade pip

.PHONY: setup
setup: $(VENV) ## Create venv + install the core stack (Qiskit, PennyLane, Streamlit…)
	$(BIN)/pip install -r requirements/core.txt
	$(BIN)/pip check
	@echo "\n✅ Setup complete. Try:  make check   then   make ui"

.PHONY: check
check: ## Token-free smoke test: run a Bell state on the Aer simulator
	$(BIN)/python -m quantumlab.setup_check

.PHONY: ui
ui: ## Launch the adaptive Streamlit Quantum Lab UI
	$(BIN)/streamlit run app/Home.py

.PHONY: lab
lab: ## Launch JupyterLab for the notebooks
	$(BIN)/jupyter lab

.PHONY: test
test: ## Run the pytest suite
	$(BIN)/pytest -q

.PHONY: venv-cirq
venv-cirq: ## Create the isolated Google Cirq environment (.venv-cirq)
	$(PY) -m venv .venv-cirq && .venv-cirq/bin/pip install --upgrade pip && \
	  .venv-cirq/bin/pip install -r requirements/cirq.txt && .venv-cirq/bin/pip check

.PHONY: venv-dwave
venv-dwave: ## Create the isolated D-Wave Ocean environment (.venv-dwave)
	$(PY) -m venv .venv-dwave && .venv-dwave/bin/pip install --upgrade pip && \
	  .venv-dwave/bin/pip install -r requirements/dwave.txt && .venv-dwave/bin/pip check

.PHONY: venv-braket
venv-braket: ## Create the isolated AWS Braket environment (.venv-braket)
	$(PY) -m venv .venv-braket && .venv-braket/bin/pip install --upgrade pip && \
	  .venv-braket/bin/pip install -r requirements/braket.txt && .venv-braket/bin/pip check

.PHONY: clean
clean: ## Remove caches (keeps venvs)
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	rm -rf .pytest_cache
