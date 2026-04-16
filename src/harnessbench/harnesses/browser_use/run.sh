#!/usr/bin/env bash
# run.sh — drive browser-use against the running Chrome (CDP 9222).
set -euo pipefail

: "${CDP_ENDPOINT:=http://127.0.0.1:9222}"
TASK_FILE="${TASK_FILE:-/opt/clawbench/shared/task.json}"

python /opt/harness/run-browser-use.py \
    --cdp "$CDP_ENDPOINT" \
    --task "$TASK_FILE" \
    --record-dir "${RECORD_DIR:-/opt/clawbench/recording}"
