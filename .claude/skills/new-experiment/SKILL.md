---
name: new-experiment
description: Scaffold a new, self-contained quantum experiment script under experiments/ that runs via the quantumlab package and logs its results. Use when the user wants to start a new experiment, test an idea/hypothesis, or compare backends/parameters.
---

# Scaffold a new experiment

Goal: create a runnable experiment script that records its results so the user builds
a research log over time.

## Steps
1. **Clarify the idea** in one line if unclear (what circuit, what is being varied,
   what outcome are we looking for?).
2. **Create** `experiments/<short_slug>.py` following this template:
   ```python
   """Experiment: <one-line description>.

   Hypothesis: <what you expect to see and why>.
   """
   from quantumlab import circuits, run, viz

   def build():
       # Return the QuantumCircuit under test (reuse circuits.py where possible).
       return circuits.bell_state()

   def main():
       qc = build()
       print(qc.draw(output="text"))
       result = run.run_circuit(qc, shots=1024, note="<slug>")
       print("counts:", result.counts)
       print("saved run_id:", result.run_id)
       # Add analysis here: compare to expectation, sweep a parameter, etc.

   if __name__ == "__main__":
       main()
   ```
3. **Run it:** `.venv/bin/python experiments/<slug>.py`. Results auto-save to
   `experiments/results/` and appear in the app's **Experiments** page.
4. **Report** what was observed vs. the hypothesis, and suggest the next variation
   (e.g., more shots, real hardware, a tweaked gate/angle).

## Conventions
- Reuse `quantumlab.circuits` builders when possible; only write new circuit code when
  needed, and consider promoting reusable circuits into `quantumlab/circuits.py`.
- Always pass a `note=` so the experiment is identifiable in the log.
- For parameter sweeps, loop and call `run.run_circuit(...)` per setting.
