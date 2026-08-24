#!/usr/bin/env bash
# Install search-cli and make it available in ~/.local/bin.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BIN_DIR="$HOME/.local/bin"
mkdir -p "$BIN_DIR"

echo "Installing search-cli from $SCRIPT_DIR ..."
python3 -m pip install --user "$SCRIPT_DIR"

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
echo "Installed: $DEST -> $SRC"
echo
echo "Make sure ~/.local/bin is on your PATH, e.g.:"
echo "  echo 'export PATH=\"\$HOME/.local/bin:\$PATH\"' >> ~/.bashrc"
echo
echo "Try it:  search-cli sources"
