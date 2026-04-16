#!/usr/bin/env bash
# setup.sh for openclaw harness — delegated to ClawBench's bundled
# setup-openclaw.sh, which is already present in the clawbench-base image.
set -euo pipefail

# Upstream ClawBench setup runs during the base-image build; nothing more
# to do here unless the user is overriding something.
echo "[openclaw] setup complete (inherited from clawbench-base image)"
