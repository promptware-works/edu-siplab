# Scenario 02 — Registration with a Wrong Password

**Test ID:** `wrong-password-registration` · **Focus:** `registration` ·
**Ground truth:** `fail` / `authentication`

## What happens

Client 1002 registers normally. Client 1001 is configured with a wrong
password: its first REGISTER is challenged with `401`, and its credentialed
REGISTER is answered with `401` again. The client gives up.

| Frames | Content |
| --- | --- |
| 1–4 | Registration of 1002 (REGISTER, 401, REGISTER with credentials, 200) |
| 5–6 | 1001: REGISTER, 401 (normal challenge) |
| 7–8 | 1001: REGISTER with credentials, **401** (rejected) |

## What it teaches

- The difference between a **challenge** (`401` to a request without
  credentials) and a **rejection** (`401` to a request with credentials).
- The verdict describes the outcome of the procedure: the registration of 1001
  failed, even though the test was designed to provoke the failure.

## Expected results

- **Worked skill #1:** `fail` / `authentication`
  ([`reference/finding-01-registration.json`](reference/finding-01-registration.json)).
- **Skeleton REPORT:** `fail` / `authentication`, coverage `complete` — the
  only planned skill is implemented
  ([`reference/report-skeleton.json`](reference/report-skeleton.json)).
