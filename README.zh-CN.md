<div align="center">

<a href="https://github.com/reacher-z/HarnessBench">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="static/hero-dark.svg">
    <img alt="HarnessBench" src="static/hero-light.svg" width="820">
  </picture>
</a>

<p align="center">
  <strong>在同一套日常在线任务上比较不同 Agent Harness 的基准</strong><br>
  <a href="docs/adding-a-harness.md">阅读文档</a>
  &nbsp;·&nbsp;
  <a href="docs/harness-comparison.md">Harness 对比</a>
  &nbsp;·&nbsp;
  <a href="docs/cloud-harness-setup.md">云端配置</a>
</p>

<p align="center">
  <a href="https://github.com/reacher-z/HarnessBench"><img alt="Star this repo" src="https://img.shields.io/badge/%E2%98%85%20Star%20this%20repo-181717?style=flat-square&logo=github&logoColor=white" /></a>
  <a href="https://harness-eval.com"><img alt="Project Page" src="https://img.shields.io/badge/harness--eval.com-D97706?style=flat-square&logo=googlechrome&logoColor=white" /></a>
  <a href="https://github.com/reacher-z/HarnessBench"><img alt="GitHub stars" src="https://img.shields.io/github/stars/reacher-z/HarnessBench?style=flat-square&logo=github&color=181717&cacheSeconds=300" /></a>
  <a href="https://discord.gg/clawbench"><img alt="Discord" src="https://img.shields.io/badge/Discord-%E5%8A%A0%E5%85%A5-5865F2?style=flat-square&logo=discord&logoColor=white" /></a>
  <a href="https://codespaces.new/reacher-z/HarnessBench?quickstart=1"><img alt="Codespaces" src="https://img.shields.io/badge/Codespaces-Open-181717?style=flat-square&logo=github&logoColor=white" /></a>
</p>

<p align="center">
  <a href="https://github.com/reacher-z/ClawBench"><img src="https://img.shields.io/badge/Sister%20Project%20%E2%86%92%20ClawBench-D97706?style=for-the-badge&labelColor=0F172A&color=F59E0B" alt="姊妹项目 ClawBench" /></a>
</p>

<p align="center">
  <a href="https://deepwiki.com/reacher-z/HarnessBench"><img alt="Ask DeepWiki" src="https://deepwiki.com/badge.svg" /></a>
</p>

<p align="center">
  想固定 Harness、比较不同<i>基础模型</i>？去看我们的姊妹项目
  <a href="https://github.com/reacher-z/ClawBench"><b>ClawBench</b></a>
  &nbsp;&mdash;&nbsp; 同一套评测流水线，正交维度。
</p>

