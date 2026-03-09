# ai-tools

[日本語](README.ja.md)

A marketplace repository for distributing AI agent skills for Claude Code and skill-directory-based CLIs such as Codex.

## Highlights

- Publishes multiple plugins through `.claude-plugin/marketplace.json`
- Includes installable skill collections such as `agent-skills` and `takt`
- Keeps `skills/` symlinks for tools that consume plain skill directories directly

## Installation

### Claude Code Plugin

```shell
/plugin marketplace add j5ik2o/ai-tools
/plugin install agent-skills@ai-tools
/plugin install takt@ai-tools
```

### Skill-directory-based CLI

```shell
npx skills add j5ik2o/ai-tools
```

## Plugins

| Plugin | Description | Key skills | Details |
|--------|-------------|------------|---------|
| [`agent-skills`](plugins/agent-skills) | Agent skills demonstrating skill creation, evaluation, and iterative improvement workflows | [`skill-forge`](plugins/agent-skills/skills/skill-forge) | [README](plugins/agent-skills/README.md) |
| [`takt`](plugins/takt) | TAKT piece engine skills for multi-agent orchestration, analysis, building, and optimization | `takt-task-builder`, `takt-piece-builder`, `takt-facet-builder`, `takt-analyzer`, `takt-optimizer`, `takt-skill-updater` | - |

## Repository Structure

```text
.claude-plugin/
└── marketplace.json

plugins/
├── agent-skills/
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
├── skill-forge -> ../plugins/agent-skills/skills/skill-forge
├── takt-analyzer -> ../plugins/takt/skills/takt-analyzer
└── ...

template/
└── SKILL.md.template
```

## Creating a New Skill

1. Copy `template/SKILL.md.template` to `plugins/agent-skills/skills/<your-skill>/SKILL.md`
2. Edit the frontmatter (`name`, `description`) and add instructions
3. Create a symlink in `skills/` if you want direct CLI consumption:
   ```shell
   ln -s ../plugins/agent-skills/skills/<your-skill> skills/<your-skill>
   ```
4. Add or update entries in `.claude-plugin/marketplace.json` if you are publishing a new plugin collection

## License

See each skill's directory for individual license information.
