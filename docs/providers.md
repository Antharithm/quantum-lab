# Providers & credentials

How to connect each quantum platform. **You need none of these to start** — every
provider has a free local simulator. Tokens are only for real hardware.

Copy the template first:

```bash
cp .env.example .env
```

---

## IBM Quantum  ·  gate-based  ·  **FREE real hardware** ✅
The easiest place to run on a real quantum computer.

1. Sign up at <https://quantum.cloud.ibm.com>.
2. Create an **API key** and copy your **instance CRN** from the dashboard.
3. In `.env`:
   ```
   QISKIT_IBM_TOKEN=your_api_key
   QISKIT_IBM_INSTANCE=your_instance_crn
   QISKIT_IBM_CHANNEL=ibm_quantum_platform
   ```
4. Use it in the app: **Backends** page. Or in code:
   ```python
   from quantumlab import backends
   print(backends.list_ibm_backends())
   ```
- Environment: main `.venv` (already installed).
- Free Open plan: a limited amount of QPU time per month — plenty for learning.

---

## Google Cirq  ·  gate-based  ·  local sim only (publicly)
1. `make venv-cirq`
2. The local simulator needs nothing:
   ```python
   import cirq
   q = cirq.LineQubit.range(2)
   c = cirq.Circuit(cirq.H(q[0]), cirq.CNOT(q[0], q[1]), cirq.measure(*q))
   print(cirq.Simulator().run(c, repetitions=100).histogram(key='0,1'))
   ```
- Google's own QPUs aren't openly available. Third-party hardware (IonQ, AQT…) via
  `cirq` plugins needs their own paid accounts.

---

## D-Wave Ocean  ·  quantum **annealing** (optimization)  ·  free tier ✅
A different paradigm: you describe a problem as an energy landscape (QUBO/Ising)
and the annealer finds low-energy = good solutions.

1. `make venv-dwave`
2. Local classical samplers work with no account. For real QPUs, sign up at
   <https://cloud.dwavesys.com/leap> and set `DWAVE_API_TOKEN` in `.env`
   (or run `dwave auth login`).
3. Example (local, no account):
   ```python
   import dimod
   bqm = dimod.BinaryQuadraticModel({'a': -1, 'b': -1}, {('a', 'b'): 2}, 0, dimod.BINARY)
   print(dimod.ExactSolver().sample(bqm).first)
   ```

---

## AWS Braket  ·  multi-vendor hardware  ·  ⚠️ **real devices cost money**
**There is no free hardware tier.** Only `LocalSimulator()` is free. Real QPUs and
managed cloud simulators bill per task and per shot — set a budget before using them.

1. `make venv-braket`
2. Configure AWS credentials (`aws configure` or `AWS_ACCESS_KEY_ID` /
   `AWS_SECRET_ACCESS_KEY` / `AWS_DEFAULT_REGION` in `.env`).
3. Free local example:
   ```python
   from braket.circuits import Circuit
   from braket.devices import LocalSimulator
   c = Circuit().h(0).cnot(0, 1)
   print(LocalSimulator().run(c, shots=100).result().measurement_counts)
   ```

---

## PennyLane  ·  quantum machine learning  ·  local by default
Already installed in the main `.venv`. Best for hybrid quantum-classical ML.

```python
import pennylane as qml
dev = qml.device("default.qubit", wires=2)
@qml.qnode(dev)
def circuit():
    qml.Hadamard(0); qml.CNOT(wires=[0, 1])
    return qml.probs(wires=[0, 1])
print(circuit())
```
The `pennylane-qiskit` plugin (installed) lets you run PennyLane on Aer/IBM devices.

---

### Security reminder
`.env` is gitignored. **Never commit real tokens.** If you ever paste one into a
file that gets committed, rotate (regenerate) it immediately.
