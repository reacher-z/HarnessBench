#!/usr/bin/env bash
# run.sh — invoke the configured Coze workflow against the task.
set -euo pipefail

: "${COZE_INSTANCE_URL:?COZE_INSTANCE_URL must be set}"
: "${COZE_API_TOKEN:?COZE_API_TOKEN must be set}"
: "${COZE_WORKFLOW_ID:?COZE_WORKFLOW_ID must be set (Coze workflow that drives the browser)}"

TASK_FILE="${TASK_FILE:-/opt/clawbench/shared/task.json}"
python /opt/harness/run-coze.py \
    --instance "$COZE_INSTANCE_URL" \
    --workflow "$COZE_WORKFLOW_ID" \
    --task "$TASK_FILE" \
    --record-dir "${RECORD_DIR:-/opt/clawbench/recording}"
