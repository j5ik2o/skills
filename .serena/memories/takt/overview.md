# TAKT（TAKT Agent Koordination Topology）概要

## 基本概念

TAKTは複数のAIエージェントを調整するマルチエージェント・オーケストレーション・システム。YAML形式の「ピース」定義により、ステートマシンの遷移とルールベースのルーティングで複数のAIエージェントを協調動作させる。

## コア用語

- **Piece（ピース）**: YAML定義ファイル。一連のMovement（動作）を含む実行単位。
- **Movement（ムーブメント）**: ピース内の個別ステップ。各ムーブメントは：
  - ペルソナ（AIの役割・ID）を指定
  - 指示（instruction）を提供
  - 次のムーブメントへのルーティングルールを定義
- **Persona（ペルソナ）**: AIエージェントの役割定義。マークダウンファイルで表現。
- **Facet（ファセット）**: ピースを構成する部品：
  - persona: AIの役割・専門性
  - policy: 判断基準・禁止パターン
  - knowledge: 詳細な知識・理由付け・事例
  - instruction: ムーブメント固有の手順・チェックリスト
  - output-contract: レポートフォーマット定義
- **Rule（ルール）**: ムーブメント実行後の次ムーブメント決定ロジック。3種類：
  1. タグベース: `[STEP:N]`タグで条件指定
  2. AI判定: `ai("条件文")`でAIが動的評価
  3. 集約: `all("X")` / `any("X")`で並列ムーブメント結果を集約

## ファイル構成

```
~/.takt/                    # グローバルユーザー設定
  config.yaml               # 言語、プロバイダ、モデル、ログレベル
  pieces/                   # ユーザー定義ピース（ビルトインを上書き）
  facets/                   # ユーザー定義ファセット
    personas/
    policies/
    knowledge/
    instructions/
    output-contracts/
  repertoire/               # インストール済みレパートリーパッケージ

.takt/                      # プロジェクトレベル設定
  config.yaml               # プロジェクト設定
  facets/                   # プロジェクトレベルファセット
  tasks/                    # タスクファイル
  runs/                     # 実行レポート（runs/{slug}/reports/）
  logs/                     # セッションログ（NDJSON形式）
  events/                   # 分析イベント（NDJSON）
```

## ピース（YAML）スキーマ

### 基本構造

```yaml
name: piece-name                  # ピース名（必須）
description: 説明                 # オプション
max_movements: 30                 # 最大ムーブメント数
initial_movement: plan            # 最初のムーブメント
interactive_mode: assistant       # インタラクティブモード

# ピースレベルプロバイダー設定（全ムーブメント継承）
piece_config:
  provider_options:
    codex:
      network_access: true
    claude:
      sandbox:
        allow_unsandboxed_commands: true

# サイクル監視（ムーブメント間のループ検出）
loop_monitors:
  - cycle: [review, fix]
    threshold: 3               # サイクル数で判定実行
    judge:
      persona: supervisor
      instruction_template: |
        ループ判定...
      rules:
        - condition: 健全（進捗あり）
          next: review
        - condition: 非生産的
          next: ABORT

# セクションマップ（キー → ファイルパス）
personas:
  coder: ../facets/personas/coder.md
  reviewer: ../facets/personas/reviewer.md
policies:
  coding: ../facets/policies/coding.md
knowledge:
  architecture: ../facets/knowledge/architecture.md
instructions:
  plan: ../facets/instructions/plan.md
report_formats:
  plan: ../facets/output-contracts/plan.md

movements:
  # 通常ムーブメント
  - name: movement-name
    persona: coder                 # ペルソナキー
    policy: [coding, testing]      # ポリシーキー（単一 or 配列）
    knowledge: architecture        # ナレッジキー
    instruction: plan              # 指示キー
    provider: claude               # オプション: プロバイダ上書き
    model: opus                    # オプション: モデル上書き
    edit: true                     # ファイル編集許可
    required_permission_mode: edit # 最小権限モード
    session: continue              # セッション継続（continue|refresh）
    provider_options:
      claude:
        allowed_tools:
          - Read
          - Glob
          - Grep
          - Edit
          - Write
          - Bash
    quality_gates:                 # 完了基準
      - "すべてのテスト通過"
    instruction_template: |
      カスタム指示...
      {task}, {previous_response}は自動注入
    pass_previous_response: true
    output_contracts:
      report:
        - name: plan.md
          format: plan             # report_formatsマップを参照
    rules:
      - condition: "実装完了"
        next: review
      - condition: "実行不可"
        next: ABORT
        requires_user_input: true  # ユーザー入力待機（インタラクティブのみ）

  # 並列ムーブメント
  - name: reviewers
    parallel:
      - name: arch-review
        persona: reviewer
        instruction: review-arch
        rules:
          - condition: approved
          - condition: needs_fix
      - name: security-review
        persona: security-reviewer
        instruction: review-security
        rules:
          - condition: approved
          - condition: needs_fix
    rules:
      - condition: all("approved")
        next: COMPLETE
      - condition: any("needs_fix")
        next: fix

  # アルペジオムーブメント（バッチ処理）
  - name: batch-process
    persona: coder
    arpeggio:
      source: csv
      source_path: ./data/items.csv
      batch_size: 5
      concurrency: 3
      template: ./templates/process.txt
      merge:
        strategy: concat
        separator: "\n---\n"
      output_path: ./output.txt
    rules:
      - condition: "完了"
        next: COMPLETE

  # チームリーダームーブメント（動的タスク分解）
  - name: implement
    team_leader:
      max_parts: 3
      timeout_ms: 600000
      part_persona: coder
      part_edit: true
    instruction_template: |
      タスク分解...
    rules:
      - condition: "全パート完了"
        next: review
```

