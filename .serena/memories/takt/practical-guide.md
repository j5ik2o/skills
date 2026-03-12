# TAKT 実践ガイド

## ピース選択フロー

```
ユーザー: 「このタスクを実装してください」
  ↓
選択: 新規実装? 既存レビュー? 調査?
  ├─ 新規実装
  │  ├─ 複雑な実装 → default
  │  ├─ バックエンド特化 → backend
  │  ├─ フロント特化 → frontend
  │  ├─ フロント+バック → dual / dual-cqrs
  │  └─ シンプル修正 → *-mini
  ├─ 既存コードレビュー
  │  └─ review-default / review-{type}
  └─ 情報収集
     └─ research / deep-research
```

## コマンド使用例

### 1. 新規実装（ユーザーがタスク説明）

```bash
# インタラクティブモード（AIが質問、ユーザーが回答）
takt "TypeScript型定義ファイルを作成してください"

# パイプラインモード（CI/CD用、非対話）
takt "TypeScript型定義ファイル作成" --pipeline --auto-pr
```

結果:
- 新規ブランチ作成
- 既定ピース（default）で実行
- コミット自動作成
- PR作成（--auto-pr時）

### 2. 既存コード修正

```bash
# GitHub Issue から タスク取得
takt #42

# PR レビューコメント取得 + 修正実行
takt --pr 99
```

### 3. 調査

```bash
takt "React 18のServer Component について調査してください" -w research
```

-w: ピース指定（research）

### 4. ピースカスタマイズ

```bash
# ビルトインをユーザー ~/.takt/pieces/ にコピー
takt eject piece default

# ~/.takt/pieces/default.yaml を編集、カスタマイズ
# 次回実行から新規定義が利用される

# グローバル config 確認
takt config
```

## ピースカスタマイズ例

### ユースケース: テストを最後に追加するバージョン

通常 default は「テスト先行」ですが、「実装後テスト」に変更する場合：

1. `takt eject piece default`
2. `~/.takt/pieces/default.yaml` 編集:
   - ムーブメント順序変更: implement → write_tests → reviewers
   - または write_tests を削除

3. 保存して次回実行

## ループ検出と Judge の役割

### Cycle Detection

```yaml
loop_monitors:
  - cycle: [ai_review, ai_fix]
    threshold: 3
    judge:
      persona: supervisor
      instruction_template: |
        ai_review ↔ ai_fix ループが {cycle_count} 回繰り返された...
      rules:
        - condition: 健全（進捗あり）
          next: ai_review
        - condition: 非生産的（同じ問題繰り返し）
          next: reviewers
```

**動作**:
- ai_review → ai_fix → ai_review → ai_fix → ai_review (3サイクル)
- 3サイクル目に自動的に supervisor persona で judge ムーブメント挿入
- judge の判定結果で次ムーブメント決定

## ルール条件の選択

### 1. タグベース（推奨、最も確実）

```yaml
rules:
  - condition: "実装完了"
    next: review
  - condition: "実装未着手"
    next: review
  - condition: "実装困難"
    next: ABORT
```

**メカニズム**: エージェント出力に `[STEP:0]`, `[STEP:1]`, `[STEP:2]` タグを付加させる。配列インデックスで条件マッチ。

```
エージェント出力:
...説明...
[STEP:0]  ← 0番目の条件（実装完了）にマッチ
```

### 2. AI 判定（複雑な条件）

```yaml
rules:
  - condition: ai("実装にセキュリティの問題がないか")
    next: review
  - condition: ai("パフォーマンス最適化の余地があるか")
    next: optimize
```

**メカニズム**: AI が条件文を読んで、エージェント出力を評価して判定。処理時間かかるため、必要な場合のみ。

### 3. 集約（並列ムーブメント限定）

```yaml
movements:
  - name: reviewers
    parallel:
      - name: arch-review
        rules:
          - condition: approved
          - condition: needs_fix
      - name: security-review
        rules:
          - condition: approved
          - condition: needs_fix
    rules:
      - condition: all("approved")
        next: COMPLETE
      - condition: any("needs_fix")
        next: fix
```

**メカニズム**: 
- all("approved"): 両方の sub-movement が "approved" を選んだ場合のみ true
- any("needs_fix"): いずれか一つが "needs_fix" を選んだ場合 true

## セッション管理

