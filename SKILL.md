---
name: wrap-up
description: >
  End-of-work checkpoint: save durable memory, persist a to-do/backlog, verify +
  commit (and push) all code across the session's repos, then leave a clean handoff
  for compaction or a fresh session. Invoke when the user says "wrap up", "wrap-up",
  "save and commit", "checkpoint this", "save memory and commit", "prepare for
  compaction", "prepare for a new session", or any end-of-work save-state request.
---

# wrap-up

A four-phase checkpoint so no work or context is lost when the user compacts, clears,
or starts a fresh session. Run the phases IN ORDER. Adapt to the project; if a phase
is genuinely N/A, do it briefly and say why — never skip silently. Be terse; this is
plumbing, not a deliverable.

**Guiding rule:** the point is durability + a cheap resume. Prefer saving work over
purity — but report status honestly (never call red tests green, never claim pushed
when held).

## Phase 0 — Pre-flight (coast clear?)
Before checkpointing, confirm nothing is mid-flight that a clear/compact would orphan:
background agents, monitors, long-running shells, cloud/remote jobs. If something is
still running, WAIT for it (or, if the user wants to stop now, record what's running +
its task id in the handoff so the resumed session can reattach). Don't checkpoint a
moving target.
- **Armed `usage-guard` loops don't self-terminate on job completion** — only on a trip
  or a blind exit. If a guard is still polling, check whether the job it's watching has
  already finished; if so, `TaskStop` it rather than leaving it running into the void.

## Phase 1 — Save memory
Capture what a FUTURE session would need and can't re-derive from the code/git.
- Follow the project's memory conventions (per-project `…/memory/`: one fact per file
  with frontmatter, a one-line pointer in `MEMORY.md`). Save: non-obvious decisions
  and their *why*, load-bearing constraints, "we deliberately did/didn't X", state of
  ongoing work, and any user feedback on how to work. Convert relative dates to absolute.
- **Dedup first:** update the existing memory file that already covers a topic rather
  than creating a near-duplicate; delete memories proven wrong.
- Do NOT save what the repo/git/CLAUDE.md already records, or what only mattered to this
  conversation.
- If memory was already kept current during the session, say so and just reconcile the
  index — don't pad.
- **If the session changed how the project WORKS** — new tooling/commands, a new
  convention, a danger zone, a renamed owner — update the project's `CLAUDE.md` too, not
  just memory. Memory is recall; `CLAUDE.md` is the contract the next agent auto-loads.

## Phase 2 — Build / persist the to-do list
- **Residue sweep** (skip with one line if the session was mechanical/docs-only):
  before persisting the backlog, list up to 3 items, each with a concrete pointer
  (file / decision / missing check) — an empty list is a valid and common answer;
  never invent one to fill the quota:
  1. A change that shipped with NO objective check exercising it — including a
     green-unit-tests-but-unexercised seam. Name the file and the missing check.
  2. A decision made on an assumption we never verified. Name the assumption and
     how a future session would check it.
  3. An early-session decision that something learned LATER contradicts or weakens,
     and that we never revisited. Name both.
  Every finding gets exactly one disposition: a backlog item below (phrased as the
  check to run), a caveat line in the relevant Phase-1 memory file, or a flagged
  user decision. No pointer or no disposition → drop it, it's vibes. Record, don't
  fix — except if a finding undermines a push, hold that push and say so. Dedup
  against the existing backlog; don't re-add a standing doubt every wrap-up.
- Reconcile the in-session task list (mark done, drop stale).
- **Persist the remaining + deferred work to memory** (a backlog memory file, or update
  the relevant project memory) so a fresh context recalls it — the in-session task list
  does NOT survive compaction/new sessions. Group as: in-flight (should be none after
  Phase 3), actionable backlog, and standing/gated (with who/what gates it).
- Each item: one line, enough to act on cold (what + where + effort if known). Flag
  anything that needs a user decision.

## Phase 3 — Verify + commit (+ push) all code
For EACH git repo the session changed (check the working dirs you touched, not just cwd):
1. **Verify** with the project's quick gate if one exists and is reasonably fast
   (`gf verify` / `make verify` / `make test` / `npm test` / `pytest -q` / `cargo check`).
   Show the real result. If RED: still commit (don't lose work) but say so PROMINENTLY,
   put the failure in the message, and DO NOT push to a shared/public remote without
   asking.
2. **Commit** all changes with a clear, specific message (what changed + why). If on the
   repo's default branch and the change is non-trivial, branch first per project policy.
   Use the project's safe-commit path if it has one (e.g. `gf ship`).
3. **Scan the diff for secrets/PHI** before pushing — keys, tokens, credentials,
   patient/clinical data, private identifiers. Mandatory for public/mirrored repos; if
   the project has a leak-scan/pre-push guard, run it and NEVER override it. A hit blocks
   the push until scrubbed.
4. **Push** for durability when a remote exists and verify is green (or the user okays a
   red push). If a repo has a documented "commit/push only when asked" rule, treat
   invoking this skill as the ask for COMMIT; confirm before the first PUSH unless the
   user already said push.
   **A successful push is not the same as landed.** On a feature branch that ships via
   PR, `git push` succeeding only means the remote branch ref moved — it says nothing
   about whether that branch's PR already merged. A PR merged earlier in the session
   does NOT retroactively pick up commits pushed to the branch afterward; they sit
   orphaned on a dead branch. Before treating the repo as shipped, check the branch's PR
   state (e.g. `gh pr view <branch> --json state,mergedAt`) and, if it's already merged,
   confirm the latest commit is reachable from the default branch (`git merge-base
   --is-ancestor HEAD origin/main`) rather than assuming this push landed it — if not,
   open a new PR (or otherwise land the delta) instead of just pushing again to the same
   branch. Treat a `not yet merged to HEAD` warning on branch delete as a hard stop to
   investigate, never something to force past with `-D`.
5. **Resolve downstream/mirror obligations.** If the commit touched code that is
   duplicated/mirrored/ported elsewhere (a public mirror, a sibling package, a shared
   engine), run the project's sync check (e.g. `gf sync check`) and either sync it or
   RECORD the deliberate hold (with the reason) in memory. Skipping this lets the mirror
   silently drift — the most common "I thought we were done" gap.
- Leave intentional untracked artifacts (scratch files, generated outputs, gitignored
  data) alone — don't sweep them in. Stage deliberately.
- Report per repo: branch, commit hash, pushed-or-held, verify status, sync status.

## Phase 4 — Prepare for compaction / new session
- Confirm every touched repo is clean (no stray tracked changes) and pushed/held as
  intended. "Pushed" means reachable from the repo's actual integration target (the
  default branch, via a merged PR) — not just that `git push` succeeded on a feature
  branch. State it plainly.
- Re-confirm Phase 0: nothing is still running (or the in-flight items + task ids are in
  the handoff). Only then is it safe to clear/compact.
- Print a tight **HANDOFF**: (a) what shipped this session, (b) what's left (point to the
  Phase-2 backlog), (c) where the memory + backlog live, (d) the usage tally if the
  triage/tier layer was used (per its tally convention), and (e) residue-sweep titles, if
  any (one line each — the durable copies live in the backlog/memory).
- Remind the resume path: a fresh session auto-loads `MEMORY.md` + `CLAUDE.md`, so it
  starts cheaply; for a DIFFERENT project, start the new session in THAT repo's dir so
  it loads the right context. Note whether to `/compact` (keep this thread) vs `/clear`
  or a new `claude` (drop it) — a fresh context is cheaper for the next chunk.
- Do NOT start new substantive work. End here.
