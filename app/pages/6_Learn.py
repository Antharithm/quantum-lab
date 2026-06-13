"""Learn — adaptive lessons that unlock as you grow."""

from __future__ import annotations

import streamlit as st

from components import ui

from quantumlab import circuits, curriculum
from quantumlab import profile as profile_mod
from quantumlab import run, viz

st.set_page_config(page_title="Learn", page_icon="📚", layout="wide")
p = ui.sidebar()
ui.page_header("📚 Learn", "Bite-size lessons. Complete them to earn XP and unlock more.")

# Progress overview
all_lessons = curriculum.LESSONS
done = set(p.completed_lessons)
st.progress(len(done) / len(all_lessons), text=f"{len(done)} / {len(all_lessons)} lessons complete")

nxt = curriculum.next_recommended(p.completed_lessons, p.unlocked_tiers)
if nxt:
    st.caption(f"🎯 Recommended next: **{nxt.title}**")

st.divider()

for lesson in all_lessons:
    locked = ui.tier_locked(p, lesson.tier)
    completed = lesson.id in done
    icon = "✅" if completed else ("🔒" if locked else ui.TIER_EMOJI[lesson.tier])
    with st.expander(f"{icon} {lesson.title}  ·  _{lesson.tier}_", expanded=(lesson is nxt)):
        st.markdown(f"**{lesson.concept}**")
        if locked:
            ui.lock_notice(lesson.tier)
            continue
        st.write(lesson.explanation)

        if lesson.circuit and lesson.circuit in circuits.all_circuits():
            qc = circuits.all_circuits()[lesson.circuit]["builder"]()
            st.code(viz.draw_circuit_text(qc), language="text")
            cols = st.columns([1, 1, 2])
            if cols[0].button("▶️ Try it", key=f"try_{lesson.id}", type="primary"):
                result = run.run_circuit(qc, shots=1024, save=True, note=f"lesson: {lesson.id}")
                profile_mod.record_run(p, provider="simulator")
                ui.refresh_profile()
                st.plotly_chart(
                    viz.counts_bar(result.counts, lesson.title),
                    width="stretch",
                    key=f"chart_{lesson.id}",
                )
            if not completed:
                if cols[1].button("✔️ Mark complete", key=f"done_{lesson.id}"):
                    profile_mod.complete_lesson(p, lesson.id)
                    ui.refresh_profile()
                    st.success("Lesson complete! +25 XP")
                    st.rerun()
            else:
                cols[1].caption("Completed ✅")
