#!/usr/bin/env bash
# run.sh for openclaw harness — thin pass-through to ClawBench's run-openclaw.sh.
set -euo pipefail

exec /opt/clawbench/run-openclaw.sh "$@"
