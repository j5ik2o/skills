# j5ik2o-ai-plugins

[日本語](README.ja.md)

A Claude Code Plugin marketplace for distributing AI agent skills.

## Installation

### Claude Code Plugin

```shell
/plugin marketplace add j5ik2o/ai-tools
/plugin install example-skills@j5ik2o-agent-skills
```

### Vercel Skills CLI

```shell
npx skills add j5ik2o/ai-tools
```

## Plugins

### example-skills

A collection of skills for AI coding agents.

| Skill | Description |
|-------|-------------|
| [skill-creator](plugins/example-skills/skills/skill-creator) | Create new skills, modify and improve existing skills, and measure skill performance |

## Repository Structure

```
.claude-plugin/
└── marketplace.json          # Plugin marketplace catalog

plugins/
└── example-skills/
    └── skills/
        └── skill-creator/    # Skill implementation (SKILL.md + resources)

skills/                       # Symlinks for Vercel Skills CLI compatibility
└── skill-creator -> ../plugins/example-skills/skills/skill-creator

template/
└── SKILL.md                  # Template for creating new skills
```

## Creating a New Skill

1. Copy `template/SKILL.md` to `plugins/example-skills/skills/<your-skill>/SKILL.md`
2. Edit the frontmatter (`name`, `description`) and add instructions
3. Create a symlink in `skills/` for Vercel Skills CLI compatibility:
   ```shell
   ln -s ../plugins/example-skills/skills/<your-skill> skills/<your-skill>
   ```
4. Add the plugin entry to `.claude-plugin/marketplace.json` if creating a new plugin

## License

See each skill's directory for individual license information.
