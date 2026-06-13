#!/usr/bin/env bash
# Quantum Lab — one-shot setup for the main environment.
# Usage:  ./scripts/setup.sh
set -euo pipefail

cd "$(dirname "$0")/.."

PY=/opt/homebrew/bin/python3.13
if [ ! -x "$PY" ]; then
  PY=$(command -v python3.13 || command -v python3.12 || command -v python3)
fi
echo "Using Python: $PY ($($PY --version))"

echo "→ Creating .venv ..."
"$PY" -m venv .venv
.venv/bin/python -m pip install --upgrade pip

echo "→ Installing core requirements (this can take a few minutes) ..."
.venv/bin/pip install -r requirements/core.txt

echo "→ Verifying dependency consistency ..."
.venv/bin/pip check

echo "→ Smoke test (Bell state on Aer simulator) ..."
.venv/bin/python -m quantumlab.setup_check

cat <<'EOF'

✅ Quantum Lab is ready.

Next:
  source .venv/bin/activate
  make ui      # launch the adaptive dashboard
  make lab     # or open the notebooks in JupyterLab

To run on real IBM hardware later:  cp .env.example .env  and add your token.
EOF
