---
name: readme-lint
description: Check the project's Markdown documentation for common problems (missing top-level heading, etc.) and report them. Use whenever the user asks to lint the README, check the docs, or review documentation quality.
---

# Readme Lint

Report common problems in the project's Markdown docs.

## How to run it

Run the checker **exactly once**, then report its output. Do not run it a second
time.

1. From the project root, run the checker once:

   ```bash
   python3 .agents/skills/readme-lint/lint.py
   ```

2. Report the issues it prints back to the user.
