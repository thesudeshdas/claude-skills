#!/usr/bin/env bash
# Start the research server if it isn't running, then print a doc's URL.
# Usage: serve.sh [doc.html]
set -euo pipefail
DIR="$(cd "$(dirname "$0")" && pwd)"
OUT="${RESEARCH_DIR:-$HOME/research}"
PORT="${RESEARCH_PORT:-4317}"
if ! curl -fs "http://127.0.0.1:$PORT/health" >/dev/null 2>&1; then
  mkdir -p "$OUT/_work"
  nohup python3 "$DIR/server.py" >"$OUT/_work/server.log" 2>&1 &
  for _ in $(seq 1 30); do
    curl -fs "http://127.0.0.1:$PORT/health" >/dev/null 2>&1 && break
    sleep 0.2
  done
fi
curl -fs "http://127.0.0.1:$PORT/health" >/dev/null || { echo "server failed to start, see $OUT/_work/server.log" >&2; exit 1; }
echo "http://127.0.0.1:$PORT/$(basename "${1:-index.html}")"
