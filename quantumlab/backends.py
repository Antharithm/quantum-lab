"""Where circuits actually run.

Two worlds:
  * **Local simulator** (Aer) — free, instant, no account. The default.
  * **Real IBM hardware** — needs a free token in ``.env``. Slower (you wait in
    a queue) but it's a genuine quantum computer.

The functions here hide the setup so the rest of the app just asks for a backend.
"""

from __future__ import annotations

from functools import lru_cache

from qiskit_aer import AerSimulator

from . import config


@lru_cache(maxsize=1)
def simulator() -> AerSimulator:
    """Return the local Aer simulator (cached). No account required."""
    return AerSimulator()


@lru_cache(maxsize=1)
def ibm_service():
    """Return an authenticated ``QiskitRuntimeService`` or None if no token.

    Importing qiskit_ibm_runtime is done lazily so the app starts fine even if
    you never set up IBM credentials.
    """
    creds = config.ibm_credentials()
    if not creds:
        return None
    from qiskit_ibm_runtime import QiskitRuntimeService

    kwargs = {"channel": creds["channel"], "token": creds["token"]}
    if creds["instance"]:
        kwargs["instance"] = creds["instance"]
    return QiskitRuntimeService(**kwargs)


def list_ibm_backends(min_qubits: int = 1, simulator_only: bool = False) -> list[dict]:
    """List available IBM backends with basic status, or [] if not connected."""
    service = ibm_service()
    if service is None:
        return []
    backends = service.backends(min_num_qubits=min_qubits, simulator=simulator_only or None)
    out = []
    for b in backends:
        try:
            status = b.status()
            out.append(
                {
                    "name": b.name,
                    "qubits": b.num_qubits,
                    "pending_jobs": getattr(status, "pending_jobs", None),
                    "operational": getattr(status, "operational", None),
                }
            )
        except Exception:  # noqa: BLE001 - status calls can flake; skip gracefully
            out.append({"name": b.name, "qubits": b.num_qubits})
    return out


def least_busy_ibm(min_qubits: int = 1):
    """Return the least-busy real IBM backend object, or None if unavailable."""
    service = ibm_service()
    if service is None:
        return None
    return service.least_busy(operational=True, simulator=False, min_num_qubits=min_qubits)
