---
description: "Print a SIPLab skill body verbatim for dispatch (usage: /siplab-skill <N>)"
argument-hint: <skill number, e.g. 1>
allowed-tools: Read, Glob
---

The operator wants to dispatch SIPLab skill **#$ARGUMENTS**.

1. Resolve the prompt file `siplab/skills/<NN>-*/SKILL.md` (two-digit,
   zero-padded, e.g. `1` → `siplab/skills/01-registration/SKILL.md`).
2. Output the file's **body** — everything below its closing frontmatter `---`
   line — **verbatim**, inside a fenced block, so the operator can paste it.
3. Do **not** execute the skill, produce a finding, or invent input. After
   printing, remind the operator to paste the body as the reply to the
   DISPATCH turn and then type `next`.

This is a thin dispatch helper; it only loads the canonical prompt.
