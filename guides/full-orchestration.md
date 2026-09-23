# Sol + Luna Orchestration

This guide documents the single supported configuration. Sol plans, orchestrates,
integrates, and reviews; Luna handles the bounded execution roles. Astra is
outside the normal orchestration path and is only an explicitly selected option
for an exceptional hard problem. The setup scripts copy "codex/" to ".codex/"
and "agents/" to ".agents/" in the target repository without rewriting
configuration.

The topology is:

~~~
Sol root (high)
├── Luna explorer (max)
├── Luna worker (max)
├── Luna tester (max)
├── Luna researcher (max)
└── Sol reviewer (max)
~~~

Put the root settings in the project-scoped ".codex/config.toml", or merge
them into "~/.codex/config.toml" for a personal/global setup:

~~~
model = "gpt-6-sol"
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
# explorer.toml, worker.toml, tester.toml, researcher.toml
model = "gpt-6-luna"
model_reasoning_effort = "max"
~~~

~~~
# reviewer.toml
model = "gpt-6-sol"
model_reasoning_effort = "max"
~~~

The role files override the inherited "[agents]" defaults. Keep those explicit
overrides when you want the topology above to remain stable. Remove them only
when you intentionally want all named roles to follow the defaults in
"config.toml".
