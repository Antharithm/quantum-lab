# CLAUDE.md — Quantum Lab

Project guide for Claude Code. Read this first.

## What this is
A personal **quantum-computing lab**: learn the field hands-on and run experiments
across IBM (Qiskit), Google (Cirq), D-Wave (Ocean), AWS Braket, and PennyLane. It has
an adaptive Streamlit UI, a reusable `quantumlab` package, learning notebooks, and docs.
The owner is new to quantum and enthusiastic — favor clarity, intuition, and runnable
demos over heavy math.

## Environment
- **Python 3.13** via Homebrew (`/opt/homebrew/bin/python3.13`). The system Python 3.9
  is too old — never use it.
- Main virtual env: **`.venv`** (Qiskit + PennyLane + Streamlit stack). Always run
  project code with `.venv/bin/python` (or `source .venv/bin/activate`).
- Provider SDKs conflict if mixed, so Cirq / D-Wave / Braket live in **separate** venvs
  (`.venv-cirq`, `.venv-dwave`, `.venv-braket`), created on demand via the Makefile.
- If a package ever rejects Python 3.13, fall back to `brew install python@3.12` and
  recreate that venv with it.

## Common commands
```bash
make setup        # create .venv + install core stack (one time)
make check        # token-free smoke test: Bell state on the Aer simulator
make ui           # launch the adaptive Streamlit dashboard
make lab          # open the notebooks in JupyterLab
make test         # run pytest
make venv-cirq    # (or venv-dwave / venv-braket) create an isolated provider env
make help         # list everything
```

## Layout
- `quantumlab/` — the reusable package (import name `quantumlab`; distribution name
  `quantum-lab`). UI, notebooks, and scripts all import this — keep logic here, not in
  the UI.
  - `config.py` paths + credentials · `circuits.py` canonical circuits (a `GALLERY`
    registry) · `run.py` run + experiment logging · `viz.py` charts/statevector ·
    `backends.py` simulator + IBM service · `profile.py` adaptive XP/level ·
    `curriculum.py` lessons · `setup_check.py` smoke test.
- `app/` — Streamlit UI. `Home.py` is the entry; `pages/` are the tools; `components/ui.py`
  holds the shared sidebar + the adaptive-experience logic.
- `notebooks/` — guided learning track (each imports `quantumlab`).
- `docs/` — `GLOSSARY.md`, `ROADMAP.md`, `providers.md` (auth + cost notes).
- `experiments/results/` — saved run logs (JSON), shown in the UI's Experiments page.
- `requirements/` — `core.txt` (main env) + per-provider files.
- `.claude/` — skills (`new-experiment`, `run-circuit`, `explain-concept`) and agents
  (`quantum-tutor`, `circuit-reviewer`, `quantum-researcher`).

## Conventions
- **Reuse `quantumlab`.** Add new circuits to `circuits.py` (register in `GALLERY`),
  run via `run.run_circuit(...)` so results get logged consistently.
- **Default to the simulator** (free, instant). Use real hardware only when asked.
- **Qiskit 2.x gotchas:** `.c_if()` is REMOVED (use controlled/deferred form or
  `qc.if_test`); `qiskit.IBMQ` is gone (use `qiskit_ibm_runtime`); Aer is
  `from qiskit_aer import AerSimulator`. Run with `transpile()` then `backend.run()`.
- **Streamlit:** use `width="stretch"` (not the deprecated `use_container_width`).
- After changing the package, run `make test`. After changing the UI, validate pages
  render (Streamlit `AppTest`) before claiming it works.

## Security & cost
- **Never commit `.env` or real tokens** (it's gitignored). If a token is ever exposed,
  tell the user to rotate it.
- **AWS Braket real devices cost money** — there is no free hardware tier. Only IBM
  offers free real-QPU time. Warn before anything that bills.

## GitHub
- Remote: `git@github.com:Antharithm/quantum-lab.git`. Commit/push only when asked.
