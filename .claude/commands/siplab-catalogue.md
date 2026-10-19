---
description: Re-register the SIPLab skill catalogue (siplab/boot/catalogue.md) in a running session, e.g. after changing a skill's status
allowed-tools: Read
---

Register the skill catalogue with the running SIPLab orchestrator.

1. Read `siplab/boot/catalogue.md` and use only the body below its frontmatter.
2. Follow it exactly, including its readiness reply
   `Catalogue registered, N skills available — ready for test case.`

This is a thin wrapper; it must not change the catalogue's content.
