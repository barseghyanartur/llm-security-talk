#!/usr/bin/env python3
"""Build a shareable, offline copy of the deck.

Takes the built reveal.js deck (docs/_build/revealjs) and writes
docs/_build/handout/: a self-contained copy where

  * the live demo iframes (marimo :2718, ttyd terminal :3000, capture panel
    :8085) are replaced by labelled placeholders — they point at the presenter's
    localhost and would be blank for anyone else, and
  * the CDN assets (Prism, jsphinx) are downloaded and referenced locally, so the
    deck opens with no internet.

Everything else — text, code snippets, transcripts, images — is already static in
the build. Zip the folder and share it, or render it to PDF with ``make pdf``.

Run after ``make slides``:  python docs/make_handout.py
"""

import re
import shutil
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE / "_build" / "revealjs"
OUT = HERE / "_build" / "handout"

PRISM = "https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0"
JSPHINX = "https://cdn.jsdelivr.net/gh/barseghyanartur/jsphinx/src"

# CDN file -> local path inside the handout. The deck references the cdnjs ones
# scheme-relative (//cdnjs…); we rewrite every scheme form below.
CDN_FILES = {
    f"{PRISM}/themes/prism.min.css": "vendor/prism/themes/prism.min.css",
    f"{PRISM}/plugins/toolbar/prism-toolbar.min.css": "vendor/prism/plugins/toolbar/prism-toolbar.min.css",
    f"{JSPHINX}/css/sphinx_rtd_theme.css": "vendor/jsphinx/sphinx_rtd_theme.css",
    f"{PRISM}/prism.min.js": "vendor/prism/prism.min.js",
    f"{PRISM}/plugins/autoloader/prism-autoloader.min.js": "vendor/prism/plugins/autoloader/prism-autoloader.min.js",
    f"{PRISM}/plugins/toolbar/prism-toolbar.min.js": "vendor/prism/plugins/toolbar/prism-toolbar.min.js",
    f"{PRISM}/plugins/copy-to-clipboard/prism-copy-to-clipboard.min.js": "vendor/prism/plugins/copy-to-clipboard/prism-copy-to-clipboard.min.js",
    f"{JSPHINX}/js/download_adapter.js": "vendor/jsphinx/download_adapter.js",
}
# Language grammars the Prism autoloader would otherwise fetch from the CDN at
# runtime; vendored so highlighting works offline (python/json literalincludes).
PRISM_COMPONENTS = ["markup", "clike", "python", "json", "bash"]

PLACEHOLDER_CSS = """
<style>
.handout-live { display:flex; flex-direction:column; justify-content:center;
  align-items:center; min-height:460px; box-sizing:border-box; padding:2rem;
  border:2px dashed #888; border-radius:12px; background:#1a1a1a; color:#e6e6e6;
  font-size:0.62em; text-align:center; gap:.7em; }
.handout-live .k { font-weight:700; }
.handout-live .sub { font-size:.8em; color:#9aa0a6; }
.handout-live code { color:#46c267; }
</style>
"""


def fetch(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "handout-builder"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read()


def placeholder(kind: str, detail: str) -> str:
    return (
        '<div class="handout-live"><div class="k">▶ Live demo &mdash; '
        f"{kind}</div><div class=\"sub\">{detail} &middot; run it locally with "
        "<code>make stage</code></div></div>"
    )


def replace_iframe(m: re.Match) -> str:
    tag = m.group(0)
    if "2718" in tag:
        return placeholder("marimo notebook", "the Part 1 before / after")
    if "3000" in tag:
        return placeholder("web terminal (ttyd)", "you run the attack here")
    if "8085" in tag:
        return placeholder("webhook.site capture panel", "the leak lands here")
    return tag


def main() -> None:
    if not (SRC / "presentation.html").exists():
        raise SystemExit("docs/_build/revealjs/presentation.html missing — run `make slides` first")
    if OUT.exists():
        shutil.rmtree(OUT)
    shutil.copytree(SRC, OUT)

    html = (OUT / "presentation.html").read_text(encoding="utf-8")

    # 1) live iframes -> static placeholders
    html, n = re.subn(
        r"<iframe\b[^>]*(?:2718|3000|8085)[^>]*>.*?</iframe>",
        replace_iframe,
        html,
        flags=re.S,
    )
    html = html.replace("</head>", PLACEHOLDER_CSS + "</head>")
    print(f"  replaced {n} live iframes with placeholders")

    # 2) vendor the top-level CDN assets and rewrite every scheme form
    for url, rel in CDN_FILES.items():
        dest = OUT / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(fetch(url))
        bare = url.split("://", 1)[1]
        for form in (url, "//" + bare, "http://" + bare, "https://" + bare):
            html = html.replace(form, rel)
    print(f"  vendored {len(CDN_FILES)} CDN assets")

    # 2b) vendor the Prism grammars and point the autoloader at them locally
    comp_dir = OUT / "vendor/prism/components"
    comp_dir.mkdir(parents=True, exist_ok=True)
    got = 0
    for c in PRISM_COMPONENTS:
        try:
            (comp_dir / f"prism-{c}.min.js").write_bytes(
                fetch(f"{PRISM}/components/prism-{c}.min.js")
            )
            got += 1
        except Exception as exc:  # noqa: BLE001
            print(f"  warn: could not vendor prism-{c} ({exc})")
    html = html.replace(
        'src="vendor/prism/plugins/autoloader/prism-autoloader.min.js"',
        'src="vendor/prism/plugins/autoloader/prism-autoloader.min.js" '
        'data-autoloader-path="vendor/prism/components/"',
    )
    print(f"  vendored {got} Prism grammars")

    (OUT / "presentation.html").write_text(html, encoding="utf-8")

    # A root index.html, so a site root (e.g. GitHub Pages) opens the deck
    # instead of 404ing — the deck itself is presentation.html.
    (OUT / "index.html").write_text(
        '<!doctype html><html lang="en"><head><meta charset="utf-8">'
        '<meta http-equiv="refresh" content="0; url=presentation.html">'
        "<title>LLM security for beginners</title></head>"
        '<body><a href="presentation.html">Open the slides</a></body></html>\n',
        encoding="utf-8",
    )
    print(f"handout written to {OUT}  (+ index.html -> presentation.html)")


if __name__ == "__main__":
    main()
