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
# Use a dedicated venv so this works on externally-managed Pythons
# (PEP 668, e.g. Homebrew or system Python on macOS) and keeps the tool's
# dependencies isolated from the rest of the system.

BIN_DIR="$HOME/.local/bin"
VENV_DIR="$HOME/.local/share/search-cli/venv"
mkdir -p "$BIN_DIR"

echo "Installing search-cli from $SCRIPT_DIR into $VENV_DIR ..."

if [ ! -x "$VENV_DIR/bin/python" ]; then
  if ! python3 -m venv "$VENV_DIR"; then
    echo "error: could not create a venv. Install a Python with venv support" >&2
    echo "  macOS (Homebrew):  brew install python" >&2
    exit 1
  fi
fi

"$VENV_DIR/bin/pip" install -q --upgrade pip
"$VENV_DIR/bin/pip" install -q "$SCRIPT_DIR"

# Symlink the venv console script into ~/.local/bin so it lands on PATH.
SRC="$VENV_DIR/bin/search-cli"
DEST="$BIN_DIR/search-cli"

if [ ! -x "$SRC" ]; then
  echo "error: $SRC not found after install" >&2
  exit 1
fi

ln -sfn "$SRC" "$DEST"
echo "Installed: $DEST -> $SRC"

# --- 2. Install the web-search agent skill ----------------------------------
# The skill ships in this repo (skills/web-search); install it into the
# shared agent skills dir, optionally linked into the Claude skills folder.

SKILL_SRC="$SCRIPT_DIR/skills/web-search"
SKILL_DEST="$HOME/.agents/skills/web-search"
CLAUDE_SKILLS_DIR="$HOME/.claude/skills"

if [ ! -f "$SKILL_SRC/SKILL.md" ]; then
  echo "error: $SKILL_SRC/SKILL.md not found" >&2
  exit 1
fi

mkdir -p "$HOME/.agents/skills"
rm -rf "$SKILL_DEST"
cp -r "$SKILL_SRC" "$SKILL_DEST"
echo "Installed: $SKILL_DEST"

# Optionally symlink into the Claude skills folder (auto if it already
# exists, or force with --claude).
if [ -d "$CLAUDE_SKILLS_DIR" ] || [ "$WITH_CLAUDE" = true ]; then
  mkdir -p "$CLAUDE_SKILLS_DIR"
  ln -sfn "$SKILL_DEST" "$CLAUDE_SKILLS_DIR/web-search"
  echo "Linked: $CLAUDE_SKILLS_DIR/web-search -> $SKILL_DEST"
fi

echo
echo "Make sure ~/.local/bin is on your PATH, e.g.:"
echo "  echo 'export PATH=\"\$HOME/.local/bin:\$PATH\"' >> ~/.bashrc"
echo
echo "Try it:  search-cli sources"
