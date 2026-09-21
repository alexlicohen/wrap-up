# wrap-up

[![check](https://github.com/alexlicohen/wrap-up/actions/workflows/check.yml/badge.svg)](https://github.com/alexlicohen/wrap-up/actions/workflows/check.yml)

An end-of-work checkpoint skill so no work or context is lost when you compact, clear,
or start a fresh session. Works with [Claude Code](https://claude.com/claude-code) and
the Codex CLI.

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

Clone into your agent's skills directory:

```sh
git clone https://github.com/alexlicohen/wrap-up.git ~/.agents/skills/wrap-up
```

Claude Code and Codex discover it automatically on the next session.

## Notes

Personal tool, shared as-is. It adapts to each project's memory conventions and gates;
it never fabricates a green test result or claims a push it held.

`scripts/check-skill.py` (run in CI) validates the skill's structure — frontmatter and
the five phase headers. It's a shape check, not a behavioral one: a prose skill has no
executable surface to unit-test.

## License

[MIT](LICENSE) © 2026 Alexander Li Cohen
