<div align="center">

<a href="https://github.com/reacher-z/HarnessBench">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="static/hero-dark.svg">
    <img alt="HarnessBench" src="static/hero-light.svg" width="820">
  </picture>
</a>

<p align="center">
  <strong>The Benchmark for Comparing Agent Harnesses on Everyday Online Tasks</strong><br>
  <a href="docs/adding-a-harness.md">Read the Docs</a>
  &nbsp;·&nbsp;
  <a href="docs/harness-comparison.md">Harness Comparison</a>
  &nbsp;·&nbsp;
  <a href="docs/cloud-harness-setup.md">Cloud Setup</a>
</p>

<p align="center">
  <a href="https://github.com/reacher-z/HarnessBench"><img alt="Star this repo" src="https://img.shields.io/badge/%E2%98%85%20Star%20this%20repo-181717?style=flat-square&logo=github&logoColor=white" /></a>
  <a href="https://harness-eval.com"><img alt="Project Page" src="https://img.shields.io/badge/harness--eval.com-D97706?style=flat-square&logo=googlechrome&logoColor=white" /></a>
  <a href="https://github.com/reacher-z/HarnessBench"><img alt="GitHub stars" src="https://img.shields.io/github/stars/reacher-z/HarnessBench?style=flat-square&logo=github&color=181717&cacheSeconds=300" /></a>
  <a href="https://discord.gg/clawbench"><img alt="Discord" src="https://img.shields.io/badge/Discord-Join-5865F2?style=flat-square&logo=discord&logoColor=white" /></a>
  <a href="https://codespaces.new/reacher-z/HarnessBench?quickstart=1"><img alt="Codespaces" src="https://img.shields.io/badge/Codespaces-Open-181717?style=flat-square&logo=github&logoColor=white" /></a>
</p>

<p align="center">
  <a href="https://github.com/reacher-z/ClawBench"><img src="https://img.shields.io/badge/Sister%20Project%20%E2%86%92%20ClawBench-D97706?style=for-the-badge&labelColor=0F172A&color=F59E0B" alt="Sister project of ClawBench" /></a>
</p>

<p align="center">
  <a href="https://deepwiki.com/reacher-z/HarnessBench"><img alt="Ask DeepWiki" src="https://deepwiki.com/badge.svg" /></a>
</p>

<p align="center">
  If you want to compare <i>base models</i> on a fixed harness, check out our sister project
  <a href="https://github.com/reacher-z/ClawBench"><b>ClawBench</b></a>
  &nbsp;&mdash;&nbsp; same pipeline, orthogonal axis.
</p>

<a href="#-human-quick-start"><img src="https://img.shields.io/badge/Run%20in%20one%20line%20of%20code-D97706?style=for-the-badge&labelColor=D97706&logoColor=white&logo=data:image/svg%2Bxml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCA1NzYgNTEyIj48cGF0aCBmaWxsPSIjZmZmZmZmIiBkPSJNMjYzLjQtMjdMMjc4LjIgOS44IDMxNSAyNC42YzMgMS4yIDUgNC4yIDUgNy40cy0yIDYuMi01IDcuNEwyNzguMiA1NC4yIDI2My40IDkxYy0xLjIgMy00LjIgNS03LjQgNXMtNi4yLTItNy40LTVMMjMzLjggNTQuMiAxOTcgMzkuNGMtMy0xLjItNS00LjItNS03LjRzMi02LjIgNS03LjRMMjMzLjggOS44IDI0OC42LTI3YzEuMi0zIDQuMi01IDcuNC01czYuMiAyIDcuNCA1ek0xMTAuNyA0MS43bDIxLjUgNTAuMSA1MC4xIDIxLjVjNS45IDIuNSA5LjcgOC4zIDkuNyAxNC43cy0zLjggMTIuMi05LjcgMTQuN2wtNTAuMSAyMS41LTIxLjUgNTAuMWMtMi41IDUuOS04LjMgOS43LTE0LjcgOS43cy0xMi4yLTMuOC0xNC43LTkuN0w1OS44IDE2NC4yIDkuNyAxNDIuN0MzLjggMTQwLjIgMCAxMzQuNCAwIDEyOHMzLjgtMTIuMiA5LjctMTQuN0w1OS44IDkxLjggODEuMyA0MS43QzgzLjggMzUuOCA4OS42IDMyIDk2IDMyczEyLjIgMy44IDE0LjcgOS43ek00NjQgMzA0YzYuNCAwIDEyLjIgMy44IDE0LjcgOS43bDIxLjUgNTAuMSA1MC4xIDIxLjVjNS45IDIuNSA5LjcgOC4zIDkuNyAxNC43cy0zLjggMTIuMi05LjcgMTQuN2wtNTAuMSAyMS41LTIxLjUgNTAuMWMtMi41IDUuOS04LjMgOS43LTE0LjcgOS43cy0xMi4yLTMuOC0xNC43LTkuN2wtMjEuNS01MC4xLTUwLjEtMjEuNWMtNS45LTIuNS05LjctOC4zLTkuNy0xNC43czMuOC0xMi4yIDkuNy0xNC43bDUwLjEtMjEuNSAyMS41LTUwLjFjMi41LTUuOSA4LjMtOS43IDE0LjctOS43ek00NjAgMGMxMSAwIDIxLjYgNC40IDI5LjUgMTIuMmw0Mi4zIDQyLjNDNTM5LjYgNjIuNCA1NDQgNzMgNTQ0IDg0cy00LjQgMjEuNi0xMi4yIDI5LjVsLTg4LjIgODguMi0xMDEuMy0xMDEuMyA4OC4yLTg4LjJDNDM4LjQgNC40IDQ0OSAwIDQ2MCAwek00NC4yIDM5OC41TDMwOC40IDEzNC4zIDQwOS43IDIzNS42IDE0NS41IDQ5OS44QzEzNy42IDUwNy42IDEyNyA1MTIgMTE2IDUxMnMtMjEuNi00LjQtMjkuNS0xMi4yTDQ0LjIgNDU3LjVDMzYuNCA0NDkuNiAzMiA0MzkgMzIgNDI4czQuNC0yMS42IDEyLjItMjkuNXoiLz48L3N2Zz4=" alt="Run in one line of code"></a>

