# webhook.mk — shared local webhook.site capture server (the attacker's catcher).
#
# Any demo that needs an external exfil target includes this:
#
#     include ../webhook/webhook.mk
#
# It provides: webhooksite, token, open, requests, webhook-down, webhook-pull,
# and the variables WEBHOOK (base URL) and TOKENF (shared token file). The
# service, token, and compose file are centralized here, so every demo posts to
# the same catcher and watches the same page.

SHELL := /bin/bash
export APP_KEY := base64:MXV9xFf/nIRopLV+nKMAW1RuSts1FbqAZ1brscJyPLg=

# directory of THIS file, resolved relative to whoever includes it
WEBHOOK_DIR := $(dir $(lastword $(MAKEFILE_LIST)))
WEBHOOK     := http://127.0.0.1:8084
TOKENF      := $(WEBHOOK_DIR).webhook-token
COMPOSE     := docker compose -p agentic-webhook -f $(WEBHOOK_DIR)compose.yml

.PHONY: webhook-pull webhooksite token open requests webhook-down

webhook-pull: ## pull the webhook.site docker images
	$(COMPOSE) pull

webhooksite: ## start webhook.site + mint a capture token
	$(COMPOSE) up -d
	@printf "waiting for webhook.site to come up "
	@for i in $$(seq 1 60); do \
	  uuid=$$(curl -s --ipv4 -m 3 -X POST $(WEBHOOK)/token -H 'Content-Type: application/json' -d '{}' \
	    | python3 -c "import sys,json;print(json.load(sys.stdin).get('uuid',''))" 2>/dev/null); \
	  if [ -n "$$uuid" ]; then echo "$$uuid" > $(TOKENF); echo " ready"; break; fi; \
	  printf "."; sleep 1; \
	done; \
	test -s $(TOKENF) || { echo " timeout (is Docker running?)"; exit 1; }
	@echo "token: $$(cat $(TOKENF))   capture URL: $(WEBHOOK)/$$(cat $(TOKENF))"
	@echo ""
	@echo "  WATCH LIVE:  $(WEBHOOK)/#!/$$(cat $(TOKENF))"

token: ## (re)create the shared capture token (service must already be up)
	@uuid=$$(curl -s --ipv4 -m 5 -X POST $(WEBHOOK)/token -H 'Content-Type: application/json' -d '{}' \
	  | python3 -c "import sys,json;print(json.load(sys.stdin).get('uuid',''))" 2>/dev/null); \
	if [ -n "$$uuid" ]; then echo "$$uuid" > $(TOKENF); echo "token: $$uuid   capture URL: $(WEBHOOK)/$$uuid"; \
	else echo "token: webhook.site is not responding — run 'make webhooksite' first"; exit 1; fi

open: ## open the webhook.site page in your browser
	@open "$(WEBHOOK)/#!/$$(cat $(TOKENF))"

requests: ## print what the token has captured
	@curl -s --ipv4 "$(WEBHOOK)/token/$$(cat $(TOKENF))/requests" \
	  | python3 -c "import sys,json;d=json.load(sys.stdin);print('captured requests:',d.get('total',0));[print('---\n'+r.get('content','')[:500]) for r in d.get('data',[])]"

webhook-down: ## stop webhook.site
	$(COMPOSE) down
