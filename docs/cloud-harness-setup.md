# Cloud Harness Setup

Two of the six bundled harnesses require third-party credentials. They are opt-in:
without the env vars, they are **skipped**, not failed. Credential setup controls
preflight only: the currently released CLI cannot execute `run` or non-dry `batch`
until ClawBench exposes the required public runner API. Do not spend cloud credits
or paste live secrets into logs while that execution boundary remains in place.

## Stagehand (BrowserBase)

Stagehand drives a cloud-hosted Chrome at BrowserBase. You need a BrowserBase account.

1. Sign up at [browserbase.com](https://www.browserbase.com/) and create an API key.
2. Export it:
   ```bash
   export BROWSERBASE_API_KEY=bb_live_...
   ```
3. (Optional) pin a project id: `export BROWSERBASE_PROJECT_ID=...`.
4. Confirm that the matrix is eligible:
   ```bash
   harness-bench matrix --harness stagehand --model gpt-4o-mini --case smoke-search
   ```

Do not start a Stagehand session from HarnessBench until an end-to-end runner is
published and verified.

## Coze Studio

Coze Studio workflows execute against a Coze instance — either self-hosted from [coze-dev/coze-studio](https://github.com/coze-dev/coze-studio) or a managed deployment.

1. Stand up a Coze instance (self-hosted docker-compose works).
2. Create a workflow that accepts a task description and drives the browser.
3. Export:
   ```bash
   export COZE_INSTANCE_URL=https://coze.your-org.internal
   export COZE_API_TOKEN=pat_...
   export COZE_WORKFLOW_ID=<the workflow you created>
   ```
4. Confirm that the matrix is eligible:
   ```bash
   harness-bench matrix --harness coze-studio --model gpt-4o-mini --case smoke-search
   ```

## What "skipped" looks like

With nothing set:

```
$ harness-bench matrix --harness stagehand --harness coze-studio --harness openclaw --model gpt-4o-mini --case smoke-search
total=3 eligible=1 skipped=2
[SKIP] stagehand      gpt-4o-mini            smoke-search  (missing_credential:BROWSERBASE_API_KEY)
[SKIP] coze-studio    gpt-4o-mini            smoke-search  (missing_credential:COZE_INSTANCE_URL,COZE_API_TOKEN,COZE_WORKFLOW_ID)
[OK]   openclaw       gpt-4o-mini            smoke-search
```

Use this output only to identify missing configuration. It is not a benchmark result
or a leaderboard entry.
