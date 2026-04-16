#!/usr/bin/env bash
# setup.sh — install Coze Python SDK for workflow invocation.
set -euo pipefail

pip install --no-cache-dir cozepy
python -c "import cozepy; print('cozepy ready')"
