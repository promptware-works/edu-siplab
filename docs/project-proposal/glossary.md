# SIPLab — Glossary

**Companion to:** [`proposal.md`](./proposal.md),
[`delivery-plan.md`](./delivery-plan.md),
[`test-worksheet.md`](./test-worksheet.md)

This file defines the abbreviations, acronyms, and project-specific terms
used in the proposal, delivery plan, and test worksheet. Terms are grouped
by topic; within each group entries are alphabetical.

---

## A. Project-specific terms

| Term | Expansion / definition |
| --- | --- |
| **AI SIP Test Engineer** | The orchestrator plus the protocol skills that analyze saved captures of the group's PBX tests. |
| **APR** | Architectural Principle Record — a principle of the PROMPTARCH collection, e.g. APR-001 ASPECT. |
| **ASPECT** | *Agent & Skill Prompt-Engineered Component Template* (PROMPTARCH APR-001): the specification format of SIPLab prompts. **ASPECT-A** specifies agents (the orchestrator); **ASPECT-S** specifies skills. |
| **Boot payload** | `boot/boot.md`: the operator message format, the finding and report contracts, the verdict rule, the operator vocabulary, and policies P1–P4. Pasted after the orchestrator. |
| **Body** | The part of a prompt file below its frontmatter — the only part pasted into the chat. |
| **Consolidated report** | The orchestrator's REPORT: overall verdict, coverage and gaps, every skill finding unchanged, conflicts, deterministic facts, and the AI interpretation (`report.schema.json`). |
| **Corpus (group)** | The group's labeled tests — test case, truth file, sanitized capture, evidence table — built in P2. |
| **Corpus (held-out)** | The instructor's labeled cases with hidden labels, used for the final evaluation; not in the repository. |
| **Coverage** | `complete` when every planned skill returned a usable finding and every focus tag had a skill; otherwise `partial`. Reported separately from the verdict (PROMPTARCH APR-024). |
| **Deliverables folder** | The top-level `deliverables/` folder of a team repository: PBX extracts, corpus, specifications, test runs, worksheet, and report. |
| **Evidence table** | The tab-separated file produced from a capture by the TShark recipe: one row per SIP message, keyed by frame number. The only packet data the AI sees. |
| **Evidence validator** | `tools/validate_evidence.py`: the instructor's deterministic checker for schemas, citations, the verdict rule, and (optionally) the ground truth. |
| **Failure stage** | The enumerated point at which observed behavior departs from the expected behavior (`registration`, `authentication`, `routing`, `call_setup`, `media_negotiation`, `media_path`, `teardown`, `messaging`, `transport`, `unknown`, or `none`). |
| **Finding** | The shared 10-key JSON object every skill returns (`skill`, `test_id`, `summary`, `verdict`, `failure_stage`, `confidence`, `evidence`, `rfc_ref`, `next_check`, `rationale`). |
| **Focus tag** | A test-case value (`registration`, `call`, …) that selects one skill in the orchestrator's routing table. |
| **Frontmatter** | The YAML block at the top of a prompt file holding its machine-readable metadata (PROMPTARCH APR-014 DECLARE). Never pasted into the chat. |
| **Gap** | A recorded fact that a planned skill did not contribute (placeholder, not pasted, invalid reply, no skill for a focus tag), with the action that would close it. |
| **Gate** | A worksheet check that must pass before the next phase starts. |
| **Governance (two tiers)** | The pre-submission review of a skill: tier 1, the deterministic skill linter; tier 2, the advisory skill reviewer. Neither grades. |
| **Ground truth** | The verdict and failure stage a test is known to have, recorded in its truth file. |
| **Insufficient evidence** | The verdict returned when the evidence cannot decide the question; a correct answer, not an error. |
| **Milestone tag** | A git tag (`ms01`–`ms03`, or `cp1`, `cp2`, `final`) on the group's repository that marks a submission; the tagged commit is what is graded. |
| **Operator** | The human (group member, instructor, or grader) driving the chat session. |
| **Orchestrator** | The ASPECT-A agent that plans, waits for approval, dispatches skills, and consolidates findings; it never analyzes the evidence itself. |
| **Placeholder skill** | A skill file shipped in ASPECT-S form with scope, inputs, and checks pre-filled, which returns a fixed placeholder finding until a group implements it. |
| **Plan-and-Approve** | The orchestration protocol: the orchestrator proposes a plan, waits for operator approval, and only then dispatches skills. |
| **PROMPTARCH** | Promptware Works' collection of Architectural Principle Records for promptware. |
| **Protocol skill** | A single prompt-defined specialist, specified in ASPECT-S, that judges one SIP procedure from the evidence table. |
| **Scope (skill)** | The `When to Use` / `When NOT to Use` section of a SIPLab skill — a SIPLab extension to ASPECT-S. Each negative case redirects `→ #N` to the skill that owns it. |
| **Self-check** | The step where a component re-reads its output against its Quality Gates and rules (skills) or Guardrails (orchestrator) before replying. |
| **Skill linter** | `tools/lint_skill.py`: deterministic checks L1–L9 of a skill's frontmatter, sections, status, scope redirects, output keys, verdict table, stricter-mode elements, portability, and catalogue alignment. |
| **Skill reviewer** | `agents/skill-reviewer.agent.md`: the ASPECT-A governance agent that reviews a candidate skill against checks R1–R13 and proposes fixes; advisory only. |
| **SIPLab** | This project: build and test a SIP PBX with an AI Test Engineer. |
| **Team repository** | A group's private copy of `edu-siplab`, created at kickoff (proposal § 3.8). The group works and submits only there; the instructor has read access. |
| **Test case** | The AI input describing one test: objective, focus tags, endpoints, preconditions, steps, expected observations, observed outcome (`test-case.schema.json`). |
| **Test message** | The operator message: the line `TEST CASE`, the test case, the line `EVIDENCE TABLE`, the table. |
| **Truth file** | `<test-id>.truth.yaml`: the ground truth of a test (`truth.schema.json`). Never pasted into the chat. |
| **Worked example** | The single complete reference skill (`skills/01-registration/SKILL.md`). |

