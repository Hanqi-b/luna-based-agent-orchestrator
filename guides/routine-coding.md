# Routine Coding

Choose this preset for predictable, routine coding tasks where lower cost and
faster orchestration are preferred.

This is an optional root override that lowers Astra from "medium" to "low".
The installed Luna execution subagents remain at "max" and the Astra reviewer
remains at "low". If you adopt this override, update the installed Skill's
root-reasoning wording to match.

Add or merge this into "~/.codex/config.toml":

~~~
model = "gpt-6-astra"
model_reasoning_effort = "low"
service_tier = "fast"
~~~

If your Codex version does not support "service_tier", remove that line and
keep the model and reasoning settings.
