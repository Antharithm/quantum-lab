"""Visualization helpers — turn results into pictures.

Kept framework-light: these return Plotly figures (used by the Streamlit UI) and
matplotlib figures (used by notebooks / Qiskit's drawers).
"""

from __future__ import annotations

import plotly.graph_objects as go
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector


def counts_bar(counts: dict[str, int], title: str = "Measurement results") -> go.Figure:
    """A bar chart of measurement outcomes (a histogram), sorted by bitstring."""
    items = sorted(counts.items())
    labels = [k for k, _ in items]
    values = [v for _, v in items]
    fig = go.Figure(go.Bar(x=labels, y=values, marker_color="#6c5ce7"))
    fig.update_layout(
        title=title,
        xaxis_title="Outcome (bitstring)",
        yaxis_title="Times measured",
        bargap=0.25,
        template="plotly_white",
    )
    return fig


def statevector_table(qc: QuantumCircuit) -> list[dict]:
    """Return amplitude + probability per basis state for a (measure-free) circuit.

    Strips measurements first so we can compute the pure statevector. Returns a
    list of {state, amplitude, probability} dicts ready for a table.
    """
    clean = qc.remove_final_measurements(inplace=False) or qc
    # If there were no measurements, remove_final_measurements returns None.
    sv = Statevector.from_instruction(clean if clean is not None else qc)
    n = sv.num_qubits
    rows = []
    for i, amp in enumerate(sv.data):
        prob = abs(amp) ** 2
        if prob < 1e-9:
            continue
        rows.append(
            {
                "state": f"|{i:0{n}b}⟩",
                "amplitude": f"{amp.real:+.3f}{amp.imag:+.3f}i",
                "probability": round(prob, 4),
            }
        )
    return rows


def draw_circuit_mpl(qc: QuantumCircuit):
    """Return a matplotlib Figure of the circuit (uses pylatexenc for nice gates)."""
    return qc.draw(output="mpl", style="iqp")


def draw_circuit_text(qc: QuantumCircuit) -> str:
    """Return a plain-text rendering of the circuit (works everywhere)."""
    return str(qc.draw(output="text"))
