# LLM security for beginners

The whole talk in one project — slides and the live demos behind them.

- **Part 1 — OWASP Top 10 for LLM apps.** Ten tiny, real-API [marimo](https://marimo.io)
  demos (`llm01_…` … `llm10_…`), served on `:2718` and embedded in the slides.
  Each shows the vulnerable code, the one-line fix, and a live before/after.
- **Part 2 — OWASP Agentic Skills.** Three self-contained [opencode](https://opencode.ai)
  + [nono](https://docs.nono.sh) demos (`ast01_…`, `ast03_…`, `ast06_…`): a real
  skill looks ordinary, the agent runs it, the attack lands — then the same run
  inside the nono sandbox is blocked. They share one local
  [webhook.site](https://webhook.site) catcher in [`webhook/`](webhook/).

The deck lives directly in [`docs/presentation.rst`](docs/presentation.rst) — one
reStructuredText file (an opener, Part 1, Part 2, and a links page) that you edit
by hand. Code and the nono profile are pulled from the demo folders with
`literalinclude`, so the snippets never drift from the code that runs.

## Prerequisites

The slides build and present with **no secrets**. The **live demos** need your own
API key — without it they won't run:

- **Part 1** (marimo demos) reads an OpenAI API key from `.env`. Copy
  `.env.example` to `.env` and add your key. `.env` is git-ignored, so your key is
  **never committed** — and this repo never ships one.
- **Part 2** (opencode + nono) authenticates opencode to OpenAI itself
  (`opencode auth login`), and also needs Docker and [nono](https://docs.nono.sh).

The deck published to GitHub Pages is fully static and uses none of these.

## Setup

```bash
make install                  # uv sync
cp .env.example .env          # then add your own OPENAI_API_KEY — never commit it
```

Part 2 also needs the sandbox and its opencode pack (one-time):

```bash
nono pull nolabs-ai/opencode-v1
cp ast01_malicious_skills/nono/opencode-demo.json ~/.config/nono/profiles/
```

Part 2's agent (opencode) authenticates to OpenAI itself — see each demo's README.

## Present

```bash
make slides          # build the reveal.js deck into docs/_build/revealjs
make serve-slides    # build, serve the Part 1 demos (:2718) and the deck (:8000)
```

Open <http://127.0.0.1:8000>. Part 1's slides embed the live demos from `:2718`;
Part 2's demos are shown as code, the exact commands, and verified transcripts.

## Share it (offline or online)

```bash
make handout   # a self-contained static copy: live demos -> placeholders, assets vendored
make pdf       # render that copy to docs/_build/presentation.pdf (uses your installed Chrome)
```

Every push to `main` also builds the static deck and publishes it to GitHub Pages,
where the live demos show as labelled placeholders (clone and run them locally):

**<https://barseghyanartur.github.io/llm-security-talk/>**

## Run a demo directly

```bash
make run                                   # Part 1: all ten demos on :2718
cd ast01_malicious_skills && make help     # Part 2: one agentic-skills demo
```

## Layout

```
docs/            the slide deck (presentation.rst, conf.py, images/)
serve.py         serves the ten Part 1 demos under /llm01 … /llm10
llm01_… llm10_…  the Part 1 marimo demos
ast01_… …        the Part 2 agentic-skills demos
webhook/         the shared webhook.site catcher (compose + make-include)
nono/            the example nono profile shown in Part 2
```

> Every exfiltrated secret in the demos is **fake decoy data** — see each demo's
> README. Your real key stays in the root `.env` (git-ignored) and is never
> written into a demo.
