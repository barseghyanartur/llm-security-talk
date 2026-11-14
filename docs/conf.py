"""Sphinx config for the slide deck — "LLM security for beginners".

Build with: make slides

Part 1 embeds the live marimo demos (served on :2718 by serve.py) in iframes;
Part 2 shows the agentic-skills demos. Every code snippet is pulled straight from
the demo files with ``literalinclude``, and jsphinx makes each snippet expand to
the whole file in place. See https://github.com/barseghyanartur/jsphinx.
"""

project = "LLM security for beginners"
author = "Artur Barseghyan"

extensions = ["sphinx_revealjs", "sphinx_design"]

root_doc = "presentation"
exclude_patterns = ["_build"]

# The revealjs builder replaces html_static_path with revealjs_static_path.
revealjs_static_path = ["_static"]

revealjs_style_theme = "black"

# RST comments become speaker notes (press S); write them as ``.. Say: ...``.
revealjs_notes_from_comments = True
html_theme = "alabaster"

# -- jsphinx + Prism: expandable code snippets -------------------------------
prismjs_base = "//cdnjs.cloudflare.com/ajax/libs/prism/1.29.0"

html_css_files = [
    f"{prismjs_base}/themes/prism.min.css",
    f"{prismjs_base}/plugins/toolbar/prism-toolbar.min.css",
    "https://cdn.jsdelivr.net/gh/barseghyanartur/jsphinx/src/css/sphinx_rtd_theme.css",  # noqa
]

html_js_files = [
    f"{prismjs_base}/prism.min.js",
    f"{prismjs_base}/plugins/autoloader/prism-autoloader.min.js",
    f"{prismjs_base}/plugins/toolbar/prism-toolbar.min.js",
    f"{prismjs_base}/plugins/copy-to-clipboard/prism-copy-to-clipboard.min.js",
    "https://cdn.jsdelivr.net/gh/barseghyanartur/jsphinx/src/js/download_adapter.js",  # noqa
]

# The revealjs builder reads its own asset lists, not the html_* ones.
revealjs_css_files = html_css_files + [
    "revealjs/plugin/highlight/monokai.css",
]
# Re-fit a slide to the viewport when jsphinx expands a snippet in place.
revealjs_js_files = list(html_js_files) + ["relayout.js"]

revealjs_script_plugins = [
    {
        "src": "revealjs/plugin/highlight/highlight.js",
        "name": "RevealHighlight",
    },
    {
        "src": "revealjs/plugin/notes/notes.js",
        "name": "RevealNotes",
    },
]

# Load each embedded demo iframe (data-src) only while its slide is on screen,
# and unload it when you leave. Otherwise all ten marimo apps start at once on
# deck open and the later ones (llm08–10) lose the race — they come up blank or
# unstyled. Combined with data-src on those iframes in presentation.rst, this
# means at most the current demo's app is running.
revealjs_script_conf = """{
    preloadIframes: false
}"""
