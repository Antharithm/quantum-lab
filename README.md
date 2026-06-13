# ⚛️ Quantum Lab

A personal lab for **learning quantum computing** and **running experiments** on real
quantum computers — IBM (Qiskit), Google (Cirq), D-Wave (Ocean), AWS Braket, and
PennyLane — with an adaptive UI that grows with you.

> New to quantum? Perfect. Everything runs on a **free local simulator** until you
> decide to connect real hardware. Start with `make ui` and the **Learn** page.

## Quickstart

```bash
# 1. Set up the main environment (Python 3.13, Qiskit + PennyLane + Streamlit)
make setup

# 2. Confirm it works — runs a Bell state on the simulator (no account needed)
make check

# 3. Launch the adaptive dashboard
make ui
```

Then open the browser tab Streamlit prints, and:
1. **Learn → What is a qubit?** — start here.
2. **Circuit Builder** — add `H` on q0, then `CX` q0→q1, and run it. You just made
   entanglement (a Bell state).
3. **Algorithm Gallery** — run Grover's search and quantum teleportation.

Prefer notebooks? `make lab` opens the guided track in `notebooks/`.

## What's inside
- **Adaptive UI** (`app/`) — a dashboard that tracks your XP/level and unlocks tools and
  lessons as you progress. Tools: Circuit Builder, Simulator, Algorithm Gallery,
  Backends (real IBM hardware), Experiments log, and Learn.
- **`quantumlab/` package** — the shared engine (circuits, run+logging, visualization,
  backends, profile, curriculum) used by the UI, notebooks, and scripts.
- **Notebooks** (`notebooks/`) — hello-qubit → entanglement → Grover.
- **Docs** (`docs/`) — a plain-language [glossary](docs/GLOSSARY.md), a learning
  [roadmap](docs/ROADMAP.md), and [provider setup](docs/providers.md).

## Running on real quantum computers
Free with IBM:
```bash
cp .env.example .env      # then add your IBM token (see docs/providers.md)
make ui                   # → Backends page → run a Bell state on a real QPU
```
Other providers each get an isolated environment: `make venv-cirq`, `make venv-dwave`,
`make venv-braket`. ⚠️ **AWS Braket real hardware costs money** — see `docs/providers.md`.

## Project commands
Run `make help` for the full list (`setup`, `check`, `ui`, `lab`, `test`, `venv-*`).

## Status
Prototype / learning tool — built to explore the field and grow into a real use case.
See `CLAUDE.md` for the developer guide.
