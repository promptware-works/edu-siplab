# Scenario 03 — Call to an Unregistered User

**Test ID:** `call-to-unregistered-user` · **Focus:** `registration`, `call` ·
**Ground truth:** `fail` / `routing`

## What happens

User 1001 registers and calls 1003, which is configured on the PBX but whose
client is switched off. The PBX challenges the first INVITE, accepts the
credentialed INVITE with `100`, and then rejects it with `404 Not Found` —
the answer of Asterisk's default dial plan (`Dial(PJSIP/${EXTEN})` then
`Hangup()`) when the endpoint has no registered contact; the caller acknowledges. No second call leg is
created.

| Frames | Content |
| --- | --- |
| 1–4 | Registration of 1001 |
| 30–32 | INVITE, 401, ACK (normal challenge) |
| 33–34 | INVITE with credentials, 100 |
| 35–36 | **404**, ACK |

## What it teaches

- The response to an unavailable user depends on the dial plan — `404` by
  default, `480` if the dial plan hangs up with cause 20, `503` if it simply
  ends — so the test case states it in `pbx.notes`. `486` would mean *busy*,
  not unavailable.
- A skill that only judges registration (#1) correctly reports `pass` for its
  scope — the call failure is outside it. Only skill #2 can decide the test.

## Expected results

- **Worked skill #1:** `pass` — 1001 registered; 1003 not evaluated
  ([`reference/finding-01-registration.json`](reference/finding-01-registration.json)).
- **Skeleton REPORT:** `insufficient_evidence`, coverage `partial` — skill #2
  is a placeholder ([`reference/report-skeleton.json`](reference/report-skeleton.json)).
  Without the coverage rule, the skeleton would wrongly report `pass`.
- **With #2 implemented:** `fail` / `routing`, citing frames 33 and 35.
