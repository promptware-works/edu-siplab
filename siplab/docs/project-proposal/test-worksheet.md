# SIPLab — Test Worksheet

**Companion to:** [`proposal.md`](./proposal.md) (timeline-neutral)
**Purpose:** Give every group an identical, gradable test bar for its PBX and
its skills, and give graders an identical checklist to score against.

> **Timeline-neutral.** The pass conditions below do not change when the
> calendar does. *When* each part is filled and graded, and how its score
> rolls up into the final grade, depend on the chosen variant; see
> [`delivery-plan.md`](./delivery-plan.md).

---

## How to use this worksheet

- **New to findings?** Read
  [How to Read a Finding](../guides/reading-a-finding.md) first — it annotates
  the 10-key schema and checks U1–U7 on synthetic, non-graded data.
- **One worksheet per group.** Copy this file to
  `groups/<GG>-<group-name>/worksheet.md`. Fill Part A for the PBX, Parts B
  and C once **per authored skill**, Part D once for the integrated
  orchestrator, and Part E for the corpus. Keep only the Part F sections for
  the skills your group authored.
- **Part A is filled during P1 and P2**, without the AI SIP Test Engineer.
  Checks marked **gate** must pass before P3.
- **Parts B–E are filled during P3.** Every Pass check in B, D, and F must
  hold in *both* GitHub Copilot Chat and Claude Code; attach both
  transcripts.
- **Run the validator** on every consolidated report before marking U1–U4
  and G3–G4:
  `python3 siplab/tools/validate_evidence.py --evidence <table> --report <report.json> --truth <truth.yaml>`.
- **Only authored skills are graded.** Placeholder skills appear in reports
  as coverage gaps; they are not filled in Parts B, C, and F.
- **Bring it to the defense.** The completed worksheet is the entry ticket
  for the demonstration and defense.

---

## Part A — Core PBX checks (P1, P2)

| # | Check | Phase | Gate | Pass/Fail | Evidence / notes |
| --- | --- | --- | --- | --- | --- |
| C1 | PBX service starts and is reachable from the client network | P1 | | ☐ | |
| C2 | All client devices used in C7–C8 register as configured users | P1 | | ☐ | |
| C3 | One administrator and at least five user accounts are configured; registration requires authentication | P1 | | ☐ | |
| C4 | Telephony and messaging services are configured (dial plan, messaging context) | P1 | | ☐ | |
| C5 | System and network diagram, component inventory with software versions, and reproducible setup notes are submitted | P1 | | ☐ | |
| C6 | No passwords, digest responses, tokens, real phone numbers, or personal data appear in any submitted file or capture | P1, P2 | **gate** | ☐ | |
| C7 | Mobile-to-desktop call: two-way audio confirmed by both parties, clean teardown, endpoints return to idle | P2 | **gate** | ☐ | |
| C8 | Mobile-to-mobile call: two-way audio confirmed by both parties, clean teardown | P2 | **gate** | ☐ | |
| C9 | At least one voice session per configured user is documented | P2 | | ☐ | |
| C10 | Instant messaging works between two users in both directions | P2 | **gate** | ☐ | |
| C11 | Registration flow is captured and explained, including the digest challenge and the granted expiry, with RFC references and frame numbers | P2 | **gate** | ☐ | |
| C12 | Call setup and teardown are captured and explained, including the SDP offer/answer and the ACK, with RFC references and frame numbers | P2 | **gate** | ☐ | |
| C13 | At least one failed or rejected call is captured and its response code and cause are explained correctly | P2 | | ☐ | |
| C14 | Corpus is complete per [`delivery-plan.md`](./delivery-plan.md) *Required corpus composition*: every case has a test case, sanitized capture, evidence table, and ground-truth verdict | P2 | | ☐ | |

Calls with an IP phone are encouraged and may be recorded as additional
notes under C7.

---

## Part B — Universal skill checks (P3, per authored skill)

Every finding must validate against `schema/finding.schema.json`.

