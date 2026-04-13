# takt

Claude Code および Codex CLI 向けの TAKT スキル集です。TAKT ワークフローの作成、分析、最適化、保守更新を支援します。

## 利用可能なスキル

| スキル | 説明 |
|--------|------|
| `takt-task-builder` | TAKT の `tasks.yaml` エントリと `.takt/tasks/{slug}/order.md` タスクディレクトリを作成・編集 |
| `takt-workflow-builder` | TAKT のワークフロー YAML と関連ファセットを作成・カスタマイズ |
| `takt-facet-builder` | Persona / Policy / Instruction / Knowledge / Output Contract などの TAKT ファセットを個別に作成・編集 |
| `takt-analyzer` | 既存の TAKT ワークフロー、facet、実行ログを分析し、問題点と改善案を提示 |
| `takt-optimizer` | 既存の TAKT ワークフローをトークン消費、ルール構成、実行フローの観点で最適化 |
| `takt-skill-updater` | `references/takt` サブモジュール更新後に `takt-*` スキル群を追従更新 |

## インストール

### Claude Code の場合

#### 前提条件

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) がインストールされていること

#### ステップ 1: マーケットプレースの追加

このリポジトリをプラグインマーケットプレースとして登録します。

```bash
# ローカルパスから
claude plugin marketplace add /path/to/ai-tools

# または GitHub リポジトリから
claude plugin marketplace add j5ik2o/ai-tools
```

#### ステップ 2: プラグインのインストール

```bash
claude plugin install takt
```

#### インストールの確認

```bash
claude plugin list
```

### Codex CLI の場合

#### 前提条件

- [Codex CLI](https://github.com/openai/codex) がインストールされていること

#### セットアップ

使いたい TAKT スキルを `.codex/skills/` または `.agents/skills/` にコピーまたはシンボリックリンクします。

```bash
# 例: 1つのスキルだけ導入
ln -s /path/to/ai-tools/plugins/takt/skills/takt-workflow-builder .codex/skills/takt-workflow-builder

# 例: TAKT スキルを一括導入
for skill in /path/to/ai-tools/plugins/takt/skills/*; do
  ln -s "$skill" ".codex/skills/$(basename "$skill")"
done
```

Codex CLI は `.codex/skills/` および `.agents/skills/` からスキルを自動検出します。

## アンインストール

### Claude Code

```bash
claude plugin uninstall takt
```

マーケットプレースの登録も解除する場合:

```bash
claude plugin marketplace remove j5ik2o-takt
```

### Codex CLI

導入した TAKT スキルのディレクトリまたはシンボリックリンクを削除します。

```bash
rm -rf .codex/skills/takt-*
```

## スキル構造

各 TAKT スキルは概ね次の構成です。

```text
skill-name/
├── SKILL.md          # 日本語版スキル定義
├── SKILL.en.md       # 英語版がある場合
└── ...
```
