# Changelog

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
