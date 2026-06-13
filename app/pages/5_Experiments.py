"""Experiments — your saved run history, for research and comparison."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from components import ui

from quantumlab import run, viz

st.set_page_config(page_title="Experiments", page_icon="🧪", layout="wide")
ui.sidebar()
ui.page_header("🧪 Experiments", "Every run is logged here so you can compare and learn.")

records = run.load_experiments()
if not records:
    st.caption("No experiments yet. Run something in the Simulator or Algorithm Gallery.")
    st.stop()

df = pd.DataFrame(records)
view = df[["timestamp", "circuit_name", "backend", "shots", "depth", "width", "note", "run_id"]]
st.dataframe(view, width="stretch", hide_index=True)

st.divider()
st.subheader("Inspect a run")
ids = [f"{r['timestamp']} · {r['circuit_name']} ({r['run_id']})" for r in records]
pick = st.selectbox("Choose an experiment", range(len(records)), format_func=lambda i: ids[i])
chosen = records[pick]
st.plotly_chart(
    viz.counts_bar(chosen["counts"], f"{chosen['circuit_name']} on {chosen['backend']}"),
    width="stretch",
)

st.subheader("Compare two backends for the same circuit")
st.caption("Run the same circuit on the simulator and on real hardware, then compare the noise.")
names = sorted({r["circuit_name"] for r in records})
target = st.selectbox("Circuit", names)
matches = [r for r in records if r["circuit_name"] == target]
if len(matches) >= 2:
    cols = st.columns(2)
    for col, rec in zip(cols, matches[:2]):
        col.plotly_chart(
            viz.counts_bar(rec["counts"], rec["backend"]), width="stretch", key=rec["run_id"]
        )
else:
    st.caption("Only one run of this circuit so far — run it on another backend to compare.")
