"""Token-free smoke test.

Run it with::

    python -m quantumlab.setup_check
    # or
    make check

It builds a Bell state, runs it on the local Aer simulator, and prints the
result. If you see roughly half '00' and half '11', your install works — no
account or internet needed.
"""

from __future__ import annotations

from . import backends, circuits, config, run


def main() -> int:
    print("Quantum Lab — setup check")
    print("=" * 40)

    qc = circuits.bell_state()
    print("\nCircuit:")
    print(qc.draw(output="text"))

    result = run.run_circuit(qc, shots=1024, save=False)
    print(f"\nBackend : {result.backend}")
    print(f"Shots   : {result.shots}")
    print("Counts  :")
    for state, n in sorted(result.counts.items()):
        bar = "█" * round(40 * n / result.shots)
        print(f"  {state}: {n:5d}  {bar}")

    only_correlated = set(result.counts) <= {"00", "11"}
    print("\nIBM hardware token configured:", config.has_ibm_credentials())

    if only_correlated and len(result.counts) >= 1:
        print("\n✅ Success — entanglement looks correct. You're ready!")
        print("   Next:  make ui   (launch the dashboard)")
        return 0
    print("\n⚠️  Unexpected outcomes:", result.counts)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