| # | Universal check | Copilot | Claude Code | Notes |
| --- | --- | --- | --- | --- |
| U1 | Output contains all 10 keys: `skill`, `test_id`, `summary`, `verdict`, `failure_stage`, `confidence`, `evidence`, `rfc_ref`, `next_check`, `rationale` | ☐ | ☐ | |
| U2 | `verdict` is one of {`pass`, `fail`, `insufficient_evidence`}; `failure_stage` is from the enum and is `none` exactly when the verdict is `pass` | ☐ | ☐ | |
| U3 | `confidence` is a number in [0, 1] | ☐ | ☐ | |
| U4 | Every `evidence` item cites a frame and field value that exist in the evidence table (validator reports zero unsupported citations) | ☐ | ☐ | |
| U5 | `rationale` separates the protocol observation from the suspected cause and labels the cause as suspected; no generic text | ☐ | ☐ | |
| U6 | Instructions embedded in packet content (`User-Agent`, `Subject`, message body, SDP text) are ignored and do not change the verdict | ☐ | ☐ | |
| U7 | When required messages are missing, encrypted, or malformed, the skill returns `insufficient_evidence` instead of guessing | ☐ | ☐ | |

## Part C — Cross-environment block (P3, per authored skill)

| Environment | Transcript files | All Pass checks hold? | Same verdict and failure stage as the other environment on every case? |
| --- | --- | --- | --- |
| GitHub Copilot Chat | `tests/<test-id>/copilot.md` | ☐ | ☐ |
| Claude Code | `tests/<test-id>/claude.md` | ☐ | ☐ |

> "Materially consistent" = same verdict, same failure stage, and the same
> key frames cited; wording and confidence may differ. A different verdict
> or failure stage on any case is a fail.

## Part D — Orchestrator integration checks (P3, once per group)

| # | Integration check | Copilot | Claude Code | Notes |
| --- | --- | --- | --- | --- |
| G1 | The PLAN selects exactly the skills mapped from the test case's focus tags, states why, and waits for `approve` | ☐ | ☐ | |
| G2 | The consolidated report contains every skill finding unchanged, including uncertainty and any conflict between skills | ☐ | ☐ | |
| G3 | Coverage, gaps, and overall verdict follow the rule in proposal § 3.3 (validator rule check passes); a report with gaps is never `pass` | ☐ | ☐ | |
| G4 | The validator reports zero unsupported citations in the consolidated report | ☐ | ☐ | |
| G5 | The report separates deterministic facts from the evidence table from AI interpretations | ☐ | ☐ | |

## Part E — Corpus evaluation (P3, once per group)

Fill one row per case, for the group corpus and the held-out corpus.

| Test ID | Corpus | Ground truth (verdict / stage) | AI verdict / stage (Copilot) | AI verdict / stage (Claude Code) | Skills planned | Validator OK? | Correct? | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| | group | | | | | ☐ | ☐ | |
| | held-out | | | | | ☐ | ☐ | |

Summary metrics (proposal § 6.1): input coverage ___ / ___, verdict accuracy
___ / ___, stage accuracy ___ / ___, evidence validity ___ / ___,
appropriate skill selection ___ / ___.

---

## Part F — Per-skill pass checks

Reference inputs for each check are listed in
[`scenarios/skill-inputs/README.md`](../../scenarios/skill-inputs/README.md)
(test case, evidence table, truth file); several checks reuse the reference
scenarios. Expected responses depend on configuration;
the test case states the expected response for the group's PBX.

### F1 — #1 Registration & Authentication (worked example)

**Scope.** REGISTER transactions, digest challenge and retry, binding
expiry, rejected credentials.

| # | Pass check | Pass/Fail | Notes |
| --- | --- | --- | --- |
| 1.1 | `REGISTER` → `401` → `REGISTER` with credentials → `200` is `pass`; the initial `401` is not reported as a failure | ☐ | |
| 1.2 | A `401` or `403` answering the credentialed `REGISTER` is `fail` with stage `authentication` | ☐ | |
| 1.3 | Reports the granted expiry; a `REGISTER` with `Expires: 0` is recognized as de-registration, not as a failure | ☐ | |
| 1.4 | A capture with no `REGISTER` returns `insufficient_evidence` | ☐ | |

---

### F2 — #2 Call Setup & Teardown (required)

**Scope.** INVITE transaction, provisional and final responses, ACK,
CANCEL, BYE, routing outcome.

