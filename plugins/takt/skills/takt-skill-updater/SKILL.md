---
name: takt-skill-updater
description: >
  references/taktサブモジュール更新時に、takt-*スキル群（takt-task-builder, takt-piece-builder,
  takt-facet-builder, takt-analyzer, takt-optimizer）を最新のtaktバージョンに追従させるスキル。
  TypeScriptスキーマ（schema.ts）、ピースYAML、ファセットMarkdownの差分を検出し、
  SKILL.md・参照ドキュメント（task-schema.md等）を体系的に更新する。
  トリガー：「taktスキルを更新」「takt-*スキルの鮮度チェック」「taktバージョンアップ対応」
  「スキルが古くないか確認」「takt skill updater」
---

# TAKT Skill Updater

references/taktサブモジュール更新後に、takt-*スキル群を最新バージョンに追従させる。

> **前提 takt バージョン**: v0.31.0

## パス表記について

本スキルでは `skills/` で始まるパスを使用する。実際のパスは実行環境に応じて読み替える：

| 環境 | プレフィックス |
|------|---------------|
| Claude Code | `.claude/skills/` |
| Codex CLI | `.codex/skills/` |
| 共通（実体） | `.agents/skills/` |

## 対象スキル

| スキル | 実体パス | チェック対象 |
|--------|---------|-------------|
| takt-task-builder | `skills/takt-task-builder/SKILL.md` | TaskRecordスキーマ、ステータス遷移、フィールド一覧 |
| takt-piece-builder | `skills/takt-piece-builder/SKILL.md` | ビルトインピース一覧、YAML構造、新機能フィールド |
| takt-facet-builder | `skills/takt-facet-builder/SKILL.md` | ファセット種別、スタイルガイド参照パス |
| takt-analyzer | `skills/takt-analyzer/SKILL.md` | エンジン仕様参照、ビルトインパス |
| takt-optimizer | `skills/takt-optimizer/SKILL.md` | ログ形式、最適化パラメータ |

## ワークフロー

### Step 1: takt バージョン確認

references/taktの現在のバージョンと、各スキルが前提とするバージョンを比較する。

```bash
# 現在のサブモジュールバージョン
cd references/takt && git describe --tags --abbrev=0

# 各スキルの前提バージョン
grep -r "前提 takt バージョン" skills/takt-*-builder/SKILL.md skills/takt-analyzer/SKILL.md skills/takt-optimizer/SKILL.md
```

バージョンが一致していれば更新不要。差分がある場合は Step 2 に進む。

### Step 2: 差分領域の特定

takt のバージョン間で何が変わったかを特定する。以下の領域を順にチェックする。

#### a) TaskRecord スキーマ差分（→ takt-task-builder）

`references/takt/src/infra/task/schema.ts` を読み、以下を確認する。

チェックポイント:

| 確認項目 | 参照元 | 更新先 |
|---------|--------|--------|
| ステータス enum 値 | `TaskStatusSchema` | `skills/takt-task-builder/references/task-schema.md` |
| TaskExecutionConfig フィールド | `TaskExecutionConfigSchema` | `skills/takt-task-builder/references/task-schema.md` |
| TaskRecord フィールド | `TaskRecordSchema` | `skills/takt-task-builder/references/task-schema.md` |
| superRefine バリデーション | `TaskRecordSchema.superRefine` | `skills/takt-task-builder/references/task-schema.md` ステータス遷移表 |
| TaskFailure 構造 | `TaskFailureSchema` | `skills/takt-task-builder/references/task-schema.md` |

**過去の更新例**: v0.29.0 で `exceeded` ステータス追加、`base_branch`/`exceeded_max_movements`/`exceeded_current_iteration` フィールド追加。

#### b) ビルトインピース差分（→ takt-piece-builder）

```bash
# 現在のビルトインピース一覧
ls references/takt/builtins/ja/pieces/
```

チェックポイント:

