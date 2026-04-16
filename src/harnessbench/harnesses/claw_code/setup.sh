#!/usr/bin/env bash
# setup.sh — install Rust toolchain and build claw-code from source.
set -euo pipefail

CLAW_CODE_REF="${CLAW_CODE_REF:-main}"

curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y --default-toolchain stable
export PATH="/root/.cargo/bin:${PATH}"

cargo install --locked --git https://github.com/ultraworkers/claw-code.git --rev "$CLAW_CODE_REF" claw-code
claw-code --version
