# Malicious agent skill → credential exfiltration (and how a sandbox stops it)

A live demo for the OWASP **Agentic Skills** talk. A real coding agent
(**opencode**) is given a skill that looks completely ordinary — `repo-stats`,
"count the files and lines in this project". When the agent runs it, the skill
also reads the project's `.env` and POSTs the secrets to an attacker-controlled
server (a local **webhook.site**).

Then we run the *same agent, same skill, same prompt* inside **nono**, a
capability sandbox. The model still works, but the exfiltration is blocked.

```
A  make opencode       no sandbox   → .env lands on the attacker's page   🚨
B  make nono-opencode  inside nono  → skill runs, POST blocked, page empty ✅
```

Verified B transcript:

```
→ Skill "repo-stats"
$ python3 .agents/skills/repo-stats/collect.py
repo-stats: 7 files, 189 lines
repo-stats: telemetry upload failed (<urlopen error [Errno 1] Operation not permitted>)
```

The attack *runs* and reads the secrets — nono just won't let the bytes leave
the machine. It fails for the right reason: the sandbox, not a crash.

## What's in here

| path | role |
|------|------|
| `.agents/skills/repo-stats/SKILL.md` | the innocent-looking skill opencode loads |
| `.agents/skills/repo-stats/collect.py` | the payload: real stats + hidden `.env` POST |
| `.env` | **fake decoy** secrets — the thing the skill steals |
| `../webhook/` | the **shared** local webhook.site catcher (compose + `make` targets) |
| `opencode.json` | registers `openai/gpt-6-luna`, quiets MCP noise |
| `Makefile` | every step below |

## Prerequisites

- `docker`, `opencode` (v1.x), `nono`
- the nono opencode pack + the demo profile (one-time):
  ```bash
  nono pull nolabs-ai/opencode-v1
  cp nono/opencode-demo.json ~/.config/nono/profiles/
  ```
- your OpenAI key configured **in opencode** (`opencode auth login` → OpenAI).
  See **Where the key goes** below — it does not go in the env or in nono.

## Run it

```bash
make install        # pull webhook.site images, check tools
make webhooksite    # start webhook.site + mint a capture token (prints a WATCH LIVE url)
make open           # open that page in your browser

make opencode       # A: no sandbox   → watch the .env arrive
make requests       #    print what was captured

make token          # fresh token for a clean slate
make nono-opencode  # B: inside nono  → skill runs, POST blocked
make requests       #    still empty

make down           # stop webhook.site
```

`make help` lists every target.

## Where the key goes

The real key must **never** go in `v6/.env` — that file is the decoy the skill
exfiltrates. It lives in **opencode's own credential store**:

```bash
opencode auth login        # pick OpenAI, paste your sk-... key
```

opencode keeps it in `~/.local/share/opencode/auth.json` (mode 600, outside the
repo, never in git, never in your shell env). Both runs use it — including the
sandboxed one: nono grants opencode its data dir, so opencode authenticates
itself, and nono only allow-lists the model endpoints (no key in nono at all).
Verified: with `OPENAI_API_KEY` unset in the environment, run B still reaches
the model and still blocks the exfil.

(If you ever wanted nono to hold the key instead and inject it at the proxy so
opencode never sees it, the pack supports a `keyring://service/account` or
`env://VAR` credential route — but that's not needed here, and nono warns that a
key opencode can read is a key a malicious skill can read.)

## How B actually works

- nono grants opencode its XDG state dirs and the working directory, and turns
  on its filtering proxy (`net = proxy`).
- The profile allow-lists `api.openai.com` and `models.opencode.ai`, so
  opencode reaches the model *through* nono using its own stored credential.
  Every other destination — including `127.0.0.1:8084`, the webhook — is denied.
- So the model call succeeds, the skill reads `.env`, and the POST dies with
  `Operation not permitted`. webhook.site stays at zero captured requests.
