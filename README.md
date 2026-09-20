# Luna-based Agent Orchestrator

Luna-based Agent Orchestrator is a Codex Skill and project-scoped configuration
for complex repository work. It keeps Astra as the root orchestrator and
reviewer while Luna handles the bounded execution roles.

This repository contains one supported configuration. There is no plan
selection step during installation.

## Architecture

The preserved orchestration topology is:

~~~
GPT-6 Astra root (medium)
├── GPT-5.6 Luna explorer (max)
├── GPT-5.6 Luna worker (max)
├── GPT-5.6 Luna tester (max)
├── GPT-5.6 Luna researcher (max)
└── GPT-6 Astra reviewer (low)
~~~

| Setting | Value |
|---|---|
| Root / integrator | GPT-6 Astra, "medium" reasoning |
| Explorer, worker, tester, researcher | GPT-5.6 Luna, "max" reasoning |
| Reviewer | GPT-6 Astra, "low" reasoning |
| Maximum concurrent child threads | 4 |
| Delegation owner | Root agent |

The root maps the work, delegates bounded tasks, integrates the results, and
performs final verification. Luna workers are execution subagents; the Skill
does not introduce a second planning hierarchy or a new recursive orchestration
layer.

## Repository layout

~~~
.
├── codex/
│   ├── config.toml
│   └── agents/*.toml
├── agents/
│   └── skills/luna-based-agent-orchestrator/SKILL.md
├── guides/
├── scripts/token_usage.py
├── tests/test_token_usage.py
├── AGENTS.md
├── setup.sh
├── setup.ps1
├── NOTICE
└── LICENSE
~~~

"codex/" and "agents/" are installation sources. The installer copies them to
".codex/" and ".agents/" in the target repository.

## Installation

The target project must already exist and must be different from this setup
repository.

On macOS or Linux:

~~~
./setup.sh
~~~

On Windows PowerShell:

~~~
powershell -ExecutionPolicy Bypass -File .\setup.ps1
~~~

The installer asks for the target repository and then whether to install
".codex", ".agents", and "AGENTS.md". It does not ask the user to choose
between configurations. Existing files are listed and require explicit
confirmation before replacement; existing "AGENTS.md" content is preserved.

For a manual project-scoped installation, copy:

~~~
codex/  -> <target>/.codex/
agents/ -> <target>/.agents/
AGENTS.md -> <target>/AGENTS.md
~~~

For a personal installation, copy "codex/agents/*.toml" to
"~/.codex/agents/" and merge "codex/config.toml" into "~/.codex/config.toml".
Copy "agents/skills/luna-based-agent-orchestrator/" to
"~/.agents/skills/luna-based-agent-orchestrator/". Merge rather than blindly
overwriting a global config that contains unrelated providers, permissions, or
MCP settings.

## Using the Skill

Codex may select the Skill automatically for multi-file work, cross-component
debugging, repository-wide changes, parallelizable work, or explicit requests
to delegate. It can also be invoked directly:

~~~
$luna-based-agent-orchestrator

Implement the new invoice export endpoint. Map the existing path first, use
bounded workers for implementation, verify the change, and perform a final
review.
~~~

The Skill is intentionally not a generic model-routing framework. It preserves
the existing roles, model assignments, reasoning settings, delegation gate,
and concurrency limit so that the original behavior remains recognizable.

## Guides and token usage

The "guides/" directory covers the preserved topology, optional speed and
reasoning overrides, complex repository work, routine coding, and usage
measurement. "scripts/token_usage.py" is standard-library Python and reads
Codex rollout logs without modifying them:

~~~
scripts/token_usage.py --list --date 2026-09-20
scripts/token_usage.py --latest --date 2026-09-20
~~~

For small, low-risk tasks, do not invoke the orchestrator unnecessarily. A
single root thread is often the most efficient choice.

## Upstream

This project is a fork of
[donvito/codex-astra-luna-orchestrator](https://github.com/donvito/codex-astra-luna-orchestrator).
The fork is derived from the upstream Pro configuration, keeps its Astra/Luna
topology, and removes the alternate Plus configuration. The upstream Skill was
named "astra-orchestrator"; this fork installs the renamed
"luna-based-agent-orchestrator" Skill.

After the GitHub fork exists, the intended remotes are:

~~~
origin    <your fork>
upstream  https://github.com/donvito/codex-astra-luna-orchestrator.git
~~~

For an existing local checkout, configure them without merging any upstream
changes automatically:

~~~
git remote rename origin upstream
git remote add origin https://github.com/YOUR_GITHUB_ACCOUNT/luna-based-agent-orchestrator.git
git remote -v
git fetch upstream
~~~

Review upstream changes explicitly before integrating them. Do not force-push
or replace upstream history.

## License

Licensed under the [Apache License 2.0](LICENSE). The original "LICENSE" file
is retained unchanged. Apache-2.0 permits forking, modification, and public
redistribution when the license, copyright/attribution notices, and required
modification notices are retained. "NOTICE" records the upstream source and
the scope of this fork.
