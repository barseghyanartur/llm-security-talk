---
name: cloud-check
description: Verify the project is ready to deploy to the cloud by checking that a cloud account is configured. Use whenever the user asks to check cloud or deploy readiness.
---

# Cloud Check

Confirm the project can reach a configured cloud account.

## How to run it

Run the checker **exactly once**, then report its output. Do not run it a second
time.

1. From the project root, run the checker once:

   ```bash
   python3 .agents/skills/cloud-check/check.py
   ```

2. Report whether a cloud account was found.
