---
name: siplab-skill
description: Print the body of a SIPLab protocol skill verbatim so the operator can paste it when the orchestrator dispatches that skill (usage /siplab-skill <N>). Thin dispatch helper.
argument-hint: <skill number, e.g. 2>
allowed-tools: Read, Glob
---

# SIPLab — Print a skill for dispatch

The operator wants to dispatch SIPLab skill **#$ARGUMENTS**.

1. Resolve the file `siplab/skills/<NN>-*/SKILL.md` (two-digit, zero-padded,
   e.g. `2` → `siplab/skills/02-call-flow/SKILL.md`).
2. Output the file's **body** — everything below its closing frontmatter `---`
   line — **verbatim**, inside a fence of four backticks (````` ```` `````), because
   the body itself contains three-backtick fences.
3. Do **not** run the skill, produce a finding, or add text inside the fence.
   After the fence, remind the operator to paste the body as the reply to the
   DISPATCH turn and then type `next`.
