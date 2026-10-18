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
| **Consolidated report** | The orchestrator's final output: overall verdict, every skill finding unchanged, conflicts, and the split between deterministic facts and AI interpretations. |
| **Corpus (group)** | The group's labeled test cases with sanitized captures and evidence tables, built in P2. |
| **Corpus (held-out)** | The instructor's labeled cases with hidden labels, used for the final evaluation; not in the repository. |
| **Evidence table** | The tab-separated file produced from a capture by the TShark recipe: one row per SIP message, keyed by frame number. The only packet data the AI sees. |
| **Evidence validator** | The instructor-provided deterministic tool that checks every frame and field value cited in a report against the evidence table. |
| **Failure stage** | The enumerated point at which observed behavior departs from the expected behavior (`registration`, `authentication`, `routing`, `call_setup`, `media_negotiation`, `media_path`, `teardown`, `messaging`, `transport`, `unknown`, or `none`). |
| **Finding** | The shared 10-key JSON object every skill returns (`skill`, `test_id`, `summary`, `verdict`, `failure_stage`, `confidence`, `evidence`, `rfc_ref`, `next_check`, `rationale`). |
| **Gate** | A worksheet check that must pass before the next phase starts. |
| **Ground truth** | The verdict and failure stage a test case is known to have, recorded by the group (or instructor) from the test conditions and the capture. |
| **Insufficient evidence** | The verdict a skill returns when the evidence table cannot decide the question; a correct answer, not an error. |
| **Operator** | The human (group member, instructor, or grader) driving the chat session. |
| **Orchestrator** | The control prompt that runs PLAN → APPROVE → EXECUTE, dispatches skills, and consolidates findings. |
| **Plan-and-Approve** | The orchestration protocol: the orchestrator proposes a plan, waits for operator approval, and only then dispatches skills. |
| **Protocol skill** | A single prompt-defined specialist, authored in RICTOC, that analyzes one aspect of SIP behavior from the evidence table. |
| **RICTOC** | The prompt-design template used for every skill and the orchestrator: **R**ole, **I**nput, **C**ontext, **T**ask, **O**utput, **C**onstraints. |
| **Self-check** | The step where a skill re-reads its own output against its Constraints section before returning. |
| **SIPLab** | This project: build and test a SIP PBX with an AI Test Engineer. |
| **Stub** | A pre-filled but incomplete skill file shipped by the instructor. |
| **Test case** | The labeled description of one test: objective, preconditions, steps, expected observations, observed outcome, ground truth (`test-case.schema.json`). |
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
| **PR** | Pull request — the unit of submission per milestone or checkpoint. |
| **TShark** | The command-line version of Wireshark, used for deterministic extraction. |
| **TSV** | Tab-separated values — the format of the evidence table. |
| **Wireshark** | Packet capture and protocol analysis tool; its *Telephony → SIP Flows / VoIP Calls* views are the non-AI baseline in the evaluation. |
