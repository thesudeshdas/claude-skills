#!/usr/bin/env bash
# symlink the skills in this repo into ~/.claude/skills so claude code picks them up
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
dest="${CLAUDE_SKILLS_DIR:-$HOME/.claude/skills}"
mkdir -p "$dest"
for dir in "$here"/skills/*/; do
  name="$(basename "$dir")"
  target="$dest/$name"
  if [ -e "$target" ] && [ ! -L "$target" ]; then
    echo "skip $name: $target exists and is not a symlink"
    continue
  fi
  ln -sfn "${dir%/}" "$target"
  echo "linked $name -> $target"
done
