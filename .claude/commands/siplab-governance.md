---
description: "Review a SIPLab skill before submission: deterministic lint plus the advisory skill reviewer (usage: /siplab-governance <path to SKILL.md> [group catalogue path])"
argument-hint: <path to SKILL.md> [path to a group catalogue.md]
allowed-tools: Read, Bash(python3 siplab/tools/lint_skill.py:*)
---

Review the SIPLab skill named in **$ARGUMENTS** (first argument: the skill
file; optional second argument: a group catalogue, default
`siplab/boot/catalogue.md`).

1. **Tier 1 — lint.** Run
   `python3 siplab/tools/lint_skill.py <skill file> --catalogue <catalogue>`
   and keep its full output.
2. **Tier 2 — review.** Use only the **body** of each file below — everything
   below its closing frontmatter `---` line — and follow it exactly:
   1. `siplab/agents/skill-reviewer.agent.md` — adopt the reviewer; reply
      `SIPLab skill reviewer loaded — waiting for boot.`
   2. `siplab/boot/boot.md` — reply `SIPLab boot loaded — waiting for catalogue.`
   3. The catalogue — reply `Catalogue registered, N skills available — ready for skill review.`
   4. Then treat the following as the operator message: the line
      `SKILL UNDER REVIEW`, the body of the skill file, the line
      `LINT REPORT`, and the lint output from step 1. Reply with the REVIEW.
3. Do not edit the skill, run it on test data, or read any truth file.

This is a thin wrapper; the reviewer specification decides what the review contains.
