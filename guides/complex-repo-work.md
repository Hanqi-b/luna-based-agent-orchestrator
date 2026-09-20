# Complex Repository Work

Choose this preset for architecture changes, difficult debugging, and work
where higher-confidence reasoning matters more than latency.

The standard root setting is Astra "medium". This optional override raises the
root effort while leaving the installed Luna "max" roles and Astra "low"
reviewer in place. If you adopt it, update the installed Skill's root-reasoning
wording to match.

Add or merge this into "~/.codex/config.toml":

~~~
model = "gpt-6-astra"
model_reasoning_effort = "high"
service_tier = "standard"
~~~

If your Codex version does not support "service_tier", remove that line and
keep the model and reasoning settings.
