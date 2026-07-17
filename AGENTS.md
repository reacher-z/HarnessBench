# HarnessBench Agent Guide

## Scope

HarnessBench is a research-engineering repository for describing, discovering, and
preflighting agent-harness adapters. Keep its public materials grounded in checked-in
code and reproducible local commands.

## Safe local checks

Use Python 3.11 or newer. The supported no-side-effect checks are:

```bash
uv run pytest -q
uv run harness-bench harnesses
uv run harness-bench matrix --harness openclaw --model example-model --case example-case
uv run harness-bench batch --dry-run --harness openclaw --model example-model --case example-case
```

Do not place credentials in source files, tests, fixtures, issue text, or command
output. Use synthetic identifiers in tests and documentation.

## Execution boundary

The released `clawbench-eval` package does not currently expose HarnessBench's
required public `run_case` API. `harness-bench run` and a non-dry `batch` therefore
stop before creating output. Do not fabricate recordings, scores, leaderboard rows,
or claims that an adapter ran end-to-end. Revisit this boundary only after the public
upstream API is available and covered by an integration test.

## Adapter changes

An adapter needs a spec, a Dockerfile, `setup.sh`, and `run.sh`. Every executable
referenced by the adapter must exist in the image, credential requirements must match
the adapter's actual runtime inputs, and metadata-only changes need a regression test
when they affect discovery or preflight. See [docs/adding-a-harness.md](docs/adding-a-harness.md).

## Publication and citation

The repository's citation block says `Preprint in preparation`. Do not change
publication status, author list, score claims, or citation metadata without a
responsible-author approved canonical record.
