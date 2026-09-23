# Fast Iteration

Choose this preset when latency matters and you want Sol to orchestrate
quickly with Luna subagents.

Add or merge this root override into "~/.codex/config.toml":

~~~
model = "gpt-6-sol"
model_reasoning_effort = "high"
service_tier = "fast"
~~~

The installed Luna roles and Sol reviewer remain at "max". If your Codex
version does not support "service_tier", remove that line and keep the model
and reasoning settings.