```bash
uv tool install harness-bench && harness-bench
```

<sub><i>Install &rarr; List &rarr; Preflight. &nbsp; Cloud harnesses opt in via env vars. &nbsp; Execution awaits a public ClawBench runner API.</i></sub>

### Which Harness Wins on the Same Task?

Given one task (order food, book travel, apply for a job) and **one fixed base model** --<br/>
which agentic harness actually gets it done?<br/>
**Six named harnesses**, four runtimes, one pipeline, one leaderboard.

---

**6** harnesses &nbsp;&middot;&nbsp; **4** runtimes (Python / Node / Rust / Web) &nbsp;&middot;&nbsp; **153** shared tasks &nbsp;&middot;&nbsp; **15** categories

<a href="README.zh-CN.md"><img src="static/icons/language.svg" width="16" height="16"> 中文</a>

</div>

<br/>

<p align="center">
<img src="static/icons/layer-group.svg" width="24" height="24">&nbsp;<b>Plugin Entry-Points</b>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
<img src="static/icons/cube.svg" width="24" height="24">&nbsp;<b>One Container per Harness</b>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
<img src="static/icons/shield-halved.svg" width="24" height="24">&nbsp;<b>Cloud Opt-in</b>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
<img src="static/icons/globe.svg" width="24" height="24">&nbsp;<b>Same Pipeline as ClawBench</b>
</p>

<br/>

## How It Works

```
   You pick a task            HarnessBench spins up        Each harness drives       Same 5-layer recording
   from ClawBench's           one container per            the browser its own       + DOM-match + LLM judge
   shared 153-task pool       harness (Python / Node       way on the same task      partitioned by harness
                              / Rust / Web)

   ┌──────────────┐           ┌──────────────┐           ┌──────────────┐           ┌──────────────┐
   │  "Book a     │    ──►    │  6 containers│    ──►    │  6 different │    ──►    │  Per-harness │
   │   flight on  │           │  (one per    │           │  agent loops │           │  leaderboard │
   │   Expedia"   │           │   harness)   │           │  same task   │           │  by category │
   └──────────────┘           └──────────────┘           └──────────────┘           └──────────────┘
```

<br/>

# <img src="static/icons/robot.svg" width="28" height="28"> LLM Quick Start

Point your coding agent (Claude Code, Cursor, Copilot, etc.) at [`AGENTS.md`](AGENTS.md) and prompt away. HarnessBench shares ClawBench's test-cases, container base image, and 5-layer recording stack -- if your agent already knows ClawBench, there is nothing new to learn about the pipeline, only a new harness axis.

<br/>

# <img src="static/icons/person.svg" width="28" height="28"> Human Quick Start

