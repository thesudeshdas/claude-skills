#!/usr/bin/env bash
# Install the shared stylesheet and script into the research folder.
# Safe to rerun: always copies, so edits to the skill's assets reach every doc.
set -euo pipefail
SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
OUT="${RESEARCH_DIR:-$HOME/research}"
mkdir -p "$OUT/_assets"
cp "$SKILL_DIR/assets/research.css" "$SKILL_DIR/assets/research.js" "$OUT/_assets/"
echo "$OUT"
