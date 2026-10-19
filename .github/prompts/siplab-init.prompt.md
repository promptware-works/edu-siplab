---
mode: ask
description: Start the SIPLab AI SIP Test Engineer — orchestrator, boot payload, catalogue
---

Initialize the SIPLab AI SIP Test Engineer in this chat. Process the three
canonical payloads **in order** and follow each exactly. Use only the **body**
of each file — everything below its closing frontmatter `---` line.

1. [`siplab/agents/sip-test-engineer.agent.md`](../../siplab/agents/sip-test-engineer.agent.md) —
   adopt it; reply `SIP Test Engineer orchestrator loaded — waiting for boot.`
2. [`siplab/boot/boot.md`](../../siplab/boot/boot.md) —
   reply `SIPLab boot loaded — waiting for catalogue.`
3. [`siplab/boot/catalogue.md`](../../siplab/boot/catalogue.md) —
   reply `Catalogue registered, N skills available — ready for test case.`

Do not act on any test yet; wait for a test message.