<a href="#-human-quick-start"><img src="https://img.shields.io/badge/%E4%B8%80%E8%A1%8C%E5%91%BD%E4%BB%A4%E8%BF%90%E8%A1%8C-D97706?style=for-the-badge&labelColor=D97706&logoColor=white&logo=data:image/svg%2Bxml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCA1NzYgNTEyIj48cGF0aCBmaWxsPSIjZmZmZmZmIiBkPSJNMjYzLjQtMjdMMjc4LjIgOS44IDMxNSAyNC42YzMgMS4yIDUgNC4yIDUgNy40cy0yIDYuMi01IDcuNEwyNzguMiA1NC4yIDI2My40IDkxYy0xLjIgMy00LjIgNS03LjQgNXMtNi4yLTItNy40LTVMMjMzLjggNTQuMiAxOTcgMzkuNGMtMy0xLjItNS00LjItNS03LjRzMi02LjIgNS03LjRMMjMzLjggOS44IDI0OC42LTI3YzEuMi0zIDQuMi01IDcuNC01czYuMiAyIDcuNCA1ek0xMTAuNyA0MS43bDIxLjUgNTAuMSA1MC4xIDIxLjVjNS45IDIuNSA5LjcgOC4zIDkuNyAxNC43cy0zLjggMTIuMi05LjcgMTQuN2wtNTAuMSAyMS41LTIxLjUgNTAuMWMtMi41IDUuOS04LjMgOS43LTE0LjcgOS43cy0xMi4yLTMuOC0xNC43LTkuN0w1OS44IDE2NC4yIDkuNyAxNDIuN0MzLjggMTQwLjIgMCAxMzQuNCAwIDEyOHMzLjgtMTIuMiA5LjctMTQuN0w1OS44IDkxLjggODEuMyA0MS43QzgzLjggMzUuOCA4OS42IDMyIDk2IDMyczEyLjIgMy44IDE0LjcgOS43ek00NjQgMzA0YzYuNCAwIDEyLjIgMy44IDE0LjcgOS43bDIxLjUgNTAuMSA1MC4xIDIxLjVjNS45IDIuNSA5LjcgOC4zIDkuNyAxNC43cy0zLjggMTIuMi05LjcgMTQuN2wtNTAuMSAyMS41LTIxLjUgNTAuMWMtMi41IDUuOS04LjMgOS43LTE0LjcgOS43cy0xMi4yLTMuOC0xNC43LTkuN2wtMjEuNS01MC4xLTUwLjEtMjEuNWMtNS45LTIuNS05LjctOC4zLTkuNy0xNC43czMuOC0xMi4yIDkuNy0xNC43bDUwLjEtMjEuNSAyMS41LTUwLjFjMi41LTUuOSA4LjMtOS43IDE0LjctOS43ek00NjAgMGMxMSAwIDIxLjYgNC40IDI5LjUgMTIuMmw0Mi4zIDQyLjNDNTM5LjYgNjIuNCA1NDQgNzMgNTQ0IDg0cy00LjQgMjEuNi0xMi4yIDI5LjVsLTg4LjIgODguMi0xMDEuMy0xMDEuMyA4OC4yLTg4LjJDNDM4LjQgNC40IDQ0OSAwIDQ2MCAwek00NC4yIDM5OC41TDMwOC40IDEzNC4zIDQwOS43IDIzNS42IDE0NS41IDQ5OS44QzEzNy42IDUwNy42IDEyNyA1MTIgMTE2IDUxMnMtMjEuNi00LjQtMjkuNS0xMi4yTDQ0LjIgNDU3LjVDMzYuNCA0NDkuNiAzMiA0MzkgMzIgNDI4czQuNC0yMS42IDEyLjItMjkuNXoiLz48L3N2Zz4=" alt="一行命令运行"></a>

```bash
uv tool install harness-bench && harness-bench
```

<sub><i>安装 &rarr; 列出 &rarr; 运行。 &nbsp; 复用 ClawBench 的流水线。 &nbsp; 云端 Harness 通过环境变量可选启用。</i></sub>

### 同一个任务，哪种 Harness 能把事情做完？

给定一个日常在线任务（订外卖、订机票、投简历）、**一个固定的基础模型** --<br/>
到底哪种 agentic harness 真的能完成？<br/>
**六个命名 Harness**，四种运行时，一套流水线，一个排行榜。

---

**6** 个 Harness &nbsp;&middot;&nbsp; **4** 种运行时（Python / Node / Rust / Web） &nbsp;&middot;&nbsp; **153** 个共享任务 &nbsp;&middot;&nbsp; **15** 个生活类别

<a href="README.md"><img src="static/icons/language.svg" width="16" height="16"> English</a>

</div>

<br/>

<p align="center">
<img src="static/icons/layer-group.svg" width="24" height="24">&nbsp;<b>Plugin 入口点</b>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
<img src="static/icons/cube.svg" width="24" height="24">&nbsp;<b>每个 Harness 独立容器</b>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
<img src="static/icons/shield-halved.svg" width="24" height="24">&nbsp;<b>云端 Harness 可选</b>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
<img src="static/icons/globe.svg" width="24" height="24">&nbsp;<b>复用 ClawBench 流水线</b>
</p>

<br/>

## 它是怎么跑的

```
   你挑一个 ClawBench 的        HarnessBench 为每个         每个 Harness 用            五层录制 + DOM 判决
   共享任务（共 153 个）         Harness 起一个独立容器      自己的方式驱动浏览器        + LLM 判决，结果按
                                （Python/Node/Rust/Web）                              harness 分区

   ┌──────────────┐            ┌──────────────┐            ┌──────────────┐          ┌──────────────┐
   │ "在 Expedia  │    ──►     │   6 个容器    │     ──►    │   6 个不同    │   ──►   │  按 harness  │
   │  上订机票"   │            │  每个 harness │            │   agent loop │          │   分区的     │
   │              │            │   一个        │            │   同一任务    │          │   排行榜     │
   └──────────────┘            └──────────────┘            └──────────────┘          └──────────────┘
```

