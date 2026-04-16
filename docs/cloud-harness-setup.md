# Cloud Harness Setup

Two of the six bundled harnesses require third-party credentials. They are opt-in: without the env vars, they are **skipped**, not failed.

## Stagehand (BrowserBase)

Stagehand drives a cloud-hosted Chrome at BrowserBase. You need a BrowserBase account.

1. Sign up at [browserbase.com](https://www.browserbase.com/) and create an API key.
2. Export it:
   ```bash
   export BROWSERBASE_API_KEY=bb_live_...
   ```
3. (Optional) pin a project id: `export BROWSERBASE_PROJECT_ID=...`.
4. Run:
   ```bash
   harnessbench run --harness stagehand --model gpt-4o-mini --case fixtures/smoke.json
   ```

Each Stagehand run consumes BrowserBase browser minutes. Check your plan before a large matrix.

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
4. Run:
   ```bash
   harnessbench run --harness coze-studio --model gpt-4o-mini --case fixtures/smoke.json
   ```

## What "skipped" looks like

With nothing set:

```
$ harnessbench matrix --harnesses stagehand,coze-studio,openclaw --models gpt-4o-mini
harness       model         status
stagehand     gpt-4o-mini   skipped:missing_credential:BROWSERBASE_API_KEY
coze-studio   gpt-4o-mini   skipped:missing_credential:COZE_INSTANCE_URL
openclaw      gpt-4o-mini   eligible
```

The leaderboard preserves these entries verbatim so you can see exactly what credentials to set to unblock a slot.
