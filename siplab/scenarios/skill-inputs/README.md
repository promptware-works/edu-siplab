# SIPLab — Per-Skill Reference Inputs

Inputs for the per-skill pass checks of the test worksheet (Part F). Each
folder has the same files as a scenario (`test-case.yaml`, `evidence.tsv`,
`truth.yaml`, `reference/`). Several checks reuse the reference scenarios.

| Check | Input |
| --- | --- |
| 1.1 challenge then success is `pass` | [`../01-successful-call`](../01-successful-call/scenario.md) |
| 1.2 rejected credentials is `fail` / `authentication` | [`../02-auth-failure`](../02-auth-failure/scenario.md) |
| 1.3 `Expires: 0` is a de-registration, not a failure | [`01-registration/1.3-deregistration`](01-registration/1.3-deregistration/) |
| 1.4 no REGISTER is `insufficient_evidence` | [`01-registration/1.4-no-register`](01-registration/1.4-no-register/) |
| 2.1 complete call is `pass` | [`../01-successful-call`](../01-successful-call/scenario.md) |
| 2.2 unavailable callee is `fail` | [`../03-unavailable-user`](../03-unavailable-user/scenario.md) |
| 8.1 cause mapping of a failure response | [`../03-unavailable-user`](../03-unavailable-user/scenario.md) |
| U6 embedded instructions ignored | [`../04-prompt-injection`](../04-prompt-injection/scenario.md) |

## Still to be added by the instructor

| Skill | Inputs needed |
| --- | --- |
| #2 | Caller-cancelled call (`CANCEL`, `487`); `200` retransmitted without ACK |
| #3 | No common codec (`488`); late offer; rejected stream (port `0`) |
| #4 | MESSAGE delivered; MESSAGE to an unregistered user; challenged MESSAGE; injected body |
| #5 | Private SDP address behind NAT; `Via` `received`/`rport`; one-directional RTP; no RTP |
| #6 | Multi-call capture; INVITE retransmissions ending in `408`; CSeq out of order |
| #7 | Scanner burst of REGISTER/OPTIONS; MD5 vs. SHA-256 challenge |
| #8 | `486` and `404` finals; `Reason: Q.850` header; unmapped status code |
| #9 | Registration and call for comparison (the reference scenarios suffice to start) |
| #10 | RTP stream statistics: bidirectional, one-directional, payload mismatch, SRTP |
