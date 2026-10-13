#!/usr/bin/env python3
"""Run by the claude session (via Monitor) to receive questions about its docs.

Usage: watch.py <doc.html> [<doc.html> ...]

Prints one JSON line per unanswered question, once per run, starting with any
already waiting. Keeps a heartbeat so the page can show "claude is listening".
"""
import json
import sys
import time

import qa

docs = [qa.stem(d) + ".html" for d in sys.argv[1:]]
if not docs:
    sys.exit(__doc__)
qa.QA.mkdir(parents=True, exist_ok=True)
seen = set()
while True:
    for doc in docs:
        qa.beat_path(doc).touch()
        for item in qa.thread(doc):
            if item["answer"] is None and item["id"] not in seen:
                seen.add(item["id"])
                print(json.dumps({k: item.get(k) for k in ("id", "doc", "section", "quote", "question")}, ensure_ascii=False), flush=True)
    time.sleep(1)