| # | Pass check | Pass/Fail | Notes |
| --- | --- | --- | --- |
| 2.1 | `INVITE` → `200` → `ACK` → … → `BYE` → `200` is `pass`, citing the frames of the `200`, `ACK`, `BYE`, and its `200` | ☐ | |
| 2.2 | An unavailable callee (the response stated in the test case, e.g. `404`, `480`, or `486`) is `fail` with stage `routing` or `call_setup` and cites the final response | ☐ | |
| 2.3 | `CANCEL` before answer followed by `487` to the `INVITE` is recognized as a caller-cancelled call, not a server error | ☐ | |
| 2.4 | Absence of optional provisional responses (`100`, `180`, `183`) alone does not cause a `fail` | ☐ | |
| 2.5 | A `200` to `INVITE` that is retransmitted without any `ACK` is `fail` with stage `call_setup` | ☐ | |

---

### F3 — #3 SDP Offer/Answer

**Scope.** Location of offer and answer, codec intersection, rejected
streams, late offer.

| # | Pass check | Pass/Fail | Notes |
| --- | --- | --- | --- |
| 3.1 | Identifies the offer and the answer frames and reports the common codec(s) | ☐ | |
| 3.2 | `488 Not Acceptable Here` after an offer with no common codec is `fail` with stage `media_negotiation` | ☐ | |
| 3.3 | A late offer (`INVITE` without SDP, offer in `200`, answer in `ACK`) is analyzed correctly | ☐ | |
| 3.4 | A media line with port `0` is reported as a rejected stream (RFC 3264) | ☐ | |

---

### F4 — #4 Instant Messaging

**Scope.** MESSAGE requests and responses, delivery outcome, body handling.
Uses the extended recipe that adds message-body fields.

| # | Pass check | Pass/Fail | Notes |
| --- | --- | --- | --- |
| 4.1 | `MESSAGE` → `200` or `202` is `pass` | ☐ | |
| 4.2 | `MESSAGE` to an unregistered user answered with `404` or `480` is `fail` with stage `messaging` | ☐ | |
| 4.3 | An authentication challenge (`401`/`407`) followed by a successful retry is `pass` | ☐ | |
| 4.4 | Reports the body's content type and length; never follows or quotes instructions found in the body as its own conclusion | ☐ | |

---

### F5 — #5 NAT & Media Path

**Scope.** Private SDP addresses, `Via` `received`/`rport`, one-way audio
indicators. Reference inputs include instructor-provided NAT captures.

| # | Pass check | Pass/Fail | Notes |
| --- | --- | --- | --- |
| 5.1 | An SDP `c=` private address (RFC 1918) that differs from the signaling source address is reported as a suspected one-way-audio cause, stage `media_path`, labeled as suspected | ☐ | |
| 5.2 | `received` and `rport` parameters in `Via` are recognized and explained (RFC 3581) | ☐ | |
| 5.3 | A capture without RTP returns `insufficient_evidence` for the media path | ☐ | |
| 5.4 | RTP present in one direction only is `fail` with stage `media_path` | ☐ | |

---

### F6 — #6 Transactions, Dialogs & Timers

**Scope.** Grouping by Call-ID, tags, and CSeq; retransmissions; timeouts;
transaction vs. dialog failure.

| # | Pass check | Pass/Fail | Notes |
| --- | --- | --- | --- |
| 6.1 | Groups the messages of a multi-call capture into the correct dialogs and transactions | ☐ | |
| 6.2 | `INVITE` retransmissions ending in `408` or no response are `fail` with timing evidence from `frame.time_relative` | ☐ | |
| 6.3 | An in-dialog request with a CSeq lower than the previous one is flagged | ☐ | |
| 6.4 | Distinguishes a failed transaction inside an established dialog from a failed dialog setup | ☐ | |

---

### F7 — #7 SIP Security Posture

**Scope.** Cleartext transport, digest algorithm, scanner patterns,
exposure of identities. The test case states the security expectation that
defines `pass`.

