#!/usr/bin/env bash
# setup.sh — install Node.js 22 and Stagehand beside the harness driver.
set -euo pipefail

STAGEHAND_VERSION="${STAGEHAND_VERSION:-latest}"
HARNESS_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"

curl -fsSL https://deb.nodesource.com/setup_22.x | bash -
apt-get install -y --no-install-recommends nodejs
npm install --prefix "$HARNESS_DIR" "@browserbasehq/stagehand@${STAGEHAND_VERSION}"
# Current Stagehand releases expose an ESM-only entry point. Import from the
# install directory so this also checks the module lookup used by the driver.
cd -- "$HARNESS_DIR"
node --input-type=module -e "import '@browserbasehq/stagehand'"
