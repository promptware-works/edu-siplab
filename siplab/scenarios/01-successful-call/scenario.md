# Scenario 01 — Successful Registered Call

**Test ID:** `basic-registered-call` · **Focus:** `registration`, `call` ·
**Ground truth:** `pass` / `none`

## What happens

Users 1001 (Linphone desktop, `192.168.56.21`) and 1002 (Linphone Android,
`192.168.56.22`) register at an Asterisk PBX (`192.168.56.10`). Each REGISTER
is first challenged with `401` and then accepted with `200`. User 1001 calls
1002; the PBX challenges the first INVITE, the credentialed INVITE succeeds,
and the PBX opens a second call leg to 1002. Both legs are answered,
acknowledged, and later terminated with BYE.

| Frames | Content |
| --- | --- |
| 1–4 | Registration of 1002 (REGISTER, 401, REGISTER with credentials, 200) |
| 5–8 | Registration of 1001 |
| 41–45 | Leg A (1001 → PBX): INVITE, 401, ACK, credentialed INVITE, 100 |
| 46–48 | Leg B (PBX → 1002): INVITE, 100, 180 |
| 49 | Leg A: 180 |
| 80–83 | Answer: 200 and ACK on both legs |
| 84–5946 | RTP media (not in the evidence table; the PBX anchors media) |
| 5947–5950 | Teardown: BYE and 200 on both legs |

## What it teaches

- A back-to-back PBX creates **two dialogs** with different Call-IDs.
- A `401` answering a REGISTER or INVITE **without credentials** is a normal
  challenge, not a failure.
- The 200 to REGISTER lists the granted binding in its Contact (`;expires=3600`).
- The ACK for a 2xx repeats the INVITE's credentials (frame 83).
- Signaling cannot prove audio; `observed_by_tester` carries that claim.

## Expected results

- **Worked skill #1:** `pass` — both users registered
  ([`reference/finding-01-registration.json`](reference/finding-01-registration.json)).
- **Skeleton REPORT:** `insufficient_evidence`, coverage `partial`, one gap —
  skill #2 is a placeholder
  ([`reference/report-skeleton.json`](reference/report-skeleton.json)). This
  is the correct, coverage-honest answer for the skeleton.
- **With #2 implemented:** `pass` / `none`, coverage `complete`.
