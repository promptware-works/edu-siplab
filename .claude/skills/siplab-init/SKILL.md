---
name: siplab-init
description: Start the SIPLab AI SIP Test Engineer in one step — load the orchestrator, the boot payload, and the skill catalogue. Use when the user wants to start, boot, or initialize SIPLab or the SIP test engineer. Thin wrapper over the canonical files under siplab/.
allowed-tools: Read
---

# SIPLab — Initialize

This is a **thin wrapper**. The canonical prompts live under `siplab/`; if this
wrapper ever disagrees with them, the files win. Use only the **body** of each file — everything below its closing frontmatter `---` line; the frontmatter is metadata and never part of the prompt.

Read these files and process them **in order**, as if the operator had pasted
their bodies one after another:

1. `siplab/agents/sip-test-engineer.agent.md` — adopt the orchestrator.
2. `siplab/boot/boot.md` — load the boot payload.
3. `siplab/boot/catalogue.md` — register the catalogue.

Give the three readiness lines the orchestrator's Session Bootstrap defines, in
order, and stop. Do **not** act on any test yet; wait for a test message
(e.g. built with `/siplab-test`).
