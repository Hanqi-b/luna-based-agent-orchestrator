# Routine Coding

Choose this preset for predictable, routine coding tasks where faster
orchestration is preferred.

This preset keeps the GPT-6.1 Sol root at "high" while selecting the fast
service tier. The installed Luna execution subagents remain at "max", and the
GPT-6.1 Sol reviewer remains at "high".

Add or merge this into "~/.codex/config.toml":

~~~
model = "gpt-6.1-sol"
model_reasoning_effort = "high"
service_tier = "fast"
~~~

If your Codex version does not support "service_tier", remove that line and
keep the model and reasoning settings.
