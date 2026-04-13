# takt

TAKT skills for Claude Code and Codex CLI. This plugin bundles builders, analyzers, optimizers, and maintenance helpers for TAKT workflows.

## Available Skills

| Skill | Description |
|-------|-------------|
| `takt-task-builder` | Create and edit TAKT `tasks.yaml` entries and `.takt/tasks/{slug}/order.md` task directories |
| `takt-workflow-builder` | Create and customize TAKT workflow YAML and related facet files |
| `takt-facet-builder` | Create and edit individual TAKT facets such as Persona, Policy, Instruction, Knowledge, and Output Contract |
| `takt-analyzer` | Analyze existing TAKT workflows, facets, and execution logs to find issues and improvement opportunities |
| `takt-optimizer` | Optimize existing TAKT workflows for lower token usage, simpler rules, and better execution flow |
| `takt-skill-updater` | Update the `takt-*` skills after the `references/takt` submodule is refreshed |

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
claude plugin install takt
```

#### Verify Installation

```bash
claude plugin list
```

### For Codex CLI

#### Prerequisites

- [Codex CLI](https://github.com/openai/codex) installed

#### Setup

Copy or symlink the TAKT skills you want into `.codex/skills/` or `.agents/skills/`:

```bash
# Example: install a single skill
ln -s /path/to/ai-tools/plugins/takt/skills/takt-workflow-builder .codex/skills/takt-workflow-builder

# Example: install all TAKT skills
for skill in /path/to/ai-tools/plugins/takt/skills/*; do
  ln -s "$skill" ".codex/skills/$(basename "$skill")"
done
```

Codex CLI automatically discovers skills from `.codex/skills/` and `.agents/skills/`.

## Uninstallation

### Claude Code

```bash
claude plugin uninstall takt
```

To remove the marketplace registration as well:

```bash
claude plugin marketplace remove j5ik2o-takt
```

### Codex CLI

Remove the installed TAKT skill directories or symlinks:

```bash
rm -rf .codex/skills/takt-*
```

## Skill Structure

Each TAKT skill follows this structure:

```text
skill-name/
├── SKILL.md          # Japanese skill definition
├── SKILL.en.md       # English variant when provided
└── ...
```
