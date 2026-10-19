# Scenario 03 — Call to an Unregistered User

**Test ID:** `call-to-unregistered-user` · **Focus:** `registration`, `call` ·
**Ground truth:** `fail` / `routing`

## What happens

User 1001 registers and calls 1003, which is configured on the PBX but whose
client is switched off. The PBX challenges the first INVITE, accepts the
credentialed INVITE with `100`, and then rejects it with
`480 Temporarily Unavailable`; the caller acknowledges. No second call leg is
created.

| Frames | Content |
| --- | --- |
| 1–4 | Registration of 1001 |
| 30–32 | INVITE, 401, ACK (normal challenge) |
| 33–34 | INVITE with credentials, 100 |
| 35–36 | **480**, ACK |

## What it teaches

- The response to an unavailable user depends on the PBX configuration
  (`404`, `480`, or `486`); the test case states it in `pbx.notes`.
- A skill that only judges registration (#1) correctly reports `pass` for its
  scope — the call failure is outside it. Only skill #2 can decide the test.

## Expected results

- **Worked skill #1:** `pass` — 1001 registered; 1003 not evaluated
  ([`reference/finding-01-registration.json`](reference/finding-01-registration.json)).
- **Skeleton REPORT:** `insufficient_evidence`, coverage `partial` — skill #2
  is a placeholder ([`reference/report-skeleton.json`](reference/report-skeleton.json)).
  Without the coverage rule, the skeleton would wrongly report `pass`.
- **With #2 implemented:** `fail` / `routing`, citing frames 33 and 35.