<br/>

# <img src="static/icons/robot.svg" width="28" height="28"> LLM Quick Start

把你的编码 Agent（Claude Code、Cursor、Copilot 等）指向 [`AGENTS.md`](AGENTS.md) 就可以提问。HarnessBench 与 ClawBench 共享测试用例、容器底座、五层录制栈 -- 如果你的 Agent 已经熟悉 ClawBench，那对流水线就没有新东西要学，只是多了一个 harness 维度。

<br/>

# <img src="static/icons/person.svg" width="28" height="28"> Human Quick Start

```bash
# 方式 A -- PyPI 安装（推荐）
uv tool install harness-bench && harness-bench
```

```bash
# 方式 B -- 克隆仓库（贡献者 / 新增 harness）
git clone https://github.com/reacher-z/HarnessBench.git && cd HarnessBench && uv run harness-bench
```

**前置依赖：** [Python 3.10+](https://python.org)、[uv](https://docs.astral.sh/uv/)，以及一个容器引擎 -- [Docker](https://www.docker.com/) **或** [Podman](https://podman.io/)。和 ClawBench 一样会自动探测；通过 `export CONTAINER_ENGINE=docker` 强制选择。

**1. 列出已注册的 Harness：**

```bash
harness-bench harnesses
# openclaw       ready
# hermes         ready
# claw-code      ready
# browser-use    ready
# stagehand      skipped: set BROWSERBASE_API_KEY
# coze-studio    skipped: set COZE_INSTANCE_URL, COZE_API_TOKEN
```

**2. 预览将要运行的 matrix**（无副作用）：

```bash
harness-bench matrix \
    --harness openclaw --harness hermes --harness browser-use \
    --model   claude-sonnet-4-6 \
    --case    001-daily-life-food-uber-eats \
    --case    007-daily-life-travel-expedia
```

**3. 端到端跑一组 triple：**

```bash
harness-bench run \
    --harness openclaw \
    --model   claude-sonnet-4-6 \
    --case    001-daily-life-food-uber-eats
```

结果落在 `./harness-output/<harness>/<model>/<case>-<timestamp>/`，包含完整的五层录制 -- 目录结构和 ClawBench 完全一致，所以一份分析脚本两边通用。

**4. Matrix 批跑**（跑完所有合格的 triple）：

```bash
harness-bench batch \
    --harness openclaw --harness hermes --harness browser-use --harness claw-code \
    --model   claude-sonnet-4-6 \
    --case    $(cat fixtures/lite.txt)
```

**5. 渲染排行榜：**

```bash
harness-bench leaderboard --results-dir ./harness-output/
```

<br/>

# <img src="static/icons/cube.svg" width="28" height="28"> 六个命名 Harness

| Harness | 上游 | 运行时 | 云端？ | 是什么 |
|---------|------|:------:|:------:|--------|
| `openclaw` | [reacher-z/ClawBench](https://github.com/reacher-z/ClawBench) | Python | &mdash; | 参考 Harness，与 ClawBench 共享。所有对比的基线。 |
| `hermes` | [nousresearch/hermes-agent](https://github.com/nousresearch/hermes-agent) | Python | &mdash; | Hermes 风格的 tool-use 循环，带显式 plan/act 步骤。 |
| `claw-code` | [ultraworkers/claw-code](https://github.com/ultraworkers/claw-code) | Rust | &mdash; | 原生 Rust agent 循环，无 GIL 并发。 |
| `browser-use` | [browser-use/browser-use](https://github.com/browser-use/browser-use) | Python | &mdash; | 社区热门的 Playwright-based harness。 |
| `stagehand` | [browserbase/stagehand](https://github.com/browserbase/stagehand) | Node/TS | **是** | BrowserBase 的 Stagehand -- 需要 `BROWSERBASE_API_KEY`。 |
| `coze-studio` | [coze-dev/coze-studio](https://github.com/coze-dev/coze-studio) | Web | **是** | Coze Studio 流程执行器 -- 需要 `COZE_INSTANCE_URL` + `COZE_API_TOKEN`。 |

云端 Harness **可选启用**：未提供凭证时在 matrix 中标记为 `skipped:missing_credential:<VAR>` -- **绝不会被静默记 0 分**。更多 Harness 通过独立 PR 加入；见 [`docs/scout-2026-04-16.md`](docs/scout-2026-04-16.md)。

<br/>

# <img src="static/icons/chart-bar.svg" width="28" height="28"> 排行榜预览

<div align="center">

**Work in progress。** 在 `claude-sonnet-4-6` 上跑六个 Harness 的首轮结果还在路上 -- 下表仅展示排行榜形态。

</div>

| 排名 | Harness | 总体 | Daily | Travel | Work | Dev | 备注 |
|:----:|---------|:----:|:-----:|:------:|:----:|:---:|------|
| &mdash; | `openclaw` | TBD | TBD | TBD | TBD | TBD | 参考 harness（ClawBench） |
| &mdash; | `hermes` | TBD | TBD | TBD | TBD | TBD | Python tool-use 循环 |
| &mdash; | `claw-code` | TBD | TBD | TBD | TBD | TBD | Rust agent 循环 |
| &mdash; | `browser-use` | TBD | TBD | TBD | TBD | TBD | Playwright-based |
| &mdash; | `stagehand` | TBD | TBD | TBD | TBD | TBD | 云端可选 |
| &mdash; | `coze-studio` | TBD | TBD | TBD | TBD | TBD | 云端可选 |

<sub><i>分区：<code>(harness, model, category)</code>。在本地 <code>harness-bench leaderboard</code> 就能渲染自己的。</i></sub>

<br/>

# <img src="static/icons/circle-question.svg" width="28" height="28"> 示例走查

好奇一个 triple 到底长什么样？看同一个基础模型下，**任务 001** 跑在 **三种不同 Harness** 上：

```
task    = 001-daily-life-food-uber-eats
model   = claude-sonnet-4-6

harness = openclaw      ──►  ./harness-output/openclaw/claude-sonnet-4-6/001-.../
                             （Python 循环，通过 ClawBench 扩展驱动 Chrome）

harness = hermes        ──►  ./harness-output/hermes/claude-sonnet-4-6/001-.../
                             （Python 循环，Hermes tool-use 约定）

harness = browser-use   ──►  ./harness-output/browser-use/claude-sonnet-4-6/001-.../
                             （Playwright 驱动 + 原子 action 原语）
```

三种 Harness 落盘的都是 **同一份五层 bundle**（recording.mp4、screenshots、actions.jsonl、requests.jsonl、agent-messages.jsonl），外加 ClawBench CDP 级拦截器产出的 `interception.json`。这种一致性就是跨-Harness 对比有意义的前提：输入一样、judge 一样、rubric 一样 -- 变的只有 agent loop 本身。

<br/>

# <img src="static/icons/layer-group.svg" width="28" height="28"> 架构

<details>
<summary>HarnessBench 如何叠在 ClawBench 之上</summary>

```
 ┌─────────────────────────────────────────────────────────┐
 │  harness-bench CLI                                      │
 │  (matrix 展开、凭证门禁、排行榜)                          │
 └───────────────────────┬─────────────────────────────────┘
                         │
                         ▼
 ┌─────────────────────────────────────────────────────────┐
 │  clawbench.harnesses  (entry-point 插件组)              │
 │  运行时通过 importlib.metadata 发现                      │
 └───────────────────────┬─────────────────────────────────┘
                         │
          ┌──────────────┼──────────────┬──────────────┐
          ▼              ▼              ▼              ▼
      openclaw         hermes        claw-code      browser-use      stagehand      coze-studio
      (Python)         (Python)      (Rust)         (Python)         (Node/TS)      (Web)
      独立容器          独立容器       独立容器        独立容器          独立容器        独立容器
          │              │              │              │              │              │
          └──────────────┴──────────────┴──────────────┴──────────────┴──────────────┘
                                                 │
                                                 ▼
 ┌─────────────────────────────────────────────────────────┐
 │  clawbench/base:<version>                               │
 │  (Chrome + Xvfb + FFmpeg + extension-server + CDP)      │
 │  与 ClawBench 使用同一镜像 -- 零漂移。                   │
 └─────────────────────────────────────────────────────────┘
```

每个 Harness 自带 `Dockerfile`（3 文件适配器：`Dockerfile` + `setup.sh` + `run.sh`），都 `FROM clawbench/base:<version>`，所以共享栈跨 harness 逐字节一致。适配器做法见 [`docs/adding-a-harness.md`](docs/adding-a-harness.md)。

</details>

<br/>

# <img src="static/icons/terminal.svg" width="28" height="28"> CLI

```bash
# 列出 + 门禁
harness-bench harnesses

# Matrix 预览（无副作用）
harness-bench matrix --harness openclaw -h hermes -m claude-sonnet-4-6 -c 001-daily-life-food-uber-eats

# 单次运行
harness-bench run --harness openclaw --model claude-sonnet-4-6 --case 001-daily-life-food-uber-eats

# 批跑（matrix 展开，跳过不合格的，跑剩下的）
harness-bench batch -h openclaw -h hermes -h browser-use -m claude-sonnet-4-6 -c 001 -c 007

# 渲染排行榜 markdown
harness-bench leaderboard --results-dir ./harness-output/
```

<br/>

# <img src="static/icons/chart-bar.svg" width="28" height="28"> 评测

评测逻辑完全继承 ClawBench -- post-session judge，用 `eval/agentic_eval.md` 的 rubric 对比 agent 轨迹和人工参考轨迹。

```
 1. 跑 Harness（batch）           2. 评测（clawbench eval）
 ─────────────────────────         ────────────────────────────────
 harness-bench batch ...    ──►   复用 DOM-match + LLM judge
 产出 harness-output/              （rubric 和 prompt 都和 ClawBench
   包含五层录制                      逐字一致）
```

见 [ClawBench 的评测指南](https://github.com/reacher-z/ClawBench/blob/main/eval/README.md) -- 录制格式一致，ClawBench `eval/` 目录里的每个工具都能直接在 HarnessBench 的输出上跑。

<br/>

# <img src="static/icons/circle-question.svg" width="28" height="28"> FAQ

<details>
<summary><b>为什么要分两个仓库，而不是一个工具加 <code>--harness</code> flag？</b></summary>

**运行时不兼容。** ClawBench 的共享 `openclaw-bench` 容器能把三个 Python harness 塞进同一个虚拟环境。HarnessBench 的六个 Harness 跨越 Python、Node/TS、Rust、Web -- 不可能共存于一个镜像。每个 Harness 都有自己的容器，但都 `FROM` 共享的 `clawbench/base:<version>`。

**维度正交。** ClawBench 固定 harness 扫模型；HarnessBench 固定模型扫 harness。同一套流水线，关注的维度不一样 -- 分仓库避免任一方 CLI 的 flag 面板被拖肿。

</details>

<details>
<summary><b>必须跑云端 Harness 吗？</b></summary>

不用。`stagehand` 和 `coze-studio` 在没有凭证时会自动跳过，在 matrix 中显示为 `skipped:missing_credential:<VAR>`。四个本地优先的 Harness（`openclaw`、`hermes`、`claw-code`、`browser-use`）足够在任何装了 Docker 的工作站上产出有意义的排行榜。

</details>

<details>
<summary><b>能加自己的 Harness 吗？</b></summary>

可以 -- 三个文件（`Dockerfile` + `setup.sh` + `run.sh`）加一段 `pyproject.toml`。走查见 [`docs/adding-a-harness.md`](docs/adding-a-harness.md)。Plugin 通过 `clawbench.harnesses` entry-point group 加载，外部包不需要 fork 任何一个仓库就能注册。

</details>

<details>
<summary><b>和 ClawBench 的差异？</b></summary>

- **维度。** ClawBench：单 harness × 多模型；HarnessBench：多 harness × 单（或多）模型。
- **运行时。** ClawBench 在同一个容器里装三个 Python harness；HarnessBench 为每个 harness 分配独立容器（Python / Node / Rust / Web 不可共存）。
- **云端。** ClawBench 完全本地优先；HarnessBench 同时支持本地 **和** 云端可选 harness。
- **代码复用。** 100% -- HarnessBench 直接 import `clawbench-eval`，不 fork。

</details>

<details>
<summary><b>应该从哪个基础模型开始？</b></summary>

用你已经信任的模型。HarnessBench 的重点是固定一个模型，观察不同 harness 把它包起来会怎么样。对外公布的数字我们用 `claude-sonnet-4-6`（ClawBench 的榜首，33.3% 总分），它给每个 harness 提供一个已知有竞争力的底座。自己跑时 `models.yaml` 里的任何模型都可以。

</details>

<br/>

## 贡献

欢迎新 harness 适配器，尤其是能通过 [30-agent 全球扫描](docs/scout-2026-04-16.md) 的。多数适配器就是 `src/harnessbench/harnesses/` 下一个目录加三个文件；走查见 [`docs/adding-a-harness.md`](docs/adding-a-harness.md)。

**快速贡献：**

- [新增 Harness 适配器](docs/adding-a-harness.md)（若上游有 CLI 约 1-2 小时，若从零写约 1 天）
- 提交我们还没跑过的 harness + model 对的排行榜条目
- 挑一个 [good first issue](https://github.com/reacher-z/HarnessBench/labels/good%20first%20issue)

## 社区

<table>
<tr>
<td align="center" width="33%">
<a href="https://discord.gg/clawbench">
<img src="https://img.shields.io/badge/Discord-Join-5865F2?style=for-the-badge&logo=discord&logoColor=white" alt="Discord">
</a>
<br/>
<sub><b>英文社区</b><br/>与 ClawBench 共享</sub>
</td>
<td align="center" width="33%">
<a href="https://github.com/reacher-z/ClawBench/blob/main/docs/community.md#%E5%BE%AE%E4%BF%A1%E7%BE%A4-chinese">
<img src="https://img.shields.io/badge/%E5%BE%AE%E4%BF%A1%E7%BE%A4-%E5%8A%A0%E5%85%A5-07C160?style=for-the-badge&logo=wechat&logoColor=white" alt="微信群">
</a>
<br/>
<sub><b>中文社区</b><br/>研究者、开发者、贡献者交流</sub>
</td>
<td align="center" width="33%">
<a href="https://github.com/reacher-z/HarnessBench/discussions">
<img src="https://img.shields.io/badge/GitHub-Discussions-181717?style=for-the-badge&logo=github&logoColor=white" alt="GitHub Discussions">
</a>
<br/>
<sub><b>异步问答</b><br/>可搜索、长文、永久</sub>
</td>
</tr>
</table>

## 许可证

仓库整体 Apache-2.0。每个内置 harness 适配器只链接到上游代码，上游保持各自许可证；不兼容许可证的代码一概不 vendor。

## 引用

<!-- Placeholder: replace with full arXiv block once preprint is submitted. -->

如果 HarnessBench 对你的研究有帮助，请引用：

```bibtex
@misc{zhang2026harnessbench,
  title        = {HarnessBench: Comparing Agentic Harnesses on Everyday Online Tasks},
  author       = {Yuxuan Zhang and Yubo Wang and Yipeng Zhu and Penghui Du and Junwen Miao and Xuan Lu and Wendong Xu and Yunzhuo Hao and Songcheng Cai and Xiaochen Wang and Huaisong Zhang and Xian Wu and Yi Lu and Minyi Lei and Kai Zou and Huifeng Yin and Ping Nie and Liang Chen and Dongfu Jiang and Wenhu Chen and Kelsey R. Allen},
  year         = {2026},
  note         = {Preprint in preparation},
  howpublished = {\url{https://github.com/reacher-z/HarnessBench}}
}
```

## 核心贡献者

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

## 指导

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

## 支持 HarnessBench

如果 HarnessBench 对你的研究或工具选型有用，
帮助最大的一件事就是 **[给仓库加星](https://github.com/reacher-z/HarnessBench)** --
这能让更多 agent 研究者看到 harness 对比这条轴，也让我们有理由继续投入适配器工作。

<p align="center">
<a href="https://github.com/reacher-z/HarnessBench">
<img src="https://img.shields.io/badge/%E2%98%85%20Star%20this%20repo-181717?style=for-the-badge&logo=github&logoColor=white" alt="Star this repo">
</a>
</p>

欢迎贡献 -- 新 harness 适配器、排行榜提交、评测 bug 修复。见 [CONTRIBUTING.md](CONTRIBUTING.md)。

<p align="center">
<a href="https://github.com/reacher-z/HarnessBench/graphs/contributors">
<img src="https://contrib.rocks/image?repo=reacher-z/HarnessBench" alt="Contributors">
</a>
</p>

## Star 历史

<a href="https://star-history.com/#reacher-z/HarnessBench&Date">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=reacher-z/HarnessBench&type=Date&theme=dark" />
    <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=reacher-z/HarnessBench&type=Date" />
    <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=reacher-z/HarnessBench&type=Date" />
  </picture>
</a>
