#!/usr/bin/env bash
# Install search-cli, make it available in ~/.local/bin, and install the
# web-search agent skill (optionally linked into the Claude skills folder).
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

WITH_CLAUDE=false
for arg in "$@"; do
  case "$arg" in
    -c|--claude) WITH_CLAUDE=true ;;
    *)
      echo "unknown option: $arg (usage: install.sh [--claude])" >&2
      exit 1
      ;;
  esac
done

# --- 1. Install the CLI -----------------------------------------------------

BIN_DIR="$HOME/.local/bin"
mkdir -p "$BIN_DIR"

echo "Installing search-cli from $SCRIPT_DIR ..."
python3 -m pip install --user -q "$SCRIPT_DIR"

# pip --user places console scripts in the user base bin dir;
# symlink it into ~/.local/bin so it lands on PATH.
USER_BASE="$(python3 -m site --user-base)"
SRC="$USER_BASE/bin/search-cli"
DEST="$BIN_DIR/search-cli"

if [ ! -x "$SRC" ]; then
  echo "error: $SRC not found after install" >&2
  exit 1
fi

if [ "$(readlink -f "$SRC")" = "$(readlink -f "$DEST" 2>/dev/null)" ]; then
  echo "Installed: $DEST (already in place)"
else
  ln -sfn "$SRC" "$DEST"
  echo "Installed: $DEST -> $SRC"
fi

# --- 2. Install the web-search agent skill ----------------------------------

SKILL_SRC="$HOME/.agents/skills/web-search"
CLAUDE_SKILLS_DIR="$HOME/.claude/skills"

if [ ! -d "$SKILL_SRC" ]; then
  echo "note: $SKILL_SRC not found; skipping web-search skill"
else
  echo "Skill available: $SKILL_SRC"

  # Optionally symlink into the Claude skills folder (auto if it already
  # exists, or force with --claude).
  if [ -d "$CLAUDE_SKILLS_DIR" ] || [ "$WITH_CLAUDE" = true ]; then
    mkdir -p "$CLAUDE_SKILLS_DIR"
    ln -sfn "$SKILL_SRC" "$CLAUDE_SKILLS_DIR/web-search"
    echo "Linked: $CLAUDE_SKILLS_DIR/web-search -> $SKILL_SRC"
  fi
fi

echo
echo "Make sure ~/.local/bin is on your PATH, e.g.:"
echo "  echo 'export PATH=\"\$HOME/.local/bin:\$PATH\"' >> ~/.bashrc"
echo
echo "Try it:  search-cli sources"
