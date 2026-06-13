"""The learning curriculum that powers the adaptive 'Learn' page.

Each lesson is small: a concept, a plain-language explanation, and (usually) a
circuit from ``circuits.py`` you can run to see it for real. The UI shows
lessons matching your tier and recommends the next unfinished one.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Lesson:
    id: str
    title: str
    tier: str
    concept: str          # one-line "what you'll learn"
    explanation: str      # a short beginner-friendly paragraph
    circuit: str | None   # key into circuits.GALLERY, or None


LESSONS: list[Lesson] = [
    Lesson(
        id="qubit",
        title="What is a qubit?",
        tier="beginner",
        concept="Qubits can be 0, 1, or a blend of both (superposition).",
        explanation=(
            "A classical bit is either 0 or 1. A qubit can be in a *superposition* — "
            "a weighted combination of 0 and 1 at the same time. You never see the "
            "superposition directly: when you measure, it randomly collapses to 0 or 1 "
            "with probabilities set by those weights. The Hadamard (H) gate creates an "
            "equal 50/50 superposition — a perfect quantum coin flip."
        ),
        circuit="Single qubit superposition",
    ),
    Lesson(
        id="entanglement",
        title="Entanglement & the Bell state",
        tier="beginner",
        concept="Two qubits can be linked so their results are always correlated.",
        explanation=(
            "Entanglement is the 'spooky' link Einstein worried about. Put one qubit in "
            "superposition, then use a CNOT (CX) gate to tie a second qubit to it. Now "
            "they share a single combined state: measure one and you instantly know the "
            "other. The Bell state only ever gives 00 or 11 — never 01 or 10."
        ),
        circuit="Bell state (entanglement)",
    ),
    Lesson(
        id="ghz",
        title="Scaling up: the GHZ state",
        tier="beginner",
        concept="Entanglement isn't limited to two qubits.",
        explanation=(
            "The GHZ state entangles three (or more) qubits at once. All of them are "
            "perfectly correlated: you'll only see all-zeros or all-ones. It's a building "
            "block for quantum error correction and tests of quantum mechanics."
        ),
        circuit="GHZ state (3-qubit entanglement)",
    ),
    Lesson(
        id="deutsch-jozsa",
        title="A first quantum speedup: Deutsch–Jozsa",
        tier="intermediate",
        concept="Quantum parallelism can answer some questions in one query.",
        explanation=(
            "Imagine a hidden function that's either 'constant' (same answer always) or "
            "'balanced' (half 0s, half 1s). Classically you might need many checks. "
            "Deutsch–Jozsa decides it with a *single* evaluation by querying all inputs "
            "in superposition at once, then using interference to read off the answer: "
            "all-zeros means constant, anything else means balanced."
        ),
        circuit="Deutsch–Jozsa",
    ),
    Lesson(
        id="grover",
        title="Quantum search: Grover's algorithm",
        tier="intermediate",
        concept="Find a needle in a haystack quadratically faster.",
        explanation=(
            "To search N unsorted items classically you check ~N of them. Grover's "
            "algorithm needs only about √N steps. It works by 'marking' the answer with "
            "a phase flip (the oracle), then 'amplifying' its probability (the diffuser) "
            "so it's very likely to be measured. Here we amplify the |11> state."
        ),
        circuit="Grover search (2 qubits)",
    ),
    Lesson(
        id="teleportation",
        title="Quantum teleportation",
        tier="advanced",
        concept="Move a quantum state using entanglement + classical bits.",
        explanation=(
            "Teleportation transfers a qubit's exact state to a distant qubit. It uses a "
            "shared entangled pair and two classical bits of communication. Nothing "
            "travels faster than light and the original state is destroyed (no cloning). "
            "It's foundational for quantum networks and distributed quantum computing."
        ),
        circuit="Quantum teleportation",
    ),
]


def by_id(lesson_id: str) -> Lesson | None:
    return next((l for l in LESSONS if l.id == lesson_id), None)


def for_tiers(tiers: list[str]) -> list[Lesson]:
    """Lessons available for the given unlocked tiers."""
    return [l for l in LESSONS if l.tier in tiers]


def next_recommended(completed: list[str], tiers: list[str]) -> Lesson | None:
    """First unlocked, not-yet-completed lesson — what to do next."""
    for lesson in for_tiers(tiers):
        if lesson.id not in completed:
            return lesson
    return None
