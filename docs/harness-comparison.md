# Harness Comparison

What each bundled harness optimizes for, so you know what you're actually measuring.

| Harness | Philosophy | Control surface | Strength | Watch-out |
|---------|-----------|-----------------|----------|-----------|
| `openclaw` | Reference loop — plain browser + minimal scaffolding. | CDP via Chrome extension. | Deterministic baseline; identical to ClawBench. | Intentionally unfancy. |
| `hermes` | Hermes-style function-calling loop, model-agnostic. | Python tool-use. | Clean tool abstraction; easy to extend. | Depends on model quality for planning. |
| `claw-code` | Rust agent loop; low overhead, strict types. | CDP via Rust client. | Fast, predictable memory. | Smaller ecosystem than Python. |
| `browser-use` | Playwright-first with rich accessibility-tree extraction. | Playwright. | Robust action coverage; good at forms. | Heavier runtime. |
| `stagehand` | Cloud browser (BrowserBase) + structured acts. | BrowserBase SDK. | Scales headless concurrency; built-in observability. | Cloud dependency; billable. |
| `coze-studio` | Workflow-builder harness; GUI-composed agent graphs. | Coze instance API. | Non-code users can iterate. | Requires Coze instance; web-only. |

## Runtime matrix

| Harness | Language | Container | Needs cloud? |
|---------|----------|-----------|--------------|
| openclaw | Python | shared (ClawBench base) | No |
| hermes | Python | dedicated | No |
| claw-code | Rust | dedicated | No |
| browser-use | Python | dedicated | No |
| stagehand | Node/TS | dedicated | Yes (BrowserBase) |
| coze-studio | Web | dedicated | Yes (Coze instance) |

## Interpretation tips

- Results cluster by **control surface**, not by language. Stagehand and browser-use both win/lose on form-heavy tasks for structural reasons, not Python-vs-Node ones.
- Cloud harnesses have lower variance but higher tail latency — account for that if you gate on wall-clock.
- `openclaw` is the reference point. Treat it as the "no-fancy-harness" baseline when reading the leaderboard.
