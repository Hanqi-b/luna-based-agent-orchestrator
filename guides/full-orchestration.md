# Sol + Luna Orchestration

This guide documents the single supported configuration. Sol plans, orchestrates,
integrates, and reviews; Luna handles the bounded execution roles. Astra is
outside the normal orchestration path and is only an explicitly selected option
for an exceptional hard problem. The setup scripts copy "codex/" to ".codex/"
and "agents/" to ".agents/" in the target repository without rewriting
configuration.

The topology is:

~~~
GPT-6.1 Sol root (high)
├── Luna explorer (max)
├── GPT-6 Luna worker (max)
├── Luna tester (max)
├── Luna researcher (max)
└── GPT-6.1 Sol reviewer (high)
~~~

Put the root settings in the project-scoped ".codex/config.toml", or merge
them into "~/.codex/config.toml" for a personal/global setup:

~~~
model = "gpt-6.1-sol"
model_reasoning_effort = "high"

[agents]
enabled = true
max_concurrent_threads_per_session = 4
default_subagent_model = "gpt-6-luna"
default_subagent_reasoning_effort = "max"
~~~

For the named roles, use these model settings in the corresponding files under
"codex/agents/":

~~~
# explorer.toml, tester.toml, researcher.toml
model = "gpt-6-luna"
model_reasoning_effort = "max"
~~~

~~~
# worker.toml
model = "gpt-6-luna"
model_reasoning_effort = "max"
~~~

Keep `sandbox_mode = "read-only"` in `reviewer.toml`, but leave model and effort
unset. Spawn the reviewer with `gpt-6.1-sol` / `high` normally, or `gpt-6-luna` /
`max` in `luna-reserve` mode. The Luna role files override the inherited "[agents]"
defaults; the reviewer would inherit the Luna default if its spawn omitted the
explicit model and effort.