| 確認項目 | 参照元 | 更新先 |
|---------|--------|--------|
| ピース名のリネーム | 新旧ファイル名の比較 | `skills/takt-piece-builder/SKILL.md` Step 2 ビルトインテーブル |
| 新規追加ピース | 新ファイルの検出 | `skills/takt-piece-builder/SKILL.md` Step 2 ビルトインテーブル |
| 削除されたピース | 消失ファイルの検出 | `skills/takt-piece-builder/SKILL.md` Step 2 ビルトインテーブル |
| ピースYAML新フィールド | ビルトインYAMLの読み取り | `skills/takt-piece-builder/SKILL.md` Step 3 設計判断ガイド |

**過去の更新例**: v0.28.1 で `expert` → `dual` リネーム、`default-mini` 廃止。v0.29.0 で `review-fix` 系ピース群追加、`quality_gates` フィールド追加。

#### c) ファセット構造差分（→ takt-facet-builder）

```bash
# スタイルガイドの確認
ls references/takt/builtins/ja/*STYLE_GUIDE*.md

# ビルトインファセットの確認
ls references/takt/builtins/ja/facets/{personas,policies,instructions,knowledge,output-contracts}/
```

チェックポイント:

| 確認項目 | 参照元 | 更新先 |
|---------|--------|--------|
| スタイルガイドのパス変更 | ファイル存在チェック | `skills/takt-facet-builder/SKILL.md` 参照資料テーブル |
| ファセット種別の追加/変更 | スタイルガイド内容 | `skills/takt-facet-builder/SKILL.md` ファセット作成規約 |
| 新規ビルトインファセット | 新ファイルの検出 | `skills/takt-facet-builder/SKILL.md` 参照例 |

#### d) エンジン仕様差分（→ takt-analyzer, takt-optimizer）

以下のドキュメントを読み、変更を確認する:
- `references/takt/builtins/skill/references/engine.md`
- `references/takt/builtins/skill/references/yaml-schema.md`

チェックポイント:

| 確認項目 | 参照元 | 更新先 |
|---------|--------|--------|
| ルール評価方式の変更 | engine.md | `skills/takt-analyzer/SKILL.md`, `skills/takt-piece-builder/SKILL.md` |
| 新しいムーブメント種別 | yaml-schema.md | `skills/takt-piece-builder/SKILL.md` |
| ログフォーマット変更 | ソースコード | `skills/takt-optimizer/SKILL.md` |
| テンプレート変数の追加 | InstructionBuilder | `skills/takt-task-builder/references/task-schema.md` |

### Step 3: スキル更新の実施

差分が見つかった領域ごとに更新する。

#### 更新ルール

1. **バージョン表記**: 各 SKILL.md の `> **前提 takt バージョン**:` を最新バージョンに更新
2. **フィールド追加**: 新フィールドは既存テーブルの末尾に追加（順序を保持）
3. **リネーム**: 旧名→新名の注意書きを添える（例: 「v0.28.1 で `expert` → `dual` にリネーム」）
4. **削除**: テーブルから削除し、注意書きで言及
5. **参照ドキュメント**: `skills/takt-task-builder/references/task-schema.md` 等のリファレンスファイルも同時に更新

#### 更新対象ファイル一覧

| ファイル | 更新内容 |
|---------|---------|
| `skills/takt-task-builder/SKILL.md` | ステータス遷移表、フィールド参照、ピース名例 |
| `skills/takt-task-builder/references/task-schema.md` | フィールド一覧、ステータス遷移図、不変条件テーブル |
| `skills/takt-piece-builder/SKILL.md` | ビルトインテーブル、YAML構造例、設計判断ガイド |
| `skills/takt-facet-builder/SKILL.md` | 参照パス、ファセット作成規約 |
| `skills/takt-analyzer/SKILL.md` | 参照パス、分析基準 |
| `skills/takt-optimizer/SKILL.md` | ログ形式、最適化パラメータ |

