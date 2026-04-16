#!/usr/bin/env bash
# run.sh — drive claw-code against the running Chrome instance.
set -euo pipefail

export PATH="/root/.cargo/bin:${PATH}"
: "${CDP_ENDPOINT:=http://127.0.0.1:9222}"
TASK_FILE="${TASK_FILE:-/opt/clawbench/shared/task.json}"

claw-code run \
    --cdp-endpoint "$CDP_ENDPOINT" \
    --task "$TASK_FILE" \
    --output "${RECORD_DIR:-/opt/clawbench/recording}"
