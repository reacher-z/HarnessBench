"""HarnessBench CLI — thin wrapper that delegates the actual run to ClawBench.

Subcommands:

``harness-bench harnesses``      list registered harnesses and their cloud-credential status
``harness-bench matrix``         show what a matrix expansion would run (no side effects)
``harness-bench run``            execute a single (harness, model, case) triple
``harness-bench batch``          expand the matrix and execute each eligible triple
``harness-bench leaderboard``    render aggregated results as markdown
``harness-bench version``
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

import click

from harnessbench import __version__
from harnessbench import matrix as matrix_mod
from harnessbench import leaderboard as lb_mod


@click.group(invoke_without_command=True)
@click.pass_context
def main(ctx: click.Context) -> None:
    """HarnessBench: compare agentic harnesses on everyday online tasks."""
    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())


@main.command("version")
def version_cmd() -> None:
    """Print the installed HarnessBench version."""
    click.echo(__version__)


@main.command("harnesses")
def harnesses_cmd() -> None:
    """List registered harnesses and which ones are gated on credentials."""
    regs = matrix_mod.discover_registrations()
    if not regs:
        click.echo("(no harnesses registered — is harness-bench installed?)", err=True)
        sys.exit(1)
    for reg in sorted(regs, key=lambda r: r.spec.name):
        missing = reg.missing_credentials()
        if not reg.requires_credentials:
            status = "ready"
        elif missing:
            status = f"skipped: set {', '.join(missing)}"
        else:
            status = "ready (credentials present)"
        click.echo(f"{reg.spec.name:<14}  {status}")


@main.command("matrix")
@click.option("--harness", "-h", multiple=True, required=True, help="Harness name (repeatable).")
@click.option("--model", "-m", multiple=True, required=True, help="Model id (repeatable).")
@click.option("--case", "-c", multiple=True, required=True, help="Test-case id (repeatable).")
def matrix_cmd(harness: tuple[str, ...], model: tuple[str, ...], case: tuple[str, ...]) -> None:
    """Preview the (harness, model, case) triples a run would expand to."""
    cases = [{"id": c} for c in case]
    specs = matrix_mod.expand(harness, model, cases)
    counts = matrix_mod.summarize(specs)
    click.echo(f"total={counts['total']} eligible={counts['eligible']} skipped={counts['skipped']}")
    for s in specs:
        tag = "[OK]   " if s.is_eligible else "[SKIP] "
        detail = "" if s.is_eligible else f"  ({s.skip_reason})"
        click.echo(f"{tag}{s.harness:<14} {s.model:<22} {s.case_id}{detail}")


@main.command("run")
@click.option("--harness", required=True)
@click.option("--model", required=True)
@click.option("--case", required=True)
@click.option(
    "--output-dir",
    type=click.Path(file_okay=False, path_type=Path),
    default=Path("harness-output"),
)
@click.option("--no-upload", is_flag=True, default=True, help="Skip HF upload (default on).")
def run_cmd(harness: str, model: str, case: str, output_dir: Path, no_upload: bool) -> None:
    """Run one (harness, model, case) through the ClawBench pipeline."""
    regs = {r.spec.name: r for r in matrix_mod.discover_registrations()}
    reg = regs.get(harness)
    if reg is None:
        click.echo(f"error: harness '{harness}' not registered", err=True)
        sys.exit(2)
    missing = reg.missing_credentials()
    if missing:
        click.echo(
            f"error: harness '{harness}' requires {', '.join(missing)} — set them or pick another harness",
            err=True,
        )
        sys.exit(3)

    # Delegate to ClawBench once it exposes ``run_case`` in its public API.
    try:
        from clawbench import run_case  # type: ignore[attr-defined]
    except ImportError:
        click.echo(
            "error: clawbench does not yet expose `run_case` — install clawbench-eval>=0.2.0 "
            "once the plugin surface lands. See "
            "https://github.com/reacher-z/ClawBench for progress.",
            err=True,
        )
        sys.exit(10)

    output_dir.mkdir(parents=True, exist_ok=True)
    run_case(
        case=case,
        model=model,
        harness=harness,
        output_dir=output_dir,
        no_upload=no_upload,
    )


@main.command("batch")
@click.option("--harness", "-h", multiple=True, required=True)
@click.option("--model", "-m", multiple=True, required=True)
@click.option("--case", "-c", multiple=True, required=True)
@click.option(
    "--output-dir",
    type=click.Path(file_okay=False, path_type=Path),
    default=Path("harness-output"),
)
@click.option("--dry-run", is_flag=True, default=False)
def batch_cmd(
    harness: tuple[str, ...],
    model: tuple[str, ...],
    case: tuple[str, ...],
    output_dir: Path,
    dry_run: bool,
) -> None:
    """Matrix-expand, then run every eligible triple."""
    cases = [{"id": c} for c in case]
    specs = matrix_mod.expand(harness, model, cases)
    counts = matrix_mod.summarize(specs)
    click.echo(
        f"matrix: total={counts['total']} eligible={counts['eligible']} skipped={counts['skipped']}"
    )
    if dry_run:
        for s in specs:
            click.echo(f"{s.harness} {s.model} {s.case_id} -> {s.status}")
        return

    try:
        from clawbench import run_case  # type: ignore[attr-defined]
    except ImportError:
        click.echo(
            "error: clawbench does not yet expose `run_case`; install clawbench-eval>=0.2.0.",
            err=True,
        )
        sys.exit(10)

    output_dir.mkdir(parents=True, exist_ok=True)
    for s in specs:
        if not s.is_eligible:
            click.echo(f"skip: {s.harness} {s.model} {s.case_id} ({s.skip_reason})")
            continue
        run_case(
            case=s.case_id,
            model=s.model,
            harness=s.harness,
            output_dir=output_dir,
            no_upload=True,
        )


@main.command("leaderboard")
@click.option(
    "--results-dir",
    type=click.Path(exists=True, file_okay=False, path_type=Path),
    default=Path("harness-output"),
)
def leaderboard_cmd(results_dir: Path) -> None:
    """Aggregate results under --results-dir into a markdown leaderboard."""
    rows = lb_mod.aggregate(lb_mod.load_results(results_dir))
    click.echo(lb_mod.render_markdown(rows))


if __name__ == "__main__":
    main()