### Session Continuity

デフォルト: `session: continue`
- Phase 1 → Phase 2 → Phase 3 でセッション再開
- エージェント・コンテキスト保持
- 同じペルソナ・プロバイダの組み合わせは再利用

### Session Refresh

```yaml
- name: implement
  session: refresh
```

前のセッションを破棄、新規セッション開始。
- メモリリセット
- 新しい観点での実装開始
- CPU コスト増加

## Phase 1, 2, 3 の理解

### Phase 1: Main Work

メインの作業実行。エージェントがツールを使用。

```
入力: {task}, {instruction_template}, ポリシー・ナレッジ
出力: エージェント作業結果
      + [STEP:N] タグ（ルール評価用）
```

### Phase 2: Report Output

output_contracts 定義あるとき、レポート生成フェーズ。Write ツールのみ使用。

```
入力: Phase 1 出力 + {report_dir}
出力: report_formats に基づくファイル生成
```

Phase 2 指示例:
```
Move the analysis results to {report_dir}/analysis.md
```

### Phase 3: Status Judgment

タグベースルール定義ありのとき、ステータス判定フェーズ（ツールなし）。

```
入力: Phase 1 + Phase 2 出力
判定: [STEP:N] タグ検出 → ルール評価
出力: 次ムーブメント決定
```

## ファセット配置の原則

4つのファセット、それぞれ異なる責務：

| ファセット | 役割 | 例 |
|----------|------|------|
| **persona** | WHO: AIの役割・専門性・振る舞い | "あなたは経験豊富なPython開発者です..." |
| **policy** | HOW: 判定基準・禁止パターン・REJECT リスト | "内部実装をパブリックAPIとしてエクスポート → REJECT" |
| **knowledge** | WHAT: 詳細知識・理由付け・事例 | "パブリックAPIの公開範囲: 外部利用を前提に..." |
| **instruction** | DO: このムーブメント限定の手順・チェックリスト | "以下の観点でレビュー: 構造・設計..." |

**重要**:
- policy の REJECT リストに載らない基準は、reviewers が検査しない（knowledge にあっても）
- persona は再利用可能。piece 固有の手順を含めない
- instruction は piece・movement 限定。他で再利用不可
- knowledge は推論・事例に使う。instruction ではなく knowledge に詳細を書く

## CI/CD 統合例

GitHub Actions での TAKT 実行：

```yaml
name: TAKT Code Review

on:
  pull_request:
    types: [opened, synchronize]

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
      - run: npm install -g takt

      # 既存 PR コメント取得 + 修正
      - run: |
          takt --pr ${{ github.event.pull_request.number }} \
               -w review-default \
               --pipeline \
               --skip-git
```

`--skip-git`: git 操作スキップ（既に CI 内）

## トラブルシューティング

### Issue: "ループ検出: 同じムーブメントが連続"

```
⚠️ Loop detected: movement 'implement' repeated 10 times
```

原因: ムーブメントの条件が常に同じ。

**対処**:
1. output_contracts/report 定義確認
2. [STEP:N] タグ埋め込み確認
3. ai() 条件の場合、AI 判定ロジック確認
4. 必要に応じて cycle detection で judge 設定

### Issue: "ルール評価失敗"

```
ERROR: Rules exist but no rule matched. Aborting.
```

原因: [STEP:N] タグなし、ai() 評価失敗、集約条件ミスマッチ。

**対処**:
1. Phase 1 出力に [STEP:N] あるか確認
2. 条件数と rules 数の一致確認
3. エージェント出力ログ確認
4. `takt prompt {piece}` で最終指示確認

### Issue: "セッション情報消失"

```
takt clear
```

全セッション初期化。新規セッション再開。

### Issue: "複数の [STEP:N] タグ"

```
...説明...
[STEP:0]
...続き...
[STEP:1]
```

**動作**: 最後の [STEP:1] が採用される。

## デバッグ tips

```bash
# 最終プロンプト確認
takt prompt {piece}

# ピース構造確認
takt eject piece {name}  # ~/.takt/pieces/{name}.yaml 生成

# セッションログ確認
tail -f .takt/logs/latest.jsonl

# ビルトイン ピース確認
takt catalog pieces

# デバッグモード有効化
# ~/.takt/config.yaml:
logging:
  debug: true
  level: debug
```

