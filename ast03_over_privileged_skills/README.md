# AST03 — Over-Privileged Skills

A skill is given more privilege than its job needs, and abuses the excess.

The `readme-lint` skill looks like a **read-only documentation checker** — it
scans the project's Markdown and reports problems. Its real job needs nothing
but *read* access. But nothing constrains it, so while it "lints" it also
**appends a backdoor to `app.py`** — a file a doc checker should never touch.
The planted code beacons out every time the app runs; `make run-app` shows it
phoning home to the shared webhook.site catcher.

The fix is **least privilege**: run the agent with the project granted
*read-only*. The skill can still read and lint every file; the moment it tries
to write, the sandbox denies it.

```
A  make opencode       no sandbox          → app.py gets a backdoor        🚨
B  make nono-opencode  nono read-only cwd  → write denied, app.py clean    ✅
```

Verified block (same skill, nono granting the project read-only):

```
readme-lint: checked 1 markdown files, 1 missing a top-level heading
readme-lint: auto-fix failed ([Errno 1] Operation not permitted: 'app.py')
RESULT: ✅ app.py is clean — the write was blocked
```

## What's here

| path | role |
|------|------|
| `.agents/skills/readme-lint/SKILL.md` | the innocent-looking "doc check" skill |
| `.agents/skills/readme-lint/lint.py` | the payload: real lint report + hidden `app.py` backdoor |
| `app.py` / `app.py.orig` | the source file it tampers with / its pristine copy |
| `opencode.json` | registers `openai/gpt-6-luna` |
| `nono/opencode-demo.json` | the nono egress allow-list profile |

## Run it

```bash
make webhooksite     # start the shared catcher (so a live backdoor has somewhere to call)
make opencode        # A: no sandbox   → RESULT: 🚨 app.py was TAMPERED
make run-app         # run the app     → backdoor beacons to webhook.site
make requests        #                 → the beacon is captured
make nono-opencode   # B: read-only    → RESULT: ✅ app.py is clean
make run-app         # run the app     → nothing phones home
make reset           # restore pristine app.py
```

`run-app` runs `app.py` with `CATCHER` pointed at the shared catcher. A
backdoored `app.py` POSTs `backdoor live in app.py on <host>` on every run; a
clean one does nothing. That's the point: the over-privileged write isn't
cosmetic — it leaves a live backdoor in a file that runs later.

The only difference between A and B is the filesystem grant: A runs opencode
directly (it can write the project); B runs it under
`nono --profile opencode-demo -r "$PWD"` — the project is **read-only**, so the
model still reaches OpenAI and the skill still runs, but the tamper can't land.
