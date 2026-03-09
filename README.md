# j5ik2o-ai-plugins

[日本語](README.ja.md)

A marketplace repository for distributing AI agent skills for Claude Code and skill-directory-based CLIs such as Codex.

## Highlights

- Publishes multiple plugins through `.claude-plugin/marketplace.json`
- Includes installable skill collections such as `example-skills` and `takt`
- Keeps `skills/` symlinks for tools that consume plain skill directories directly

## Installation

### Claude Code Plugin

```shell
/plugin marketplace add j5ik2o/ai-tools
/plugin install example-skills@j5ik2o-agent-skills
```

### Skill-directory-based CLI

```shell
npx skills add j5ik2o/ai-tools
```

## Plugins

| Plugin | Description | Key skills |
|--------|-------------|------------|
| [`example-skills`](plugins/example-skills) | Example skills for Claude Code and Codex CLI | [`skill-forge`](plugins/example-skills/skills/skill-forge) |
| [`takt`](plugins/takt) | TAKT piece-engine skills for multi-agent orchestration | `takt-task-builder`, `takt-piece-builder`, `takt-facet-builder`, `takt-analyzer`, `takt-optimizer`, `takt-skill-updater` |

## Repository Structure

```text
.claude-plugin/
└── marketplace.json

plugins/
├── example-skills/
│   ├── README.md
│   └── skills/
│       └── skill-forge/
└── takt/
    └── skills/
        ├── takt-analyzer/
        ├── takt-facet-builder/
        ├── takt-optimizer/
        ├── takt-piece-builder/
        ├── takt-skill-updater/
        └── takt-task-builder/

skills/
├── skill-forge -> ../plugins/example-skills/skills/skill-forge
├── takt-analyzer -> ../plugins/takt/skills/takt-analyzer
└── ...

template/
└── SKILL.md.template
```

## Creating a New Skill

1. Copy `template/SKILL.md.template` to `plugins/example-skills/skills/<your-skill>/SKILL.md`
2. Edit the frontmatter (`name`, `description`) and add instructions
3. Create a symlink in `skills/` if you want direct CLI consumption:
   ```shell
   ln -s ../plugins/example-skills/skills/<your-skill> skills/<your-skill>
   ```
4. Add or update entries in `.claude-plugin/marketplace.json` if you are publishing a new plugin collection

## License

See each skill's directory for individual license information.
