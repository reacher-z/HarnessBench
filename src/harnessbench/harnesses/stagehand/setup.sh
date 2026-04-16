#!/usr/bin/env bash
# setup.sh — install Node.js 20 and Stagehand.
set -euo pipefail

STAGEHAND_VERSION="${STAGEHAND_VERSION:-latest}"

curl -fsSL https://deb.nodesource.com/setup_20.x | bash -
apt-get install -y --no-install-recommends nodejs
npm install -g "@browserbasehq/stagehand@${STAGEHAND_VERSION}"
node -e "require('@browserbasehq/stagehand')"
