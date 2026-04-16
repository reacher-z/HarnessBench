#!/usr/bin/env bash
# setup.sh — install browser-use.
set -euo pipefail

BROWSER_USE_VERSION="${BROWSER_USE_VERSION:-}"
if [[ -n "$BROWSER_USE_VERSION" ]]; then
    pip install --no-cache-dir "browser-use==${BROWSER_USE_VERSION}"
else
    pip install --no-cache-dir "browser-use"
fi
python -c "import browser_use; print('browser-use ready')"
