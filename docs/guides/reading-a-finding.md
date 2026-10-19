# How to Read (and Write) a SIPLab Finding

**Type:** Teaching aid — **not** a graded scenario. The data below is invented
(lab addresses `10.20.0.0/24`, extension `2001`) and matches none of the
scenarios under [`../../scenarios/`](../../siplab/scenarios/README.md).
**Companion to:** the finding contract in [`boot/boot.md`](../../siplab/boot/boot.md)
(Block 2), the machine schema
[`schema/finding.schema.json`](../../siplab/schema/finding.schema.json), the worked
skill [`skills/01-registration/SKILL.md`](../../siplab/skills/01-registration/SKILL.md),
and the worksheet checks U1–U7 in
[`test-worksheet.md`](../project-proposal/test-worksheet.md).

Every skill speaks the same language: **one JSON object with ten shared
keys**. Reading one well is how you tell a diagnosis grounded in packets from
a confident-sounding guess.

---

## The synthetic case

Four rows of an evidence table (reference recipe, columns shortened here):

```text
frame.number  sip.Method  sip.Status-Code  sip.from.user  sip.Call-ID  sip.CSeq.seq  sip.CSeq.method  sip.Expires  sip.auth.username
12            REGISTER                     2001           kq7Lm2       1             REGISTER         3600
13                        401              2001           kq7Lm2       1             REGISTER
15            REGISTER                     2001           kq7Lm2       2             REGISTER         3600         2001
16                        200              2001           kq7Lm2       2             REGISTER         600
```

The client asked for 3600 s; the registrar accepted the binding but granted
only 600 s. Registration succeeded — the shorter expiry is a configuration
fact worth reporting, not a failure.

---

## The annotated finding

The `//` comments are explanation only; a real finding is plain JSON. `(U#)`
points at the matching worksheet check.

```jsonc
{
  // WHICH skill, by catalogue number and short name.                     (U1)
  "skill": "01-registration",

  // WHICH test — copied from the test case, never invented.
  "test_id": "guide-short-expiry",

  // ONE sentence a reader can act on.
  "summary": "User 2001 registered after a digest challenge; the PBX granted 600 s instead of 3600 s.",

  // OUTCOME of the SIP procedure — pass | fail | insufficient_evidence.   (U2)
  "verdict": "pass",

  // WHERE it broke — 'none' exactly when the verdict is 'pass'.           (U2)
  "failure_stage": "none",

  // HOW SURE — a number in [0, 1], set by the skill's own rule.           (U3)
  "confidence": 0.9,

  // WHAT IT RESTS ON — frame, column, exact cell value. The validator
  // looks up every item in the evidence table.                           (U4)
  "evidence": [
    {"frame": 15, "field": "sip.auth.username", "value": "2001"},
    {"frame": 16, "field": "sip.Status-Code",   "value": "200"},
    {"frame": 16, "field": "sip.Expires",       "value": "600"}
  ],

  // WHICH rules the judgment applied.
  "rfc_ref": ["RFC 3261 §10.3", "RFC 3261 §22.2", "RFC 3261 §10.2.1.1"],

  // A MANUAL check for the operator — never an action the system takes.
  "next_check": "Check the maximum expiry configured for endpoint 2001 on the PBX if 600 s is unexpected.",

  // WHY — observations first, then the expected behavior, then any cause,
  // labeled as suspected.                                                (U5)
  "rationale": "REGISTER (frame 12) was challenged with 401 (frame 13); the credentialed REGISTER (frame 15) requested Expires 3600 and was accepted with 200 and Expires 600 (frame 16). Expected: a registrar may shorten the requested expiry (RFC 3261 §10.2.1.1). Suspected cause: a maximum-expiry setting on the PBX.",

  // Skill-specific keys follow the shared ones.
  "registrations": [
    {"user": "2001", "call_id": "kq7Lm2", "request_frames": [12, 15], "challenge_frames": [13],
     "final_frame": 16, "final_status": "200", "credentials_sent": true,
     "digest_algorithm": null, "granted_expires": "600", "outcome": "registered"}
  ]
}
```

---

## Field by field

| Key | Ask yourself |
| --- | --- |
| `verdict` | Did the **procedure** succeed? Not: did the test meet its expectation? |
| `failure_stage` | Is it `none` exactly when the verdict is `pass`? |
| `evidence` | Could a grader find every item in the table, character for character? |
| `rationale` | Are observations, expectations, and suspected causes kept apart? |
| `confidence` | Does it follow the skill's rule, or is it a gut feeling? |
| `next_check` | Is it something a person does, not something the system does? |

---

## Weak vs. strong (same case)

**Weak:**

```json
{
  "skill": "01-registration",
  "test_id": "guide-short-expiry",
  "summary": "Registration problem detected.",
  "verdict": "fail",
  "failure_stage": "authentication",
  "confidence": 0.95,
  "evidence": [{"frame": 13, "field": "sip.Status-Code", "value": "401 Unauthorized"}],
  "rfc_ref": ["RFC 3261"],
  "next_check": "Reset the user's password.",
  "rationale": "The server returned 401, so authentication failed."
}
```

What is wrong:

- The `401` at frame 13 answers a REGISTER **without** credentials — a normal
  challenge, not a failure (worksheet check 1.1).
- `"401 Unauthorized"` is not the cell value; the column holds `401` (U4 —
  the validator rejects it).
- The success at frame 16 is ignored; high confidence on a wrong reading.
- `next_check` proposes an action on a user account instead of a check.

**Strong:** the annotated finding above.

---

## Self-check before the finding leaves the skill (U1–U7)

1. All ten shared keys present, plus the skill's extra keys. (U1)
2. `verdict` and `failure_stage` from the allowed values; `none` iff `pass`. (U2)
3. `confidence` is a number in [0, 1]. (U3)
4. Every evidence item copied exactly from the table. (U4)
5. `rationale` separates observation, expectation, and suspected cause. (U5)
6. Nothing in the table changed the verdict by *telling* the skill what to conclude. (U6)
7. Where rows are missing, encrypted, or malformed: `insufficient_evidence`, not a guess. (U7)

---

## See also

- [`tools/extract-evidence.md`](../../siplab/tools/extract-evidence.md) — how the table is made, and how to run the validator.
- [`scenarios/04-prompt-injection`](../../siplab/scenarios/04-prompt-injection/scenario.md) — U6 in practice.