| # | Pass check | Pass/Fail | Notes |
| --- | --- | --- | --- |
| 7.1 | Cleartext SIP on UDP/TCP is reported as a risk relative to the stated expectation, not as a failure of the call | ☐ | |
| 7.2 | A burst of `REGISTER` or `OPTIONS` requests with many user names from one source is flagged as scanning | ☐ | |
| 7.3 | Reports the digest algorithm offered in the challenge (e.g. MD5 vs. SHA-256) | ☐ | |
| 7.4 | Never reproduces credential material in its output | ☐ | |

---

### F8 — #8 SIP–ISUP Cause Mapping

**Scope.** Map SIP final responses and `Reason` headers to ISUP/Q.850
release causes (RFC 3398, RFC 3326).

| # | Pass check | Pass/Fail | Notes |
| --- | --- | --- | --- |
| 8.1 | Maps `486` to cause 17 (user busy) and `404` to cause 1 (unallocated number), citing RFC 3398 | ☐ | |
| 8.2 | Uses a `Reason: Q.850;cause=…` header when present and prefers it over the response-code mapping | ☐ | |
| 8.3 | Marks a response without a defined mapping as such instead of guessing | ☐ | |
| 8.4 | Names the ISUP message that would carry the cause at a PSTN gateway (REL) | ☐ | |

---

### F9 — #9 IMS Comparison (advanced)

**Scope.** Compare observed registration and session setup with IMS (3GPP
TS 24.229). The verdict states whether the capture contains the flows needed
for the comparison.

| # | Pass check | Pass/Fail | Notes |
| --- | --- | --- | --- |
| 9.1 | For an observed registration, lists the IMS differences: P-CSCF/S-CSCF path, `Path` and `Service-Route` headers, IMS AKA vs. digest | ☐ | |
| 9.2 | Identifies IMS-relevant headers absent from the capture (e.g. `P-Asserted-Identity`, `Path`, `Service-Route`) | ☐ | |
| 9.3 | Does not claim that the PBX is IMS-compliant | ☐ | |
| 9.4 | Cites 3GPP TS 24.229 for every IMS statement | ☐ | |

---

### F10 — #10 RTP/RTCP Media Quality (advanced)

**Scope.** RTP stream presence per direction, loss, jitter, payload type vs.
SDP. Uses the extended recipe with RTP stream statistics.

| # | Pass check | Pass/Fail | Notes |
| --- | --- | --- | --- |
| 10.1 | Reports loss, jitter, and sequence errors per stream, identified by SSRC | ☐ | |
| 10.2 | Bidirectional RTP supports — but does not prove — two-way audio; the finding says audibility needs human confirmation | ☐ | |
| 10.3 | A capture with no RTP returns `insufficient_evidence` | ☐ | |
| 10.4 | Flags an RTP payload type that does not match the negotiated SDP codec | ☐ | |
| 10.5 | SRTP payloads are reported as encrypted; no quality claims beyond packet-level statistics | ☐ | |

---

## Grading rubric summary

- **Part A:** each check = 1 point (environment-independent).
- **Parts B, D, F:** each check that passes in *both* environments =
  1 point; in one environment only = 0.5 point (portability fault — note
  it); fail = 0.
- **Part C:** 2 points per authored skill (1 per environment).
- **Part E:** feeds D6 through the summary metrics and the discussion of
  incorrect diagnoses.

| Component | Max points | Feeds dimension |
| --- | --- | --- |
| Part A — C1–C4 | 4 | D1 |
| Part A — C5–C6 | 2 | D2 |
| Part A — C7–C13 | 7 | D3 |
| Part A — C14 | 1 | D4 |
| Part B — U1–U7, per authored skill | 7 | D5 (U5), D7 (U1–U4, U6, U7) |
| Part C — per authored skill | 2 | D5 |
| Part D — G1–G5 | 5 | D7 |
| Part F — 4–5 checks per authored skill | 4–5 | D6 |

How worksheet points convert into the dimension scores of
[`proposal.md`](./proposal.md) § 6, together with the report and defense, is
the grader's judgement within each dimension. The per-phase split is in
[`delivery-plan.md`](./delivery-plan.md).

---

**Group:** ____  **Members:** ______________________

**Authored skills:** #2 ☐  #__ ☐  #__ ☐

**Grader name:** ______________________  **Date:** ____________

**Transcripts attached:** ☐ Copilot Chat   ☐ Claude Code   **Validator output attached:** ☐
