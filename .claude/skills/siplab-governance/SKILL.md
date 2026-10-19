---
name: siplab-governance
description: Review a SIPLab protocol skill before submission — run the deterministic linter (tools/lint_skill.py) and then the advisory skill reviewer agent. Use when the user wants to check, review, lint, or self-check a SIPLab skill. Thin wrapper over the canonical files under siplab/.
---

# SIPLab — Governance review (skill wrapper)

This is a **thin wrapper**. The canonical reviewer lives at
`siplab/agents/skill-reviewer.agent.md`; if this wrapper disagrees with it,
the file wins. Use only the body of each prompt file.

1. Run `python3 siplab/tools/lint_skill.py <SKILL.md>`
   on the skill the user names and keep the output.
2. Load, in order, the reviewer, `siplab/boot/boot.md`, and `siplab/boot/catalogue.md`,
   giving each readiness reply defined by the reviewer's Session Bootstrap.
3. Submit `SKILL UNDER REVIEW` + the skill body + `LINT REPORT` + the lint
   output, and return the reviewer's REVIEW.

Never edit the skill, run it on test data, or read a truth file.
