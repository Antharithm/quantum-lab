# Learning Roadmap

A suggested path from zero to running real experiments. The app's **Learn** page
mirrors this and unlocks content as you earn XP.

## 🌱 Stage 1 — Foundations (beginner)
**Goal:** understand qubits, superposition, and entanglement by *seeing* them.
1. Read `docs/GLOSSARY.md` (10 min).
2. App → **Learn → What is a qubit?** Run the superposition circuit.
3. App → **Learn → Entanglement & the Bell state.**
4. App → **Circuit Builder**: build H on q0, then CX q0→q1. Run it. You made a Bell state.
5. Notebook: `notebooks/01_hello_qubit.ipynb`.

✅ You can explain what a qubit is and why a Bell state only gives 00/11.

## 🚀 Stage 2 — First algorithms (intermediate)
**Goal:** see real quantum advantage and how circuits encode logic.
1. App → **Algorithm Gallery**: run **Deutsch–Jozsa** (try both oracles).
2. App → **Algorithm Gallery**: run **Grover search**; watch |11> get amplified.
3. Notebook: `notebooks/03_grover_intro.ipynb` — tweak the oracle.
4. Concept: *interference* — why negative amplitudes make wrong answers cancel.

✅ You understand how superposition + interference beat brute force.

## 🛰️ Stage 3 — Real hardware & noise (advanced)
**Goal:** run on an actual quantum computer and reason about noise.
1. Make a free IBM account, add your token to `.env` (see `docs/providers.md`).
2. App → **Backends**: run a Bell state on a real device.
3. App → **Experiments**: compare the real-hardware histogram vs. the simulator.
   Notice the 01/10 noise that "shouldn't" exist.
4. Concept: transpilation, qubit connectivity, and error.

✅ You ran a program on real quantum hardware and can explain why it's noisy.

## 🌌 Stage 4 — Branch out (your interests)
Pick what excites you — each has its own environment (`make venv-...`):
- **Optimization** → D-Wave Ocean (`make venv-dwave`). Express a problem as a QUBO
  and anneal it. Great for scheduling, routing, portfolios.
- **Quantum machine learning** → PennyLane (already installed). Build a variational
  quantum classifier; train it with gradients.
- **Chemistry** → VQE to estimate a molecule's ground-state energy.
- **Other hardware** → Google Cirq (`make venv-cirq`), AWS Braket (`make venv-braket`,
  ⚠️ real devices cost money).

## 🛠️ Stage 5 — Build something
Turn an experiment into a tool: a script in `scripts/`, a new page in `app/`, or a
new reusable circuit in `quantumlab/circuits.py`. Log results in **Experiments** and
iterate. This is where your prototype becomes a real use case.
