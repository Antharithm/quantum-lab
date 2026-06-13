"""Simulator — run any circuit locally and inspect the results in detail."""

from __future__ import annotations

import streamlit as st

from components import ui

from quantumlab import circuits
from quantumlab import profile as profile_mod
from quantumlab import run, viz

st.set_page_config(page_title="Simulator", page_icon="🎛️", layout="wide")
p = ui.sidebar()
ui.page_header("🎛️ Simulator", "Run on the free local Aer simulator and look under the hood.")

gallery = circuits.all_circuits()
source = st.selectbox("Pick a circuit", list(gallery.keys()))
entry = gallery[source]
qc = entry["builder"]()

st.info(entry["blurb"])

left, right = st.columns(2)
with left:
    st.subheader("Circuit")
    st.code(viz.draw_circuit_text(qc), language="text")
    st.caption(f"Depth {qc.depth()} · {qc.num_qubits} qubits · tier: {entry['tier']}")

with right:
    st.subheader("Statevector (before measurement)")
    try:
        rows = viz.statevector_table(qc)
        st.dataframe(rows, width="stretch", hide_index=True)
        st.caption(
            "Amplitudes are the 'weights' of each possible outcome; probability = "
            "|amplitude|². Measuring picks one outcome at random by these probabilities."
        )
    except Exception as e:  # noqa: BLE001
        st.caption(f"(Statevector unavailable for this circuit: {e})")

st.divider()
shots = st.select_slider("Shots (how many times to run)", [128, 256, 512, 1024, 2048, 4096], value=1024)
if st.button("▶️ Run", type="primary"):
    result = run.run_circuit(qc, shots=shots, save=True, note=f"simulator: {source}")
    profile_mod.record_run(p, provider="simulator")
    ui.refresh_profile()
    st.plotly_chart(viz.counts_bar(result.counts, f"{source} — {shots} shots"), width="stretch")
    cols = st.columns(2)
    cols[0].dataframe(
        [{"outcome": k, "count": v, "probability": round(v / shots, 3)} for k, v in sorted(result.counts.items())],
        hide_index=True,
        width="stretch",
    )
    cols[1].success(f"Saved to experiment log · +5 XP\nBackend: {result.backend}")
