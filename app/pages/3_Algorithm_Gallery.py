"""Algorithm Gallery — explore famous quantum algorithms, adapted to your level."""

from __future__ import annotations

import streamlit as st

from components import ui

from quantumlab import circuits
from quantumlab import profile as profile_mod
from quantumlab import run, viz

st.set_page_config(page_title="Algorithm Gallery", page_icon="📐", layout="wide")
p = ui.sidebar()
ui.page_header("📐 Algorithm Gallery", "The classics — read, run, and tweak them.")

TIER_ORDER = {"beginner": 0, "intermediate": 1, "advanced": 2}
gallery = circuits.all_circuits()

show_locked = st.toggle("Show algorithms above my level", value=False)

for name, entry in sorted(gallery.items(), key=lambda kv: TIER_ORDER[kv[1]["tier"]]):
    locked = ui.tier_locked(p, entry["tier"])
    if locked and not show_locked:
        continue
    with st.expander(f"{ui.TIER_EMOJI[entry['tier']]} {name}  ·  _{entry['tier']}_", expanded=False):
        st.write(entry["blurb"])
        if locked:
            ui.lock_notice(entry["tier"])
            continue
        qc = entry["builder"]()
        st.code(viz.draw_circuit_text(qc), language="text")
        cols = st.columns([1, 1, 3])
        shots = cols[1].select_slider(
            "Shots", [256, 512, 1024, 2048], value=1024, key=f"shots_{name}"
        )
        if cols[0].button("▶️ Run", key=f"run_{name}", type="primary"):
            result = run.run_circuit(qc, shots=shots, save=True, note=f"gallery: {name}")
            profile_mod.record_run(p, provider="simulator")
            ui.refresh_profile()
            st.plotly_chart(
                viz.counts_bar(result.counts, name), width="stretch", key=f"chart_{name}"
            )
            st.success("Saved · +5 XP")
