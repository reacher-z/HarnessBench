<div align="center">

# HarnessBench

<p align="center">
  <strong>在日常在线任务上比较不同的 Agent Harness</strong><br>
  <a href="docs/adding-a-harness.md">阅读文档</a>
  &nbsp;·&nbsp;
  <a href="docs/harness-comparison.md">Harness 对比</a>
  &nbsp;·&nbsp;
  <a href="docs/cloud-harness-setup.md">云端配置</a>
</p>

<p align="center">
  <a href="https://github.com/reacher-z/HarnessBench/blob/main/LICENSE"><img alt="License" src="https://img.shields.io/badge/License-Apache%202.0-181717?style=flat-square&labelColor=000" /></a>
  <a href="https://pypi.org/project/harness-bench/"><img alt="PyPI" src="https://img.shields.io/badge/pypi-harness--bench-3775A9?style=flat-square&logo=pypi&logoColor=white&labelColor=000" /></a>
  <a href="https://www.python.org/downloads/"><img alt="Python 3.10+" src="https://img.shields.io/badge/python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white&labelColor=000" /></a>
  <a href="https://github.com/reacher-z/HarnessBench"><img alt="GitHub stars" src="https://img.shields.io/github/stars/reacher-z/HarnessBench?style=flat-square&logo=github&color=181717&cacheSeconds=300" /></a>
  <a href="https://discord.gg/clawbench"><img alt="Discord" src="https://img.shields.io/badge/Discord-%E5%8A%A0%E5%85%A5%E7%A4%BE%E5%8C%BA-00D26A?style=flat-square&logo=discord&logoColor=white&labelColor=000" /></a>
</p>

<p align="center">
  <a href="https://github.com/reacher-z/ClawBench"><img src="https://img.shields.io/badge/%F0%9F%94%97%20ClawBench%20%E5%A7%8A%E5%A6%B9%E9%A1%B9%E7%9B%AE-181717?style=for-the-badge&labelColor=6C2BD9&color=FFD21E" alt="ClawBench 姊妹项目" /></a>
</p>

<p align="center">
  <a href="https://deepwiki.com/reacher-z/HarnessBench"><img alt="Ask DeepWiki" src="https://deepwiki.com/badge.svg" /></a>
</p>

<p align="center">
  想固定 Harness、比较不同<i>基础模型</i>？看看我们的姊妹项目
  <a href="https://github.com/reacher-z/ClawBench"><b>ClawBench</b></a>
  &nbsp;—&nbsp; 同一套评测流水线，正交维度。
</p>

[English](README.md) &nbsp;·&nbsp; [简体中文](README.zh-CN.md)

</div>

---

## 它回答什么问题

给定一个日常在线任务（订机票、退订推送、比较三台笔记本），以及一个固定的基础模型，到底哪种 agentic harness 真的能把事情做完？

HarnessBench 用**同样的任务**、跑**不同的 harness**、走**同一套评分流水线**（5 层录制、DOM-match judge、LLM judge），再按 `(harness, model, task)` 拆分排行榜。

## 六个默认支持的 Harness

| Harness | 上游 | 语言 | 需要云端？ | 备注 |
|---------|------|------|------------|------|
| `openclaw` | [reacher-z/ClawBench](https://github.com/reacher-z/ClawBench) | Python | 否 | 参考 harness，与 ClawBench 共享。|
| `hermes` | [nousresearch/hermes-agent](https://github.com/nousresearch/hermes-agent) | Python | 否 | Hermes 风格的 tool-use 循环。|
| `claw-code` | [ultraworkers/claw-code](https://github.com/ultraworkers/claw-code) | Rust | 否 | 原生 Rust agent loop。|
| `browser-use` | [browser-use/browser-use](https://github.com/browser-use/browser-use) | Python | 否 | 社区热门的 Playwright-based harness。|
| `stagehand` | [browserbase/stagehand](https://github.com/browserbase/stagehand) | Node/TS | **是** | 需要 `BROWSERBASE_API_KEY`。|
| `coze-studio` | [coze-dev/coze-studio](https://github.com/coze-dev/coze-studio) | Web | **是** | 需要 `COZE_INSTANCE_URL`、`COZE_API_TOKEN`。|

云端 harness **可选启用**。未提供凭证时，它们会在 matrix 中显示为 `skipped:missing_credential:<VAR>`，绝不会被静默记 0 分。

另有 30-agent 全网扫描产出的候选框架（见 `docs/scout-2026-04-16.md`），通过资质门槛的项目以独立 PR 形式加入。

## 安装

```bash
pip install harness-bench
```

HarnessBench 把 [`clawbench-eval`](https://pypi.org/project/clawbench-eval/) 当作库使用：容器编排、5 层录制、评分流水线都在那边。

## 快速上手

```bash
# 列出已注册的 harness
harness-bench harnesses

# 预览将要运行的 matrix（已经应用云端 gating）
harness-bench matrix --harnesses openclaw,hermes,browser-use --models gpt-4o-mini

# 端到端跑一组 triple
harness-bench run \
    --harness openclaw \
    --model  gpt-4o-mini \
    --case   ./fixtures/book-a-flight.json

# 从结果目录渲染 Markdown 排行榜
harness-bench leaderboard ./harness-output/
```

## 新增 Harness

HarnessBench 通过 `clawbench.harnesses` entry point 发现 harness。添加一个新 harness = 3 个文件 + `pyproject.toml` 一段声明。详细步骤见 [`docs/adding-a-harness.md`](docs/adding-a-harness.md)。

## 云端 Harness 凭证

详细步骤见 [`docs/cloud-harness-setup.md`](docs/cloud-harness-setup.md)。简版：

```bash
export BROWSERBASE_API_KEY=...              # 启用 stagehand
export COZE_INSTANCE_URL=https://...        # 启用 coze-studio
export COZE_API_TOKEN=...                   # 必须和 URL 一起设置
```

其他凭证（OpenAI、Anthropic 等）按所选基础模型需要设置，和 ClawBench 的环境变量约定一致。

## 与 ClawBench 的差异

- **维度。** ClawBench：单 harness × 多模型；HarnessBench：多 harness × 单（或多）模型。
- **运行时。** ClawBench 在同一个容器里装三个 Python harness；HarnessBench 为每个 harness 分配独立容器（Python / Node / Rust / Web 不可共存）。
- **云端。** ClawBench 完全本地优先；HarnessBench 支持本地 + 云端可选 harness 混合 matrix。
- **代码复用。** 100%——HarnessBench 直接 import `clawbench-eval`，不 fork。

## 许可证

仓库整体 Apache-2.0。每个内置 harness 适配器只链接到上游代码，上游保持各自许可证；不兼容许可证的代码一概不 vendor。

## 引用

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
