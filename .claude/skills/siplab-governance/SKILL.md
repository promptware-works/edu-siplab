---
name: siplab-governance
description: Review a SIPLab protocol skill before submission — run the deterministic linter (siplab/tools/lint_skill.py), then the advisory skill reviewer agent (usage /siplab-governance <path to SKILL.md>). Use when the user wants to check, review, lint, or self-check a SIPLab skill.
argument-hint: <path to SKILL.md, e.g. siplab/skills/02-call-flow/SKILL.md>
allowed-tools: Read, Bash(python3 siplab/tools/lint_skill.py *)
---

# SIPLab — Governance review

This is a **thin wrapper**. The canonical reviewer lives at
`siplab/agents/skill-reviewer.agent.md`; if this wrapper disagrees with it, the
file wins. Use only the **body** of each file — everything below its closing frontmatter `---` line; the frontmatter is metadata and never part of the prompt.

1. **Tier 1 — lint.** Run `python3 siplab/tools/lint_skill.py $ARGUMENTS` and keep
   its full output.
2. **Tier 2 — review.** Read and process, in order: the reviewer
   (`siplab/agents/skill-reviewer.agent.md`), `siplab/boot/boot.md`, and
   `siplab/boot/catalogue.md`, giving the readiness lines of the reviewer's
   Session Bootstrap. Then treat as the operator message: the line
   `SKILL UNDER REVIEW`, the body of the skill file, the line `LINT REPORT`, and
   the lint output from step 1. Reply with the REVIEW.
3. Do not edit the skill, run it on test data, or read any truth file.
