# example-skills

Claude Code 向けのサンプルスキルコレクションです。スキルの作成、評価、反復的な改善など、さまざまな機能を示します。

## 利用可能なスキル

| スキル | 説明 |
|--------|------|
| `skill-creator` | 新しいスキルの作成、既存スキルの修正・改善、評価とベンチマークによるスキル性能の測定 |

## インストール

### 前提条件

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) がインストールされていること

### ステップ 1: マーケットプレースの追加

このリポジトリをプラグインマーケットプレースとして登録します：

```bash
# ローカルパスから
claude plugin marketplace add /path/to/ai-tools

# または GitHub リポジトリから
claude plugin marketplace add j5ik2o/ai-tools
```

### ステップ 2: プラグインのインストール

```bash
claude plugin install example-skills
```

### インストールの確認

```bash
claude plugin list
```

## アンインストール

```bash
claude plugin uninstall example-skills
```

マーケットプレースの登録も解除する場合：

```bash
claude plugin marketplace remove j5ik2o-agent-skills
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
