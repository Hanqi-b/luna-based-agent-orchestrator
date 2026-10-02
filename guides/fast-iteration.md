# Fast Iteration

Choose this preset when latency matters and you want Sol to orchestrate
quickly with Luna subagents.

Add or merge this root override into "~/.codex/config.toml":

~~~
model = "gpt-6.1-sol"
model_reasoning_effort = "high"
service_tier = "fast"
~~~

The installed Luna roles remain at "max", and the GPT-6.1 Sol reviewer remains
at "high". If your Codex version does not support "service_tier", remove that
line and keep the model and reasoning settings.
