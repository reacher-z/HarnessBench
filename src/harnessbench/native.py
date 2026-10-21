"""Explicit delegation to ClawBench's public CLI, not its future plugin API."""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path
from typing import Iterable

import click

# These names are present in both projects' registries. Native execution uses
# ClawBench's own drivers; HarnessBench's bundled scripts are not substituted.
NATIVE_HARNESSES = frozenset({"openclaw", "hermes", "claw-code", "browser-use"})


def validate_harnesses(harnesses: Iterable[str]) -> None:
    unsupported = sorted(set(harnesses) - NATIVE_HARNESSES)
    if unsupported:
        raise click.ClickException(
            f"Harness {', '.join(unsupported)} is not supported by the native ClawBench CLI. "
            "Supported native drivers: " + ", ".join(sorted(NATIVE_HARNESSES))
        )


def run_case(*, case: str, model: str, harness: str, output_dir: Path, no_upload: bool) -> None:
    """Keep task/model/output and ClawBench's judging and recording semantics intact."""
    validate_harnesses([harness])
    executable = shutil.which("clawbench-run")
    if executable is None:
        raise click.ClickException(
            "clawbench-run is not on PATH. Install a ClawBench release exposing the "
            "public clawbench-run command (validated with clawbench-eval 0.11.0)."
        )
    command = [executable, "--harness", harness, "--output-dir", str(output_dir)]
    if no_upload:
        command.append("--no-upload")
    # End options before arbitrary task/model strings; never build a shell command.
    command.extend(["--", case, model])
    try:
        result = subprocess.run(command, check=False)
    except OSError as exc:
        raise click.ClickException(f"Could not start clawbench-run: {exc}") from exc
    if result.returncode:
        # Preserve runner outcomes (1 failed task, 2 infrastructure, 3 judge
        # inconclusive); signal termination follows the shell's 128+signal rule.
        code = result.returncode if result.returncode > 0 else 128 - result.returncode
        raise click.exceptions.Exit(code)
