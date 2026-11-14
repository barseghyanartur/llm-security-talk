#!/usr/bin/env python3
"""A small, frameable live view of what the webhook.site catcher has captured.

The slides embed this (a stable URL on :8085) instead of webhook.site itself, so
there is no random token in the slide URL and no X-Frame-Options to fight. It
reads the shared token file and polls webhook.site *server-side*, so the browser
only ever talks to this origin — no CORS, no cross-port fetch.

    python3 webhook/panel.py            # serves http://127.0.0.1:8085
"""

import json
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

HERE = Path(__file__).resolve().parent
TOKEN_FILE = HERE / ".webhook-token"
WEBHOOK = "http://127.0.0.1:8084"
PORT = 8085

PAGE = """<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Captured requests</title>
<style>
  :root { color-scheme: dark; }
  html, body { margin:0; height:100%; }
  body { display:flex; flex-direction:column; background:#111; color:#eee;
    font: 15px/1.5 SFMono-Regular, Menlo, Consolas, monospace; }
  header { flex:0 0 auto; padding:.6rem 1rem; background:#1a1a1a;
    border-bottom:1px solid #333; display:flex; align-items:center; gap:.5rem; }
  .dot { width:.7rem; height:.7rem; border-radius:50%; background:#46c267;
    box-shadow:0 0 0 0 rgba(70,194,103,.6); }
  .dot.hit { background:#ff5d5d; }
  .count { font-weight:700; font-size:1.1rem; }
  .muted { color:#888; }
  main { flex:1 1 auto; min-height:0; overflow-y:auto; padding:1rem; }
  .req { background:#161616; border:1px solid #333; border-left:3px solid #ff5d5d;
    border-radius:6px; padding:.7rem .9rem; margin-bottom:.7rem;
    white-space:pre-wrap; word-break:break-word; }
  .meta { color:#9aa0a6; font-size:.82rem; letter-spacing:.03em;
    margin-bottom:.4rem; padding-bottom:.4rem; border-bottom:1px solid #2a2a2a; }
  .empty { color:#888; padding:2rem 1rem; text-align:center; }
</style></head><body>
<header>
  <span class="dot" id="dot"></span>
  <span class="count" id="count">—</span>
  <span class="muted">captured</span>
  <span class="muted" id="status"></span>
</header>
<main id="list"><div class="empty">waiting for the catcher…</div></main>
<script>
function esc(s){ return s.replace(/[&<>]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;'}[c])); }
async function tick(){
  try {
    const r = await fetch('/api/captures', {cache:'no-store'});
    const d = await r.json();
    document.getElementById('count').textContent = d.total;
    document.getElementById('dot').className = 'dot' + (d.total ? ' hit' : '');
    document.getElementById('status').textContent = d.ok ? '' : '· ' + d.error;
    const list = document.getElementById('list');
    if (!d.requests.length) {
      list.innerHTML = '<div class="empty">' +
        (d.ok ? '0 requests — nothing captured yet' : 'catcher offline') + '</div>';
    } else {
      list.innerHTML = d.requests.map((r, i) => {
        const n = d.requests.length - i;   // API returns newest first
        const meta = '#' + n + '  ·  ' + esc(r.time || '--:--:--') +
                     '  ·  ' + esc(r.method || 'POST');
        return '<div class="req"><div class="meta">' + meta + '</div>' +
               esc(r.content) + '</div>';
      }).join('');
    }
  } catch (e) {
    document.getElementById('status').textContent = '· panel error';
  }
}
tick(); setInterval(tick, 1500);
</script></body></html>"""


def read_token():
    try:
        return TOKEN_FILE.read_text().strip()
    except Exception:
        return ""


def _time(stamp):
    # "2024-01-15 12:34:56" or ISO "2024-01-15T12:34:56.0Z" -> "12:34:56"
    s = (stamp or "").replace("T", " ")
    if " " in s:
        s = s.split(" ", 1)[1]
    return s[:8]


def fetch_captures():
    token = read_token()
    if not token:
        return {"ok": False, "error": "no token (run 'make webhooksite')",
                "total": 0, "requests": []}
    try:
        with urllib.request.urlopen(
            f"{WEBHOOK}/token/{token}/requests", timeout=3
        ) as resp:
            data = json.load(resp)
    except Exception as exc:
        return {"ok": False, "error": f"catcher unreachable ({exc})",
                "total": 0, "requests": []}
    reqs = [
        {
            "time": _time(r.get("created_at", "")),
            "method": r.get("method", ""),
            "content": (r.get("content") or "")[:1000],
        }
        for r in data.get("data", [])
    ]
    return {"ok": True, "error": "", "total": data.get("total", len(reqs)),
            "requests": reqs}


class Handler(BaseHTTPRequestHandler):
    def _send(self, code, body, ctype):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        # No X-Frame-Options / CSP, so the deck can embed this in an iframe.
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path.startswith("/api/captures"):
            self._send(200, json.dumps(fetch_captures()).encode(), "application/json")
        elif self.path in ("/", "/index.html") or self.path.startswith("/?"):
            self._send(200, PAGE.encode(), "text/html; charset=utf-8")
        else:
            self._send(404, b"not found", "text/plain; charset=utf-8")

    def log_message(self, *args):  # keep the stage output quiet
        pass


if __name__ == "__main__":
    print(f"capture panel on http://127.0.0.1:{PORT}  (reads {TOKEN_FILE})")
    ThreadingHTTPServer(("127.0.0.1", PORT), Handler).serve_forever()
