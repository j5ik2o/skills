# ai-tools

[日本語](README.ja.md)

A marketplace repository for distributing AI agent skills for Claude Code and skill-directory-based CLIs such as Codex.

## Highlights

- Publishes multiple plugins through `.claude-plugin/marketplace.json`
- Provides an APM marketplace manifest through `marketplace.yml` and generated `marketplace.json`
- Includes installable skill collections such as `agent-skills`, `takt`, and `software-design`
- Keeps `skills/` symlinks for tools that consume plain skill directories directly

## Installation

### Claude Code Plugin

```shell
/plugin marketplace add j5ik2o/ai-tools
/plugin install agent-skills@ai-tools
/plugin install takt@ai-tools
/plugin install software-design@ai-tools
```

### Agent Package Manager

```shell
apm marketplace add j5ik2o/ai-tools --name ai-tools
apm install software-design@ai-tools
```

Available APM package names are `agent-skills`, `takt`, and `software-design`.

### Skill-directory-based CLI

```shell
npx skills add j5ik2o/ai-tools
```

## Plugins

| Plugin | Description | Key skills | Details |
|--------|-------------|------------|---------|
| [`agent-skills`](plugins/agent-skills) | Agent skills demonstrating skill creation, evaluation, and iterative improvement workflows | [`skill-forge`](plugins/agent-skills/skills/skill-forge) | [README](plugins/agent-skills/README.md) |
| [`takt`](plugins/takt) | TAKT piece engine skills for multi-agent orchestration, analysis, building, and optimization | `takt-task-builder`, `takt-piece-builder`, `takt-facet-builder`, `takt-analyzer`, `takt-optimizer`, `takt-skill-updater` | [README](plugins/takt/README.md) |
| [`software-design`](plugins/software-design) | Software design skills for DDD, clean architecture, error handling, package design, refactoring, and maintainable domain modeling | `ddd-aggregate-design`, `clean-architecture`, `error-handling`, `package-design`, `refactoring-packages` | [plugin.json](plugins/software-design/.claude-plugin/plugin.json) |

## Repository Structure

```text
.claude-plugin/
└── marketplace.json

marketplace.yml
marketplace.json
mise.toml

plugins/
├── agent-skills/
│   ├── README.md
│   └── skills/
│       └── skill-forge/
├── takt/
│   ├── README.md
│   └── skills/
│       ├── takt-analyzer/
│       ├── takt-facet-builder/
│       ├── takt-optimizer/
│       ├── takt-skill-updater/
│       └── takt-task-builder/
└── software-design/
    └── skills/
        ├── clean-architecture/
        ├── ddd-aggregate-design/
        ├── error-handling/
        └── ...

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

## Maintaining the APM Marketplace

This repository keeps `marketplace.yml` as the APM authoring source and commits the generated `marketplace.json` for consumers.

APM is managed through `mise`:

```shell
mise install
mise run apm:version
```

Preview marketplace resolution without writing files:

```shell
mise run apm:marketplace:check
```

Regenerate `marketplace.json` from `marketplace.yml`:

```shell
mise run apm:marketplace:build
```

Package refs in `marketplace.yml` are pinned to commit SHAs for reproducible APM builds. Update those refs when publishing a new marketplace revision.

## License

See each skill's directory for individual license information.
