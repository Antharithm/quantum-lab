"""Smoke tests: every gallery circuit should build and run on the simulator."""

import pytest

from quantumlab import circuits, run


def test_bell_is_correlated():
    result = run.run_circuit(circuits.bell_state(), shots=512, save=False)
    # Only correlated outcomes should appear.
    assert set(result.counts) <= {"00", "11"}
    assert result.shots == 512


@pytest.mark.parametrize("name", list(circuits.all_circuits().keys()))
def test_gallery_circuit_runs(name):
    builder = circuits.all_circuits()[name]["builder"]
    qc = builder()
    result = run.run_circuit(qc, shots=256, save=False)
    assert sum(result.counts.values()) == 256
    assert result.depth >= 1


def test_grover_amplifies_target():
    # Grover should make |11> the most likely outcome.
    result = run.run_circuit(circuits.grover_2q(), shots=1024, save=False)
    top = max(result.counts, key=result.counts.get)
    assert top == "11"


def test_experiment_logging(tmp_path, monkeypatch):
    from quantumlab import config

    monkeypatch.setattr(config, "RESULTS_DIR", tmp_path)
    monkeypatch.setattr(run.config, "RESULTS_DIR", tmp_path)
    run.run_circuit(circuits.bell_state(), shots=128, save=True, note="test")
    saved = list(tmp_path.glob("*.json"))
    assert len(saved) == 1
