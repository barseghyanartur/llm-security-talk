"""Serve all ten demos under one server.

    OPENAI_API_KEY=sk-... uv run uvicorn serve:app --port 2718

Each demo gets its own URL: /llm01, /llm02, ... /llm10. These are the URLs the
slide deck embeds.
"""

import glob
import os
import sys

import marimo
from dotenv import load_dotenv

# Put OPENAI_API_KEY (from .env) into the environment before any demo loads.
# Each demo builds its OpenAI client at import time, so the key must be set
# first — otherwise the app errors and only its title renders.
load_dotenv()

if not os.environ.get("OPENAI_API_KEY"):
    sys.exit(
        "OPENAI_API_KEY is not set. Copy .env.example to .env and add your key:\n"
        "    cp .env.example .env    # then edit .env"
    )

server = marimo.create_asgi_app()
for path in sorted(glob.glob("llm[0-9][0-9]_*/01_*.py")):
    slug = path.split("_", 1)[0]  # "llm01_prompt_injection/01_..." -> "llm01"
    server = server.with_app(path=f"/{slug}", root=path)


# All ten demos are served from one origin (localhost:2718) under /llm01../llm10,
# and every one ships marimo's static assets under the SAME build hashes. marimo
# also registers a per-app service worker (public-files-sw.js) whose only job is
# to tag requests for its /public/ file directory — which none of these demos
# use. On a shared origin that service worker plus the HTTP cache can hand one
# app a cached response meant for a sibling, so a demo loads with no stylesheet
# or renders blank until the cache is cleared. We don't need it, so we replace
# it with a no-op worker that takes control and intercepts nothing: assets then
# always load straight from the network, and an already-registered stale worker
# is updated to this harmless one on the next visit.
NOOP_SW = (
    b"// Neutralized by serve.py: these demos use no marimo public files, and a\n"
    b"// caching/proxying service worker on this shared origin broke sibling demos\n"
    b"// (one would load unstyled or blank). This worker intercepts no fetches, so\n"
    b"// assets always load straight from the network; on activation it also wipes\n"
    b"// any cache a previous worker left and unregisters itself, so a stale\n"
    b"// per-scope registration cleans itself up on its next visit.\n"
    b"self.addEventListener('install', () => self.skipWaiting());\n"
    b"self.addEventListener('activate', (e) => e.waitUntil((async () => {\n"
    b"  try { const ks = await caches.keys();\n"
    b"        await Promise.all(ks.map((k) => caches.delete(k))); } catch (_) {}\n"
    b"  try { await self.clients.claim(); } catch (_) {}\n"
    b"  try { await self.registration.unregister(); } catch (_) {}\n"
    b"})()));\n"
)


class NeutralizeServiceWorker:
    """Serve a do-nothing worker for any */public-files-sw.js, before marimo."""

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] == "http" and scope.get("path", "").endswith(
            "/public-files-sw.js"
        ):
            await send(
                {
                    "type": "http.response.start",
                    "status": 200,
                    "headers": [
                        (b"content-type", b"application/javascript; charset=utf-8"),
                        (b"cache-control", b"no-cache, no-store, must-revalidate"),
                        (b"content-length", str(len(NOOP_SW)).encode()),
                    ],
                }
            )
            await send({"type": "http.response.body", "body": NOOP_SW})
            return
        await self.app(scope, receive, send)


app = NeutralizeServiceWorker(server.build())
