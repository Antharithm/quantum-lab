"""Adaptive experience tracking.

This is what makes the UI 'adapt to your experience'. We keep a tiny JSON file
(``data/profile.json``) recording your self-reported level, your XP, and which
lessons you've completed. The UI reads this to:

  * choose how much hand-holding to show,
  * unlock more advanced tools as you level up,
  * recommend what to learn or try next.

Nothing here is quantum-specific — it's just lightweight progress state.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field

from . import config

TIERS = ["beginner", "intermediate", "advanced"]

# XP needed to *reach* each tier (you can also self-report a starting tier).
TIER_XP = {"beginner": 0, "intermediate": 100, "advanced": 300}

# XP awarded for actions.
XP_RUN = 5            # running any circuit
XP_LESSON = 25        # completing a lesson
XP_REAL_HARDWARE = 30  # running on a real quantum computer
XP_NEW_PROVIDER = 20   # first time using a new provider


@dataclass
class Profile:
    name: str = "explorer"
    self_reported_tier: str = "beginner"
    xp: int = 0
    completed_lessons: list[str] = field(default_factory=list)
    runs: int = 0
    providers_used: list[str] = field(default_factory=list)

    @property
    def earned_tier(self) -> str:
        """Tier implied by XP alone."""
        tier = "beginner"
        for t in TIERS:
            if self.xp >= TIER_XP[t]:
                tier = t
        return tier

    @property
    def tier(self) -> str:
        """Effective tier = the higher of self-reported and XP-earned."""
        return max(
            self.self_reported_tier, self.earned_tier, key=lambda t: TIERS.index(t)
        )

    @property
    def unlocked_tiers(self) -> list[str]:
        """All tiers at or below the current effective tier."""
        return TIERS[: TIERS.index(self.tier) + 1]

    def xp_to_next_tier(self) -> int | None:
        idx = TIERS.index(self.earned_tier)
        if idx + 1 >= len(TIERS):
            return None
        return TIER_XP[TIERS[idx + 1]] - self.xp


def load() -> Profile:
    """Load the profile, creating a default one on first run."""
    if config.PROFILE_PATH.exists():
        try:
            data = json.loads(config.PROFILE_PATH.read_text())
            return Profile(**{k: v for k, v in data.items() if k in Profile.__annotations__})
        except (json.JSONDecodeError, TypeError):
            pass
    p = Profile()
    save(p)
    return p


def save(profile: Profile) -> None:
    config.PROFILE_PATH.parent.mkdir(parents=True, exist_ok=True)
    config.PROFILE_PATH.write_text(json.dumps(asdict(profile), indent=2))


def record_run(profile: Profile, provider: str = "simulator", real_hardware: bool = False) -> Profile:
    profile.runs += 1
    profile.xp += XP_RUN
    if real_hardware:
        profile.xp += XP_REAL_HARDWARE
    if provider not in profile.providers_used:
        profile.providers_used.append(provider)
        profile.xp += XP_NEW_PROVIDER
    save(profile)
    return profile


def complete_lesson(profile: Profile, lesson_id: str) -> Profile:
    if lesson_id not in profile.completed_lessons:
        profile.completed_lessons.append(lesson_id)
        profile.xp += XP_LESSON
        save(profile)
    return profile


def set_tier(profile: Profile, tier: str) -> Profile:
    if tier in TIERS:
        profile.self_reported_tier = tier
        save(profile)
    return profile
