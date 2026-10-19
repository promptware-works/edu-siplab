---
mode: ask
description: Print a SIPLab skill body verbatim for dispatch (provide the skill number)
---

The operator wants to dispatch a SIPLab skill. Ask for the skill number if
not supplied.

1. Resolve the prompt file `siplab/skills/<NN>-*/SKILL.md` (two-digit, zero-padded).
2. Output the file's **body** — everything below its closing frontmatter `---`
   line — **verbatim**, inside a fenced block.
3. Do not execute the skill or invent input. Remind the operator to paste the
   body as the reply to the DISPATCH turn and then type `next`.
