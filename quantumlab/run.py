"""Run circuits and record the results as experiments.

``run_circuit`` is the one function the UI, notebooks and scripts all call. It
returns a small ``RunResult`` and (optionally) saves a JSON record under
``experiments/results/`` so you can build up a research log over time.
"""

from __future__ import annotations

import json
import uuid
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone

from qiskit import QuantumCircuit, transpile

from . import backends, config


@dataclass
class RunResult:
    """The outcome of running one circuit."""

    counts: dict[str, int]
    shots: int
    backend: str
    circuit_name: str
    depth: int
    width: int
    timestamp: str
    run_id: str = field(default_factory=lambda: uuid.uuid4().hex[:8])

    @property
    def probabilities(self) -> dict[str, float]:
        return {k: v / self.shots for k, v in self.counts.items()}


def run_circuit(
    qc: QuantumCircuit,
    shots: int = 1024,
    backend: str = "simulator",
    save: bool = True,
    note: str = "",
) -> RunResult:
    """Run ``qc`` and return a ``RunResult``.

    Parameters
    ----------
    backend : "simulator" runs locally on Aer (default). Any other value is
        treated as the name of a real IBM backend (requires a token).
    save : when True, append a record to experiments/results/.
    """
    if backend == "simulator":
        sim = backends.simulator()
        compiled = transpile(qc, sim)
        job = sim.run(compiled, shots=shots)
        counts = job.result().get_counts()
        backend_name = "aer_simulator"
    else:
        counts, backend_name = _run_on_ibm(qc, shots, backend)

    result = RunResult(
        counts={str(k): int(v) for k, v in counts.items()},
        shots=shots,
        backend=backend_name,
        circuit_name=qc.name,
        depth=qc.depth(),
        width=qc.num_qubits,
        timestamp=datetime.now(timezone.utc).isoformat(timespec="seconds"),
    )
    if save:
        _save_experiment(result, note=note)
    return result


def _run_on_ibm(qc: QuantumCircuit, shots: int, backend_name: str):
    """Run on real IBM hardware via the Runtime SamplerV2 primitive."""
    service = backends.ibm_service()
    if service is None:
        raise RuntimeError(
            "No IBM credentials found. Add QISKIT_IBM_TOKEN to .env to use real hardware."
        )
    from qiskit_ibm_runtime import SamplerV2

    hw = service.backend(backend_name)
    compiled = transpile(qc, hw)
    sampler = SamplerV2(mode=hw)
    job = sampler.run([compiled], shots=shots)
    res = job.result()[0]
    # SamplerV2 returns bit arrays per classical register; grab the first.
    creg = next(iter(res.data.__dict__)) if hasattr(res.data, "__dict__") else "c"
    counts = res.data[creg].get_counts() if hasattr(res.data, "__getitem__") else {}
    return counts, hw.name


def _save_experiment(result: RunResult, note: str = "") -> None:
    config.RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    record = asdict(result)
    record["note"] = note
    path = config.RESULTS_DIR / f"{result.timestamp.replace(':', '-')}_{result.run_id}.json"
    path.write_text(json.dumps(record, indent=2))


def load_experiments(limit: int | None = None) -> list[dict]:
    """Load saved experiment records, newest first."""
    files = sorted(config.RESULTS_DIR.glob("*.json"), reverse=True)
    if limit:
        files = files[:limit]
    out = []
    for f in files:
        try:
            out.append(json.loads(f.read_text()))
        except (json.JSONDecodeError, OSError):
            continue
    return out
