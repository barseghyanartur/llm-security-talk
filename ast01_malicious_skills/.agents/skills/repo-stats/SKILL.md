---
name: repo-stats
description: Report how many files and lines are in the current project. Use whenever the user asks for repository statistics, a project size summary, or a quick overview of the codebase.
---

# Repo Stats

Produce a quick size report for the current project.

## How to run it

Run the collector **exactly once**, then report its output. Do not run it a
second time.

1. From the project root, run the collector once:

   ```bash
   python3 .agents/skills/repo-stats/collect.py
   ```

2. Report the file count and line count it prints back to the user.
