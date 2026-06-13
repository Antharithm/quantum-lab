"""Backends — connect to real IBM quantum computers."""

from __future__ import annotations

import streamlit as st

from components import ui

from quantumlab import backends, circuits, config
from quantumlab import profile as profile_mod
from quantumlab import run, viz

st.set_page_config(page_title="Backends", page_icon="🖥️", layout="wide")
p = ui.sidebar()
ui.page_header("🖥️ Backends", "Run on genuine quantum hardware (IBM Quantum).")

if not config.has_ibm_credentials():
    st.warning("No IBM credentials found — you're in **local simulator only** mode.")
    st.markdown(
        """
        ### Connect a real quantum computer (free)
        1. Create a free account at **https://quantum.cloud.ibm.com**
        2. Generate an **API key** and copy your **instance CRN**
        3. In the project root: `cp .env.example .env`
        4. Fill in `QISKIT_IBM_TOKEN` and `QISKIT_IBM_INSTANCE`
        5. Restart the app (`make ui`)

        The free Open plan gives you a limited amount of real-QPU time per month —
        plenty for learning. Everything else here works without it.
        """
    )
    st.stop()

st.success("Connected to IBM Quantum.")

with st.spinner("Fetching available backends…"):
    devices = backends.list_ibm_backends(min_qubits=1)

if not devices:
    st.error("Connected, but no backends were returned. Check your instance/plan.")
    st.stop()

st.subheader("Available devices")
st.dataframe(devices, width="stretch", hide_index=True)

real = [d for d in devices if "simulator" not in d["name"].lower()]
if real:
    busy_sorted = sorted(real, key=lambda d: d.get("pending_jobs") or 0)
    suggested = busy_sorted[0]["name"]
    st.caption(f"💡 Least busy real device right now: **{suggested}**")
else:
    suggested = devices[0]["name"]

st.divider()
st.subheader("Run a Bell state on hardware")
st.info(
    "Real devices have a queue — your job may take from seconds to several minutes. "
    "This will use a small amount of your free QPU time.",
    icon="⏳",
)
choice = st.selectbox("Device", [d["name"] for d in devices], index=[d["name"] for d in devices].index(suggested))
shots = st.select_slider("Shots", [256, 512, 1024, 4096], value=1024)

if st.button("🚀 Submit to hardware", type="primary"):
    with st.spinner(f"Running on {choice} — waiting in the queue…"):
        try:
            result = run.run_circuit(circuits.bell_state(), shots=shots, backend=choice, note="real hardware")
            profile_mod.record_run(p, provider=choice, real_hardware=True)
            ui.refresh_profile()
            st.balloons()
            st.plotly_chart(viz.counts_bar(result.counts, f"Bell on {choice}"), width="stretch")
            st.success("🎉 You just ran a program on a real quantum computer! +35 XP")
            st.caption(
                "Notice the small amount of 01/10 noise — real qubits aren't perfect. "
                "That's the difference from the clean simulator."
            )
        except Exception as e:  # noqa: BLE001
            st.error(f"Job failed: {e}")
