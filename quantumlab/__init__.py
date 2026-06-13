"""Quantum Lab — a small toolkit shared by the UI, notebooks and scripts.

The goal of this package is to give you ONE place where the quantum logic lives,
so the Streamlit app, your Jupyter notebooks, and standalone experiment scripts
all behave identically.

Typical use::

    from quantumlab import circuits, run
    qc = circuits.bell_state()
    result = run.run_circuit(qc, shots=1024)
    print(result.counts)   # -> {'00': ~512, '11': ~512}
"""

from . import backends, circuits, config, profile, run, viz  # noqa: F401

__all__ = ["backends", "circuits", "config", "profile", "run", "viz"]
__version__ = "0.1.0"
