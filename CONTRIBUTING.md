# Contributing to HarnessBench

Thanks for helping make agent-harness comparisons easier to inspect and reproduce.

## Before opening a change

1. Use Python 3.11 or newer and keep credentials out of source, tests, fixtures, and logs.
2. Keep changes focused: adapter metadata, a concrete adapter implementation, documentation, or tests.
3. Run `uv run pytest -q` and include the relevant command output in the pull request.

## Adding or repairing an adapter

Follow [the adapter guide](docs/adding-a-harness.md). A complete adapter has a
`HarnessSpec`, `Dockerfile`, `setup.sh`, and `run.sh`; scripts must reference real
files that are included in the image. Declare every required credential in the spec
so `harness-bench matrix` can skip unavailable configurations rather than treating
them as results.

The current released runner exposes discovery, matrix preflight, and dry-run batch
planning. It does not execute benchmark cases until ClawBench provides the required
public runner API. Please do not submit generated scores, recordings, or leaderboard
entries as if they came from an end-to-end HarnessBench run.

## Evidence and attribution

Use canonical upstream URLs and licenses in `HarnessSpec`. Do not add publication
status, author lists, results, or citation metadata without an approved source of
record. The existing citation remains a preprint-in-preparation placeholder.

## Reporting problems

Open a GitHub issue with the command, a redacted error, platform and Python version,
and a minimal reproduction. Never include API keys, tokens, cookies, or private URLs.
