"""A library of canonical quantum circuits.

Each function returns a Qiskit ``QuantumCircuit`` you can run on the simulator
or real hardware. These are the classics every quantum learner meets first —
read the docstrings as mini-lessons.

All circuits include measurements unless noted, so they're ready to ``run``.
"""

from __future__ import annotations

import math

from qiskit import QuantumCircuit

# A registry the UI uses to populate the Algorithm Gallery. Each entry maps a
# friendly name to (builder, one-line explanation, difficulty tier).
GALLERY: dict[str, dict] = {}


def _register(name: str, blurb: str, tier: str):
    def deco(fn):
        GALLERY[name] = {"builder": fn, "blurb": blurb, "tier": tier}
        return fn
    return deco


@_register(
    "Bell state (entanglement)",
    "Two qubits become correlated: measuring one instantly tells you the other. "
    "You'll only ever see 00 or 11 — never 01 or 10.",
    "beginner",
)
def bell_state() -> QuantumCircuit:
    """The simplest entangled pair. H on q0 creates superposition; CX entangles."""
    qc = QuantumCircuit(2, 2, name="Bell")
    qc.h(0)
    qc.cx(0, 1)
    qc.measure([0, 1], [0, 1])
    return qc


@_register(
    "Single qubit superposition",
    "One Hadamard gate puts a qubit in an equal mix of 0 and 1 — a fair coin "
    "that only 'lands' when measured.",
    "beginner",
)
def superposition() -> QuantumCircuit:
    qc = QuantumCircuit(1, 1, name="Superposition")
    qc.h(0)
    qc.measure(0, 0)
    return qc


@_register(
    "GHZ state (3-qubit entanglement)",
    "Entanglement across three qubits at once: results are always 000 or 111.",
    "beginner",
)
def ghz_state(n: int = 3) -> QuantumCircuit:
    qc = QuantumCircuit(n, n, name="GHZ")
    qc.h(0)
    for q in range(1, n):
        qc.cx(0, q)
    qc.measure(range(n), range(n))
    return qc


@_register(
    "Deutsch–Jozsa",
    "The first algorithm to beat classical computers: decides if a hidden "
    "function is constant or balanced in ONE query instead of many.",
    "intermediate",
)
def deutsch_jozsa(oracle: str = "balanced", n: int = 3) -> QuantumCircuit:
    """Determine in one shot whether an oracle is constant or balanced.

    A constant oracle always returns the same bit; a balanced one returns 0 for
    half the inputs and 1 for the other half. Outcome all-zeros => constant.
    """
    qc = QuantumCircuit(n + 1, n, name=f"DJ-{oracle}")
    qc.x(n)                      # ancilla in |1>
    qc.h(range(n + 1))           # superposition over all inputs
    if oracle == "balanced":     # a simple balanced oracle: CX from each input
        for q in range(n):
            qc.cx(q, n)
    # constant oracle => do nothing (f(x)=0)
    qc.h(range(n))
    qc.measure(range(n), range(n))
    return qc


@_register(
    "Grover search (2 qubits)",
    "Quantum search: finds a 'marked' item in an unsorted set far faster than "
    "checking one by one. Here it amplifies the |11> answer.",
    "intermediate",
)
def grover_2q() -> QuantumCircuit:
    """Grover's algorithm searching for |11> among 4 possibilities."""
    qc = QuantumCircuit(2, 2, name="Grover")
    qc.h([0, 1])                 # uniform superposition
    # Oracle: flip the phase of |11>
    qc.cz(0, 1)
    # Diffuser (amplitude amplification about the mean)
    qc.h([0, 1])
    qc.x([0, 1])
    qc.cz(0, 1)
    qc.x([0, 1])
    qc.h([0, 1])
    qc.measure([0, 1], [0, 1])
    return qc


@_register(
    "Quantum teleportation",
    "Transfers a qubit's state to another qubit using entanglement + 2 classical "
    "bits. The state moves; no qubit physically travels.",
    "advanced",
)
def teleportation() -> QuantumCircuit:
    """Teleport the state of q0 onto q2.

    q0 = state to send, q1+q2 = a shared Bell pair. We prepare q0 with a small
    rotation (ry(pi/4)) so its state is mostly |0> with a bit of |1>. After
    teleportation, q2 should show that same ~85% / ~15% split.

    We use *controlled* corrections (cx, cz) instead of mid-circuit measurement
    + classical control. By the deferred-measurement principle these are
    equivalent, and it keeps the circuit portable across simulators.
    """
    qc = QuantumCircuit(3, 1, name="Teleport")
    # Prepare the state to send on q0.
    qc.ry(math.pi / 4, 0)
    qc.barrier()
    # Entangle q1 and q2 into a Bell pair (q2 is the destination).
    qc.h(1)
    qc.cx(1, 2)
    qc.barrier()
    # "Bell measurement" basis change on q0, q1.
    qc.cx(0, 1)
    qc.h(0)
    qc.barrier()
    # Corrections on q2 (deferred form of the classically-controlled X and Z).
    qc.cx(1, 2)
    qc.cz(0, 2)
    qc.measure(2, 0)
    return qc


def all_circuits() -> dict[str, dict]:
    """Return the gallery registry (name -> {builder, blurb, tier})."""
    return GALLERY
