"""Circuit Builder — assemble a quantum circuit gate by gate."""

from __future__ import annotations

import math

import streamlit as st
from qiskit import QuantumCircuit

from components import ui

from quantumlab import profile as profile_mod
from quantumlab import run, viz

st.set_page_config(page_title="Circuit Builder", page_icon="🛠️", layout="wide")
p = ui.sidebar()
ui.page_header("🛠️ Circuit Builder", "Add gates one at a time, then run it.")

# Each gate: name, how many qubits it needs, whether it takes an angle.
GATES = {
    "H (Hadamard — superposition)": ("h", 1, False),
    "X (NOT / bit flip)": ("x", 1, False),
    "Y": ("y", 1, False),
    "Z (phase flip)": ("z", 1, False),
    "S": ("s", 1, False),
    "T": ("t", 1, False),
    "RX (rotate, angle)": ("rx", 1, True),
    "RY (rotate, angle)": ("ry", 1, True),
    "RZ (rotate, angle)": ("rz", 1, True),
    "CX (CNOT — entangle)": ("cx", 2, False),
    "CZ (controlled-Z)": ("cz", 2, False),
}

st.session_state.setdefault("builder_ops", [])
st.session_state.setdefault("builder_nqubits", 2)


def build_circuit(n: int, ops: list[dict], measure: bool) -> QuantumCircuit:
    qc = QuantumCircuit(n, n, name="MyCircuit")
    for op in ops:
        gate, qubits, angle = op["gate"], op["qubits"], op.get("angle")
        method = getattr(qc, gate)
        if angle is not None:
            method(angle, *qubits)
        else:
            method(*qubits)
    if measure:
        qc.measure(range(n), range(n))
    return qc


# --- Configure size ----------------------------------------------------------
top = st.columns([1, 1, 2])
n = top[0].number_input("Qubits", 1, 6, st.session_state.builder_nqubits)
if n != st.session_state.builder_nqubits:
    st.session_state.builder_nqubits = n
    # Drop ops that reference now-missing qubits.
    st.session_state.builder_ops = [
        o for o in st.session_state.builder_ops if all(q < n for q in o["qubits"])
    ]
if top[1].button("🗑️ Clear", width="stretch"):
    st.session_state.builder_ops = []
    st.rerun()

# --- Add a gate --------------------------------------------------------------
st.subheader("Add a gate")
with st.form("add_gate", clear_on_submit=True):
    cols = st.columns([3, 1, 1, 1])
    label = cols[0].selectbox("Gate", list(GATES.keys()))
    gate, n_qubits, takes_angle = GATES[label]
    q0 = cols[1].selectbox("Qubit", list(range(n)), key="q0")
    q1 = None
    if n_qubits == 2:
        q1 = cols[2].selectbox("Target", list(range(n)), key="q1")
    angle = None
    if takes_angle:
        deg = cols[3].slider("Angle°", 0, 360, 90)
        angle = math.radians(deg)
    if st.form_submit_button("➕ Add gate", width="stretch"):
        qubits = [q0] if n_qubits == 1 else [q0, q1]
        if n_qubits == 2 and q0 == q1:
            st.warning("Control and target must be different qubits.")
        else:
            st.session_state.builder_ops.append(
                {"gate": gate, "qubits": qubits, "angle": angle, "label": label}
            )
            st.rerun()

# --- Show current program ----------------------------------------------------
ops = st.session_state.builder_ops
st.subheader("Your circuit")
if not ops:
    st.caption("No gates yet. Tip: add **H** on q0, then **CX** q0→q1 to make a Bell state.")
else:
    for i, op in enumerate(ops):
        c = st.columns([6, 1])
        ang = f"  ({math.degrees(op['angle']):.0f}°)" if op["angle"] is not None else ""
        c[0].write(f"{i + 1}. **{op['gate'].upper()}** on q{op['qubits']}{ang}")
        if c[1].button("✕", key=f"del{i}"):
            st.session_state.builder_ops.pop(i)
            st.rerun()

qc = build_circuit(n, ops, measure=True)
st.code(viz.draw_circuit_text(qc), language="text")
st.caption(f"Depth: {qc.depth()} · Qubits: {qc.num_qubits}")

# --- Run ---------------------------------------------------------------------
st.divider()
run_cols = st.columns([1, 1, 3])
shots = run_cols[1].select_slider("Shots", [128, 256, 512, 1024, 2048, 4096], value=1024)
if run_cols[0].button("▶️ Run on simulator", type="primary", width="stretch", disabled=not ops):
    result = run.run_circuit(qc, shots=shots, save=True, note="circuit builder")
    profile_mod.record_run(p, provider="simulator")
    ui.refresh_profile()
    st.session_state["active_circuit_counts"] = result.counts
    st.plotly_chart(viz.counts_bar(result.counts, "Results"), width="stretch")
    st.success(f"Ran on {result.backend}. Saved to your experiment log. +5 XP")
