<div align="center">

# HarnessBench

<p align="center">
  <strong>Comparing Agentic Harnesses on Everyday Online Tasks</strong><br>
  <a href="docs/adding-a-harness.md">Read the Docs</a>
  &nbsp;·&nbsp;
  <a href="docs/harness-comparison.md">Harness Comparison</a>
  &nbsp;·&nbsp;
  <a href="docs/cloud-harness-setup.md">Cloud Setup</a>
</p>

<p align="center">
  <a href="https://github.com/reacher-z/HarnessBench/blob/main/LICENSE"><img alt="License" src="https://img.shields.io/badge/License-Apache%202.0-181717?style=flat-square&labelColor=000" /></a>
  <a href="https://pypi.org/project/harness-bench/"><img alt="PyPI" src="https://img.shields.io/badge/pypi-harness--bench-3775A9?style=flat-square&logo=pypi&logoColor=white&labelColor=000" /></a>
  <a href="https://www.python.org/downloads/"><img alt="Python 3.10+" src="https://img.shields.io/badge/python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white&labelColor=000" /></a>
  <a href="https://github.com/reacher-z/HarnessBench"><img alt="GitHub stars" src="https://img.shields.io/github/stars/reacher-z/HarnessBench?style=flat-square&logo=github&color=181717&cacheSeconds=300" /></a>
  <a href="https://discord.gg/clawbench"><img alt="Discord" src="https://img.shields.io/badge/Discord-Join%20our%20community-00D26A?style=flat-square&logo=discord&logoColor=white&labelColor=000" /></a>
</p>

<p align="center">
  <a href="https://github.com/reacher-z/ClawBench"><img src="https://img.shields.io/badge/%F0%9F%94%97%20Sister%20project%20of%20ClawBench-181717?style=for-the-badge&labelColor=6C2BD9&color=FFD21E" alt="Sister project of ClawBench" /></a>
</p>

<p align="center">
  <a href="https://deepwiki.com/reacher-z/HarnessBench"><img alt="Ask DeepWiki" src="https://deepwiki.com/badge.svg" /></a>
</p>

<p align="center">
  If you want to compare <i>base models</i> on a fixed harness, check out our sister project
  <a href="https://github.com/reacher-z/ClawBench"><b>ClawBench</b></a>
  &nbsp;—&nbsp; same pipeline, orthogonal axis.
</p>

[English](README.md) &nbsp;·&nbsp; [简体中文](README.zh-CN.md)

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
@misc{zhang2026harnessbench,
  title        = {HarnessBench: Comparing Agentic Harnesses on Everyday Online Tasks},
  author       = {Yuxuan Zhang and Yubo Wang and Yipeng Zhu and Penghui Du and Junwen Miao and Xuan Lu and Wendong Xu and Yunzhuo Hao and Songcheng Cai and Xiaochen Wang and Huaisong Zhang and Xian Wu and Yi Lu and Minyi Lei and Kai Zou and Huifeng Yin and Ping Nie and Liang Chen and Dongfu Jiang and Wenhu Chen and Kelsey R. Allen},
  year         = {2026},
  note         = {Preprint in preparation},
  howpublished = {\url{https://github.com/reacher-z/HarnessBench}}
}
```
