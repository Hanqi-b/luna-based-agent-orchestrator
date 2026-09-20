# Token Usage

There is no single token number for this setup. Usage depends on repository
size, task shape, how many subagents the root actually spawns, and how much of
each subagent's context is served from cache. This guide gives a repeatable
measurement method and the caveats needed to read the numbers correctly.

## What Codex records

Codex writes one rollout file per thread under
"~/.codex/sessions/YYYY/MM/DD/rollout-*.jsonl". Root and subagent threads each
get their own file. The relevant fields are:

- "session_meta": "id", "session_id", "parent_thread_id", "cwd",
  "cli_version", and the spawned role.
- "turn_context": the "model" and "effort" in force for the turn.
- "token_usage_record": per-response input, cached input, output, reasoning,
  and total tokens.
- "token_count" inside "event_msg": cumulative totals plus rate-limit
  percentages and "plan_type".

Grouping every rollout by "session_id" gives the full cost of one
orchestrated task, split by thread, role, and model.

## Measuring a run

"scripts/token_usage.py" is standard-library Python and read-only:

~~~
scripts/token_usage.py --list --date 2026-09-20
scripts/token_usage.py --root 01a079f2 --date 2026-09-20
scripts/token_usage.py --latest --date 2026-09-20
scripts/token_usage.py --root 01a079f2 --format json
~~~

Omitting "--date" scans the whole sessions directory, which is slower.
Codex auto-review threads are listed but excluded from totals by default; add
"--include-guardian" to count them.

## Benchmark protocol

For comparable measurements:

1. Pick representative tasks in one repository: a single-file fix, a
   multi-file feature, a cross-component bug, and a research-heavy change.
2. Run each task in a root-only configuration and with the current
   Astra/Luna orchestration configuration.
3. Record uncached input, cached input, output and reasoning tokens; spawned
   subagents; wall time; and 5-hour and 7-day rate-limit changes.
4. Repeat each case two or three times because variance between identical
   prompts can be large.
5. Record the Codex version and any temporary root or service-tier override.

Suggested results table:

| Task | Config | Astra uncached / cached / out | Luna uncached / cached / out | Subagents | Wall | 5h delta | 7d delta |
|---|---|---|---|---:|---:|---:|---:|

## Reading the numbers

Cached input can dominate. Always inspect uncached input and output
separately instead of treating raw "total_tokens" as the cost.

Rate-limit percentages are account-wide and may be affected by other sessions.
The change in the 5-hour and 7-day "used_percent" values is the most useful
single measure of account impact.

The root thread is a large line item even at low reasoning: it stays alive for
the whole task, polls subagents, and re-reads context. Parallelism trades tokens
for latency because every spawned subagent reads its own context.

Auto-review guardian threads are Codex approval reviewers, not part of this
configuration. They are small but not free.

## Historical sample

Treat this as a scale reference, not a benchmark for every repository.

- Task: cross-component file-watcher refresh after an external rename.
- Configuration: historical Astra root at "low", Luna subagents at "medium",
  Astra reviewer at "low".
- Codex "0.153.4"; date 2026-09-07.
- Agents: explorer, worker, tester, reviewer; three guardian threads excluded.
- Wall time: 13m49s.
- Rate limit: 5h window 0% to 66%; 7d window 31% to 42%.

| Thread | Role | Model / effort | Responses | Uncached in | Cached in | Output | Reasoning | Total | Duration |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| "01a079f2" | root | gpt-6-astra / low | 83 | 118,590 | 4,668,928 | 6,860 | 900 | 4,794,378 | 13m49s |
| "01a079f4" | explorer | gpt-5.6-luna / medium | 11 | 50,574 | 538,880 | 2,701 | 727 | 592,155 | 1m34s |
| "01a079f5" | tester | gpt-5.6-luna / medium | 27 | 56,318 | 1,313,024 | 5,329 | 1,918 | 1,374,671 | 11m05s |
| "01a079f5" | worker | gpt-5.6-luna / medium | 34 | 67,089 | 1,842,688 | 8,868 | 1,599 | 1,918,645 | 7m12s |
| "01a079fa" | reviewer | gpt-6-astra / low | 16 | 47,797 | 588,928 | 2,214 | 172 | 638,939 | 3m35s |

| Model | Threads | Responses | Uncached in | Cached in | Output | Reasoning | Total |
|---|---:|---:|---:|---:|---:|---:|---:|
| gpt-5.6-luna | 3 | 72 | 173,981 | 3,694,592 | 16,898 | 4,244 | 3,885,471 |
| gpt-6-astra | 2 | 99 | 166,387 | 5,257,856 | 9,074 | 1,072 | 5,433,317 |
| all | 5 | 171 | 340,368 | 8,952,448 | 25,972 | 5,316 | 9,318,788 |

Cache hit rate on input: 96.3%.

## Reducing usage

- Do not orchestrate small tasks; one root thread is often enough.
- Keep "max_concurrent_threads_per_session" low unless tasks are genuinely
  independent.
- Ask subagents for short reports so the root does not repeatedly re-read logs.
- Skip the reviewer for low-risk changes when an independent audit adds little
  value.
- Lower Luna reasoning only for a deliberate speed/cost tradeoff, and keep the
  Skill and configuration wording synchronized.

If you run this protocol on your own projects, record the task shape, repository
size, Codex version, configuration, and script output. Redact local paths
before publishing results.
