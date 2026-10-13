#!/usr/bin/env python3
"""Local server for research docs: serves ~/research and takes questions.

  GET  /<doc>.html            the doc (and _assets/)
  GET  /api/thread?doc=<file> questions + answers for a doc, and whether a
                              claude session is listening
  POST /api/ask               {doc, section, quote, question}

Binds to 127.0.0.1 only. POSTs must come from this server's own pages
(Origin and Host checked, JSON only), so no other website can push text
into a claude session. Exits after 12 hours without requests.
"""
import json
import secrets
import threading
import time
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

import qa

IDLE_LIMIT = 12 * 3600
last_hit = time.time()
HOSTS = {f"127.0.0.1:{qa.PORT}", f"localhost:{qa.PORT}"}
ORIGINS = {f"http://{h}" for h in HOSTS}
MAX_LEN = {"question": 4000, "quote": 2000, "section": 200}


def valid_doc(doc):
    name = Path(doc or "").name
    return name.endswith(".html") and name != "index.html" and (qa.ROOT / name).is_file() and name


class Handler(SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def _json(self, code, body):
        data = json.dumps(body).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def _host_ok(self):
        return self.headers.get("Host") in HOSTS

    def do_GET(self):
        global last_hit
        last_hit = time.time()
        if not self._host_ok():
            return self._json(403, {"error": "bad host"})
        url = urlparse(self.path)
        if url.path == "/health":
            return self._json(200, {"ok": True})
        if url.path == "/api/thread":
            doc = valid_doc(parse_qs(url.query).get("doc", [""])[0])
            if not doc:
                return self._json(404, {"error": "no such doc"})
            return self._json(200, {"listening": qa.listening(doc), "thread": qa.thread(doc)})
        if url.path.startswith("/_work"):
            return self._json(404, {"error": "not found"})
        return super().do_GET()

    def do_POST(self):
        global last_hit
        last_hit = time.time()
        if not self._host_ok() or self.headers.get("Origin") not in ORIGINS:
            return self._json(403, {"error": "forbidden"})
        if urlparse(self.path).path != "/api/ask":
            return self._json(404, {"error": "not found"})
        if not (self.headers.get("Content-Type") or "").startswith("application/json"):
            return self._json(415, {"error": "json only"})
        try:
            length = min(int(self.headers.get("Content-Length") or 0), 20000)
            body = json.loads(self.rfile.read(length) or b"{}")
        except ValueError:
            return self._json(400, {"error": "bad json"})
        doc = valid_doc(body.get("doc"))
        question = str(body.get("question") or "").strip()
        if not doc or not question:
            return self._json(400, {"error": "doc and question required"})
        event = {"type": "q", "id": secrets.token_hex(4), "doc": doc}
        for key, limit in MAX_LEN.items():
            event[key] = str(body.get(key) or "").strip()[:limit]
        qa.append(doc, event)
        return self._json(200, {"id": event["id"], "listening": qa.listening(doc)})


def reaper(server):
    while True:
        time.sleep(300)
        if time.time() - last_hit > IDLE_LIMIT:
            server.shutdown()
            return


if __name__ == "__main__":
    server = ThreadingHTTPServer(("127.0.0.1", qa.PORT), partial(Handler, directory=str(qa.ROOT)))
    threading.Thread(target=reaper, args=(server,), daemon=True).start()
    server.serve_forever()
