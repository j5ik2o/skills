# j5ik2o-ai-plugins

[English](README.md)

AIエージェントスキルを配布するためのClaude Code Pluginマーケットプレイスです。

## インストール

### Claude Code Plugin

```shell
/plugin marketplace add j5ik2o/ai-tools
/plugin install example-skills@j5ik2o-agent-skills
```

### Vercel Skills CLI

```shell
npx skills add j5ik2o/ai-tools
```

## プラグイン

### example-skills

AIコーディングエージェント向けのスキルコレクションです。

| スキル | 説明 |
|--------|------|
| [skill-forge](plugins/example-skills/skills/skill-forge) | スキルの新規作成、改善、パフォーマンス測定 |

## リポジトリ構成

```
.claude-plugin/
└── marketplace.json          # プラグインマーケットプレイスカタログ

plugins/
└── example-skills/
    └── skills/
        └── skill-forge/    # スキル実装（SKILL.md + リソース）

skills/                       # Vercel Skills CLI互換用シンボリックリンク
└── skill-forge -> ../plugins/example-skills/skills/skill-forge

template/
└── SKILL.md                  # 新規スキル作成用テンプレート
```

## 新しいスキルの作成方法

1. `template/SKILL.md` を `plugins/example-skills/skills/<スキル名>/SKILL.md` にコピー
2. フロントマター（`name`, `description`）を編集し、指示を記述
3. Vercel Skills CLI互換のため `skills/` にシンボリックリンクを作成:
   ```shell
   ln -s ../plugins/example-skills/skills/<スキル名> skills/<スキル名>
   ```
4. 新しいプラグインを作る場合は `.claude-plugin/marketplace.json` にエントリを追加

## ライセンス

各スキルのディレクトリ内のライセンス情報を参照してください。
