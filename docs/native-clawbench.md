# Run through ClawBench's public CLI

The default `plugin` backend retains the planned `clawbench.run_case` API.
For ClawBench releases that expose `clawbench-run` instead, select the explicit
`clawbench-cli` backend:

```sh
harness-bench run --backend clawbench-cli \
  --harness browser-use --model YOUR_MODELS_YAML_KEY \
  --case /path/to/clawbench-task/task.json --output-dir harness-output

harness-bench batch --backend clawbench-cli \
  --harness openclaw --harness hermes --model YOUR_MODELS_YAML_KEY \
  --case /path/to/first-task --case /path/to/second-task
```

This backend runs **ClawBench's native drivers**, not HarnessBench's bundled
Dockerfiles or `run.sh` files. It supports the shared `openclaw`, `hermes`,
`claw-code` and `browser-use` names. Stagehand and Coze Studio are rejected before
launching any task. There is no automatic fallback from the plugin backend.
The public flags and registry were verified against ClawBench 0.11.0 at
[`07eb50a`](https://github.com/TIGER-AI-Lab/ClawBench/tree/07eb50a3d4c5a799f5ad4eebd57c67c10417787f).

Install a ClawBench release with `clawbench-run` on your `PATH` and configure its
workspace normally. `--case` is an actual ClawBench task directory or task JSON
path, not a HarnessBench case ID or `fixtures/smoke.json`. ClawBench expects
`instruction`, `time_limit` in minutes, and an `eval_schema` object with
`url_pattern` and `method`. `--model` is a key in its workspace
`models/models.yaml`. The subprocess inherits your current directory and
workspace/environment configuration, including `CLAWBENCH_WORKSPACE` if set.
ClawBench requires its container engine and infrastructure credentials, including
PurelyMail credentials, and performs model API preflight checks.

HarnessBench forwards `--no-upload`, which remains enabled by default. An explicit
`--upload` omits that flag and delegates uploading to ClawBench's configured
HuggingFace settings; both commands expose the same upload choice. The native
runner retains its own recording, container cleanup and default LLM judge. Normal
execution can call both the agent model and the judge; `batch --dry-run` only
previews the matrix and never discovers or launches the runner. No model or
container run is required to use that preview.

ClawBench owns output creation and writes raw `run-meta.json` files below the
selected output base. Native batches give each cell a unique `cell-<uuid>`
subdirectory because ClawBench's basename/model/second run names can collide for
different task paths. Single runs forward the selected base directly. This
backend does not convert the raw metadata to HarnessBench
`result.json` files or claim that `leaderboard` can ingest them. Preserve the raw
metadata and use ClawBench's reporting tools for native runs. Task failures,
infrastructure errors and inconclusive judging retain the runner's exit code;
a native batch stops at the first nonzero exit rather than hiding that outcome.
