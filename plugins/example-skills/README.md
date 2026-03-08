# example-skills

A collection of example skills for Claude Code and Codex CLI, demonstrating various capabilities including skill creation, evaluation, and iterative improvement.

## Available Skills

| Skill | Description |
|-------|-------------|
| `skill-forge` | Create new skills, modify and improve existing skills, and measure skill performance with evaluations and benchmarks |

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
claude plugin install example-skills
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
cp -r /path/to/ai-tools/plugins/example-skills/skills/skill-forge .codex/skills/skill-forge

# Or create a symlink
ln -s /path/to/ai-tools/plugins/example-skills/skills/skill-forge .codex/skills/skill-forge
```

Codex CLI automatically discovers skills from `.codex/skills/` and `.agents/skills/` directories.

## Uninstallation

### Claude Code

```bash
claude plugin uninstall example-skills
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
