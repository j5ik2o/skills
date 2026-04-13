#!/usr/bin/env bash
set -euo pipefail

# takt サブモジュールから各 takt-* スキルの references/ へ必要なファイルを同期する。
# rsync --delete により、サブモジュール側で削除されたファイルはスキル側からも削除される。
#
# Usage: ./sync-takt-references.sh [--dry-run]

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
TAKT_SRC="$REPO_ROOT/references/takt"
SKILLS_DIR="$REPO_ROOT/plugins/takt/skills"

DRY_RUN=""
if [[ "${1:-}" == "--dry-run" ]]; then
  DRY_RUN="--dry-run"
  echo "[dry-run] 実際のコピーは行いません"
fi

if [[ ! -d "$TAKT_SRC" ]]; then
  echo "ERROR: references/takt が見つかりません: $TAKT_SRC" >&2
  exit 1
fi

# --- 同期ユニット定義 ---
# 各ユニットは rsync の単位。ディレクトリは末尾 / 付き、ファイルは個別指定。

sync_dir() {
  local src="$1" dst="$2"
  mkdir -p "$dst"
  rsync -a --delete $DRY_RUN "$src" "$dst"
}

sync_files() {
  local dst_dir="$1"
  shift
  mkdir -p "$dst_dir"
  for src in "$@"; do
    local rel_dir
    rel_dir="$(dirname "$src" | sed "s|^$TAKT_SRC/||")"
    mkdir -p "$dst_dir/$rel_dir"
    rsync -a $DRY_RUN "$src" "$dst_dir/$rel_dir/"
  done
}

# 指定ディレクトリ配下で、ソースに存在しないファイルを削除
clean_orphans() {
  local src_base="$1" dst_base="$2"
  if [[ ! -d "$dst_base" ]]; then
    return
  fi
  find "$dst_base" -type f | while read -r dst_file; do
    local rel="${dst_file#$dst_base/}"
    if [[ ! -f "$src_base/$rel" ]]; then
      if [[ -z "$DRY_RUN" ]]; then
        rm -f "$dst_file"
        echo "  deleted: $rel"
      else
        echo "  [dry-run] would delete: $rel"
      fi
    fi
  done
  # 空ディレクトリを削除
  if [[ -z "$DRY_RUN" ]]; then
    find "$dst_base" -type d -empty -delete 2>/dev/null || true
  fi
}

echo "=== takt references sync ==="
echo "Source: $TAKT_SRC"
echo ""

# ------------------------------------------------------------------
# takt-task-builder
# ------------------------------------------------------------------
SKILL="takt-task-builder"
echo "[$SKILL]"
DST="$SKILLS_DIR/$SKILL/references/takt"

# docs
sync_dir "$TAKT_SRC/docs/" "$DST/docs/"
# builtins/project/tasks
sync_dir "$TAKT_SRC/builtins/project/tasks/" "$DST/builtins/project/tasks/"
# builtins/skill/references
sync_dir "$TAKT_SRC/builtins/skill/references/" "$DST/builtins/skill/references/"
# src/infra/task (schema.ts)
sync_files "$DST" "$TAKT_SRC/src/infra/task/schema.ts"
clean_orphans "$TAKT_SRC/src/infra/task" "$DST/src/infra/task"

echo ""

# ------------------------------------------------------------------
# takt-workflow-builder
# ------------------------------------------------------------------
SKILL="takt-workflow-builder"
echo "[$SKILL]"
DST="$SKILLS_DIR/$SKILL/references/takt"

# docs
sync_dir "$TAKT_SRC/docs/" "$DST/docs/"
# builtins/skill/references
sync_dir "$TAKT_SRC/builtins/skill/references/" "$DST/builtins/skill/references/"
# builtins/ja (style guides, pieces, facets, templates)
sync_dir "$TAKT_SRC/builtins/ja/" "$DST/builtins/ja/"

echo ""

# ------------------------------------------------------------------
# takt-facet-builder
# ------------------------------------------------------------------
SKILL="takt-facet-builder"
echo "[$SKILL]"
DST="$SKILLS_DIR/$SKILL/references/takt"

# docs
sync_files "$DST" "$TAKT_SRC/docs/faceted-prompting.ja.md"
# builtins/ja (style guides, facets, templates — pieces は不要だが分離コストと比較して全体同期)
sync_dir "$TAKT_SRC/builtins/ja/" "$DST/builtins/ja/"

echo ""

# ------------------------------------------------------------------
# takt-analyzer
# ------------------------------------------------------------------
SKILL="takt-analyzer"
echo "[$SKILL]"
DST="$SKILLS_DIR/$SKILL/references/takt"

# docs
sync_dir "$TAKT_SRC/docs/" "$DST/docs/"
# builtins/skill/references
sync_dir "$TAKT_SRC/builtins/skill/references/" "$DST/builtins/skill/references/"
# builtins/ja
sync_dir "$TAKT_SRC/builtins/ja/" "$DST/builtins/ja/"
# src/core/logging
sync_dir "$TAKT_SRC/src/core/logging/" "$DST/src/core/logging/"
# src/core/piece/evaluation
sync_files "$DST" "$TAKT_SRC/src/core/piece/evaluation/RuleEvaluator.ts"
clean_orphans "$TAKT_SRC/src/core/piece/evaluation" "$DST/src/core/piece/evaluation"
# src/shared/utils (types.ts)
sync_files "$DST" "$TAKT_SRC/src/shared/utils/types.ts"
clean_orphans "$TAKT_SRC/src/shared/utils" "$DST/src/shared/utils"

echo ""

# ------------------------------------------------------------------
# takt-optimizer
# ------------------------------------------------------------------
SKILL="takt-optimizer"
echo "[$SKILL]"
DST="$SKILLS_DIR/$SKILL/references/takt"

# docs
sync_dir "$TAKT_SRC/docs/" "$DST/docs/"
# builtins/skill/references
sync_dir "$TAKT_SRC/builtins/skill/references/" "$DST/builtins/skill/references/"
# builtins/ja
sync_dir "$TAKT_SRC/builtins/ja/" "$DST/builtins/ja/"

echo ""

# ------------------------------------------------------------------
# takt-skill-updater
# ------------------------------------------------------------------
SKILL="takt-skill-updater"
echo "[$SKILL]"
DST="$SKILLS_DIR/$SKILL/references/takt"

# docs
sync_dir "$TAKT_SRC/docs/" "$DST/docs/"
# builtins/skill/references
sync_dir "$TAKT_SRC/builtins/skill/references/" "$DST/builtins/skill/references/"
# builtins/ja
sync_dir "$TAKT_SRC/builtins/ja/" "$DST/builtins/ja/"
# builtins/project/tasks
sync_dir "$TAKT_SRC/builtins/project/tasks/" "$DST/builtins/project/tasks/"
# src/core/logging
sync_dir "$TAKT_SRC/src/core/logging/" "$DST/src/core/logging/"
# src/core/piece/evaluation
sync_files "$DST" "$TAKT_SRC/src/core/piece/evaluation/RuleEvaluator.ts"
clean_orphans "$TAKT_SRC/src/core/piece/evaluation" "$DST/src/core/piece/evaluation"
# src/infra/task
sync_files "$DST" "$TAKT_SRC/src/infra/task/schema.ts"
clean_orphans "$TAKT_SRC/src/infra/task" "$DST/src/infra/task"

echo ""
echo "=== sync complete ==="
