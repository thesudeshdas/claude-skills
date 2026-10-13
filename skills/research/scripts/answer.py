#!/usr/bin/env python3
"""Post an answer to a question so it shows on the doc page.

Usage: answer.py <doc.html> <question-id>   (answer text on stdin)
"""
import sys

import qa

if len(sys.argv) != 3:
    sys.exit(__doc__)
doc, qid = sys.argv[1], sys.argv[2]
if not any(q["id"] == qid for q in qa.thread(doc)):
    sys.exit(f"no question {qid} on {doc}")
text = sys.stdin.read().strip()
if not text:
    sys.exit("empty answer")
qa.append(doc, {"type": "a", "id": qid, "answer": text})
print("posted")
