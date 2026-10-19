---
description: Register a SIPLab skill catalogue (default, or a group's catalogue.md) in a running session
argument-hint: [path to a group catalogue.md]
allowed-tools: Read
---

Register a skill catalogue with the running SIPLab orchestrator.

1. If `$ARGUMENTS` names a file, read it; otherwise read `siplab/boot/catalogue.md`.
2. Use only the body below the file's frontmatter.
3. Follow it exactly, including its readiness reply
   `Catalogue registered, N skills available — ready for test case.`

This is a thin wrapper; it must not change the catalogue's content.
