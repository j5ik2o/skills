# example-skills

A collection of example skills for Claude Code, demonstrating various capabilities including skill creation, evaluation, and iterative improvement.

## Available Skills

| Skill | Description |
|-------|-------------|
| `skill-creator` | Create new skills, modify and improve existing skills, and measure skill performance with evaluations and benchmarks |

## Installation

### Prerequisites

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) installed

### Step 1: Add the Marketplace

Register this repository as a plugin marketplace:

```bash
# From a local path
claude plugin marketplace add /path/to/ai-tools

# Or from a GitHub repository
claude plugin marketplace add j5ik2o/ai-tools
```

### Step 2: Install the Plugin

```bash
claude plugin install example-skills
```

### Verify Installation

```bash
claude plugin list
```

## Uninstallation

```bash
claude plugin uninstall example-skills
```

To remove the marketplace registration as well:

```bash
claude plugin marketplace remove j5ik2o-agent-skills
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
