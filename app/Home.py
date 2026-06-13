"""Quantum Lab — adaptive dashboard (entry point).

Run with:  streamlit run app/Home.py   (or `make ui`)
"""

from __future__ import annotations

import streamlit as st

from components import ui  # noqa: E402  (ui sets up sys.path)

from quantumlab import config, curriculum, run  # noqa: E402

st.set_page_config(page_title="Quantum Lab", page_icon="⚛️", layout="wide")

p = ui.sidebar()
ui.page_header(
    "⚛️ Quantum Lab",
    "Your personal lab for learning quantum computing and running real experiments.",
)

# --- Top row: status ---------------------------------------------------------
c1, c2, c3, c4 = st.columns(4)
c1.metric("Level", p.tier.capitalize(), help="Set in the sidebar; also rises with XP.")
c2.metric("XP", p.xp)
c3.metric("Experiments", p.runs)
c4.metric(
    "IBM hardware",
    "Connected" if config.has_ibm_credentials() else "Local only",
    help="Add QISKIT_IBM_TOKEN to .env to run on real IBM quantum computers.",
)

st.divider()

left, right = st.columns([3, 2])

# --- Recommended next lesson -------------------------------------------------
with left:
    st.subheader("🎯 Recommended next")
    nxt = curriculum.next_recommended(p.completed_lessons, p.unlocked_tiers)
    if nxt is None:
        st.success("You've completed every unlocked lesson. Level up to unlock more!")
    else:
        st.markdown(f"**{nxt.title}**  ·  _{nxt.concept}_")
        st.write(nxt.explanation)
        st.page_link("pages/6_Learn.py", label="Go to Learn →", icon="📚")

    st.subheader("🧭 What's here")
    st.markdown(
        """
        - **Circuit Builder** — drag-free gate builder; make your own circuits.
        - **Simulator** — run circuits locally (no account) and see the results.
        - **Algorithm Gallery** — famous algorithms (Bell, Grover, teleportation…).
        - **Backends** — connect to real IBM quantum computers.
        - **Experiments** — your saved run history, for research & comparison.
        - **Learn** — adaptive lessons that unlock as you grow.
        """
    )

# --- Recent experiments ------------------------------------------------------
with right:
    st.subheader("🧪 Recent experiments")
    recent = run.load_experiments(limit=5)
    if not recent:
        st.caption("No runs yet — try the Simulator or Algorithm Gallery.")
    else:
        for r in recent:
            with st.container(border=True):
                st.markdown(f"**{r['circuit_name']}** on `{r['backend']}`")
                st.caption(
                    f"{r['shots']} shots · depth {r['depth']} · {r['timestamp']}"
                )
                if r.get("counts"):
                    top = max(r["counts"], key=r["counts"].get)
                    st.caption(f"Most frequent outcome: `{top}`")

st.divider()
st.caption(
    "New to this? Start with **Learn → What is a qubit?**, then build a Bell state in "
    "the **Circuit Builder**. Everything runs on a free local simulator until you add a token."
)
