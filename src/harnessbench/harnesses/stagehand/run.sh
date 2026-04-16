#!/usr/bin/env bash
# run.sh — drive Stagehand against BrowserBase cloud.
set -euo pipefail

: "${BROWSERBASE_API_KEY:?BROWSERBASE_API_KEY must be set for the stagehand harness}"
TASK_FILE="${TASK_FILE:-/opt/clawbench/shared/task.json}"

node /opt/harness/run-stagehand.js \
    --task "$TASK_FILE" \
    --output "${RECORD_DIR:-/opt/clawbench/recording}"
