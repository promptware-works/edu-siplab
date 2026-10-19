---
description: Start the SIPLab AI SIP Test Engineer — load the orchestrator, the boot payload, and the catalogue in one step
---

Initialize the SIPLab AI SIP Test Engineer in this session. Process the three
canonical payloads below **in order** and follow each exactly. Use only the **body** of each file — everything below its closing frontmatter `---` line. The frontmatter is metadata for tooling and is never part of the prompt.

1. Adopt the orchestrator specification and emit its reply
   `SIP Test Engineer orchestrator loaded — waiting for boot.`
2. Load the boot payload and emit `SIPLab boot loaded — waiting for catalogue.`
3. Register the catalogue and emit `Catalogue registered, N skills available — ready for test case.`
   with N the number of catalogue rows.

Do not act on any test yet. After the three replies, wait for a test message
(`TEST CASE` … `EVIDENCE TABLE` …) — e.g. built with `/siplab-test`.

--- ORCHESTRATOR ---

@siplab/orchestrator/sip-test-engineer.agent.md

--- BOOT PAYLOAD ---

@siplab/boot/boot.md

--- CATALOGUE ---

@siplab/boot/catalogue.md
