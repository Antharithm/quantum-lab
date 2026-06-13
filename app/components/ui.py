"""Shared Streamlit helpers used across all pages.

Centralizes: import bootstrap, the page header, and the adaptive profile sidebar
that makes the whole app respond to your experience level.
"""

from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st

# --- import bootstrap -------------------------------------------------------
# `pip install -e .` normally makes `quantumlab` importable, but add the repo
# root to sys.path too so the app works even before an editable install.
ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from quantumlab import profile as profile_mod  # noqa: E402

TIER_EMOJI = {"beginner": "🌱", "intermediate": "🚀", "advanced": "🛰️"}


def get_profile() -> profile_mod.Profile:
    """Load the profile once per session and cache it in session_state."""
    if "profile" not in st.session_state:
        st.session_state.profile = profile_mod.load()
    return st.session_state.profile


def refresh_profile() -> profile_mod.Profile:
    """Reload from disk (after XP changes) and update session_state."""
    st.session_state.profile = profile_mod.load()
    return st.session_state.profile


def page_header(title: str, subtitle: str = "") -> None:
    st.title(title)
    if subtitle:
        st.caption(subtitle)


def sidebar(active_tier_note: bool = True) -> profile_mod.Profile:
    """Render the adaptive profile sidebar and return the current profile."""
    p = get_profile()
    with st.sidebar:
        st.markdown(f"### {TIER_EMOJI.get(p.tier, '🌱')} {p.name}")
        st.markdown(f"**Level:** `{p.tier}`")

        # XP progress toward the next tier.
        to_next = p.xp_to_next_tier()
        if to_next is None:
            st.progress(1.0, text=f"XP {p.xp} — max level 🛰️")
        else:
            target = p.xp + to_next
            base = profile_mod.TIER_XP[p.earned_tier]
            frac = (p.xp - base) / max(target - base, 1)
            st.progress(min(frac, 1.0), text=f"XP {p.xp} · {to_next} to next level")

        st.metric("Experiments run", p.runs)
        if p.providers_used:
            st.caption("Providers used: " + ", ".join(p.providers_used))

        st.divider()
        st.caption("Self-report your level (the app adapts what it shows):")
        choice = st.selectbox(
            "Experience level",
            profile_mod.TIERS,
            index=profile_mod.TIERS.index(p.self_reported_tier),
            label_visibility="collapsed",
        )
        if choice != p.self_reported_tier:
            profile_mod.set_tier(p, choice)
            refresh_profile()
            st.rerun()

        if active_tier_note:
            st.divider()
            st.caption(
                "Tools and lessons unlock as you gain XP by running circuits and "
                "completing lessons."
            )
    return p


def tier_locked(profile, required_tier: str) -> bool:
    """True if a feature requiring `required_tier` is still locked."""
    return required_tier not in profile.unlocked_tiers


def lock_notice(required_tier: str) -> None:
    st.info(
        f"🔒 This is an **{required_tier}** tool. Keep running circuits and finishing "
        f"lessons to unlock it — or set your level to *{required_tier}* in the sidebar.",
        icon="🔒",
    )