### 自動注入される変数

- `{task}` - ユーザー要求（テンプレートに未指定なら自動注入）
- `{previous_response}` - 前ムーブメント出力（自動注入）
- `{user_inputs}` - ユーザー入力累積（自動注入）
- `{iteration}` - ピース全体の実行回数
- `{movement_iteration}` - ムーブメント個別の実行回数
- `{report_dir}` - レポートディレクトリ
- `{report:filename}` - レポートファイル内容埋め込み

## ルール条件3タイプ

1. **タグベース**: `"条件テキスト"` → エージェント出力の`[STEP:N]`タグで条件指定
2. **AI判定**: `ai("条件テキスト")` → AIが動的に条件評価
3. **集約**: `all("X")` / `any("X")` → 並列ムーブメント結果の集約

## ムーブメント実行フロー

### 3フェーズ実行モデル

各ムーブメントは最大3フェーズで実行：

| フェーズ | 目的 | ツール | タイミング |
|---------|------|--------|----------|
| Phase 1 | メイン作業（コーディング、レビュー等） | ムーブメント指定ツール | 常に実行 |
| Phase 2 | レポート出力 | Write のみ | output_contracts定義時 |
| Phase 3 | ステータス判定 | なし（判定のみ） | タグベースルール定義時 |

セッションはフェーズ間で再開され、コンテキスト継続。

### ルール評価（5段階フォールバック）

ムーブメント実行後、以下順序でルール評価（最初にマッチしたものが優先）：

1. 集約（all()/any()） - 並列親ムーブメント用
2. Phase 3タグ - `[STEP:N]`タグ（フェーズ3出力）
3. Phase 1タグ - `[STEP:N]`タグ（フェーズ1出力）
4. AI判定 - ai()条件のみ
5. AI判定フォールバック - すべての条件をAI評価

複数の`[STEP:N]`タグが出力された場合は**最後の一致を採用**。

## CLIコマンド主要例