### Step 4: バリデーション

更新後の整合性を確認する。

#### 自動検証

```bash
# order.md バリデーション（takt-task-builder）
bash .agents/skills/takt-task-builder/scripts/validate-order-md.sh

# ピース・ファセット バリデーション（takt-piece-builder）
bash .agents/skills/takt-piece-builder/scripts/validate-takt-files.sh --pieces
```

#### 手動検証チェックリスト

- [ ] 全 SKILL.md の `前提 takt バージョン` が最新に更新されている
- [ ] `task-schema.md` のステータス enum が `references/takt/src/infra/task/schema.ts` の `TaskStatusSchema` と一致
- [ ] `task-schema.md` のフィールド一覧が `TaskRecordSchema` と `TaskExecutionConfigSchema` の全フィールドを網羅
- [ ] `task-schema.md` の不変条件テーブルが `superRefine` のバリデーションルールと一致
- [ ] `takt-piece-builder/SKILL.md` のビルトインテーブルが `references/takt/builtins/ja/pieces/` の実態と整合
- [ ] `takt-piece-builder/SKILL.md` で廃止・リネームされたピース名が残っていない
- [ ] `takt-facet-builder/SKILL.md` の参照パスが全て実在する
- [ ] `takt-analyzer/SKILL.md` の参照パスが全て実在する

### Step 5: コミットとPR

更新内容をコミットする。

#### ブランチ命名規約

```
chore/update-takt-skills-for-v{バージョン}
```

例: `chore/update-takt-skills-for-v029`

#### コミットメッセージテンプレート

```
chore: update takt-* skills for takt v{バージョン}

- Add "前提 takt バージョン: v{バージョン}" to all takt-* skills
- takt-task: {変更サマリ}
- takt-piece: {変更サマリ}
- Update references/takt submodule to v{バージョン}
```

## 過去の更新履歴

今後の更新時に参照できるよう、主要な変更をここに記録する。

### v0.29.0 → v0.30.0（2026-03-06）

| スキル | 変更内容 |
|--------|---------|
| 全スキル | `前提 takt バージョン: v0.30.0` に更新 |
| takt-task-builder | `pr_failed` ステータス（6番目の終端状態）追加。PR作成失敗を `failed` と分離。`failure` は任意（`failed` と異なり必須ではない） |
| takt-piece-builder | `allowed_tools` → `provider_options.claude.allowed_tools` に移動。Loop monitor の `instruction_template` がビルトインファセット参照に変更（`loop-monitor-ai-fix`, `loop-monitor-reviewers-fix`）。設計判断ガイドに `provider_options` 追加 |
| takt-facet-builder | ビルトイン Instruction に `loop-monitor-ai-fix`, `loop-monitor-reviewers-fix` 追加。レビュー出力契約に `family_tag`/`new`/`persists`/`resolved`/`reopened` セクション構造追加 |
| takt-analyzer | `provider_options` 構造チェック項目追加。`*-provider-events.jsonl`（別ファイル）と `trace.md` のログ記述追加。`observability` → `logging` リネーム反映 |
| takt-optimizer | `instruction_template` テンプレート参照化の最適化項目追加 |

### v0.22.0 → v0.29.0（2026-03-04）

| スキル | 変更内容 |
|--------|---------|
| 全スキル | `前提 takt バージョン: v0.29.0` を追加 |
| takt-task-builder | `exceeded` ステータス（5番目の終端状態）追加。`base_branch`, `exceeded_max_movements`, `exceeded_current_iteration` フィールド追加 |
| takt-piece-builder | `expert` → `dual` リネーム（v0.28.1）。`default-mini` 廃止。`review-fix` 系・`backend`/`frontend` 系ピース追加。`quality_gates` フィールド追加 |
| takt-facet-builder | 変更なし |
| takt-analyzer | 変更なし |
| takt-optimizer | `provider-events.jsonl` 追加（minor） |
