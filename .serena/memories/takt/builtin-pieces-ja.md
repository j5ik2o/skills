# TAKT ビルトインピース詳細（日本語版）

## default ピース

テスト駆動開発ピース。最も汎用的で標準的なワークフロー。

**ワークフロー**: plan → write_tests → implement → ai_review → ai_fix → parallel reviewers (arch-review, supervise) → fix → COMPLETE

**特徴**:
- 計画フェーズで要件確認
- テスト先行開発
- AI特有の問題を専門チェック
- 並列アーキレビュー + スーパーバイズ
- reviewers ↔ fix ループ監視（3サイクルで judge）

**主要ムーブメント**:
- `plan`: 要件分析、実装可能性判定
  - 条件分岐: 明確/質問/不明確
  - edit: false, 読み取り専用
- `write_tests`: テスト作成
  - edit: true, 編集権限必須
  - output: test-scope.md, test-decisions.md
- `implement`: 実装
  - session: refresh (前セッション破棄)
  - policy: [coding, testing]
- `ai_review`: AI特有の問題検査
  - persona: ai-antipattern-reviewer
  - policy: [review, ai-antipattern]
- `ai_fix`: AI レビュー指摘への修正
  - pass_previous_response: false (レビュー内容を別に参照)
- `reviewers` (parallel):
  - arch-review: アーキテクチャレビュー
  - supervise: スーパーバイズ、全体確認
  - 集約: all("approved", "すべて問題なし") → COMPLETE
  - any("needs_fix", "要求未達成...") → fix
- `fix`: 指摘対応

**ループ監視**:
1. ai_review ↔ ai_fix: 3サイクルで judge
   - 健全（進捗あり）→ ai_review
   - 非生産的 → reviewers
2. reviewers ↔ fix: 3サイクルで judge
   - 健全（指摘減少）→ reviewers
   - 非生産的 → ABORT

## backend ピース

バックエンド・セキュリティ・QA専門レビュー対応

**ワークフロー**: plan → implement → ai_review → ai_fix → parallel reviewers (arch-review, security-review, qa-review, supervise) → fix → COMPLETE

**固有機能**:
- backend ナレッジ組み込み
- security ポリシー適用
- 4並列レビュー（アーキ、セキュリティ、QA、スーパーバイズ）
- ループ監視: reviewers ↔ fix

## frontend ピース

フロントエンド専門レビュー対応

**ワークフロー**: plan → implement → reviewers (frontend-review, a11y-review, supervise) → fix → COMPLETE

**特徴**:
- UI/UX レビュー専門化
- アクセシビリティ チェック
- 2並列レビュー + スーパーバイズ

## dual ピース

フロントエンド + バックエンド統合開発

**ワークフロー**: plan → parallel [frontend-dev, backend-dev] → parallel reviewers → fix → COMPLETE

**特徴**:
- フロント・バック同時開発（並列実行）
- 統合テスト
- 両領域の専門レビュー

## dual-cqrs ピース

CQRS（Command Query Responsibility Segregation）パターン対応

フロント/バック並列開発 + 分離されたコマンド/クエリハンドリング

## research ピース

調査・研究・情報収集専門ピース

**ワークフロー**: plan → dig → supervise → COMPLETE

**特徴**:
- plan: 調査計画策定
- dig: インターネット検索・情報収集
- supervise: 結果評価・要件満足確認
- ユーザー質問対応（実装タスクではない場合）

**制約**:
- max_movements: 10 (調査は短期)
- 読み取り専用（edit: false）

## *-mini ピース

軽量版。実装が簡単な場合の高速ワークフロー。

- frontend-mini, backend-mini, dual-mini
- 削減フェーズ: テスト作成スキップ、レビュー簡略化など

## compound-eye ピース

複合眼（複数視点）レビュー。

実装後、複数の専門家による同時パラレルレビュー。

## terraform ピース

Terraform / IaC（Infrastructure as Code）修正/改善

- インフラストラクチャコードの計画・検証
- plan コマンドでの検証
- セキュリティ・ベストプラクティスレビュー

## review-* ピース

既存コードへの専門レビュー・修正。新規実装ではなく、既存コードへのレビュー・指摘・修正サイクル。

- review-default
- review-frontend, review-backend, review-dual
- review-backend-cqrs, review-dual-cqrs
- review-fix-*: レビュー指摘への修正専門

## takt-default ピース

TAKT自体の開発・改善用。

テストドリブン開発 + ユニットテスト・E2Eテスト・TypeScript型チェック統合。

## unit-test, e2e-test ピース

テスト作成・実行専門。既存テスト拡充・新規テスト作成用。

## deep-research ピース

深掘り調査。一般的な research より長く、複雑な調査に対応。

- max_movements: 20
- 複数ラウンド反復可能

## magi ピース

実験的・多角的探索ピース。（「3人の賢者」の意）

複数の異なるアプローチを並列探索。

---

## ピース選択基準

| 用途 | 推奨ピース | 理由 |
|------|----------|------|
| 新規実装（汎用） | default | テスト駆動、標準ワークフロー |
| 新規バックエンド | backend | セキュリティ・QA重視 |
| 新規フロントエンド | frontend | UI/UX・a11y重視 |
| フロント+バック統合 | dual / dual-cqrs | 並列開発 |
| 既存コードレビュー | review-default / review-* | レビュー専門 |
| 簡単な修正 | *-mini | 短期ワークフロー |
| 調査・情報収集 | research / deep-research | 読み取り専用 |
| インフラコード | terraform | IaC専門 |
| TAKT開発 | takt-default | テスト・型チェック統合 |
| テスト作成 | unit-test / e2e-test | テスト専門 |

