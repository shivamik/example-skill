#!/usr/bin/env bash
set -euo pipefail

REPO="https://github.com/shivamik/example-skill.git"
TMP_DIR=$(mktemp -d)

# Parse flags
GLOBAL=false
for arg in "$@"; do
  case "$arg" in
    --global) GLOBAL=true ;;
  esac
done

if [ "$GLOBAL" = true ]; then
  SKILLS_DIR="$HOME/.agents/skills"
else
  SKILLS_DIR=".agents/skills"
fi

echo ""
echo "📦 Installing ImageKit skills to $SKILLS_DIR..."
echo ""

git clone --depth 1 --quiet "$REPO" "$TMP_DIR"
mkdir -p "$SKILLS_DIR"
cp -r "$TMP_DIR"/src/imagekit_skills/skills/* "$SKILLS_DIR/"
rm -rf "$TMP_DIR"

echo "  ✓ search-docs"
echo "  ✓ transformation-builder"
echo ""

# Interactive MCP prompt
echo "🔌 Would you also like to configure the ImageKit MCP server?"
echo "   This lets your AI tool call ImageKit APIs directly."
echo ""
echo "   [1] VS Code / Copilot"
echo "   [2] Claude Code"
echo "   [3] Cursor"
echo "   [4] Codex"
echo "   [5] All of the above"
echo "   [0] Skip"
echo ""
printf "   Choose [0]: "
read -r choice < /dev/tty

MCP_ENTRY='{ "url": "https://api-mcp.imagekit.in/sse" }'

install_mcp() {
  local file="$1"
  local key="$2"

  if [ -f "$file" ]; then
    if grep -q "imagekit_api" "$file" 2>/dev/null; then
      echo "  • $file already has imagekit_api — skipped"
      return
    fi
  fi

  mkdir -p "$(dirname "$file")"

  if [ ! -f "$file" ]; then
    echo "{}" > "$file"
  fi

  # Use python for safe JSON merge (available on macOS and most Linux)
  python3 -c "
import json, sys
with open('$file') as f:
    config = json.load(f)
config.setdefault('$key', {})
config['$key']['imagekit_api'] = {'url': 'https://api-mcp.imagekit.in/sse'}
with open('$file', 'w') as f:
    json.dump(config, f, indent=2)
    f.write('\n')
"
  echo "  ✓ Configured MCP in $file"
}

configure_mcp() {
  local client="$1"
  if [ "$GLOBAL" = true ]; then
    case "$client" in
      copilot) install_mcp "$HOME/.vscode/mcp.json" "servers" ;;
      claude)  install_mcp "$HOME/.claude/settings.json" "mcpServers" ;;
      cursor)  install_mcp "$HOME/.cursor/mcp.json" "mcpServers" ;;
      codex)   install_mcp "$HOME/.codex/config.json" "mcpServers" ;;
    esac
  else
    case "$client" in
      copilot) install_mcp ".vscode/mcp.json" "servers" ;;
      claude)  install_mcp ".claude/settings.json" "mcpServers" ;;
      cursor)  install_mcp ".cursor/mcp.json" "mcpServers" ;;
      codex)   install_mcp ".codex/config.json" "mcpServers" ;;
    esac
  fi
}

echo ""

case "${choice:-0}" in
  1) configure_mcp copilot ;;
  2) configure_mcp claude ;;
  3) configure_mcp cursor ;;
  4) configure_mcp codex ;;
  5)
    configure_mcp copilot
    configure_mcp claude
    configure_mcp cursor
    configure_mcp codex
    ;;
  0|"") echo "  Skipped MCP config." ;;
  *) echo "  Unknown choice, skipping MCP config." ;;
esac

echo ""
echo "✅ Done!"
echo ""
