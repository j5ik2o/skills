#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)
PROJECT_ROOT=$(cd "$SCRIPT_DIR/.." && pwd)
MARKETPLACE_JSON="$PROJECT_ROOT/.claude-plugin/marketplace.json"

# 認証情報の読み込み
source "$HOME/.config/claude-code/env-corporate"

# 一時ディレクトリで ~/.claude を隔離
TMPDIR=$(mktemp -d)
trap 'rm -rf "$TMPDIR"' EXIT
export CLAUDE_CONFIG_DIR="$TMPDIR"

echo "=== CLAUDE_CONFIG_DIR: $TMPDIR ==="

# marketplace.json からプラグイン名一覧を取得
plugin_names() {
  python3 -c "
import json, sys
with open('$MARKETPLACE_JSON') as f:
    data = json.load(f)
for p in data.get('plugins', []):
    print(p['name'])
"
}

# marketplace.json から全スキルパスを取得し、SKILL.md の name を抽出
skill_names() {
  python3 -c "
import json, yaml, sys, os
with open('$MARKETPLACE_JSON') as f:
    data = json.load(f)
for p in data.get('plugins', []):
    for s in p.get('skills', []):
        skill_md = os.path.join('$PROJECT_ROOT', s, 'SKILL.md')
        if os.path.exists(skill_md):
            with open(skill_md) as sf:
                content = sf.read()
            # YAML front matter を解析
            if content.startswith('---'):
                end = content.index('---', 3)
                fm = yaml.safe_load(content[3:end])
                if fm and 'name' in fm:
                    print(fm['name'])
"
}

failures=0

# --- 1. マニフェスト検証 ---
echo ""
echo "--- Validate marketplace ---"
claude plugin validate "$PROJECT_ROOT"

for plugin_dir in "$PROJECT_ROOT"/plugins/*/; do
  if [ -d "${plugin_dir}.claude-plugin" ]; then
    echo "--- Validate $(basename "$plugin_dir") ---"
    claude plugin validate "$plugin_dir"
  fi
done

# --- 2. マーケットプレイス登録 ---
echo ""
echo "--- Add marketplace ---"
claude plugin marketplace add "$PROJECT_ROOT"
claude plugin marketplace list

# --- 3. プラグインインストール ---
echo ""
echo "--- Install plugins ---"
for name in $(plugin_names); do
  echo "Installing: $name"
  claude plugin install "$name" || true
done

echo ""
echo "--- Installed plugins ---"
claude plugin list

# --- 4. スキル認識の確認 (claude -p でスラッシュコマンドを呼び出し) ---
echo ""
echo "--- Verify skill recognition ---"
for skill in $(skill_names); do
  echo -n "  /$skill ... "
  # スキルを呼び出して "Unknown skill" が出なければOK
  output=$(claude -p "/$skill" --print 2>&1 || true)
  if echo "$output" | grep -qi "Unknown skill"; then
    echo "FAIL (Unknown skill)"
    failures=$((failures + 1))
  else
    echo "OK"
  fi
done

# --- 結果 ---
echo ""
if [ "$failures" -gt 0 ]; then
  echo "=== FAILED: $failures skill(s) not recognized ==="
  exit 1
else
  echo "=== All skills recognized ==="
fi
