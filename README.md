<div align="center">

# HarnessBench

**Comparing agentic harnesses on everyday online tasks.**

Sister project to [ClawBench](https://github.com/reacher-z/ClawBench). Where ClawBench fixes the harness and varies the base model, **HarnessBench fixes the base model and varies the harness**. Same scoring pipeline, orthogonal axis.

[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![PyPI: harness-bench](https://img.shields.io/badge/pypi-harness--bench-informational)](https://pypi.org/project/harness-bench/)

[English](README.md) · [简体中文](README.zh-CN.md)

</div>

---

## What it answers

Given an everyday online task (book a flight, unsubscribe from a newsletter, compare three laptops) and a fixed base model, which agentic harness actually gets it done?

HarnessBench runs the **same task** through **different harnesses** using the **same scoring pipeline** (5-layer recording, DOM-match judge, LLM judge), then partitions the leaderboard by `(harness, model, task)`.

## The six named harnesses

| Harness | Upstream | Language | Cloud? | Notes |
|---------|----------|----------|--------|-------|
| `openclaw` | [reacher-z/ClawBench](https://github.com/reacher-z/ClawBench) | Python | No | Reference harness — shared with ClawBench. |
| `hermes` | [nousresearch/hermes-agent](https://github.com/nousresearch/hermes-agent) | Python | No | Hermes-style tool-use harness. |
| `claw-code` | [ultraworkers/claw-code](https://github.com/ultraworkers/claw-code) | Rust | No | Rust-native agent loop. |
| `browser-use` | [browser-use/browser-use](https://github.com/browser-use/browser-use) | Python | No | Popular Playwright-based harness. |
| `stagehand` | [browserbase/stagehand](https://github.com/browserbase/stagehand) | Node/TS | **Yes** | Requires `BROWSERBASE_API_KEY`. |
| `coze-studio` | [coze-dev/coze-studio](https://github.com/coze-dev/coze-studio) | Web | **Yes** | Requires `COZE_INSTANCE_URL`, `COZE_API_TOKEN`. |

Cloud harnesses are **opt-in**. Without credentials, they appear in the matrix as `skipped:missing_credential:<VAR>` — never silently zeroed.

More harnesses are discovered by a 30-agent global scout (see `docs/scout-2026-04-16.md`); each qualifying framework lands as its own follow-up PR.

## Install

```bash
pip install harness-bench
```

HarnessBench pulls in [`clawbench-eval`](https://pypi.org/project/clawbench-eval/) as a library: the container orchestration, 5-layer recording, and scoring pipeline live there.

## Quickstart

```bash
# List registered harnesses
harness-bench harnesses

# Show the matrix that would run (with cloud gating applied)
harness-bench matrix --harnesses openclaw,hermes,browser-use --models gpt-4o-mini

# Run one triple end-to-end
harness-bench run \
    --harness openclaw \
    --model  gpt-4o-mini \
    --case   ./fixtures/book-a-flight.json

# Render the markdown leaderboard from a results directory
harness-bench leaderboard ./harness-output/
```

## Adding a harness

HarnessBench uses `clawbench.harnesses` entry points. A new harness is three files plus one `pyproject.toml` stanza. Walkthrough: [`docs/adding-a-harness.md`](docs/adding-a-harness.md).

## Credentials for cloud harnesses

Step-by-step: [`docs/cloud-harness-setup.md`](docs/cloud-harness-setup.md). Short version:

```bash
export BROWSERBASE_API_KEY=...              # enables stagehand
export COZE_INSTANCE_URL=https://...        # enables coze-studio
export COZE_API_TOKEN=...                   # required together with the URL
```

Everything else (OpenAI, Anthropic, etc.) is whatever your chosen base model needs — same env-var conventions as ClawBench.

## Differences from ClawBench

- **Axis.** ClawBench: one harness, many models. HarnessBench: many harnesses, one (or many) models.
- **Runtime.** ClawBench bundles three Python harnesses in one container. HarnessBench gives each harness its own container (Python / Node / Rust / Web are not co-installable).
- **Cloud.** ClawBench is fully local-first. HarnessBench supports local-first and cloud-opt-in harnesses in the same matrix.
- **Code reuse.** 100% — HarnessBench imports `clawbench-eval` rather than forking it.

## License

Apache-2.0 for the repository. Each bundled harness adapter links to upstream code under the upstream's own license; nothing from an incompatible license is vendored.

## Citation

<!-- Placeholder: replace with full arXiv block once preprint is submitted. -->

```bibtex
@misc{harnessbench2026,
  title        = {HarnessBench: Comparing Agentic Harnesses on Everyday Online Tasks},
  author       = {Reacher and contributors},
  year         = {2026},
  note         = {Preprint in preparation},
  howpublished = {\url{https://github.com/reacher-z/HarnessBench}}
}
```
