# example-skills

A collection of example skills for Claude Code and Codex CLI, demonstrating various capabilities including skill creation, evaluation, and iterative improvement.

## Available Skills

| Skill | Description |
|-------|-------------|
| `skill-creator` | Create new skills, modify and improve existing skills, and measure skill performance with evaluations and benchmarks |

## Installation

### Prerequisites

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) or [Codex CLI](https://github.com/openai/codex)
- This repository cloned locally

### For Claude Code

Create a symlink from `.claude/skills/` to each skill you want to install:

```bash
# From the repository root
ln -s ../../plugins/example-skills/skills/skill-creator .claude/skills/skill-creator
```

To install all skills at once:

```bash
for skill in plugins/example-skills/skills/*/; do
  name=$(basename "$skill")
  ln -s "../../plugins/example-skills/skills/$name" ".claude/skills/$name"
done
```

### For Codex CLI

Create a symlink from `.codex/skills/` to each skill:

```bash
# From the repository root
ln -s ../../plugins/example-skills/skills/skill-creator .codex/skills/skill-creator
```

To install all skills at once:

```bash
for skill in plugins/example-skills/skills/*/; do
  name=$(basename "$skill")
  ln -s "../../plugins/example-skills/skills/$name" ".codex/skills/$name"
done
```

### Verify Installation

```bash
# Check the symlink was created correctly
ls -la .claude/skills/skill-creator
# Should show: skill-creator -> ../../plugins/example-skills/skills/skill-creator
```

## Uninstallation

Remove the symlinks (this does not delete the skill files):

```bash
# Claude Code
rm .claude/skills/skill-creator

# Codex CLI
rm .codex/skills/skill-creator
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

## License

See [LICENSE.txt](skills/skill-creator/LICENSE.txt) for details.
