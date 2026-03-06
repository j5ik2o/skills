# example-skills

Claude Code および Codex CLI 向けのサンプルスキルコレクションです。スキルの作成、評価、反復的な改善など、さまざまな機能を示します。

## 利用可能なスキル

| スキル | 説明 |
|--------|------|
| `skill-creator` | 新しいスキルの作成、既存スキルの修正・改善、評価とベンチマークによるスキル性能の測定 |

## インストール

### 前提条件

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) または [Codex CLI](https://github.com/openai/codex)
- このリポジトリがローカルにクローンされていること

### Claude Code の場合

`.claude/skills/` から各スキルへのシンボリックリンクを作成します：

```bash
# リポジトリのルートから実行
ln -s ../../plugins/example-skills/skills/skill-creator .claude/skills/skill-creator
```

すべてのスキルを一括インストールする場合：

```bash
for skill in plugins/example-skills/skills/*/; do
  name=$(basename "$skill")
  ln -s "../../plugins/example-skills/skills/$name" ".claude/skills/$name"
done
```

### Codex CLI の場合

`.codex/skills/` から各スキルへのシンボリックリンクを作成します：

```bash
# リポジトリのルートから実行
ln -s ../../plugins/example-skills/skills/skill-creator .codex/skills/skill-creator
```

すべてのスキルを一括インストールする場合：

```bash
for skill in plugins/example-skills/skills/*/; do
  name=$(basename "$skill")
  ln -s "../../plugins/example-skills/skills/$name" ".codex/skills/$name"
done
```

### インストールの確認

```bash
# シンボリックリンクが正しく作成されたか確認
ls -la .claude/skills/skill-creator
# 以下のように表示されるはず: skill-creator -> ../../plugins/example-skills/skills/skill-creator
```

## アンインストール

シンボリックリンクを削除します（スキルファイル自体は削除されません）：

```bash
# Claude Code
rm .claude/skills/skill-creator

# Codex CLI
rm .codex/skills/skill-creator
```

## スキルの構造

各スキルは以下の構造に従います：

```
skill-name/
├── SKILL.md          # スキル定義（必須）
├── scripts/          # 実行可能なスクリプト
├── references/       # 必要に応じて読み込まれるドキュメント
├── agents/           # サブエージェント用の指示
└── assets/           # テンプレート、HTMLファイルなど
```

## ライセンス

詳細は [LICENSE.txt](skills/skill-creator/LICENSE.txt) を参照してください。
