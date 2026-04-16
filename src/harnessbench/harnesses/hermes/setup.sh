#!/usr/bin/env bash
# setup.sh — install Nous Research hermes-agent.
set -euo pipefail

HERMES_REF="${HERMES_REF:-main}"
pip install --no-cache-dir "git+https://github.com/nousresearch/hermes-agent.git@${HERMES_REF}"
python -c "import hermes_agent; print('hermes-agent ready')"
