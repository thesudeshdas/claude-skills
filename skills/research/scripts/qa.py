"""Shared helpers for the ask flow: where questions and answers live.

Each doc gets one append-only log at ~/research/_work/qa/<stem>.jsonl:
  {"type": "q", "id": ..., "doc": ..., "section": ..., "quote": ..., "question": ..., "ts": ...}
  {"type": "a", "id": ..., "answer": ..., "ts": ...}
A watcher heartbeat file (<stem>.watch) says a claude session is listening.
"""
import json
import os
import time
from pathlib import Path

ROOT = Path(os.environ.get("RESEARCH_DIR", Path.home() / "research"))
QA = ROOT / "_work" / "qa"
PORT = int(os.environ.get("RESEARCH_PORT", "4317"))
HEARTBEAT_FRESH = 20  # seconds


def stem(doc):
    name = Path(doc).name
    return name[:-5] if name.endswith(".html") else name


def log_path(doc):
    return QA / f"{stem(doc)}.jsonl"


def beat_path(doc):
    return QA / f"{stem(doc)}.watch"


def append(doc, event):
    QA.mkdir(parents=True, exist_ok=True)
    event["ts"] = time.time()
    with open(log_path(doc), "a", encoding="utf-8") as f:
        f.write(json.dumps(event, ensure_ascii=False) + "\n")


def read(doc):
    path = log_path(doc)
    if not path.exists():
        return []
    out = []
    for line in path.read_text(encoding="utf-8").splitlines():
        try:
            out.append(json.loads(line))
        except ValueError:
            pass
    return out


def thread(doc):
    """Questions in order, each with its answer (or None)."""
    qs, answers = [], {}
    for e in read(doc):
        if e.get("type") == "q":
            qs.append(e)
        elif e.get("type") == "a":
            answers[e.get("id")] = e.get("answer")
    return [dict(q, answer=answers.get(q["id"])) for q in qs]


def listening(doc):
    try:
        return time.time() - beat_path(doc).stat().st_mtime < HEARTBEAT_FRESH
    except OSError:
        return False
