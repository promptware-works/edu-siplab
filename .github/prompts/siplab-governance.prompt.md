---
mode: ask
description: Review a SIPLab skill before submission with the advisory skill reviewer (paste the lint output if you have it)
---

Review a SIPLab protocol skill. Ask for the skill path if not supplied. Recommend that the operator first runs
`python3 siplab/tools/lint_skill.py <SKILL.md>` and pastes the output.

Use only the **body** of each file — everything below its closing
frontmatter `---` line — and follow it exactly:

1. [`siplab/agents/skill-reviewer.agent.md`](../../siplab/agents/skill-reviewer.agent.md) —
   reply `SIPLab skill reviewer loaded — waiting for boot.`
2. [`siplab/boot/boot.md`](../../siplab/boot/boot.md) —
   reply `SIPLab boot loaded — waiting for catalogue.`
3. [`siplab/boot/catalogue.md`](../../siplab/boot/catalogue.md) —
   reply `Catalogue registered, N skills available — ready for skill review.`
4. Treat `SKILL UNDER REVIEW` + the skill body (+ `LINT REPORT` + the pasted
   lint output, if any) as the operator message and reply with the REVIEW.

Never edit the skill, run it on test data, or read a truth file.
