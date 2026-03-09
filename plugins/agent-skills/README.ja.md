# agent-skills

Claude Code および Codex CLI 向けのサンプルスキルコレクションです。スキルの作成、評価、反復的な改善など、さまざまな機能を示します。

## 利用可能なスキル

| スキル | 説明 |
|--------|------|
| `skill-forge` | 新しいスキルの作成、既存スキルの修正・改善、評価とベンチマークによるスキル性能の測定 |

## 由来と差分

`skill-forge` は Anthropic の [`skill-creator`](https://github.com/anthropics/skills/tree/main/skills/skill-creator) をフォークして作成しています。

上流版と比べた主な差分は以下です。

- スキル名を `skill-creator` から `skill-forge` に変更し、トリガー説明も「スキル自体」や `SKILL.md` に明示的に関係する依頼に限定する形へ絞り込みました。
- Claude Code に加えて Codex CLI を正式に扱うようにし、`.codex/skills/...`、`.agents/skills/...`、`.codex/skills-workspaces/...`、`CODEX_HOME`、`codex exec` を前提にした手順を追記しました。
- トリガー評価の実行系を CLI ごとに分離し、[`scripts/run_eval_claude.py`](./skills/skill-forge/scripts/run_eval_claude.py) と [`scripts/run_eval_codex.py`](./skills/skill-forge/scripts/run_eval_codex.py) を追加しました。共通の入口は [`scripts/run_eval.py`](./skills/skill-forge/scripts/run_eval.py) です。
- 評価ワークフローを具体化し、実行ごとの隔離ワーキングディレクトリ、CLI 別の workspace 配置、`evals/benchmarks/README.md` へのベンチマーク蓄積を明示しました。
- 上流にはないローカル運用向けファイルとして、`pyproject.toml`、`uv.lock`、`justfile`、`evals/evals.json`、CI 検証スクリプト、`tests/` 配下の自動テストを追加しています。
- プラグイン内のスキル構成では、上流にある `LICENSE.txt` は含めていません。

## インストール

### Claude Code の場合

#### 前提条件

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) がインストールされていること

#### ステップ 1: マーケットプレースの追加

このリポジトリをプラグインマーケットプレースとして登録します：

```bash
# ローカルパスから
claude plugin marketplace add /path/to/ai-tools

# または GitHub リポジトリから
claude plugin marketplace add j5ik2o/ai-tools
```

#### ステップ 2: プラグインのインストール

```bash
claude plugin install agent-skills
```

#### インストールの確認

```bash
claude plugin list
```

### Codex CLI の場合

#### 前提条件

- [Codex CLI](https://github.com/openai/codex) がインストールされていること

#### セットアップ

スキルをプロジェクトの `.codex/skills/` ディレクトリ（または `.agents/skills/`）にコピーまたはシンボリックリンクします：

```bash
# コピーする場合
cp -r /path/to/ai-tools/plugins/agent-skills/skills/skill-forge .codex/skills/skill-forge

# シンボリックリンクの場合
ln -s /path/to/ai-tools/plugins/agent-skills/skills/skill-forge .codex/skills/skill-forge
```

Codex CLI は `.codex/skills/` および `.agents/skills/` ディレクトリからスキルを自動的に検出します。

## アンインストール

### Claude Code

```bash
claude plugin uninstall agent-skills
```

マーケットプレースの登録も解除する場合：

```bash
claude plugin marketplace remove j5ik2o-agent-skills
```

### Codex CLI

スキルディレクトリまたはシンボリックリンクを削除します：

```bash
rm -rf .codex/skills/skill-forge
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
