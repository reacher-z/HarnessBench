#!/usr/bin/env bash
# run.sh — attach hermes-agent to the running Chrome (CDP 9222) and execute
# the task provided via /opt/clawbench/shared/task.json.
set -euo pipefail

# Source the shared api-config + watchdog libs once they land in
# clawbench-base (see ClawBench toolkit refactor). For now, use env
# directly.
: "${CDP_ENDPOINT:=http://127.0.0.1:9222}"

TASK_FILE="${TASK_FILE:-/opt/clawbench/shared/task.json}"

python -m hermes_agent.cli \
    --cdp-endpoint "$CDP_ENDPOINT" \
    --task-file "$TASK_FILE" \
    --record-dir "${RECORD_DIR:-/opt/clawbench/recording}"
