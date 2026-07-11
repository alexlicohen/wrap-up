# Changelog

## 1.1.0 — 2026-07-10

- **Phase 3/4: push ≠ landed.** A successful `git push` on a feature branch only means
  the remote ref moved — it says nothing about whether that branch's PR already merged.
  Root-caused against a real incident: `claude-triage-layer` PR #5 merged before its last
  two commits landed on the branch, orphaning them until caught by chance at a later
  `git branch -d` warning and recovered by hand (PR #9). Phase 3 step 4 and Phase 4 now
  require checking the branch's PR state and confirming ancestry to the default branch
  before treating a repo as shipped, and call out a `not yet merged to HEAD` delete
  warning as a hard stop.
- **Phase 0: armed `usage-guard` loops don't self-terminate on job completion** — only on
  a trip or a blind exit. Added an explicit check: if the job a guard is watching has
  already finished, stop the guard rather than leaving it polling into the void.

## 1.0.0 — 2026-07-02

Initial public release of the `wrap-up` Claude Code skill.

- **Four-phase checkpoint:** pre-flight (coast clear?) → save memory → persist
  backlog → verify+commit(+push) all touched repos → prepare for compaction.
- **Phase 2 residue sweep:** an artifact-anchored pass — a change that shipped with
  no objective check, a decision resting on an unverified assumption, an early
  decision a later learning contradicts. Each finding requires a concrete pointer,
  an empty list is valid (never invent one), and every finding gets a forced
  disposition (backlog item / memory caveat / flagged user decision). Converts a
  session's known-unknowns into durable follow-ups instead of losing them at
  compaction, rather than the open-ended "what are you missing?" introspection that
  produces uncalibrated theater.
- **Structure gate:** `scripts/check-skill.py` + CI (`.github/workflows/check.yml`)
  assert valid frontmatter (`name`/`description`) and the five phase headers present
  and in order — catches a malformed/truncated SKILL.md that would silently fail to
  load. There is no behavioral gate (a prose skill has no executable surface); that
  would require scenario evals.
- MIT licensed.
