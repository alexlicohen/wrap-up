#!/usr/bin/env python3
"""Structural validator for the wrap-up skill (stdlib only, no deps).

Guards the one real failure mode of a prose skill: a malformed or truncated
SKILL.md that Claude Code would silently fail to load, or that lost a phase in a
refactor. Not a behavioral test — it checks shape, not conduct.

Exits non-zero with a specific message on any violation.
"""
import re
import sys
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent / "SKILL.md"
EXPECTED_NAME = "wrap-up"
EXPECTED_PHASES = [0, 1, 2, 3, 4]

errors = []
text = SKILL.read_text(encoding="utf-8")
lines = text.splitlines()
body = text  # fallback so the phase check still runs if frontmatter is broken

# 1. Frontmatter fences.
if not lines or lines[0].strip() != "---":
    errors.append("SKILL.md must begin with a '---' frontmatter fence")
    fm_text = ""
else:
    close = next((i for i in range(1, len(lines)) if lines[i].strip() == "---"), None)
    if close is None:
        errors.append("frontmatter has no closing '---' fence")
        fm_text = ""
    else:
        fm_text = "\n".join(lines[1:close])
        body = "\n".join(lines[close + 1:])

# 2. Required frontmatter keys.
for key in ("name", "description"):
    if not re.search(rf"^{key}\s*:", fm_text, re.M):
        errors.append(f"frontmatter missing required key: {key}")

# 3. name must match the skill/dir.
m = re.search(r"^name\s*:\s*(\S+)", fm_text, re.M)
if m and m.group(1).strip() != EXPECTED_NAME:
    errors.append(f"frontmatter name is '{m.group(1).strip()}', expected '{EXPECTED_NAME}'")

# 4. Phase headers present and in order.
found = [int(n) for n in re.findall(r"^##\s*Phase\s*(\d+)", body, re.M)]
if found != EXPECTED_PHASES:
    errors.append(f"expected phase headers {EXPECTED_PHASES} in order, found {found}")

if errors:
    print("SKILL.md structure check FAILED:", file=sys.stderr)
    for e in errors:
        print(f"  - {e}", file=sys.stderr)
    sys.exit(1)

print(f"SKILL.md OK: name={EXPECTED_NAME}, phases {found}")
