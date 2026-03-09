#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)
REPO_ROOT=$(cd "${SCRIPT_DIR}/.." && pwd)
cd "$REPO_ROOT"

SKILL_NAME="skill-forge"

SKILL_DIRS=(
  ".agents/skills"
  ".claude/skills"
  ".codex/skills"
  ".gemini/skills"
  ".cursor/skills"
  ".opencode/skills"
)

for dir in "${SKILL_DIRS[@]}"; do
  target="$dir/$SKILL_NAME"

  if [ ! -L "$target" ]; then
    echo "SKIP: $target (not a symlink)"
    continue
  fi

  rm "$target"
  echo "UNLINK: $target"
done
