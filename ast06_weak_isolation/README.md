# AST06 — Weak Isolation

The agent runs with no boundary around the project, so a skill can reach the
rest of the machine.

The `cloud-check` skill looks like a harmless **deploy-readiness check**. It
counts a few project files — and then reaches *outside* the project to read the
host's cloud credentials at `~/.acme-cloud/credentials` and **ships them to an
attacker's server**. Nothing about the task needs anything beyond the project
directory; weak isolation is what lets it wander.

The fix is **isolation**: confine the agent to its working directory. The skill
runs exactly as before, but any path outside the project is simply not there.

```
A  make opencode       no sandbox          → host creds read + shipped out  🚨
B  make nono-opencode  nono cwd-scoped     → out-of-project read denied     ✅
```

The read of the out-of-project file happens *before* the skill can send it, so
confining the agent to its working directory stops the theft at the source — the
credentials are never read, so nothing reaches the catcher. (Contrast AST01,
where the secret *is* read and nono blocks it from leaving over the network.)

Verified block (same skill, nono confining it to the project):

```
cloud-check: scanned 9 project paths
cloud-check: host credentials out of reach ([Errno 1] Operation not permitted: '/Users/me/.acme-cloud/credentials')
```

## What's here

| path | role |
|------|------|
| `.agents/skills/cloud-check/SKILL.md` | the innocent-looking "readiness check" skill |
| `.agents/skills/cloud-check/check.py` | the payload: project count + out-of-project credential theft and exfiltration |
| `opencode.json` | registers `openai/gpt-6-luna` |
| `nono/opencode-demo.json` | the nono egress allow-list profile |

`make setup` plants a **fake** credential at `~/.acme-cloud/credentials` to stand
in for the host secrets a project skill should never reach; `make clean` removes
it. Nothing real is ever read.

## Run it

```bash
make webhooksite     # start the local webhook.site catcher + token
make open            # watch the catcher page
make opencode        # A: no sandbox   → STOLE host credential and shipped it off-box
make requests        # the stolen credential, captured
make nono-opencode   # B: isolated     → host credentials out of reach (nothing sent)
make clean           # remove the planted credential + stop webhook.site
```

The only difference between A and B is the filesystem boundary: A runs opencode
directly (it can read your whole home dir); B runs it under
`nono --profile opencode-demo --allow-cwd` — only the **project** is granted, so
the model still reaches OpenAI and the skill still runs, but the reach into
`~/.acme-cloud` is denied.
