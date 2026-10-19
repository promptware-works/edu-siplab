---
description: "Build the SIPLab operator test message from a test case and an evidence table (usage: /siplab-test <scenario folder or corpus path + test-id>)"
argument-hint: <e.g. siplab/scenarios/02-auth-failure | siplab/groups/07-voiplab/corpus/basic-call>
allowed-tools: Read, Glob
---

Build the operator test message for **$ARGUMENTS**.

1. Locate the test case and the evidence table:
   - a scenario folder → `test-case.yaml` and `evidence.tsv` inside it;
   - a corpus path + test-id → `<test-id>.test.yaml` and `<test-id>.evidence.tsv`;
   - if an `RTP STREAMS` file exists (`<test-id>.rtp-streams.txt`), include it.
2. Output, verbatim and inside one fenced block: the line `TEST CASE`, the test
   case, the line `EVIDENCE TABLE`, the table, and — only if present — the line
   `RTP STREAMS` and the statistics.
3. **Never** read, include, or mention a `truth.yaml` / `*.truth.yaml` file.
4. Do not analyze the content and do not act as the orchestrator; the operator
   pastes the block as the next message.