```bash
# Option A -- PyPI install (recommended)
uv tool install harness-bench && harness-bench
```

```bash
# Option B -- Clone the repo (for contributors / adding a harness)
git clone https://github.com/reacher-z/HarnessBench.git && cd HarnessBench && uv run harness-bench
```

**Prerequisites:** [Python 3.11+](https://python.org), [uv](https://docs.astral.sh/uv/), and a container engine -- [Docker](https://www.docker.com/) **or** [Podman](https://podman.io/). Same engine detection as ClawBench; force one with `export CONTAINER_ENGINE=docker`.

**1. List registered harnesses:**

```bash
harness-bench harnesses
# openclaw       ready
# hermes         ready
# claw-code      ready
# browser-use    ready
# stagehand      skipped: set BROWSERBASE_API_KEY
# coze-studio    skipped: set COZE_INSTANCE_URL, COZE_API_TOKEN, COZE_WORKFLOW_ID
```

**2. Preview a matrix** (no side effects):

```bash
harness-bench matrix \
    --harness openclaw --harness hermes --harness browser-use \
    --model   claude-sonnet-4-6 \
    --case    001-daily-life-food-uber-eats \
    --case    007-daily-life-travel-expedia
```

**3. Execution status:**

```bash
harness-bench batch --dry-run \
    --harness openclaw --harness hermes \
    --model example-model \
    --case example-case
```

The released `clawbench-eval` package does not expose the public `run_case` API that HarnessBench needs. `harness-bench run` and non-dry `batch` therefore stop before creating containers or output. Use `matrix` and `batch --dry-run` for local preflight.

**4. Result availability:**

No official HarnessBench result table, HarnessBench-Lite fixture, tutorial video, or execution recording is published here.

**5. Future result rendering:**

`harness-bench leaderboard` only renders local result files after a public execution API and verified end-to-end runner are available.

<br/>

# <img src="static/icons/chart-bar.svg" width="28" height="28"> Project Status

No public HarnessBench-Lite fixture is shipped. Do not compare an unpublished subset with another benchmark or infer costs, rankings, or coverage from a missing fixture.

<br/>

# <img src="static/icons/video.svg" width="28" height="28"> Tutorial

<div align="center">

No public tutorial video is available. Start with the documented `harnesses`,
`matrix`, and dry-run commands above.

</div>

<br/>

# <img src="static/icons/play.svg" width="28" height="28"> Demos

No verified end-to-end execution demo is published. This section will remain empty
until a public runner and an inspectable recording are available.

<table>
<tr>
<td width="50%" align="center">

**No verified demo available**

No placeholder media is presented as a project result.

</td>
<td width="50%" align="center">

**No verified comparison available**

No placeholder media is presented as a project result.

</td>
</tr>
</table>

> Execution recordings will only be linked after the public runner is available and the recording is independently inspectable.

<br/>

# <img src="static/icons/cube.svg" width="28" height="28"> The Six Named Harnesses

| Harness | Upstream | Runtime | Cloud? | What it is |
|---------|----------|:-------:|:------:|------------|
| `openclaw` | [reacher-z/ClawBench](https://github.com/reacher-z/ClawBench) | Python | &mdash; | Reference harness, shared with ClawBench. The baseline everyone gets compared against. |
| `hermes` | [nousresearch/hermes-agent](https://github.com/nousresearch/hermes-agent) | Python | &mdash; | Hermes-style tool-use loop with explicit plan/act steps. |
| `claw-code` | [ultraworkers/claw-code](https://github.com/ultraworkers/claw-code) | Rust | &mdash; | Rust-native agent loop, zero-GIL concurrency. |
| `browser-use` | [browser-use/browser-use](https://github.com/browser-use/browser-use) | Python | &mdash; | Community-favorite Playwright-based harness. |
| `stagehand` | [browserbase/stagehand](https://github.com/browserbase/stagehand) | Node/TS | **Yes** | BrowserBase's Stagehand -- requires `BROWSERBASE_API_KEY`. |
| `coze-studio` | [coze-dev/coze-studio](https://github.com/coze-dev/coze-studio) | Web | **Yes** | Coze Studio flow runner -- requires `COZE_INSTANCE_URL`, `COZE_API_TOKEN`, and `COZE_WORKFLOW_ID`. |

Cloud harnesses are **opt-in**: without credentials they appear in the matrix as `skipped:missing_credential:<VAR>` -- **never silently zeroed**. Adapter requirements and comparison boundaries are documented in [`docs/harness-comparison.md`](docs/harness-comparison.md).

<br/>

# <img src="static/icons/chart-bar.svg" width="28" height="28"> Preview Leaderboard

<div align="center">

**No official HarnessBench scores are published.** The execution bridge is blocked on ClawBench's public runner API, so this repository does not present placeholder rows as benchmark results.

</div>


<br/>

# <img src="static/icons/circle-question.svg" width="28" height="28"> Intended Output Contract

The paths below describe the intended cross-harness output contract. They are not a published run, demo, or leaderboard result:

```
task    = 001-daily-life-food-uber-eats
model   = claude-sonnet-4-6

harness = openclaw      ──►  ./harness-output/openclaw/claude-sonnet-4-6/001-.../
                             (Python loop driving Chrome via the ClawBench extension)

harness = hermes        ──►  ./harness-output/hermes/claude-sonnet-4-6/001-.../
                             (Python loop, Hermes tool-use convention)

harness = browser-use   ──►  ./harness-output/browser-use/claude-sonnet-4-6/001-.../
                             (Playwright driver + atomic action primitives)
```

When the public runner is available, each adapter must emit the same documented recording contract before comparisons can be considered reproducible.

<br/>

# <img src="static/icons/layer-group.svg" width="28" height="28"> Architecture

<details>
<summary>How HarnessBench stacks on top of ClawBench</summary>

```
 ┌─────────────────────────────────────────────────────────┐
 │  harness-bench CLI                                      │
 │  (matrix expansion, credential gating, leaderboard)     │
 └───────────────────────┬─────────────────────────────────┘
                         │
                         ▼
 ┌─────────────────────────────────────────────────────────┐
 │  clawbench.harnesses  (plugin entry-point group)        │
 │  discovered at runtime via importlib.metadata           │
 └───────────────────────┬─────────────────────────────────┘
                         │
          ┌──────────────┼──────────────┬──────────────┐
          ▼              ▼              ▼              ▼
      openclaw         hermes        claw-code      browser-use      stagehand      coze-studio
      (Python)         (Python)      (Rust)         (Python)         (Node/TS)      (Web)
      dedicated        dedicated     dedicated      dedicated        dedicated      dedicated
      container        container     container      container        container      container
          │              │              │              │              │              │
          └──────────────┴──────────────┴──────────────┴──────────────┴──────────────┘
                                                 │
                                                 ▼
 ┌─────────────────────────────────────────────────────────┐
 │  clawbench/base:<version>                               │
 │  (Chrome + Xvfb + FFmpeg + extension-server + CDP wire) │
 │  Same image ClawBench uses -- zero drift.               │
 └─────────────────────────────────────────────────────────┘
```

Each harness ships its own `Dockerfile` (3-file adapter: `Dockerfile` + `setup.sh` + `run.sh`) that `FROM clawbench/base:<version>` so the shared stack is byte-for-byte identical across harnesses. See [`docs/adding-a-harness.md`](docs/adding-a-harness.md) for the walkthrough.

</details>

<br/>

# <img src="static/icons/terminal.svg" width="28" height="28"> CLI

```bash
# List and gate
harness-bench harnesses

# Matrix preview (no side effects)
harness-bench matrix --harness openclaw -h hermes -m claude-sonnet-4-6 -c 001-daily-life-food-uber-eats

# Execution boundary: this reports the unavailable public runner and exits before output
harness-bench run --harness openclaw --model claude-sonnet-4-6 --case 001-daily-life-food-uber-eats

# Batch planning remains available with --dry-run
harness-bench batch --dry-run -h openclaw -h hermes -h browser-use -m claude-sonnet-4-6 -c 001 -c 007

# Render leaderboard markdown
harness-bench leaderboard --results-dir ./harness-output/
```

<br/>

# <img src="static/icons/chart-bar.svg" width="28" height="28"> Evaluation

Evaluation is inherited verbatim from ClawBench -- post-session judge comparing agent trajectories against human reference runs under `eval/agentic_eval.md`.

```
 1. Run harnesses (batch)          2. Evaluate (clawbench eval)
 ─────────────────────────         ────────────────────────────────
 harness-bench batch ...    ──►    DOM-match + LLM judge re-used
 produces harness-output/          exactly as ClawBench does it
   with 5-layer recordings         (same rubric, same prompt)
```

See [ClawBench's eval guide](https://github.com/reacher-z/ClawBench/blob/main/eval/README.md) -- since the recording format is identical, every tool in ClawBench's `eval/` works unchanged on HarnessBench output.

<br/>

# <img src="static/icons/circle-question.svg" width="28" height="28"> FAQ

<details>
<summary><b>Why two repos instead of one tool with a <code>--harness</code> flag?</b></summary>

**Runtime incompatibility.** ClawBench's shared `openclaw-bench` container runs three Python harnesses side-by-side because they share a virtualenv. HarnessBench's six harnesses live in Python, Node/TS, Rust, and Web -- not co-installable in one image. Each gets its own container built on the shared `clawbench/base:<version>` image.

**Orthogonal axis.** ClawBench holds the harness fixed and sweeps models. HarnessBench holds the model fixed and sweeps harnesses. Same pipeline, different axis of interest -- keeping them as separate repos avoids overloading either CLI's flag surface.

</details>

<details>
<summary><b>Do I have to run cloud harnesses?</b></summary>

No. `stagehand` and `coze-studio` auto-skip without credentials and appear in the matrix as `skipped:missing_credential:<VAR>`. With all required variables set, they are eligible for preflight; execution remains unavailable for every harness until the public runner API lands.

</details>

<details>
<summary><b>Can I add my own harness?</b></summary>

Yes -- three files (`Dockerfile` + `setup.sh` + `run.sh`) plus one `pyproject.toml` stanza. See [`docs/adding-a-harness.md`](docs/adding-a-harness.md). The plugin loads via the `clawbench.harnesses` entry-point group, so external packages can register without forking either repo.

</details>

<details>
<summary><b>How is this different from ClawBench?</b></summary>

- **Axis.** ClawBench: one harness, many models. HarnessBench: many harnesses, one (or many) models.
- **Runtime.** ClawBench bundles three Python harnesses in one container. HarnessBench gives each harness its own container (Python / Node / Rust / Web are not co-installable).
- **Cloud.** ClawBench is fully local-first. HarnessBench supports local-first **and** cloud-opt-in harnesses in the same matrix.
- **Code reuse.** 100% -- HarnessBench imports `clawbench-eval` rather than forking it.

</details>

<details>
<summary><b>Which base model should I start with?</b></summary>

Use an explicitly named model for preflight. HarnessBench has no published result table or endorsed base model at this time; do not infer comparative performance from a model identifier in an example command.

</details>

<br/>

## Contributing

We welcome adapters for new harnesses. Most harness adapters are a single directory under `src/harnessbench/harnesses/` with three files; see [`docs/adding-a-harness.md`](docs/adding-a-harness.md) for the walkthrough and [`CONTRIBUTING.md`](CONTRIBUTING.md) for evidence and test expectations.

**Quick wins:**

- [Add a new harness adapter](docs/adding-a-harness.md) (~1-2 hours if upstream ships a CLI, ~1 day if you're writing one from scratch)
- Submit a leaderboard entry for a harness + model pair we haven't scored
- File a [good first issue](https://github.com/reacher-z/HarnessBench/labels/good%20first%20issue)

## Community

<table>
<tr>
<td align="center" width="33%">
<a href="https://discord.gg/clawbench">
<img src="https://img.shields.io/badge/Discord-Join-5865F2?style=for-the-badge&logo=discord&logoColor=white" alt="Discord">
</a>
<br/>
<sub><b>English community</b><br/>Shared with ClawBench</sub>
</td>
<td align="center" width="33%">
<a href="https://github.com/reacher-z/ClawBench/blob/main/docs/community.md#%E5%BE%AE%E4%BF%A1%E7%BE%A4-chinese">
<img src="https://img.shields.io/badge/%E5%BE%AE%E4%BF%A1%E7%BE%A4-%E5%8A%A0%E5%85%A5-07C160?style=for-the-badge&logo=wechat&logoColor=white" alt="微信群">
</a>
<br/>
<sub><b>中文社区</b><br/>研究者、开发者、贡献者交流</sub>
</td>
<td align="center" width="33%">
<a href="https://github.com/reacher-z/HarnessBench/issues">
<img src="https://img.shields.io/badge/GitHub-Issues-181717?style=for-the-badge&logo=github&logoColor=white" alt="GitHub Issues">
</a>
<br/>
<sub><b>Issue tracking</b><br/>Reproducible bugs and feature requests</sub>
</td>
</tr>
</table>

## License

Apache-2.0 for the repository. Each bundled harness adapter links to upstream code under the upstream's own license; nothing from an incompatible license is vendored.

## Citation

<!-- Placeholder: replace with full arXiv block once preprint is submitted. -->

If you use HarnessBench in your research, please cite:

```bibtex
@misc{zhang2026harnessbench,
  title        = {HarnessBench: Comparing Agentic Harnesses on Everyday Online Tasks},
  author       = {Yuxuan Zhang and Yubo Wang and Yipeng Zhu and Penghui Du and Junwen Miao and Xuan Lu and Wendong Xu and Yunzhuo Hao and Songcheng Cai and Xiaochen Wang and Huaisong Zhang and Xian Wu and Yi Lu and Minyi Lei and Kai Zou and Huifeng Yin and Ping Nie and Liang Chen and Dongfu Jiang and Wenhu Chen and Kelsey R. Allen},
  year         = {2026},
  note         = {Preprint in preparation},
  howpublished = {\url{https://github.com/reacher-z/HarnessBench}}
}
```

## Core Contributors

<table>
<tr>
<td align="center">
<a href="https://github.com/reacher-z">
<img src="https://github.com/reacher-z.png" width="80" height="80" style="border-radius:50%"><br/>
<sub><b>Yuxuan Zhang</b></sub>
</a>
</td>
<td align="center">
<a href="https://github.com/Wyyyb">
<img src="https://github.com/Wyyyb.png" width="80" height="80" style="border-radius:50%"><br/>
<sub><b>Yubo Wang</b></sub>
</a>
</td>
<td align="center">
<a href="https://github.com/Perry2004">
<img src="https://github.com/Perry2004.png" width="80" height="80" style="border-radius:50%"><br/>
<sub><b>Perry Zhu</b></sub>
</a>
</td>
<td align="center">
<a href="https://github.com/eternaldolphin">
<img src="https://github.com/eternaldolphin.png" width="80" height="80" style="border-radius:50%"><br/>
<sub><b>Penghui Du</b></sub>
</a>
</td>
<td align="center">
<a href="https://github.com/MEKSAAA">
<img src="https://github.com/MEKSAAA.png" width="80" height="80" style="border-radius:50%"><br/>
<sub><b>Junwen Miao</b></sub>
</a>
</td>
</tr>
</table>

## Advisors

<table>
<tr>
<td align="center">
<a href="https://github.com/k-r-allen">
<img src="https://github.com/k-r-allen.png" width="80" height="80" style="border-radius:50%"><br/>
<sub><b>Kelsey R. Allen</b></sub>
</a>
</td>
<td align="center">
<a href="https://github.com/wenhuchen">
<img src="https://github.com/wenhuchen.png" width="80" height="80" style="border-radius:50%"><br/>
<sub><b>Wenhu Chen</b></sub>
</a>
</td>
<td align="center">
<a href="https://github.com/jdf-prog">
<img src="https://github.com/jdf-prog.png" width="80" height="80" style="border-radius:50%"><br/>
<sub><b>Dongfu Jiang</b></sub>
</a>
</td>
<td align="center">
<a href="https://github.com/chenllliang">
<img src="https://github.com/chenllliang.png" width="80" height="80" style="border-radius:50%"><br/>
<sub><b>Liang Chen</b></sub>
</a>
</td>
</tr>
</table>

## Support HarnessBench

If HarnessBench is useful for your research or tool selection,
the single most helpful thing you can do is **[star the repo](https://github.com/reacher-z/HarnessBench)** --
it surfaces the harness-comparison axis to other agent researchers and helps us justify
continued adapter work.

<p align="center">
<a href="https://github.com/reacher-z/HarnessBench">
<img src="https://img.shields.io/badge/%E2%98%85%20Star%20this%20repo-181717?style=for-the-badge&logo=github&logoColor=white" alt="Star this repo">
</a>
</p>

Open to contributions -- new harness adapters, leaderboard submissions, or evaluation bug fixes. See [CONTRIBUTING.md](CONTRIBUTING.md).

<p align="center">
<a href="https://github.com/reacher-z/HarnessBench/graphs/contributors">
<img src="https://contrib.rocks/image?repo=reacher-z/HarnessBench" alt="Contributors">
</a>
</p>

## Star History

<a href="https://star-history.com/#reacher-z/HarnessBench&Date">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=reacher-z/HarnessBench&type=Date&theme=dark" />
    <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=reacher-z/HarnessBench&type=Date" />
    <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=reacher-z/HarnessBench&type=Date" />
  </picture>
</a>
