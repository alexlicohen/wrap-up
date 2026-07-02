# wrap-up

A [Claude Code](https://claude.com/claude-code) skill: an end-of-work checkpoint so no
work or context is lost when you compact, clear, or start a fresh session.

Invoke it by saying **"wrap up"**, "checkpoint this", "save and commit", "prepare for
compaction", or any end-of-work save-state request.

## What it does

Four phases, run in order:

0. **Pre-flight** — confirm nothing is mid-flight (background agents, monitors, cloud
   jobs) that a clear/compact would orphan.
1. **Save memory** — capture what a future session needs and can't re-derive from
   code/git: non-obvious decisions and their *why*, load-bearing constraints, ongoing
   state, feedback on how to work.
2. **Persist the backlog** — write remaining + deferred work to durable memory (the
   in-session task list doesn't survive compaction). Includes a **residue sweep**: a
   short, artifact-anchored pass for changes that shipped unverified, assumptions never
   confirmed, and early decisions that later learnings contradict — each captured as an
   actionable follow-up, never free-floating.
3. **Verify + commit (+ push)** every touched repo — run the project's gate and show the
   real result, scan the diff for secrets/PHI, commit, and push for durability.
4. **Prepare for compaction** — confirm repos are clean and pushed/held, then print a
   tight handoff (what shipped / what's left / where memory lives).

## Install

Clone into your Claude Code skills directory:

```sh
git clone https://github.com/alexlicohen/wrap-up.git ~/.claude/skills/wrap-up
```

Claude Code discovers it automatically on the next session.

## Notes

Personal tool, shared as-is. It adapts to each project's memory conventions and gates;
it never fabricates a green test result or claims a push it held.