```bash
# ピースの実行
takt {task}              # タスクを指定して実行
takt                     # インタラクティブモード
takt run                 # .takt/tasks/内のペンディングタスク実行
takt watch               # .takt/tasks/監視・自動実行

# タスク管理
takt add [task]          # AIとの会話でタスク追加
takt list                # タスク一覧（マージ、削除、リトライ）
takt clear               # エージェントセッション初期化

# ピース/ファセット管理
takt eject piece {name}  # ビルトイン → ~/.takt/pieces/
takt prompt {piece}      # 各ムーブメント・フェーズの最終プロンプト確認
takt catalog {type}      # 利用可能ファセット一覧

# 設定・ユーティリティ
takt config              # グローバル設定（許可モード）
takt reset config        # デフォルト設定に戻す
takt metrics review      # レビュー品質メトリクス
takt export-cc           # TAKT → Claude Code Skill エクスポート
takt export-codex        # TAKT → Codex Skill エクスポート
```

## ビルトイン・ピース一覧（日本語）

カテゴリ分類（piece-categories.yaml）：

- **🚀 クイックスタート**: default, frontend-mini, backend-mini, compound-eye
- **⚡ Mini**: 軽量版（frontend, backend, dual各mini）
- **🎨 フロントエンド**: frontend, frontend-mini
- **⚙️ バックエンド**: backend, backend-cqrs, mini各版
- **🔧 デュアル**: dual, dual-cqrs, mini各版
- **🏗️ インフラ**: terraform
- **🔍 レビュー**: review-*（デフォルト、フロント、バック、デュアル）
- **🧪 テスト**: unit-test, e2e-test
- **🎵 TAKT開発**: takt-default, review-takt-default
- **その他**: research, deep-research, magi

各ピースは`default.yaml`, `backend.yaml`, `frontend.yaml`, `dual.yaml`, `research.yaml`等の形式で参照/takt/builtins/{ja|en}/pieces/に格納。

## プロバイダ統合

5つのプロバイダをサポート：

| プロバイダ | SDK | セッション | 特徴 |
|----------|-----|-----------|------|
| **Claude** | @anthropic-ai/claude-agent-sdk | ファイルベース | クエリID, 権限モード（readonly/edit/full） |
| **Codex** | @openai/codex-sdk | インメモリ | リトライ（3試行、指数バックオフ） |
| **OpenCode** | @opencode-ai/sdk/v2 | サーバープール | クライアント権限自動応答 |
| **Cursor** | - | - | 予約済み |
| **Copilot** | - | - | 予約済み |
| **Mock** | 内部実装 | メモリ | 決定的レスポンス（テスト用） |

## レパートリー（外部パッケージ）

GitHub から ファセット・ピース集をインストール：

```bash
takt repertoire add github:{owner}/{repo}@{ref}
takt repertoire list
takt repertoire remove {scope}
```

パッケージは`~/.takt/repertoire/@{owner}/{repo}/`にインストール。

## 重要な実装上の注意点

1. **ペルソナ・プロンプト解決**: ピース YAML に相対パス指定 → ピースファイル基点で解決。ビルトイン personas は `builtins/{lang}/facets/personas/` から読み込み。
2. **セッション継続**: エージェント・セッションはフェーズ 1 → 2 → 3 で継続。session キー: `{persona}:{provider}`。worktree/clone 実行時は新規セッション。
3. **ルール評価の落とし穴**:
   - 複数の `[STEP:N]` タグがある場合は **最後の一致を採用**
   - `ai()` 条件は AI が評価（文字列マッチングではない）
   - 集約条件は並列親ムーブメント限定
   - ルール定義あるが マッチ失敗 → ABORT
4. **権限モード**: `readonly`, `edit`, `full`。movement の `required_permission_mode` は最小ライン。プロバイダプロファイルで上書き可能。
5. **Loop Detection vs Cycle Detection**:
   - LoopDetector: 同じムーブメント連続実行検出（簡易）
   - CycleDetector: ムーブメント間のサイクルパターン検出（loop_monitors）

## 参考ファイル場所

- ビルトイン日本語ピース: `/references/takt/builtins/ja/pieces/`
- ビルトイン英語ピース: `/references/takt/builtins/en/pieces/`
- E2E テスト・フィクスチャ: `/references/takt/e2e/fixtures/pieces/`
- スキーマ定義: `/references/takt/src/core/models/schemas.ts`, `piece-types.ts`
- ドキュメント: `/references/takt/docs/pieces.md`

