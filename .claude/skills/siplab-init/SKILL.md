---
name: siplab-init
description: Start the SIPLab AI SIP Test Engineer in one step — load the orchestrator specification, the boot payload, and the skill catalogue. Use when the user wants to start, boot, or initialize SIPLab or the SIP test engineer. Thin wrapper over the canonical files under siplab/.
---

# SIPLab — Initialize (skill wrapper)

This is a **thin wrapper**. The canonical prompts live under `siplab/`; if this
wrapper ever disagrees with them, the files win. Use only the body of each
file — everything below its closing frontmatter `---` line.

Process, **in order**:

1. Read `siplab/agents/sip-test-engineer.agent.md`, adopt it, and reply
   `SIP Test Engineer orchestrator loaded — waiting for boot.`
2. Read `siplab/boot/boot.md`, load it, and reply
   `SIPLab boot loaded — waiting for catalogue.`
3. Read `siplab/boot/catalogue.md`, register it, and reply
   `Catalogue registered, N skills available — ready for test case.`

Do **not** act on any test yet; wait for a test message.
