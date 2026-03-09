# agent-skills

A collection of example skills for Claude Code and Codex CLI, demonstrating various capabilities including skill creation, evaluation, and iterative improvement.

## Available Skills

| Skill | Description |
|-------|-------------|
| `skill-forge` | Create new skills, modify and improve existing skills, and measure skill performance with evaluations and benchmarks |

## Origin and Differences

`skill-forge` was forked from Anthropic's [`skill-creator`](https://github.com/anthropics/skills/tree/main/skills/skill-creator).

Compared to the upstream skill, this repository adds and changes the following points:

- Renamed the skill from `skill-creator` to `skill-forge`, and narrowed the trigger description so it activates only for requests explicitly about skills or `SKILL.md`.
- Added Codex CLI support alongside Claude Code. The skill instructions now cover `.codex/skills/...`, `.agents/skills/...`, `.codex/skills-workspaces/...`, `CODEX_HOME`, and `codex exec`.
- Split trigger-eval execution by CLI with [`scripts/run_eval_claude.py`](./skills/skill-forge/scripts/run_eval_claude.py) and [`scripts/run_eval_codex.py`](./skills/skill-forge/scripts/run_eval_codex.py), while [`scripts/run_eval.py`](./skills/skill-forge/scripts/run_eval.py) dispatches between them.
- Strengthened evaluation workflow guidance: isolated per-run working directories, CLI-specific workspace paths, and persistent benchmark snapshots under `evals/benchmarks/README.md`.
- Added repository-local development assets that are not present upstream: `pyproject.toml`, `uv.lock`, `justfile`, seed evals in `evals/evals.json`, CI verification scripts, and automated tests under `tests/`.
- Removed the upstream `LICENSE.txt` from the skill directory layout used in this plugin.

## Installation

### For Claude Code

#### Prerequisites

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) installed

#### Step 1: Add the Marketplace

Register this repository as a plugin marketplace:

```bash
# From a local path
claude plugin marketplace add /path/to/ai-tools

# Or from a GitHub repository
claude plugin marketplace add j5ik2o/ai-tools
```

#### Step 2: Install the Plugin

```bash
claude plugin install agent-skills
```

#### Verify Installation

```bash
claude plugin list
```

### For Codex CLI

#### Prerequisites

- [Codex CLI](https://github.com/openai/codex) installed

#### Setup

Copy or symlink the skill into your project's `.codex/skills/` directory (or `.agents/skills/`):

```bash
# Copy the skill
cp -r /path/to/ai-tools/plugins/agent-skills/skills/skill-forge .codex/skills/skill-forge

# Or create a symlink
ln -s /path/to/ai-tools/plugins/agent-skills/skills/skill-forge .codex/skills/skill-forge
```

Codex CLI automatically discovers skills from `.codex/skills/` and `.agents/skills/` directories.

## Uninstallation

### Claude Code

```bash
claude plugin uninstall agent-skills
```

To remove the marketplace registration as well:

```bash
claude plugin marketplace remove j5ik2o-agent-skills
```

### Codex CLI

Remove the skill directory or symlink:

```bash
rm -rf .codex/skills/skill-forge
```

## Skill Structure

Each skill follows this structure:

```
skill-name/
├── SKILL.md          # Skill definition (required)
├── scripts/          # Executable scripts
├── references/       # Documentation loaded as needed
├── agents/           # Subagent instructions
└── assets/           # Templates, HTML files, etc.
```
