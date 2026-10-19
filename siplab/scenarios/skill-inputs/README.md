# SIPLab — Per-Skill Reference Inputs

Inputs for the per-skill pass checks of the test worksheet (Part F). Each
folder has the same files as a scenario (`test-case.yaml`, `evidence.tsv`,
`truth.yaml`, `reference/`). Several checks reuse the reference scenarios.

| Check | Input |
| --- | --- |
| 1.1 challenge then success is `pass`; granted expiry reported | [`../01-successful-call`](../01-successful-call/scenario.md) |
| 1.2 rejected credentials is `fail` / `authentication` | [`../02-auth-failure`](../02-auth-failure/scenario.md) |
| 1.3 `Expires: 0` is a de-registration, not a failure | [`01-registration/1.3-deregistration`](01-registration/1.3-deregistration/) |
| 1.4 no REGISTER is `insufficient_evidence` | [`01-registration/1.4-no-register`](01-registration/1.4-no-register/) |
| 2.1 complete call is `pass` | [`../01-successful-call`](../01-successful-call/scenario.md) |
| 2.2 unavailable callee is `fail` | [`../03-unavailable-user`](../03-unavailable-user/scenario.md) |
| 8.1 cause mapping (partial: `404` → cause 1 only) | [`../03-unavailable-user`](../03-unavailable-user/scenario.md) |
| U6 embedded instructions ignored — for #1; groups add one injection variant per authored skill to their corpus | [`../04-prompt-injection`](../04-prompt-injection/scenario.md) |

## Still to be added by the instructor

| Skill | Inputs needed |
| --- | --- |
| #2 | Caller-cancelled call (`CANCEL`, `487`) (2.3); call without provisional responses (2.4); `200` retransmitted without ACK (2.5) |
| #3 | No common codec (`488`); late offer; rejected stream (port `0`) |
| #4 | MESSAGE delivered on the PBX→recipient leg; `202` to the sender but no PBX→recipient MESSAGE; challenged MESSAGE; injected body; `415` for a `message/cpim` body |
| #5 | Private SDP address behind NAT; `Via` `received`/`rport`; a `direct_media=yes` call with re-INVITEs; a capture without the needed addresses |
| #6 | Multi-call capture; INVITE retransmissions ending in `408`; CSeq out of order; a failed in-dialog transaction (6.4) |
| #7 | Scanner burst of REGISTER/OPTIONS; MD5 vs. SHA-256 challenge |
| #8 | `486` final (8.1); `Reason: Q.850` header (8.2); a status code without a listed mapping and a `487` (8.3) |
| #9 | Registration and call for comparison (the reference scenarios suffice to start) |
| #10 | `rtp-streams.txt` files: bidirectional, one-directional (10.6), payload mismatch, SRTP |
