# SIPLab — Delivery Plan (Selectable Timelines)

**Companion to:** [`proposal.md`](./proposal.md) (timeline-neutral) and
[`test-worksheet.md`](./test-worksheet.md) (pass bar)\
**Purpose:** Hold the **variable** part of the project — the schedule,
checkpoints, deliverable sizes, per-phase grade split, submission workflow,
and onboarding window — separately from the proposal, so a cohort can run on
a different calendar without forking the proposal or the worksheet.

The proposal defines three fixed phases: **P1** Install & Configure the SIP
PBX, **P2** Test & Verify the SIP PBX, **P3** Build, Integrate & Evaluate the
AI SIP Test Engineer. This document maps those phases onto a concrete
timeline. Two variants ship today; [adding a new one](#adding-a-new-variant)
is a copy-paste, not a fork.

---

## Choosing a variant

| If your cohort has… | Use |
| --- | --- |
| A full half-semester (≈6 weeks) with weekly contact | [**6-Week / 3-Milestone Plan**](#6-week--3-milestone-plan) — one milestone per phase, milestone-distributed grade |
| A block course, summer module, or late-semester capstone (≈3 weeks) | [**3-Week / Single-Milestone Plan**](#3-week--single-milestone-plan) — intensive sprint, formative weekly checkpoints, single consolidated grade |

**Scope is identical at the project level in every variant** — each group
ships a working, tested PBX and an integrated, portable, evaluated AI SIP
Test Engineer. A shorter timeline trims the number of authored skills, the
corpus size, artefact depth, and defense length — never the PBX minimum
system, the skill contract, or the pass bar.

### Variant comparison

| Item | 6-Week / 3-Milestone | 3-Week / Single-Milestone |
| --- | --- | --- |
| Calendar | 3 milestones over 6 weeks | 1 milestone, 3 weekly checkpoints |
| Grade split | 25% / 35% / 40% across milestones | 100% on one milestone (checkpoints formative) |
| Kickoff | Day 1 session, before MS01 | Day 0 pre-session, the week before Week 1 |
| AI onboarding (proposal § 3.7) | Week 3, start of MS02 | Week 2 |
| Authored skills | #2 + one elective per member beyond the first (proposal § 7.1) | #2 + at most one elective |
| Group corpus | ≥ 8 labeled cases | ≥ 5 labeled cases |
| Held-out instructor corpus | ≥ 4 cases | ≥ 3 cases |
| Injection cases | The instructor's `scenarios/04-prompt-injection` for #1, plus one group-authored injection variant per authored skill | Same as the 6-week plan |
| Final report (`report.md`) | 4,000–6,000 words | 2,500–3,500 words |
| Defense | ≤ 20 min per group (10 min demo, 10 min Q&A) | ≤ 12 min per group (6 min demo, 6 min Q&A) |
| Submission | One tag per milestone (`ms01`–`ms03`) in the group's private repository | Checkpoint tags `cp1`, `cp2` (formative) and a final tag `final` |
| Advanced skills #9, #10 | Allowed as electives | Discouraged |

> The **evaluation dimension weights** D1–D8 are identical in both variants —
> see [`proposal.md`](./proposal.md) § 6. Only the **per-phase split** of the
> project total differs.

### Required corpus composition (both variants)

Every group corpus contains at least one labeled case of each type below;
the remaining cases are the group's choice.

| Type | Expected ground truth |
| --- | --- |
| Successful registration and call, with teardown | `pass` |
| Authentication failure (wrong password) | `fail` — `authentication` |
| Unavailable or unregistered callee, or no answer / timeout | `fail` — `routing` or `call_setup` (as configured) |
| Messaging between two users | `pass` or `fail` as observed |
| Per authored skill, an injection variant of one of the skill's cases (text in `User-Agent`, `Subject`, or a message body telling the AI what to conclude) — the same capture with the injected text added to the evidence table is accepted | Correct verdict for the underlying signaling; injected text ignored |

6-week groups additionally include a **caller-cancelled call** (`CANCEL`,
`487`) and one case per elective skill that exercises its main check.

---

## Kickoff (ungraded, both variants)

Before P1, each group agrees its scope and setup:

| Exit condition |
| --- |
| Group formed (max. 3 students) and registered with the instructor |
| Short requirements list and proposed topology (server, devices, network) |
| Chosen PBX, clients, and capture setup |
| Private group repository created from `edu-siplab`, instructor invited with read access (proposal § 3.8) |

---

## 6-Week / 3-Milestone Plan

The project total is distributed **25 / 35 / 40** across three milestones,
one per phase.

**Kickoff window.** Day 1 session before MS01.\
**AI onboarding.** The bring-up in [`proposal.md`](./proposal.md) § 3.7 runs
in Week 3; each member's two transcripts are the readiness deliverable.\
**Budget guideline.** Set by the course team before the cohort starts.

### Submission workflow

- Each group works in its private copy of `edu-siplab` (proposal § 3.8).
  Paths in the deliverables below are inside `deliverables/`, except the
  skills (`siplab/skills/`) and the catalogue (`siplab/boot/catalogue.md`).
- Every milestone closes with a tag on the group's repository — `ms01`,
  `ms02`, `ms03` — pushed before the deadline. The tagged commit is the
  submission; later commits are not graded for that milestone.
- The grader reviews the tagged state and sends milestone-scoped feedback
  (e.g. as issues in the group's repository); the group resolves it before
  the next milestone opens.
- Without repository access, the group sends a `git bundle` of the tagged
  state instead (proposal § 3.8).
- Late submissions follow the course's standard late policy.

### Milestone 1 — Install & Configure the SIP PBX (Weeks 1–2) — *covers phase P1*

#### Activities — Weeks 1–2

- Confirm requirements, tools, and network topology.
- Install a Linux server or VM and the SIP PBX (e.g. Asterisk).
- Install SIP clients on at least one desktop and two mobile devices.
- Configure the network, users, authentication, dial plan, and messaging.
- Create the administrator account and at least five user accounts.
- Record software versions, addresses, account identifiers, and
  configuration decisions — without passwords or secrets.

#### Deliverables (end of Week 2)

- System and network diagram and component inventory with software
  versions, in `pbx/`.
- Sanitized configuration extracts (with `direct_media=no`) and reproducible
  setup notes in `pbx/`.
- Evidence that the PBX runs and the clients register (screenshots or a
  capture of successful registrations) in `pbx/`.
- Worksheet core checks C1–C6 marked.

**Gate to MS02:** the PBX and at least two registered clients are ready for
call testing.

**Assessment weight:** 25% (D1 20%, D2 5%)

### Milestone 2 — Test & Verify the SIP PBX (Weeks 3–4) — *covers phase P2*

#### Activities — Weeks 3–4

- Place the first internal call; verify two-way audio and clean teardown.
- Complete mobile-to-desktop and mobile-to-mobile calls, and one voice
  session per user.
- Test messaging between users.
- Capture and explain registration, call setup, teardown, and messaging;
  compare messages with the RFCs.
- Capture and explain at least one failed or rejected call.
- Build the labeled corpus: test case, sanitized capture, and evidence table
  for every case (see *Required corpus composition*).
- Complete the AI onboarding (Week 3); select the group's skills and write
  `spec.md`: one page per skill covering scope, input columns, verdict rule,
  RFC references, and planned test cases.

#### Deliverables (end of Week 4)

- `core-tests.md`: the core test table (preconditions, steps, expected,
  observed, pass/fail) and signaling walkthroughs of the essential flows,
  with frame references.
- `corpus/` with ≥ 8 labeled cases.
- `spec.md`, and the onboarding transcripts in `onboarding/`.
- Worksheet core checks C7–C14 marked.

**Gate to MS03:** worksheet checks marked *gate* pass. All MS02 tests run
without the AI SIP Test Engineer.

**Assessment weight:** 35% (D3 25%, D4 10%)

### Milestone 3 — Build, Integrate & Evaluate the AI SIP Test Engineer (Weeks 5–6) — *covers phase P3*

#### Activities — Weeks 5–6

- Implement the group's skills in ASPECT-S, starting from their runnable
  placeholders under `siplab/skills/`; mark them as `implemented` in
  `siplab/boot/catalogue.md`.
- Run every corpus case through the orchestrator in **both** Copilot Chat
  and Claude Code; save paired transcripts; run the validator on every
  consolidated report.
- Harden the skills until they are schema-compliant, materially consistent
  across environments, injection-resistant, and return
  `insufficient_evidence` where the capture cannot decide; add a
  self-check step.
- Before submitting, review every group skill in two tiers (proposal § 4.1):
  `lint_skill.py` must report no errors, and every skill-reviewer `FAIL` is
  either fixed or answered in `spec.md`; save both outputs in `governance/`.
- Run every case of the instructor's held-out corpus (test cases and
  evidence tables, no truth files) in both environments and save the
  reports in `tests/`; the instructor scores them after submission
  (proposal § 6.1).
- Write the evaluation (proposal § 6.1) and the final `report.md`.
- Demonstrate the PBX first, then the AI SIP Test Engineer, and defend the
  design as a group.

#### Deliverables (end of Week 6)

- Final skills (`siplab/skills/<NN>-<short-name>/SKILL.md`) and `siplab/boot/catalogue.md`.
- `tests/` with paired transcripts and validator output per case.
- `governance/` with the linter output and skill-reviewer review of each
  group skill.
- Filled `worksheet.md` (universal, per-skill, cross-environment, and
  integration checks).
- `report.md`, 4,000–6,000 words.
- Live demonstration and defense.

**Assessment weight:** 40% (D5 10%, D6 10%, D7 10%, D8 10%)

### Partial-credit path

A group that fails the MS02 gate after remediation may complete MS03 on
**instructor reference captures** instead of its own corpus. D1 and D3 are
graded on the state the group actually reached; the corpus part of D4 scores zero; MS03 is graded
normally. The path must be requested and approved by the instructor. It
keeps the group working through the AI phase rather than stopping.

---

## 3-Week / Single-Milestone Plan

This variant compresses the project into an intensive sprint. It keeps all
three phases and the full pass bar, collapses the grade into a single
milestone, and uses weekly checkpoints for formative feedback.

**Kickoff window.** Day 0 pre-session, the week before Week 1 — groups
arrive with their topology and devices ready.\
**AI onboarding.** Proposal § 3.7, at the start of Week 2.\
**Budget guideline.** Set by the course team before the cohort starts.

### Submission workflow

- Each group works in its private copy of `edu-siplab` (proposal § 3.8);
  paths are as in the 6-week plan.
- Each weekly checkpoint is a tag — `cp1`, `cp2` — that the grader reviews
  for formative feedback.
- The final submission is the tag `final`, pushed before the end of Week 3.
- Without repository access, the group sends a `git bundle` of the tagged
  state instead (proposal § 3.8).
- Late submissions follow the course's standard late policy.

### Week 1 — Install, Configure & First Call — *covers phase P1, starts P2*

#### Activities — Week 1

- Install and configure the PBX, clients, users, and messaging.
- Register all clients and place the first internal call.

#### Week 1 checkpoint (end of Week 1)

- Diagram, inventory, sanitized configuration extracts.
- Clients registered; first call completed.
- Core checks C1–C6 marked.

### Week 2 — Test, Verify & Specify — *covers phase P2, starts P3*

#### Activities — Week 2

- Complete the core tests (C7–C14) and signaling walkthroughs.
- Build the corpus (≥ 5 cases, including one injection variant per skill
  the group authors).
- Complete the AI onboarding; write `spec.md`; draft v1 of the group's
  skills (#2 + at most one elective).

#### Week 2 checkpoint (end of Week 2)

- `core-tests.md`; gate checks pass.
- `corpus/`, `spec.md`, `onboarding/`, v1 skills.

### Week 3 — Integrate, Evaluate & Defend — *covers phase P3*

#### Activities — Week 3

- Integrate and harden the skills; paired transcripts and validator runs
  for every case; held-out corpus run in both environments, reports saved
  for instructor scoring.
- Before submitting, lint every group skill without errors and fix or answer
  every skill-reviewer `FAIL` in `spec.md`; save both outputs in
  `governance/` (proposal § 4.1).
- Write `report.md` and prepare the demonstration.

#### Final deliverables (end of Week 3)

- Final skills, `siplab/boot/catalogue.md`, `tests/`, `governance/`, filled `worksheet.md`.
- `report.md`, 2,500–3,500 words.
- Demonstration and defense.

### Assessment weight

All dimensions in [`proposal.md`](./proposal.md) § 6 are graded **once, at
the end of Week 3 — 100% of the project total**. The weekly checkpoints are
formative.

### Partial-credit path

As in the 6-week plan: a group that fails the gate checks at the Week 2
checkpoint may finish Week 3 on instructor reference captures, with the
same scoring rules, on request and with instructor approval.

### Why three weeks is enough (and where it strains)

**Sufficient because:** the orchestrator, the worked registration skill,
the runnable placeholders, the schemas, the TShark recipes, the validator,
and the reference scenarios are instructor-provided; groups write the PBX configuration and at most two skill
bodies, not the contract or the tooling.

**Strains to expect:**

- PBX installation and client interoperability can consume most of Week 1.
  Groups must arrive at Week 1 with devices and a VM host ready.
- The corpus is small; accuracy figures are indicative only, and the report
  must say so.
- Cross-environment debugging competes with report writing in Week 3.

---

## Adding a new variant

To add another timeline, copy the skeleton below as a new `## N-… Plan`
section, add a column to the [Variant comparison](#variant-comparison)
table, and fill in the blanks. **Do not change
[`proposal.md`](./proposal.md) or [`test-worksheet.md`](./test-worksheet.md)**
— a variant that needs to change them changes the project, not the
schedule.

```markdown
## <N>-… Plan

<One-paragraph framing: who this fits, how the grade is structured.>

**Kickoff window.** <When the kickoff runs.>\
**AI onboarding.** <When the proposal § 3.7 bring-up runs.>\
**Budget guideline.** <Per-group or per-student budget for this timeline.>

### Submission workflow
<Tag conventions for this timeline.>

### <Period 1> — Install & Configure the SIP PBX — *covers phase P1*
### <Period 2> — Test & Verify the SIP PBX — *covers phase P2*
### <Period 3> — Build, Integrate & Evaluate the AI SIP Test Engineer — *covers phase P3*

### Assessment weight
<Per-phase split of the project total. Dimension weights stay as in proposal § 6.>

### What this variant changes vs. the 6-week baseline
<Authored skills, corpus size, report length, defense length, etc.>
```

**Example: 8-week / 4-milestone variant.** Where the calendar allows a
formal review of the AI design, split P3 into two milestones: **MS03 —
Specify & Implement** (orchestrator integration, two integrated skills,
paired transcripts) and **MS04 — Evaluate & Harden** (held-out corpus,
difficult captures with missing packets, encrypted signaling, and injected
payloads; final report and defense). Because each dimension belongs to one
phase, the split is **25 / 35 / 20 / 20**: MS03 carries D5 and D7, MS04
carries D6 and D8.

Each variant **must** cover all three phases and **must not** change the
pass bar in [`test-worksheet.md`](./test-worksheet.md) — only *when* it is
graded and *how much* of the total it carries.
