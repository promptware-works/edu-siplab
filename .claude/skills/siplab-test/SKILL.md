---
name: siplab-test
description: Build the SIPLab operator test message (TEST CASE + EVIDENCE TABLE, and RTP STREAMS when present) from a scenario folder or a corpus test (usage /siplab-test <folder or corpus path + test-id>). Never includes a truth file.
argument-hint: <e.g. siplab/scenarios/02-auth-failure | deliverables/corpus/basic-call>
allowed-tools: Read, Glob
---

# SIPLab — Build a test message

Build the operator test message for **$ARGUMENTS**.

1. Locate the files:
   - a scenario folder → `test-case.yaml`, `evidence.tsv`, and `rtp-streams.txt` if present;
   - a corpus path + test-id → `<test-id>.test.yaml`, `<test-id>.evidence.tsv`, and `<test-id>.rtp-streams.txt` if present.
2. Output, verbatim and inside one fence of four backticks: the line
   `TEST CASE`, the test case, the line `EVIDENCE TABLE`, the table, and — only
   if present — the line `RTP STREAMS` and the statistics.
3. **Never** read, include, or mention a `truth.yaml` / `*.truth.yaml` file.
4. Do not analyze the content and do not act as the orchestrator; the operator
   pastes the block as the next message.
