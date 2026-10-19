---
agent: agent
tools: ['search/codebase']
description: Build the SIPLab operator test message from a scenario folder or a corpus test
---

Build the operator test message. Ask for a scenario folder (e.g.
`siplab/scenarios/02-auth-failure`) or a corpus test (e.g. `deliverables/corpus/basic-call`) if not supplied.

1. Read the test case (`test-case.yaml` or `<test-id>.test.yaml`) and the
   evidence table (`evidence.tsv` or `<test-id>.evidence.tsv`); include
   `rtp-streams.txt` or `<test-id>.rtp-streams.txt` if it exists.
2. Output, verbatim inside one fence of four backticks: `TEST CASE`, the test case,
   `EVIDENCE TABLE`, the table, and — only if present — `RTP STREAMS` and the statistics.
3. **Never** read, include, or mention a truth file.
4. Do not analyze the content and do not act as the orchestrator.
