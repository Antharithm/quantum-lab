"""Central configuration: paths and credentials.

Everything that needs to know "where do files live?" or "do we have an IBM
token?" asks this module, so there is a single source of truth.
"""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

# Repo root = the folder that contains this package.
ROOT = Path(__file__).resolve().parent.parent

# Load .env from the repo root if present (safe no-op if missing).
load_dotenv(ROOT / ".env")

# Where we keep local state and experiment outputs.
DATA_DIR = ROOT / "data"
RESULTS_DIR = ROOT / "experiments" / "results"
PROFILE_PATH = DATA_DIR / "profile.json"


def _ensure_dirs() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)


def env(name: str, default: str | None = None) -> str | None:
    """Read an environment variable (already populated from .env)."""
    value = os.getenv(name, default)
    # Treat empty strings in .env as "not set".
    return value if value else default


def ibm_credentials() -> dict | None:
    """Return IBM Quantum credentials if a token is configured, else None.

    Used by ``backends.py`` to decide whether real-hardware access is available.
    """
    token = env("QISKIT_IBM_TOKEN")
    if not token:
        return None
    return {
        "token": token,
        "instance": env("QISKIT_IBM_INSTANCE"),
        "channel": env("QISKIT_IBM_CHANNEL", "ibm_quantum_platform"),
    }


def has_ibm_credentials() -> bool:
    return ibm_credentials() is not None


_ensure_dirs()