---

## B. SIP, telephony, and signaling

| Term | Expansion / definition |
| --- | --- |
| **1xx / 2xx / 3xx / 4xx / 5xx / 6xx** | SIP response classes: provisional, success, redirection, client error, server error, global failure. |
| **ACK** | SIP request that confirms a final response to an INVITE. |
| **AKA** | Authentication and Key Agreement — the authentication scheme used in IMS instead of plain digest. |
| **BYE** | SIP request that terminates an established dialog. |
| **Call-ID** | SIP header that identifies all messages of a dialog or registration. |
| **CANCEL** | SIP request that cancels a pending INVITE; the INVITE is then answered with `487`. |
| **CSeq** | SIP header holding a sequence number and method; orders requests within a dialog. |
| **Dialog** | A peer-to-peer SIP relationship identified by Call-ID, From tag, and To tag. |
| **Digest authentication** | Challenge-response authentication in SIP (`401`/`407` challenge, credentialed retry). |
| **IMS** | IP Multimedia Subsystem — the 3GPP SIP-based service architecture used for VoLTE and VoNR. |
| **INVITE** | SIP request that initiates a session. |
| **IP-PBX** | IP Private Branch Exchange — a software switch for telephony in a home or company. |
| **ISUP** | ISDN User Part — the SS7 protocol for setting up and releasing circuit-switched calls. |
| **MESSAGE** | SIP request that carries an instant message (RFC 3428). |
| **NAT** | Network Address Translation. A common cause of one-way audio when SDP advertises private addresses. |
| **Offer/answer** | The SDP negotiation model (RFC 3264): one side offers media, the other answers. |
| **P-CSCF / S-CSCF** | Proxy / Serving Call Session Control Function — IMS SIP servers. |
| **PSTN** | Public Switched Telephone Network. |
| **Q.850** | ITU-T recommendation defining call release cause values used by ISUP and in the SIP `Reason` header. |
| **REGISTER** | SIP request that binds a user's address to a contact location at the registrar. |
| **REL** | ISUP Release message; carries the release cause. |
| **RTP / RTCP** | Real-time Transport Protocol and its control protocol (RFC 3550) — carry and monitor the media. |
| **SDP** | Session Description Protocol (RFC 8866) — describes media streams, codecs, addresses, and ports. |
| **SIP** | Session Initiation Protocol (RFC 3261). |
| **SRTP** | Secure RTP — encrypted media. |
| **SS7** | Signaling System No. 7 — the PSTN signaling protocol stack (MTP2, MTP3, ISUP, …). |
| **Transaction** | A SIP request and all its responses (and the ACK for non-2xx final responses). |
| **Via** | SIP header that records the response path; `received` and `rport` record the observed source address and port (RFC 3581). |
| **VoIP / VoLTE / VoNR** | Voice over IP / over LTE / over 5G New Radio. |

---

## C. AI and prompting

| Term | Expansion / definition |
| --- | --- |
| **HITL** | Human-in-the-loop — a human approves or reviews before an AI result is acted on. |
| **Hallucination** | AI output that is fluent but not supported by the input — here, citing packets or values that are not in the evidence table. |
| **LLM** | Large Language Model. |
| **Portability** | The property that the same prompt behaves materially consistently in GitHub Copilot Chat and Claude Code. |
| **Prompt injection** | Text inside input data that tries to make the AI follow it as an instruction. |
| **Wrapper** | A thin IDE-specific file that loads a canonical prompt without changing it. |

---

## D. Tools and formats

| Term | Expansion / definition |
| --- | --- |
| **Asterisk** | Open-source PBX software. |
| **Linphone / Blink** | Open-source SIP clients. |
| **pcap / pcapng** | Packet capture file formats. |
| **PJSIP logger** | Asterisk's SIP message log (`pjsip set logger on`); an accepted secondary input for skills that declare it. |
| **TShark** | The command-line version of Wireshark, used for deterministic extraction. |
| **TSV** | Tab-separated values — the format of the evidence table. |
| **Upstream** | The git remote name for the instructor's `edu-siplab` repository in a team repository; instructor updates arrive with `git pull upstream main`. |
| **Wireshark** | Packet capture and protocol analysis tool; its *Telephony → SIP Flows / VoIP Calls* views are the non-AI baseline in the evaluation. |
