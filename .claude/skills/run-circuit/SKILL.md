---
name: run-circuit
description: Run a quantum circuit on the simulator (or real IBM hardware) and report the results with a histogram, using this repo's quantumlab package. Use when the user wants to execute, simulate, or test a circuit, or run one of the gallery algorithms.
---

# Run a circuit

Goal: execute a circuit and clearly report what happened.

## Steps
1. **Get the circuit.** In priority order:
   - A gallery circuit: `from quantumlab import circuits; circuits.bell_state()`
     (see `circuits.GALLERY` for all keys).
   - A circuit the user described — build a minimal `qiskit.QuantumCircuit`.
   - A file/path the user points to.
2. **Run it** via the shared helper so results get logged consistently:
   ```python
   from quantumlab import run
   result = run.run_circuit(qc, shots=1024)        # backend="simulator" by default
   print(result.counts)
   ```
   For real hardware, pass `backend="<ibm_device_name>"` — requires a token in `.env`
   (check `quantumlab.config.has_ibm_credentials()` first; if absent, use the simulator
   and tell the user how to connect IBM via `docs/providers.md`).
3. **Report results.**
   - Show the counts and which outcome dominated.
   - Explain briefly whether that matches the expected behavior.
   - Mention the run was saved to `experiments/results/` (view in the app's
     **Experiments** page).
4. **Visualize when helpful:** `quantumlab.viz.counts_bar(result.counts)` (Plotly) or
   `result.probabilities`.

## Notes
- Default to the **simulator** (free, instant). Only use real hardware when explicitly
  asked — it costs queue time and is noisier.
- Use the project venv: `.venv/bin/python`.
- Keep `shots` reasonable (1024 is a good default).
