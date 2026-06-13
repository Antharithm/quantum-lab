---
name: explain-concept
description: Explain a quantum computing concept in beginner-friendly terms, then show a tiny runnable demo using this repo's quantumlab package. Use when the user asks "what is X", "how does X work", or "explain X" about quantum computing (qubits, superposition, entanglement, gates, algorithms, noise, annealing, etc.).
---

# Explain a quantum concept

Goal: teach one concept clearly to a curious beginner, then prove it with code they
can run in this repo.

## Steps
1. **Explain plainly first.** 2–4 short paragraphs, no equations unless asked. Use an
   analogy. Define any jargon inline. Match the depth to the user's level if known.
2. **Connect it to the repo.** Point to the relevant place:
   - Concepts & terms: `docs/GLOSSARY.md`
   - Canonical circuits: `quantumlab/circuits.py` (Bell, GHZ, Grover, teleportation…)
   - Lessons: `quantumlab/curriculum.py` and the app's **Learn** page
3. **Show a tiny demo.** Prefer reusing existing helpers:
   ```python
   from quantumlab import circuits, run, viz
   qc = circuits.bell_state()          # or build a minimal QuantumCircuit
   print(qc.draw(output="text"))
   print(run.run_circuit(qc, shots=1024, save=False).counts)
   ```
   Only write a new circuit if no gallery entry fits.
4. **Offer to run it.** Suggest `make check`, the relevant notebook in `notebooks/`,
   or the matching app page. If asked, run it with `.venv/bin/python`.
5. **End with one "try this" tweak** so they learn by experimenting.

## Style
- Encouraging and concrete. Celebrate the "aha".
- Never dump math walls. Build intuition first; offer depth on request.
- Always tie back to something they can actually run here.
