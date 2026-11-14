# LLM security for beginners — one project, both parts.
#
#   Part 1 (llm01..llm10):  live marimo demos, served on :2718 and embedded in
#                           the slides.  `make run` / `make serve-slides`.
#   Part 2 (ast01/03/06):   self-contained agentic-skills demos; cd into one and
#                           run `make` (they share the webhook catcher below).
#
# The shared webhook.site catcher is included here too, so `make webhooksite`,
# `make open`, `make requests` work from the project root.

RUN         := uv run
PORT        ?= 2718      # the Part 1 live demo server (serve.py)
SLIDES_PORT ?= 8000
PANEL_PORT  ?= 8085      # the webhook capture panel (webhook/panel.py)
TTY_PORT    ?= 3000      # the embedded web terminal (ttyd)
HOST        ?= 127.0.0.1
STAGE_PIDS  := .stage-pids

# Free a TCP port if something already listens on it (macOS + Linux).
define free_port
pids=$$(lsof -ti tcp:$(1) 2>/dev/null); if [ -n "$$pids" ]; then echo "Port $(1) busy; freeing it (killing $$pids)."; kill $$pids 2>/dev/null || true; sleep 1; fi
endef

include webhook/webhook.mk

.DEFAULT_GOAL := help
.PHONY: help install run slides serve-slides stage stage-down handout pdf lint format clean

help: ## show these targets
	@grep -hE '^[a-zA-Z0-9_-]+:.*##' $(MAKEFILE_LIST) \
	  | awk 'BEGIN{FS=":.*##"}{printf "  \033[36m%-16s\033[0m %s\n",$$1,$$2}'
	@echo ""
	@echo "  Part 2 demos run from their own dirs: cd ast01_malicious_skills && make"

install: ## install everything into .venv (uv)
	uv sync

run: ## serve the ten Part 1 demos on http://$(HOST):$(PORT)
	@$(call free_port,$(PORT))
	$(RUN) uvicorn serve:app --host $(HOST) --port $(PORT)

slides: ## build the reveal.js deck into docs/_build (edit docs/presentation.rst)
	$(RUN) --group docs sphinx-build -b revealjs docs docs/_build/revealjs

serve-slides: slides ## serve the Part 1 demos ($(PORT)) and the deck ($(SLIDES_PORT))
	@$(call free_port,$(PORT))
	@$(call free_port,$(SLIDES_PORT))
	@echo "Part 1 demos on http://$(HOST):$(PORT). Slides on http://$(HOST):$(SLIDES_PORT)."
	$(RUN) uvicorn serve:app --host $(HOST) --port $(PORT) & \
	$(RUN) --group docs python -m http.server $(SLIDES_PORT) --directory docs/_build/revealjs

stage: slides ## bring the whole live rig up once: demos, webhook, panel, terminal, slides
	@command -v ttyd >/dev/null || { echo "ttyd not found — install it: brew install ttyd"; exit 1; }
	@$(MAKE) --no-print-directory webhooksite
	@: > $(STAGE_PIDS)
	@$(call free_port,$(PORT))
	@nohup $(RUN) uvicorn serve:app --host $(HOST) --port $(PORT) >/tmp/stage-demos.log 2>&1 & echo $$! >> $(STAGE_PIDS)
	@$(call free_port,$(PANEL_PORT))
	@nohup python3 webhook/panel.py >/tmp/stage-panel.log 2>&1 & echo $$! >> $(STAGE_PIDS)
	@$(call free_port,$(TTY_PORT))
	@nohup ttyd -W -i $(HOST) -p $(TTY_PORT) bash >/tmp/stage-ttyd.log 2>&1 & echo $$! >> $(STAGE_PIDS)
	@$(call free_port,$(SLIDES_PORT))
	@nohup $(RUN) --group docs python -m http.server $(SLIDES_PORT) --directory docs/_build/revealjs >/tmp/stage-slides.log 2>&1 & echo $$! >> $(STAGE_PIDS)
	@sleep 1
	@echo ""
	@echo "  slides     http://$(HOST):$(SLIDES_PORT)     (present here)"
	@echo "  terminal   http://$(HOST):$(TTY_PORT)     (embedded in the live slides)"
	@echo "  panel      http://$(HOST):$(PANEL_PORT)     (embedded capture view)"
	@echo "  demos      http://$(HOST):$(PORT)     (Part 1 marimo)"
	@echo "  webhook    $(WEBHOOK)/#!/$$(cat $(TOKENF) 2>/dev/null)"
	@echo ""
	@echo "  stop everything with: make stage-down"
	@echo "  (needs .env with OPENAI_API_KEY for the Part 1 demos; logs in /tmp/stage-*.log)"

stage-down: ## stop everything 'make stage' started
	@-test -f $(STAGE_PIDS) && while read p; do kill $$p 2>/dev/null || true; done < $(STAGE_PIDS); rm -f $(STAGE_PIDS)
	@$(call free_port,$(PORT))
	@$(call free_port,$(PANEL_PORT))
	@$(call free_port,$(TTY_PORT))
	@$(call free_port,$(SLIDES_PORT))
	@$(MAKE) --no-print-directory webhook-down
	@echo "stage down."

handout: slides ## build a shareable OFFLINE copy (live iframes -> placeholders, assets vendored) + zip
	$(RUN) --group docs python docs/make_handout.py
	@cd docs/_build && rm -f handout.zip && zip -qr handout.zip handout
	@echo ""
	@echo "  share:  docs/_build/handout/presentation.html   (opens offline, in any browser)"
	@echo "  or zip: docs/_build/handout.zip"

pdf: handout ## render the handout to a PDF via decktape + your installed Chrome (GUI fallback printed)
	@rm -f docs/_build/presentation.pdf; \
	chrome=""; for c in \
	  "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
	  "/Applications/Chromium.app/Contents/MacOS/Chromium" \
	  "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge"; do \
	  [ -x "$$c" ] && chrome="$$c" && break; done; \
	if command -v npx >/dev/null 2>&1 && [ -n "$$chrome" ]; then \
	  echo "decktape via Chrome: $$chrome"; \
	  PUPPETEER_EXECUTABLE_PATH="$$chrome" npx -y decktape@3.14.0 reveal \
	    "file://$(CURDIR)/docs/_build/handout/presentation.html" \
	    docs/_build/presentation.pdf || true; \
	fi; \
	if [ -f docs/_build/presentation.pdf ]; then \
	  echo "wrote docs/_build/presentation.pdf"; \
	else \
	  echo ""; echo "Automated export didn't produce a PDF. Reliable manual way (Chrome):"; \
	  echo "  1) open 'docs/_build/handout/presentation.html?print-pdf' in Chrome"; \
	  echo "  2) Print -> Save as PDF, Margins: None, Background graphics: ON"; \
	fi

lint: ## check the code with ruff
	uvx ruff check .
	uvx ruff format --check .

format: ## format the code with ruff
	uvx ruff format .

clean: ## remove caches and build output
	rm -rf .pytest_cache .ruff_cache docs/_build
	find . -name __pycache__ -type d -prune -exec rm -rf {} +
	find . -name __marimo__ -type d -prune -exec rm -rf {} +
