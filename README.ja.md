# j5ik2o-ai-plugins

[English](README.md)

Claude Code と、Codex のようなスキルディレクトリベース CLI 向けに AI エージェントスキルを配布するマーケットプレイス用リポジトリです。

## Highlights

- `.claude-plugin/marketplace.json` から複数の plugin を公開
- `example-skills` と `takt` などのスキルコレクションを収録
- `skills/` に直接参照用のシンボリックリンクを保持

## インストール

### Claude Code Plugin

```shell
/plugin marketplace add j5ik2o/ai-tools
/plugin install example-skills@j5ik2o-agent-skills
```

### スキルディレクトリ対応 CLI

```shell
npx skills add j5ik2o/ai-tools
```

## プラグイン

| Plugin | 説明 | 主なスキル |
|--------|------|------------|
| [`example-skills`](plugins/example-skills) | Claude Code / Codex CLI 向けのサンプルスキル集 | [`skill-forge`](plugins/example-skills/skills/skill-forge) |
| [`takt`](plugins/takt) | TAKT piece engine 向けのマルチエージェント支援スキル集 | `takt-task-builder`, `takt-piece-builder`, `takt-facet-builder`, `takt-analyzer`, `takt-optimizer`, `takt-skill-updater` |

## リポジトリ構成

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

## 新しいスキルの作成方法

1. `template/SKILL.md.template` を `plugins/example-skills/skills/<スキル名>/SKILL.md` にコピー
2. フロントマター（`name`, `description`）を編集し、指示を書く
3. 直接参照する CLI でも使いたい場合は `skills/` にシンボリックリンクを作成:
   ```shell
   ln -s ../plugins/example-skills/skills/<スキル名> skills/<スキル名>
   ```
4. 新しい plugin collection を公開する場合は `.claude-plugin/marketplace.json` を更新

## ライセンス

各スキル配下のライセンス情報を参照してください。
