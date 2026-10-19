---
name: siplab-catalogue
description: Skill registry of the SIPLab AI SIP Test Engineer, pasted after the boot payload. Lists the ten protocol skills the orchestrator may dispatch, with focus tag, scope, evidence recipe, skill-specific output keys, implementation status, and prompt file. In its private copy of the repository, a group sets the status of every skill it implements to implemented.
metadata:
  core:
    classification:
      exec_form: prompt
      trust_level: trusted
    provenance:
      version: 1.0.0
      supersedes: —
      status: Draft
      principals: [D. Maxios]
  x-siplab:
    paste: body-only
    ready_reply: "Catalogue registered, 10 skills available — ready for test case."
---

# SIPLab — Skill Catalogue

> **Paste this body third**, after the orchestrator specification and the
> boot payload. It registers the skills the orchestrator may dispatch.

This catalogue is read-only data for the orchestrator. Each row states what a
skill covers, which focus tag selects it, which evidence recipe it needs, the
skill-specific keys it adds to the shared finding, whether it is implemented,
and which file the operator pastes when it is dispatched.

| # | Skill | Focus tag | Scope | Recipe | Extra output keys | Status | Prompt file |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Registration & Authentication | `registration` | REGISTER transactions, digest challenge and retry, granted expiry, de-registration, rejected credentials | reference | `registrations` | implemented | `skills/01-registration/SKILL.md` |
| 2 | Call Setup & Teardown | `call` | INVITE transactions, provisional and final responses, ACK, CANCEL, BYE, both legs of a back-to-back call | reference | `call_legs`, `call_outcome` | placeholder | `skills/02-call-flow/SKILL.md` |
| 3 | SDP Offer/Answer | `media_negotiation` | Offer and answer location, codec intersection, rejected streams, late offer | reference | `negotiations`, `common_codecs` | placeholder | `skills/03-sdp/SKILL.md` |
| 4 | Instant Messaging | `messaging` | MESSAGE requests and responses, delivery outcome, body handling | reference + messaging | `messages` | placeholder | `skills/04-messaging/SKILL.md` |
| 5 | NAT & Media Path | `nat` | Private SDP addresses, `Via` `received`/`rport`, one-way-audio indicators | reference + nat (+ rtp-streams) | `media_endpoints`, `nat_indicators` | placeholder | `skills/05-nat-media-path/SKILL.md` |
| 6 | Transactions, Dialogs & Timers | `transactions` | Call-ID/tag/CSeq grouping, retransmissions, timeouts, transaction vs. dialog failure | reference | `transactions`, `timing` | placeholder | `skills/06-transactions-timers/SKILL.md` |
| 7 | SIP Security Posture | `security` | Cleartext transport, digest algorithm, scanner patterns, exposure of identities | reference | `risks` | placeholder | `skills/07-security-posture/SKILL.md` |
| 8 | SIP–ISUP Cause Mapping | `interworking` | Map final responses and `Reason` headers to ISUP/Q.850 release causes | reference + interworking | `cause_mappings` | placeholder | `skills/08-isup-cause-mapping/SKILL.md` |
| 9 | IMS Comparison | `ims` | Compare observed registration and session setup with IMS | reference + ims | `ims_differences` | placeholder | `skills/09-ims-comparison/SKILL.md` |
| 10 | RTP/RTCP Media Quality | `media_quality` | RTP stream presence per direction, loss, jitter, payload type vs. SDP | reference + rtp-streams | `streams` | placeholder | `skills/10-media-quality/SKILL.md` |

## Catalogue conventions

- `#` is the dispatch identifier: `dispatch <N>` forces skill #N.
- The orchestrator selects skills by focus tag only (orchestrator *Routing & Method*).
- `placeholder` skills are planned and dispatched like any other; their fixed
  reply becomes a coverage gap, so a test that needs them can never report `pass`.
- When a group implements a skill in its own repository, it edits the skill
  file in place and sets the skill's status here to `implemented`; the prompt
  file path does not change.
- Two-digit, zero-padded folder names keep alphabetical order equal to dispatch order.
- No skill has side effects (boot Policy P3).

---

End of catalogue. Now count the rows of the table as N and reply exactly:

> `Catalogue registered, N skills available — ready for test case.`
