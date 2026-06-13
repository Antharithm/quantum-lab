# Quantum Glossary (plain language)

A friendly reference. No equations required.

- **Qubit** — the quantum version of a bit. Unlike a bit (0 or 1), a qubit can be
  in a *superposition* — a blend of 0 and 1 at once.
- **Superposition** — a qubit holding a weighted combination of 0 and 1. You only
  ever *see* 0 or 1 when you measure; the weights set the odds.
- **Measurement** — looking at a qubit. This "collapses" its superposition to a
  definite 0 or 1, at random, according to its probabilities.
- **Amplitude** — the (possibly negative or complex) weight of an outcome. Its
  size squared is the probability. Negative amplitudes let outcomes *cancel*
  (interference) — the secret sauce of quantum speedups.
- **Entanglement** — two or more qubits sharing a single combined state, so their
  measurement results are correlated even when separated. (Einstein: "spooky action".)
- **Gate** — an operation on qubits, like a logic gate but reversible. Examples:
  - **H (Hadamard)** — creates an equal superposition (a quantum coin flip).
  - **X** — the NOT gate (flips 0↔1).
  - **Z** — flips the *phase* (sign) of the |1⟩ part.
  - **CX / CNOT** — flips a target qubit *if* a control qubit is 1; makes entanglement.
  - **RX/RY/RZ** — rotate a qubit by an angle (fine-grained control).
- **Circuit** — a sequence of gates applied to qubits, ending (usually) in measurement.
- **Shots** — how many times you run a circuit. Because results are probabilistic,
  you run many shots and look at the distribution.
- **Statevector** — the full mathematical description of all qubits before measuring.
  A simulator can show it; real hardware cannot (measuring destroys it).
- **Bloch sphere** — a globe picture of a single qubit's state.
- **Backend** — where a circuit runs: a *simulator* (software) or a real *QPU*.
- **QPU** — Quantum Processing Unit: the actual quantum chip.
- **Transpilation** — rewriting your circuit into the specific gates a given device
  physically supports.
- **Noise / decoherence** — real qubits make errors and lose their state over time.
  This is why real-hardware results look "fuzzier" than the simulator's.
- **NISQ** — "Noisy Intermediate-Scale Quantum": today's era of small, noisy devices.

## Two big paradigms
- **Gate-based / circuit model** — build circuits of gates (IBM Qiskit, Google Cirq,
  AWS Braket, PennyLane). General-purpose.
- **Quantum annealing** — encode a problem's "cost" as energy and let the machine
  settle into a low-energy (good) solution (D-Wave). Specialized for optimization.

## Algorithms you'll meet
- **Bell / GHZ states** — the simplest entanglement demos.
- **Deutsch–Jozsa** — first clear quantum advantage (toy problem).
- **Grover's search** — find an item in ~√N steps instead of N.
- **Shor's algorithm** — factor large numbers fast (the one that worries cryptographers).
- **QAOA / VQE** — hybrid quantum-classical methods for optimization and chemistry.
